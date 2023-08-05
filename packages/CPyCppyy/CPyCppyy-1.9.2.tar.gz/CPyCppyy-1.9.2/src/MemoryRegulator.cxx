// Bindings
#include "CPyCppyy.h"
#include "MemoryRegulator.h"
#include "CPPInstance.h"
#include "ProxyWrappers.h"

// Standard
#include <assert.h>
#include <string.h>
#include <iostream>


// memory regulater callback for deletion of registered objects
static PyMethodDef gObjectEraseMethodDef = {
    const_cast<char*>("MemoryRegulator_internal_EraseCallback"),
    (PyCFunction)CPyCppyy::MemoryRegulator::EraseCallback,
    METH_O, nullptr
};

//= pseudo-None type for masking out objects on the python side ===============
static PyTypeObject CPyCppyy_NoneType;

//-----------------------------------------------------------------------------
static Py_ssize_t AlwaysNullLength(PyObject*)
{
    return 0;
}

//-----------------------------------------------------------------------------
static PyMappingMethods CPyCppyy_NoneType_mapping = {
    AlwaysNullLength,
    (binaryfunc)              0,
    (objobjargproc)           0
};

// silence warning about some cast operations
#if defined(__GNUC__) && (__GNUC__ >= 5 || (__GNUC__ >= 4 && ((__GNUC_MINOR__ == 2 && __GNUC_PATCHLEVEL__ >= 1) || (__GNUC_MINOR__ >= 3)))) && !__INTEL_COMPILER
#pragma GCC diagnostic ignored "-Wstrict-aliasing"
#endif


//-----------------------------------------------------------------------------
namespace {

struct InitCPyCppyy_NoneType_t {
    InitCPyCppyy_NoneType_t() {
    // create a CPyCppyy NoneType (for references that went dodo) from NoneType
        memset(&CPyCppyy_NoneType, 0, sizeof(CPyCppyy_NoneType));

        ((PyObject&)CPyCppyy_NoneType).ob_type    = &PyType_Type;
        ((PyObject&)CPyCppyy_NoneType).ob_refcnt  = 1;
        ((PyVarObject&)CPyCppyy_NoneType).ob_size = 0;

        CPyCppyy_NoneType.tp_name        = const_cast<char*>("CPyCppyy_NoneType");
        CPyCppyy_NoneType.tp_flags       = Py_TPFLAGS_HAVE_RICHCOMPARE | Py_TPFLAGS_HAVE_GC;

        CPyCppyy_NoneType.tp_traverse    = (traverseproc)0;
        CPyCppyy_NoneType.tp_clear       = (inquiry)0;
        CPyCppyy_NoneType.tp_dealloc     = (destructor)&InitCPyCppyy_NoneType_t::DeAlloc;
        CPyCppyy_NoneType.tp_repr        = Py_TYPE(Py_None)->tp_repr;
        CPyCppyy_NoneType.tp_richcompare = (richcmpfunc)&InitCPyCppyy_NoneType_t::RichCompare;
#if PY_VERSION_HEX < 0x03000000
    // tp_compare has become tp_reserved (place holder only) in p3
        CPyCppyy_NoneType.tp_compare     = (cmpfunc)&InitCPyCppyy_NoneType_t::Compare;
#endif
        CPyCppyy_NoneType.tp_hash        = (hashfunc)&InitCPyCppyy_NoneType_t::PtrHash;

        CPyCppyy_NoneType.tp_as_mapping  = &CPyCppyy_NoneType_mapping;

        PyType_Ready(&CPyCppyy_NoneType);
    }

    static void DeAlloc(PyObject* pyobj) { Py_TYPE(pyobj)->tp_free(pyobj); }
    static int PtrHash(PyObject* pyobj) { return (int)ptrdiff_t(pyobj); }

    static PyObject* RichCompare(PyObject*, PyObject* other, int opid) {
        return PyObject_RichCompare(other, Py_None, opid);
    }

    static int Compare(PyObject*, PyObject* other) {
#if PY_VERSION_HEX < 0x03000000
        return PyObject_Compare(other, Py_None);
#else
    // TODO the following isn't correct as it doesn't order, but will do for now ...
        return !PyObject_RichCompareBool(other, Py_None, Py_EQ);
#endif
    }
};

} // unnamed namespace

