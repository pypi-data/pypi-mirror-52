/*
 * Copyright 2019 jasLogic
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include "structmember.h"

#include <mipea/gpio.h>

typedef struct {
        PyObject_HEAD;
        int pin;
} GPIOObject;

static int GPIO_init(GPIOObject *self, PyObject *args, PyObject *kwargs)
{
        static char *kwlist[] = {"pin", "output", "function", "pud", NULL};
        unsigned int output = 0;
        unsigned int function = INPUT;
        unsigned int pud = PUD_DISABLE;

        if (PyArg_ParseTupleAndKeywords(args, kwargs, "I|pII", kwlist,
                &self->pin, &output, &function, &pud) < 0)
                return -1;

        if (output)
                gpio_out(self->pin);
        else
                gpio_inp(self->pin);

        if (function != INPUT)
                gpio_func(self->pin, function);

        if (pud != PUD_DISABLE)
                gpio_pud(self->pin, pud);

        return 0;
}

static PyObject *GPIO_set(GPIOObject *self, PyObject *args)
{
        unsigned int lvl = 1;
        if (PyArg_ParseTuple(args, "|I", &lvl) < 0)
                return NULL;

        if (lvl > 0)
                gpio_set(self->pin);
        else
                gpio_clr(self->pin);

        Py_RETURN_NONE;
}
static PyObject *GPIO_clr(GPIOObject *self)
{
        gpio_clr(self->pin);
        Py_RETURN_NONE;
}
static PyObject *GPIO_tst(GPIOObject *self)
{
        if (gpio_tst(self->pin))
                Py_RETURN_TRUE;
        else
                Py_RETURN_FALSE;
}
static PyObject *GPIO_pud(GPIOObject *self, PyObject *args)
{
        unsigned int pud;
        if (PyArg_ParseTuple(args, "I", &pud) < 0)
                return NULL;
        gpio_pud(self->pin, pud);

        Py_RETURN_NONE;
}

static PyMethodDef GPIO_methods[] = {
        {"set", (PyCFunction) GPIO_set, METH_VARARGS, "set pin (HIGH or LOW)"},
        {"clr", (PyCFunction) GPIO_clr, METH_NOARGS, "clear pin"},
        {"tst", (PyCFunction) GPIO_tst, METH_NOARGS, "test pin"},
        {"pud", (PyCFunction) GPIO_pud, METH_VARARGS, "set pullup/-down"},
        {NULL}
};

// make pin not writeable
static PyObject *GPIO_get_pin(GPIOObject *self, void *closure)
{
        printf("GETTER\n");
        return PyLong_FromUnsignedLong(self->pin);
}
static int GPIO_set_pin(GPIOObject *self, PyObject *value, void *closure)
{
        printf("SETTER\n");
        PyErr_SetString(PyExc_AttributeError, "Attribute \"pin\" is not writeable");
        return -1;
}
static PyGetSetDef GPIO_getsetters[] = {
        {"pin", (getter) GPIO_get_pin, (setter) GPIO_set_pin, "pin number", NULL},
        {NULL}
};

static PyTypeObject GPIOType = {
        PyVarObject_HEAD_INIT(NULL, 0)
        .tp_name = "mipea.gpio.GPIO",
        .tp_doc = "mipea GPIO object",
        .tp_basicsize = sizeof(GPIOObject),
        .tp_itemsize = 0,
        .tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
        .tp_new = PyType_GenericNew,
        .tp_init = (initproc) GPIO_init,
        .tp_methods = GPIO_methods,
        .tp_getset = GPIO_getsetters
};

static PyModuleDef gpiomodule = {
        PyModuleDef_HEAD_INIT,
        .m_name = "gpio",
        .m_doc = "gpio from mipea for the Raspberry Pi",
        .m_size = -1,
        .m_free = (freefunc) gpio_unmap
};

PyMODINIT_FUNC PyInit_gpio(void)
{
        // initialize module
        PyObject *module;
        module = PyModule_Create(&gpiomodule);
        if (module == NULL)
                return NULL;

        // initialize classes
        if (PyType_Ready(&GPIOType) < 0)
                return NULL;

        Py_INCREF(&GPIOType);
        // add class to module
        if (PyModule_AddObject(module, "GPIO", (PyObject *)&GPIOType) < 0)
                return NULL;

        // enums
        PyModule_AddIntConstant(module, "HIGH", 1);
        PyModule_AddIntConstant(module, "LOW", 0);

        PyModule_AddIntConstant(module, "INPUT", INPUT);
        PyModule_AddIntConstant(module, "OUTPUT", OUTPUT);
        PyModule_AddIntConstant(module, "ALT0", ALT0);
        PyModule_AddIntConstant(module, "ALT1", ALT1);
        PyModule_AddIntConstant(module, "ALT2", ALT2);
        PyModule_AddIntConstant(module, "ALT3", ALT3);
        PyModule_AddIntConstant(module, "ALT4", ALT4);
        PyModule_AddIntConstant(module, "ALT5", ALT5);

        PyModule_AddIntConstant(module, "PUD_DISABLE", PUD_DISABLE);
        PyModule_AddIntConstant(module, "PUD_DOWN", PUD_DOWN);
        PyModule_AddIntConstant(module, "PUD_UP", PUD_UP);

        if (gpio_map() < 0)
                return PyErr_SetFromErrno(PyExc_Exception);

        return module;
}
