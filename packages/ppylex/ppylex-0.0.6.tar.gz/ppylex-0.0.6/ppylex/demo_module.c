// pulls in the Python API 
#include <Python.h>
static int mul(int a,int b){
    return a*b;
}
static int add(int a,int b){
    return a+b;
}
// C function always has two arguments, conventionally named self and args
// The args argument will be a pointer to a Python tuple object containing the arguments.
// Each item of the tuple corresponds to an argument in the call's argument list.
static PyObject* demo_mul_and_add(PyObject *self, PyObject *args)
{
    const int a, b;
    // convert PyObject to C values
    if (!PyArg_ParseTuple(args, "ii", &a, &b))
        return NULL;
    int c=mul(a,b);
    int d=add(c,c);
    // convert C value to PyObject
    return Py_BuildValue("i", d);
}

// module's method table
static   PyMethodDef DemoMethods[] = {
    {"mul_and_add", demo_mul_and_add, METH_VARARGS, "Mul and Add two integers"},
    {NULL, NULL, 0, NULL} 
};
static struct PyModuleDef demomodule = {
    PyModuleDef_HEAD_INIT,
    "demo", /* module name */
    NULL, /* module documentation, may be NULL */
    -1,
    DemoMethods /* the methods array */
};

PyMODINIT_FUNC PyInit_demo(void)
{
    return PyModule_Create(&demomodule);
}