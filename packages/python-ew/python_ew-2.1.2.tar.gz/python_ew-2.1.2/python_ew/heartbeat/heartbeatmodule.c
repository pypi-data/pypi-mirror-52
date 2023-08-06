/* Python wrapper for heartbeating into an Earthworm ring.
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

#include <ringwriter.h>
#include <ringreader.h>

static PyObject *ring_write(PyObject *self, PyObject *args, PyObject *kws)
{
    char *unix_time, *ring, *module, *sequence;
    char *keywords[] = {"unix_time", "ring", "module", "sequence", NULL};
    int parsed;

    parsed = PyArg_ParseTupleAndKeywords(args, kws, "ssss", keywords, &unix_time, &ring, &module, &sequence);
    if (!parsed) {
	printf("HeartBeat: Wrong parameters! \n");
    }

    else {
	char *raw_data;
	char *params[] = {ring, "TYPE_HEARTBEAT", module, sequence};

	write_ring(unix_time, params, strlen(unix_time));
    }

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

static PyMethodDef heartbeatmodule_methods[] = {
    {"ring_write", (void*)ring_write, METH_VARARGS | METH_KEYWORDS, "Writes a TYPE_HEARTBEAT message into the a ring."},
    {"error_out", (PyCFunction)error_out, METH_NOARGS, NULL},
    {NULL, NULL}
};

#if PY_MAJOR_VERSION >= 3

static int heartbeatmodule_traverse(PyObject *m, visitproc visit, void *arg) {
    Py_VISIT(GETSTATE(m)->error);
    return 0;
}

static int heartbeatmodule_clear(PyObject *m) {
    Py_CLEAR(GETSTATE(m)->error);
    return 0;
}


static struct PyModuleDef moduledef = {
    PyModuleDef_HEAD_INIT,
    "heartbeatmodule",
    NULL,
    sizeof(struct module_state),
    heartbeatmodule_methods,
    NULL,
    heartbeatmodule_traverse,
    heartbeatmodule_clear,
    NULL
};

#define INITERROR return NULL

    PyMODINIT_FUNC
PyInit_heartbeatmodule(void)

#else
#define INITERROR return

    void
initheartbeatmodule(void)
#endif
{
#if PY_MAJOR_VERSION >= 3
    PyObject *module = PyModule_Create(&moduledef);
#else
    PyObject *module = Py_InitModule("heartbeatmodule", heartbeatmodule_methods);
#endif

    if (module == NULL)
        INITERROR;
    struct module_state *st = GETSTATE(module);

    st->error = PyErr_NewException("heartbeatmodule.Error", NULL, NULL);
    if (st->error == NULL) {
        Py_DECREF(module);
        INITERROR;
    }

#if PY_MAJOR_VERSION >= 3
    return module;
#endif
}
