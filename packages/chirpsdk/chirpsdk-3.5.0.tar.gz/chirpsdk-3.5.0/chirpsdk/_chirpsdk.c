/* ------------------------------------------------------------------------
 *
 *  This file is part of the Chirp Python SDK.
 *  For full information on usage and licensing, see https://chirp.io/
 *
 *  Copyright (c) 2011-2019, Asio Ltd.
 *  All rights reserved.
 *
 * ------------------------------------------------------------------------ */

#include <Python.h>
#include "include/chirp_sdk_events.h"

#if PY_MAJOR_VERSION >= 3
#define ERROR_INIT NULL
#else
#define ERROR_INIT /**/
#endif

#if PY_MAJOR_VERSION >= 3
static struct PyModuleDef moduledef = {
  PyModuleDef_HEAD_INIT,
  "_chirpsdk",
  NULL,
  -1,
  NULL,
  NULL,
  NULL,
  NULL,
  NULL
};
#endif

PyMODINIT_FUNC
#if PY_MAJOR_VERSION >= 3
PyInit__chirpsdk(void)
#else
init_chirpsdk(void)
#endif
{
    PyObject* m;
    PyEval_InitThreads();

#if PY_MAJOR_VERSION >= 3
    m = PyModule_Create(&moduledef);
#else
    m = Py_InitModule("_chirpsdk", NULL);
#endif

    // Constants
    PyModule_AddIntMacro(m, CHIRP_SDK_STATE_NOT_CREATED);
    PyModule_AddIntMacro(m, CHIRP_SDK_STATE_STOPPED);
    PyModule_AddIntMacro(m, CHIRP_SDK_STATE_RUNNING);
    PyModule_AddIntMacro(m, CHIRP_SDK_STATE_SENDING);
    PyModule_AddIntMacro(m, CHIRP_SDK_STATE_RECEIVING);

#if PY_MAJOR_VERSION >= 3
    return m;
#endif
}
