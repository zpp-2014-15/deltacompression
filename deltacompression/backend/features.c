#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <malloc.h>
#include <string.h>

typedef unsigned long long ULL;

static PyObject* features_calculateFeatures(PyObject *self, PyObject *args) {
    const char *data;
    ULL prim, qmod, win, fmod, val, ppow, fval, mul, add;
    int i, j;
    Py_ssize_t amount;
    ULL *best, *features;
    PyObject *pis, *item, *result;
    Py_ssize_t data_len;

    if (!PyArg_ParseTuple(args, "s#KKKKO", &data, &data_len, &prim, &qmod,
                          &win, &fmod, &pis))
        return NULL;

    amount = PyList_Size(pis);
    if (!(best = malloc(2 * amount * sizeof(ULL))))
        return NULL;
    features = best + amount;

    for (i = 0; i < amount; i++) {
        // TODO ugly
        best[i] = 0;
        features[i] = 0;
    }

    ppow = 1;
    for (i = 1; i < win; i++)
        ppow = (ppow * prim) % qmod;

    val = 0;
    // TODO should be min
    for (i = 0; i < win; i++)
        val = (val * prim + data[i]) % qmod;

    for (i = win; i < data_len; i++) {
        val = (val + (qmod - data[i - win]) * ppow) % qmod;
        val = (val * prim + data[i]) % qmod;
        for (j = 0; j < amount; j++) {
            item = PyList_GET_ITEM(pis, j);
            // TODO free memory
            if (!PyArg_ParseTuple(item, "KK", &mul, &add))
                return NULL;
            fval = (val * mul + add) % fmod;
            if (fval > best[j]) {
                best[j] = fval;
                features[j] = val;
            }
        }
    }

    result = PyList_New(amount);
    for (i = 0; i < amount; i++) {
        PyList_SetItem(result, i, Py_BuildValue("K", features[i]));
    }
    free(best);
    return result;
}

static PyMethodDef FeaturesMethods[] = {
    {"calculateFeatures", features_calculateFeatures, METH_VARARGS,
     "calculate features for the given chunk"},
    {NULL, NULL, 0, NULL}
};

PyMODINIT_FUNC initfeatures(void) {
    Py_InitModule("features", FeaturesMethods);
}