// Memory regulation hooks
CPyCppyy::MemHook_t CPyCppyy::MemoryRegulator::registerHook = nullptr;
CPyCppyy::MemHook_t CPyCppyy::MemoryRegulator::unregisterHook = nullptr;


//- ctor/dtor ----------------------------------------------------------------
CPyCppyy::MemoryRegulator::MemoryRegulator()
{
// setup NoneType for referencing and create weakref cache
    static InitCPyCppyy_NoneType_t initCPyCppyy_NoneType;
}


//- public members -----------------------------------------------------------
bool CPyCppyy::MemoryRegulator::RecursiveRemove(
        Cppyy::TCppObject_t cppobj, Cppyy::TCppType_t klass)
{
// if registerd by the framework, called whenever a cppobj gets destroyed
    if (!cppobj)
        return false;

    PyObject* pyscope = GetScopeProxy(klass);
    if (!CPPScope_Check(pyscope)) {
        Py_XDECREF(pyscope);
        return false;
    }

    CppToPyMap_t* cppobjs = ((CPPClass*)pyscope)->fImp.fCppObjects;
    if (!cppobjs) {       // table may have been deleted on shutdown
        Py_DECREF(pyscope);
        return false;
    }

// see whether we're tracking this object
    CppToPyMap_t::iterator ppo = cppobjs->find(cppobj);

    if (ppo != cppobjs->end()) {
    // get the tracked object and cleanup weak reference
        CPPInstance* pyobj = (CPPInstance*)PyWeakref_GetObject(ppo->second);
        Py_DECREF(ppo->second);
        if ((PyObject*)pyobj == Py_None) {
            cppobjs->erase(ppo);
            Py_DECREF(pyscope);
            return false;
        }

    // nullify the object
        if (!CPyCppyy_NoneType.tp_traverse) {
        // take a reference as we're copying its function pointers
            Py_INCREF(Py_TYPE(pyobj));

        // all object that arrive here are expected to be of the same type ("instance")
            CPyCppyy_NoneType.tp_traverse   = Py_TYPE(pyobj)->tp_traverse;
            CPyCppyy_NoneType.tp_clear      = Py_TYPE(pyobj)->tp_clear;
            CPyCppyy_NoneType.tp_free       = Py_TYPE(pyobj)->tp_free;
        } else if (CPyCppyy_NoneType.tp_traverse != Py_TYPE(pyobj)->tp_traverse) {
        // TODO: SystemError?
            std::cerr << "in CPyCppyy::MemoryRegulater, unexpected object of type: "
                      << Py_TYPE(pyobj)->tp_name << std::endl;

        // drop object and leave before too much damage is done
            cppobjs->erase(ppo);
            Py_DECREF(pyscope);
            return false;
        }

    // notify any other weak referents by playing dead
        Py_ssize_t refcnt = ((PyObject*)pyobj)->ob_refcnt;
        ((PyObject*)pyobj)->ob_refcnt = 0;
        PyObject_ClearWeakRefs((PyObject*)pyobj);
        ((PyObject*)pyobj)->ob_refcnt = refcnt;

    // erase the object from tracking (weakref table already cleared, above)
        cppobjs->erase(ppo);

    // cleanup object internals
        pyobj->CppOwns();              // held object is out of scope now anyway
        op_dealloc_nofree(pyobj);      // normal object cleanup, while keeping memory

    // reset type object
        Py_INCREF((PyObject*)(void*)&CPyCppyy_NoneType);
        Py_DECREF(Py_TYPE(pyobj));
        ((PyObject*)pyobj)->ob_type = &CPyCppyy_NoneType;

        Py_DECREF(pyscope);
        return true;
    }

// unknown cppobj
    Py_DECREF(pyscope);
    return false;
}

