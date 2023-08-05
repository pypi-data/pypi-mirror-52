/* Example of embedding Python in another program */

#include <stdio.h>
#include "Python.h"

void initrmsd(void); /* Forward */

main(int argc, char **argv) {
    /* Pass argv[0] to the Python interpreter */
    Py_SetProgramName(argv[0]);

    /* Initialize the Python interpreter.  Required. */
    Py_Initialize();

    /* Add a static module */
    initrmsd();

    /* Define sys.argv.  It is up to the application if you
       want this; you can also leave it undefined (since the Python
       code is generally not a main program it has no business
       touching sys.argv...) 

       If the third argument is true, sys.path is modified to include
       either the directory containing the script named by argv[0], or
       the current working directory.  This can be risky; if you run
       an application embedding Python in a directory controlled by
       someone else, attackers could put a Trojan-horse module in the
       directory (say, a file named os.py) that your application would
       then import and run.
       */
    PySys_SetArgvEx(argc, argv, 0);

    /* Do some application specific code */
    printf("Hello, brave new world\n\n");

    /* Execute some Python statements (in module __main__) */
    PyRun_SimpleString("import sys\n");
    PyRun_SimpleString("print sys.builtin_module_names\n");
    PyRun_SimpleString("print sys.modules.keys()\n");
    PyRun_SimpleString("print sys.executable\n");
    PyRun_SimpleString("print sys.argv\n");

    /* Note that you can call any public function of the Python
       interpreter here, e.g. call_object(). */

    /* Some more application specific code */
    printf("\nGoodbye, cruel world\n");

    /* Exit, cleaning up the interpreter */
    Py_Exit(0);
    /*NOTREACHED*/
}

typedef struct {
    double x;
    double y;
    double z;
} Atom;

Atom *atom_init(PyObject *o) {
    Atom *atom;

    atom = (Atom *) malloc(sizeof(Atom));
    atom->x = PyFloat_AsDouble(PyList_GetItem(o, 0));
    atom->y = PyFloat_AsDouble(PyList_GetItem(o, 1));
    atom->z = PyFloat_AsDouble(PyList_GetItem(o, 2));

    return atom;
}

typedef struct {
    int n;
    Atom **atoms;
} Residue;

Residue *residue_init(PyObject *o) {
    Residue *residue;
    int i;
    int num_atoms;

    residue = (Residue *) malloc(sizeof(Residue));

    num_atoms = PyList_Size(o);
    residue->n = num_atoms;
    residue->atoms = (Atom **) malloc(num_atoms * sizeof(Atom *));

    for (i = 0; i < num_atoms; i++) {
        residue->atoms[i] = atom_init(PyList_GET_ITEM(o, i));
    }

    return residue;
}

void residue_free(Residue *residue) {
    int i;

    for (i = 0; i < residue->n; i++) {
        free(residue->atoms[i]);
    }

    free(residue->atoms);
}

typedef struct {
    int n;
    Residue **residues;
} Chain;

Chain *chain_init(PyObject *o) {
    Chain *chain;
    int i;
    int num_residues;

    chain = (Chain *) malloc(sizeof(Chain));

    num_residues = PyList_Size(o);
    chain->n = num_residues;

    chain->residues = (Residue **) malloc(num_residues * sizeof(Residue *));
    for (i = 0; i < num_residues; i++) {
        chain->residues[i] = residue_init(PyList_GET_ITEM(o, i));
    }

    return chain;
}

void chain_free(Chain *chain) {
    int i;
    for (i = 0; i < chain->n; i++) {
        residue_free(chain->residues[i]);
    }

    free(chain->residues);
}

double atom_distance(Atom *atom1, Atom *atom2) {
    double x = atom1->x - atom2->x;
    double y = atom1->y - atom2->y;
    double z = atom1->z - atom2->z;
    return sqrt(x * x + y * y + z * z);
}

/* A static module */

/* 'self' is not used */
static PyObject * rmsd_foo(PyObject *self, PyObject* args) {
//    const char *command;
//    int sts;
//
//    if (!PyArg_ParseTuple(args, "s", &command)) return NULL;
//    sts = system(command);
//    if (sts < 0) {
//        PyErr_SetString(SpamError, "System command failed");
//        return NULL;
//    }
//    return PyLong_FromLong(sts);

    PyObject *pList;
//    PyObject *pItem;
    int n;
    int i, j, a, b;
    int *m;
    double cutoff;
    double threshold;
    int sum;
    double d;
    Chain *chain;

    if (!PyArg_ParseTuple(args, "O!dd", &PyList_Type, &pList, &cutoff, &threshold)) {
        PyErr_SetString(PyExc_TypeError, "parameter type error");
        return NULL;
    }

    chain = chain_init(pList);
    n = chain->n;

    m = (int *) malloc(n * n * sizeof(int));

    for (i = 0; i < n; i++) {
        for (j = i; j < n; j++) {
            if (i == j) {
                m[i * n + j] = 0;
            }
            else {
                sum = 0;
                for (a = 0; a < chain->residues[i]->n; a++) {
                    for (b = 0; b < chain->residues[j]->n; b++) {
                        d = atom_distance(chain->residues[i]->atoms[a], chain->residues[j]->atoms[b]);
                        if (d <= cutoff) {
                            sum = sum + 1;
                        }
                    }
                }
                m[i * n + j] = m[j * n + i] = (sum >= threshold ? sum : 0);
            }
        }
    }

    chain_free(chain);

    // Convert m to PyObject
    PyObject *l = PyList_New(n * n);
    for (i = 0; i < n * n; i++) {
//        printf("%d\n", m[i]);
        PyList_SET_ITEM(l, i, PyFloat_FromDouble((double)m[i]));
    }

    free(m);

    return l;
}

static PyMethodDef rmsd_methods[] = {
    {"rmsd", rmsd_foo, METH_VARARGS, "Return the meaning of everything."},
    {NULL, NULL}           /* sentinel */
};

void initrmsd(void) {
    PyImport_AddModule("rmsd");
    Py_InitModule("rmsd", rmsd_methods);
}

