#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <malloc.h>
#include <string.h>

typedef unsigned long long ULL;

static PyObject* features_calculateFeatures(PyObject *self, PyObject *args) {
    const char *data;
    ULL prim, qmod, win, fmod, val, ppow, fval, mul, add;
    int i, j, min;
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

    ppow = 1;
    for (i = 1; i < win; i++)
        ppow = (ppow * prim) % qmod;

    val = 0;
    min = (win < data_len) ? win : data_len;
    for (i = 0; i < min; i++)
        val = (val * prim + data[i]) % qmod;

    if (win <= data_len) {
        for (j = 0; j < amount; j++) {
            item = PyList_GET_ITEM(pis, j);
            if (!PyArg_ParseTuple(item, "KK", &mul, &add))
                goto free_best;
            best[j] = (val * mul + add) % fmod;
            features[j] = val;
        }
    }

    for (i = win; i < data_len; i++) {
        val = (val + (qmod - data[i - win]) * ppow) % qmod;
        val = (val * prim + data[i]) % qmod;
        for (j = 0; j < amount; j++) {
            item = PyList_GET_ITEM(pis, j);
            if (!PyArg_ParseTuple(item, "KK", &mul, &add))
                goto free_best;
            fval = (val * mul + add) % fmod;
            if (fval > best[j]) {
                best[j] = fval;
                features[j] = val;
            }
        }
    }

    if (!(result = PyList_New(amount)))
        goto free_best;
    for (i = 0; i < amount; i++) {
        if (!(item = Py_BuildValue("K", features[i])))
            goto free_result;
        PyList_SET_ITEM(result, i, item);
    }
    free(best);
    return result;
free_result:
    Py_DECREF(result);
free_best:
    free(best);
    return NULL;
}

static PyMethodDef FeaturesMethods[] = {
    {"calculateFeatures", features_calculateFeatures, METH_VARARGS,
     "calculate features for the given chunk"},
    {NULL, NULL, 0, NULL}
};

PyMODINIT_FUNC initfeatures_calculator(void) {
    Py_InitModule("features_calculator", FeaturesMethods);
}