//-----------------------------------------------------------------------------
bool CPyCppyy::MemoryRegulator::RegisterPyObject(
        CPPInstance* pyobj, Cppyy::TCppObject_t cppobj)
{
// start tracking <cppobj> proxied by <pyobj>
    if (!(pyobj && cppobj))
        return false;

    if (registerHook) {
        auto res = registerHook(cppobj, pyobj->ObjectIsA(false));
        if (!res.second) return res.first;
    }

    static PyObject* objectEraseCallback = PyCFunction_New(&gObjectEraseMethodDef, nullptr);

    CppToPyMap_t* cppobjs = ((CPPClass*)Py_TYPE(pyobj))->fImp.fCppObjects;
    if (!cppobjs)
         return false;

    CppToPyMap_t::iterator ppo = cppobjs->find(cppobj);
    if (ppo == cppobjs->end()) {
        PyObject* pyref = PyWeakref_NewRef((PyObject*)pyobj, objectEraseCallback);
        cppobjs->insert(std::make_pair(cppobj, pyref));
        return true;
    }

    return false;
}

//-----------------------------------------------------------------------------
bool CPyCppyy::MemoryRegulator::UnregisterPyObject(
        Cppyy::TCppObject_t cppobj, Cppyy::TCppType_t klass)
{
// stop tracking <object>, without notification
    if (!(cppobj && klass))
        return false;

    PyObject* pyscope = GetScopeProxy(klass);
    if (!CPPScope_Check(pyscope)) {
        Py_XDECREF(pyscope);
        return false;
    }

    if (unregisterHook) {
        auto res = unregisterHook(cppobj, klass);
        if (!res.second) return res.first;
    }

    CppToPyMap_t* cppobjs = ((CPPClass*)pyscope)->fImp.fCppObjects;
    if (!cppobjs) {
        Py_DECREF(pyscope);
        return false;
    }

    CppToPyMap_t::iterator ppo = cppobjs->find(cppobj);
    if (ppo != cppobjs->end()) {
        Py_DECREF(ppo->second);
        cppobjs->erase(ppo);
        Py_DECREF(pyscope);
        return true;
    }

    Py_DECREF(pyscope);
    return false;
}

//-----------------------------------------------------------------------------
PyObject* CPyCppyy::MemoryRegulator::RetrievePyObject(
        Cppyy::TCppObject_t cppobj, Cppyy::TCppType_t klass)
{
// lookup <object>, return old proxy if tracked
    if (!(cppobj && klass))
       return nullptr;

    PyObject* pyscope = GetScopeProxy(klass);
    if (!CPPScope_Check(pyscope)) {
        Py_XDECREF(pyscope);
        return nullptr;
    }

    CppToPyMap_t* cppobjs = ((CPPClass*)pyscope)->fImp.fCppObjects;
    if (!cppobjs) {
        Py_DECREF(pyscope);
        return nullptr;
    }

    CppToPyMap_t::iterator ppo = cppobjs->find(cppobj);
    if (ppo != cppobjs->end() ) {
        PyObject* pyobj = PyWeakref_GetObject(ppo->second);
        if (pyobj == Py_None) {
            Py_DECREF(ppo->second);
            cppobjs->erase(ppo);
            Py_DECREF(pyscope);
            return nullptr;
        }
        Py_DECREF(pyscope);
        Py_INCREF(pyobj);
        return pyobj;
    }

    Py_DECREF(pyscope);
    return nullptr;
}


//- private static members ------------------------------------------------------
PyObject* CPyCppyy::MemoryRegulator::EraseCallback(PyObject*, PyObject* pyref)
{
// called when one of the python objects we've registered is going away
    CPPInstance* pyobj = (CPPInstance*)PyWeakref_GetObject(pyref);
    if ((PyObject*)pyobj != Py_None) {
        CPPClass* pyclass = (CPPClass*)Py_TYPE(pyobj);
        void* cppobj = pyobj->GetObject();
        if (cppobj && pyclass->fImp.fCppObjects) {
        // erase if tracked
            CppToPyMap_t::iterator ppo = pyclass->fImp.fCppObjects->find(cppobj);
            if (ppo != pyclass->fImp.fCppObjects->end()) {
                Py_DECREF(ppo->second);
                pyclass->fImp.fCppObjects->erase(ppo);
            }
        }
    }

    Py_RETURN_NONE;
}
