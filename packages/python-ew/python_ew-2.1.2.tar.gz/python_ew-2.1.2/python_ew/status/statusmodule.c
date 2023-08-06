/* Python wrapper for getting the current Earthworm status.
    Copyright (C) 2013, OSOP SA Panama

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>. */
    
#include <stdio.h>
#include <stdlib.h>

#include <Python.h>
#include <transport.h>
#include <earthworm.h>

#include <ringwriter.h>
#include <ringreader.h>

#define MAX_BYTES_STATUS MAX_BYTES_PER_EQ

static PyObject *ring_read(PyObject *self, PyObject *args, PyObject *kws)
{	
    char *ring, *module, *sequence;
    char *keywords[] = {"ring", "module", "sequence", NULL};

    if (!PyArg_ParseTupleAndKeywords(args, kws, "sss", keywords, &ring, &module, &sequence)) {
        printf("Status: Wrong parameters! \n");
        return Py_BuildValue("");		
    }

    unsigned char items = 0;
    char *params[] = {ring, "TYPE_STATUS", module};
    char *raw_data[1000];
    char *write_params[] = {ring, "TYPE_REQSTATUS", module, sequence};

    // Request status before reading.
    write_ring(module, write_params, strlen(module));
    
    sleep(10);

    items = read_ring(params, MAX_BYTES_STATUS, raw_data);

    if (items > 0)
        return Py_BuildValue("s", raw_data[0]);

    else 
        return Py_BuildValue("");
}

// Module initialization

struct module_state {
    PyObject *error;
};

#if PY_MAJOR_VERSION >= 3
#define GETSTATE(m) ((struct module_state*)PyModule_GetState(m))
#else
#define GETSTATE(m) (&_state)
static struct module_state _state;
#endif

static PyObject *
error_out(PyObject *m) {
    struct module_state *st = GETSTATE(m);
    PyErr_SetString(st->error, "something bad happened");
    return NULL;
}

static PyMethodDef statusmodule_methods[] = {
    {"ring_read", (void*)ring_read, METH_VARARGS | METH_KEYWORDS, "Reads TYPE_STATUS messages from the ring."},
    {"error_out", (PyCFunction)error_out, METH_NOARGS, NULL},
    {NULL, NULL}
};

#if PY_MAJOR_VERSION >= 3

static int statusmodule_traverse(PyObject *m, visitproc visit, void *arg) {
    Py_VISIT(GETSTATE(m)->error);
    return 0;
}

static int statusmodule_clear(PyObject *m) {
    Py_CLEAR(GETSTATE(m)->error);
    return 0;
}


static struct PyModuleDef moduledef = {
    PyModuleDef_HEAD_INIT,
    "statusmodule",
    NULL,
    sizeof(struct module_state),
    statusmodule_methods,
    NULL,
    statusmodule_traverse,
    statusmodule_clear,
    NULL
};

#define INITERROR return NULL

    PyMODINIT_FUNC
PyInit_statusmodule(void)

#else
#define INITERROR return

    void
initstatusmodule(void)
#endif
{
#if PY_MAJOR_VERSION >= 3
    PyObject *module = PyModule_Create(&moduledef);
#else
    PyObject *module = Py_InitModule("statusmodule", statusmodule_methods);
#endif

    if (module == NULL)
        INITERROR;
    struct module_state *st = GETSTATE(module);

    st->error = PyErr_NewException("statusmodule.Error", NULL, NULL);
    if (st->error == NULL) {
        Py_DECREF(module);
        INITERROR;
    }

#if PY_MAJOR_VERSION >= 3
    return module;
#endif
}
