// alsmodule.c - a non-obstrusive (raw data returned) interface to access
//               ambient light sensors samples from python 3 on Apple computers
//               running Mac OS X
//
// Copyright (C) 2019 Jean-Jacques Puig
// 
// This program is free software: you can redistribute it and/or modify it
// under the terms of the GNU General Public License as published by the Free
// Software Foundation, either version 3 of the License, or (at your option)
// any later version.
// 
// This program is distributed in the hope that it will be useful, but WITHOUT
// ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
// FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
// more details.
// 
// You should have received a copy of the GNU General Public License along with
// this program. If not, see <https://www.gnu.org/licenses/>.

#define PY_SSIZE_T_CLEAN

#include <mach/mach.h>
#include <IOKit/IOKitLib.h>
#include "Python.h"

#define LMU_CONTROLLER "AppleLMUController"
#define K_GET_SENSOR_READING_ID 0

static PyObject *AlsError;
static io_connect_t dataPort = 0;

static PyObject *
getSensorReadings(PyObject *self, PyObject *args)
{
    PyObject *readings, *reading;
    uint32_t values_nb = 2;
    uint64_t values[values_nb];
    kern_return_t kret;

    if (!PyArg_ParseTuple(args, ";"))
        return NULL;

    kret = IOConnectCallMethod(dataPort, K_GET_SENSOR_READING_ID,
                                NULL, 0, NULL, 0,
                                values, &values_nb, NULL, 0);

    if (kret == KERN_SUCCESS) {
        readings = PyList_New(values_nb);
        if (readings == NULL)
            return NULL;

        while (values_nb > 0) {
            values_nb--;

            reading = PyLong_FromLong(values[values_nb]);
            if (reading == NULL)
                return NULL;

            if (PyList_SetItem(readings, values_nb, reading))
                return NULL;
        }

        return readings;
    }

    /* mach_error("IOConnectCallMethod:", kret); */
    switch (kret) {

    case kIOReturnBusy:
        PyErr_SetString(AlsError, "device busy");
        break;

    default:
        PyErr_SetString(AlsError, "unknown error");
        break;
    }

    return NULL;
}

static PyMethodDef AlsMethods[] = {
    {"getSensorReadings",
    	getSensorReadings, METH_VARARGS,
	"Returns light sensor readings as a list of integers"},
    {NULL, NULL, 0, NULL} /* Sentinel */
};

static struct PyModuleDef AlsModule = {
    PyModuleDef_HEAD_INIT,
    "als",
    "A module to access ambient light sensor on Mac OS X",
    -1,
    AlsMethods
};

PyMODINIT_FUNC
PyInit_als(void)
{
    PyObject *mod;

    io_service_t servObj;
    kern_return_t kret;

    mod = PyModule_Create(&AlsModule);
    if (mod == NULL)
        return NULL;

    AlsError = PyErr_NewException("als.error", NULL, NULL);
    Py_INCREF(AlsError);
    PyModule_AddObject(mod, "error", AlsError);

    servObj = IOServiceGetMatchingService(kIOMasterPortDefault,
                                            IOServiceMatching(LMU_CONTROLLER));

    if (!servObj) {
        PyErr_SetString(PyExc_OSError, "no matching service");
        return NULL;
    }

    kret = IOServiceOpen(servObj, mach_task_self(), 0, &dataPort);
    if (kret != KERN_SUCCESS) {
        PyErr_SetString(PyExc_OSError, "service open failed");
        /* mach_error("IOServiceOpen:", kret); */
        return NULL;
    }

    kret = IOObjectRelease(servObj);
    if (kret != KERN_SUCCESS) {
        PyErr_SetString(PyExc_OSError, "object release failed");
        /* mach_error("IOObjectRelease:", kret); */
        return NULL;
    }

    return mod;
}
