#include <stdio.h>
#include <Python.h>

static PyObject* cpydemo_helloworld(PyObject* self, PyObject* args) {
    printf("Hello World!\n");
    return Py_BuildValue("");
}

static PyMethodDef methods[] = {
    {"helloworld", cpydemo_helloworld, METH_VARARGS, "Test"},
    {NULL, NULL, METH_VARARGS, NULL}
};

static PyModuleDef module = {
    PyModuleDef_HEAD_INIT,
    "cpydemo",
    NULL,
    -1,
    methods
};

void PyInit_cpydemo() {
    PyModule_Create(&module);
}
