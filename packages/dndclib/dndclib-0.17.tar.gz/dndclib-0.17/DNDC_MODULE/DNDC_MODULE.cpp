//
//  DNDC_Library.cpp
//
//
//  Created by zhang feng on 2015/3/13.
//
//

#ifdef _DEBUG
#define _DEBUG_WSD_DEFINED 1
#undef _DEBUG
#endif

#include <Python.h>//;

#ifdef _DEBUG_WAS_DEFINED
#define _DEBUG 1
#endif



//#include "DNDC_MODULE.h"//;

#include "math.h"//;
#include <algorithm>////;
#include <iostream>
#include <fstream>
#include <vector>
//#include <wchar.h>


using std::string;

//using namespace std;

static PyObject* py_myFunction(PyObject* self, PyObject* args)
{
    double x, y;
    PyArg_ParseTuple(args, "dd", &x, &y);
    return Py_BuildValue("d", x*y);
};


//void Heat_Transfer(int n, int qq,float F_snow,float snow_pack,float K[200], float Z[200], float C[200],
//                   float Surf_Temp,float temp[200],float yr_avetj)



static PyObject* O2_diffusion(PyObject* self, PyObject* args)
{

	// O2 diffusion function
	PyObject *Soil_Eh_list;
	PyObject *Soil_O2_list;
	PyObject *full_O2_list;

	PyArg_ParseTuple(args, "OOO", &Soil_Eh_list, &Soil_O2_list,&full_O2_list);


	if (PyList_Check(Soil_Eh_list) == false)
	{
		std::cout << " Soil_Eh_list should be a list " << std::endl;
		return NULL;
	}

	if (PyList_Check(Soil_O2_list) == false)
	{
		std::cout << " Soil_O2_list should be a list " << std::endl;
		return NULL;
	}

	if (PyList_Check(full_O2_list) == false)
	{
		std::cout << " full_O2_list should be a list " << std::endl;
		return NULL;
	}


	const long int maxlength = 50000;

	double Soil_Eh[maxlength];
	double Soil_O2[maxlength];
	double full_O2[maxlength];

	long int length = PyObject_Length(Soil_O2_list);
	// since VC not support variable-length arrays, use this const variable in here.

	for (int bbb = 0; bbb <= length; bbb++)
	{

		if (PyList_Check(Soil_O2_list) == true)
		{
			Soil_Eh[bbb] = PyFloat_AsDouble(PyList_GetItem(Soil_Eh_list, bbb));
			Soil_O2[bbb] = PyFloat_AsDouble(PyList_GetItem(Soil_O2_list, bbb));
			full_O2[bbb] = PyFloat_AsDouble(PyList_GetItem(full_O2_list, bbb));
		}

	}
	for (int l = 0; l <= length; l++)
	{
		if (l > 0) // diffusion
		{
			float ave_O2 = (Soil_O2[l] + Soil_O2[l - 1]) * 0.5;
			Soil_O2[l - 1] = ave_O2;
			Soil_O2[l] = ave_O2;
		}

		if (Soil_O2[l] < 0.0)
		{
			Soil_O2[l] = 0.0;
		}
		if (Soil_O2[l] > 0.0)
		{
			Soil_Eh[l] = 626.1 * Soil_O2[l] / full_O2[l];
		}
		else
		{
			if (Soil_Eh[l] > 0.0) Soil_Eh[l] = 0.0;
		}

	}



	//Py_RETURN_TRUE
	// Return value.
	PyObject *pyO2list, *pyEhlist,*item,*return_list;
	pyO2list = PyList_New(length);
	pyEhlist = PyList_New(length);
	return_list = PyList_New(2);
	if (pyO2list != NULL)
	{
		for (int nn = 0; nn<length; nn++)
		{
			item = PyFloat_FromDouble(Soil_Eh[nn]);
			PyList_SET_ITEM(pyEhlist, nn, item);
			item = PyFloat_FromDouble(Soil_O2[nn]);
			PyList_SET_ITEM(pyO2list, nn, item);
		}
	}
	//return pyEhlist, pyO2list;
	PyList_SetItem(return_list, 0, pyEhlist);
	//PyList_SET_ITEM(return_list, 1, pyO2list);
	PyList_SetItem(return_list, 1, pyO2list);
	return return_list;

};



static PyObject* Heat_Transfer(PyObject* self, PyObject* args)

{
    int qq;
    int WV;
    double snow_pack;
    double Surf_Temp;
    double yr_avetj;

    PyObject *K_list;
    PyObject *Z_list;
    PyObject *C_list;
    PyObject *temp_list;


    double outQ[200], Kave, dQ;
    double a = 10000.0; //5000

    PyArg_ParseTuple(args, "iidddOOOO", &qq, &WV,&snow_pack,&yr_avetj,&Surf_Temp,&K_list,&Z_list,&C_list,&temp_list);

//    std::cout << "yr_avetj -->" << yr_avetj<<"  "<<qq<<"  "<<snow_pack << std::endl;


//    PyObject *K_list = PyTuple_GetItem(args, 4);
//    PyObject *Z_list = PyTuple_GetItem(args,5);
//    PyObject *C_list = PyTuple_GetItem(args,6);
//    PyObject *temp_list = PyTuple_GetItem(args,7);

    if (PyList_Check(K_list) == false)
    {
        std::cout << " K should be a list "<< std::endl;
        return NULL;
    }

    if (PyList_Check(Z_list) == false)
    {
        std::cout << " Z should be a list "<< std::endl;
        return NULL;
    }

    if (PyList_Check(C_list) == false)
    {
        std::cout << " C should be a list "<< std::endl;
        return NULL;
    }

    if (PyList_Check(temp_list) == false)
    {
        std::cout << " temp should be a list "<< std::endl;
        return NULL;
    }

	// since VC not support variable-length arrays, use this const variable in here.
	const int max_length = 65535;
    int length = PyObject_Length(temp_list);

//    std::cout << "object length -->" << length << std::endl;


//     long length = PyNumber_Long(PyTuple_Size(temp_list));



    double K[max_length];
    double Z[max_length];
    double C[max_length];
    double temp[max_length];


//    PyObject *iter = PyObject_GetIter(K_list);
//    if (!iter) {
//        std::cout << " Wrong type "<< std::endl;
//        return NULL;
//    }
//
//    while (true)
//    {
//        PyObject *next = PyIter_Next(iter);
//        if (!next)
//        {
//            // nothing left in the iterator
//            break;
//        }
//
//
//        if (!PyFloat_Check(next))
//        {
//            // error, we were expecting a floating point value
//        }
//
//        double foo = PyFloat_AsDouble(next);
//        // do something with foo
//    }

    for (int bbb=0; bbb<=length; bbb++)
    {

        if (PyList_Check(K_list) == true)
        {
            K[bbb] = PyFloat_AsDouble(PyList_GetItem(K_list,bbb));
            Z[bbb] = PyFloat_AsDouble(PyList_GetItem(Z_list,bbb));
            C[bbb] = PyFloat_AsDouble(PyList_GetItem(C_list,bbb));
            temp[bbb] = PyFloat_AsDouble(PyList_GetItem(temp_list,bbb));

//            std::cout << C[bbb] << " " << Z[bbb] << " " << K[bbb] << " "<< temp[bbb] << std::endl;

        }


    }

//    std::cout << "yr_avetj -->" << yr_avetj<<"  "<<qq<<"  "<<snow_pack << std::endl;


//    PyObject *num = PyNumber_Float(PyTuple_GetItem(args, 3));
//    float voltage = PyFloat_AsDouble(num);
//    Py_XDECREF(num);


    //Heat flux from layer L-1 down to L

//    int WV = 200;

    for (int n=1; n<=WV; n++)
    {

        for (int l=1; l<=qq; l++)
        {
            a = 10000.0; //5000

            if (l==1)
            {
                float F_snow = 100.0 * snow_pack;
                if (F_snow < 1.0) F_snow = 1.0;

                //heat transfer between air and first layer

                if(snow_pack > 0.0)
                    outQ[l-1] = a * K[l] * (Surf_Temp - temp[l]) / Z[l] / F_snow;//J/(cm2*day)
                else
                    outQ[l-1] = a * K[l] * (Surf_Temp - temp[l]) / Z[l];
            }

            if (l<qq)
            {
                Kave = (K[l] + K[l+1]) / 2.0;
                //heat from layer l to l+1
                outQ[l] = 2000.0 * Kave * (temp[l] - temp[l+1]) / (Z[l+1] - Z[l]);
            }
            else
            {
                //heat from bottom layer to deeper soil
                outQ[l] = a * K[l] * (temp[l] - yr_avetj) / (200.0 - Z[l]);
            }

            dQ = outQ[l-1] - outQ[l];

            float dT = dQ / C[l];

            temp[l] += dT;

//            std::cout << temp[l] << std::endl;
//
//            std::cout << K[l] << std::endl;
//
//            std::cout << Z[l] << std::endl;
//
//            std::cout << C[l] << std::endl;
//
//            std::cout << outQ[l] << std::endl;


            if(Surf_Temp>=yr_avetj) temp[l] = std::min(Surf_Temp, std::max(yr_avetj, temp[l]));
            else temp[l] = std::min(yr_avetj, std::max(Surf_Temp, temp[l]));


        } // l loop

    } // n


    //Py_RETURN_TRUE
    // Return value.
    PyObject *pylist, *item;
    pylist = PyList_New(length);
    if (pylist != NULL)
    {
        for (int nn=0; nn<length; nn++)
        {
            item = PyFloat_FromDouble(temp[nn]);
            PyList_SET_ITEM(pylist, nn, item);
        }
    }
    return pylist;


    //return Py_BuildValue("d", &temp);

};

static PyObject* test_func(PyObject* self, PyObject* args)

{
	int qq;
	//    int WV;
	double snow_pack;
	double Surf_Temp;
	double yr_avetj;

	PyObject *K_list;
	PyObject *Z_list;
	PyObject *C_list;
	PyObject *temp_list;

	//    PyArg_ParseTuple(args, "iidddOOOO", &qq,&WV,&snow_pack,&yr_avetj,&Surf_Temp,&K_list,&Z_list,&C_list,&temp_list);
	PyArg_ParseTuple(args, "idddOOOO", &qq, &snow_pack, &yr_avetj, &Surf_Temp, &K_list, &Z_list, &C_list, &temp_list);

	
	if (PyList_Check(K_list) == false)
	{
		std::cout << " K should be a list " << std::endl;

		return NULL;
	}
	std::cout << K_list << std::endl;

	if (PyList_Check(Z_list) == false)
	{
		std::cout << " Z should be a list " << std::endl;
		return NULL;
	}

	if (PyList_Check(C_list) == false)
	{
		std::cout << " C should be a list " << std::endl;
		return NULL;
	}

	if (PyList_Check(temp_list) == false)
	{
		std::cout << " temp should be a list " << std::endl;
		return NULL;
	}

	// since VC not support variable-length arrays, use this const variable in here.
	const long int max_length = 30000;
	long int length = PyObject_Length(temp_list);
	//int length = 10000;
	//int length = malloc(PyObject_Length(temp_list));
	//    std::cout << "object length -->" << length << std::endl;


	//     long length = PyNumber_Long(PyTuple_Size(temp_list));

	//    vector<double>K(length);
	//	vector<double> K[length];
	//    vector<double> Z[length];
	//    vector<double> C[length];
	//    vector<double> temp[length];
	//	vector<double> outQ[length];

	double outQ[max_length];

	double K[max_length];
	double Z[max_length];
	double C[max_length];
	double temp[max_length];

	//double outQ[max_length];

	double Kave, dQ;
	double a = 10000.0; //5000

	for (int bbb = 0; bbb<length; bbb++)
	{


		K[bbb] = PyFloat_AsDouble(PyList_GetItem(K_list, bbb));
		Z[bbb] = PyFloat_AsDouble(PyList_GetItem(Z_list, bbb));
		C[bbb] = PyFloat_AsDouble(PyList_GetItem(C_list, bbb));
		temp[bbb] = PyFloat_AsDouble(PyList_GetItem(temp_list, bbb));

		//std::cout << C[bbb] << " " << Z[bbb] << " " << K[bbb] << " "<< temp[bbb] << std::endl;

	}

	int WV = 200;
	float outQ_surface;
	float F_snow;
	float dT;

	for (int n = 0; n<WV; n++)
	{

		for (int l = 0; l<qq; l++)
		{
			outQ_surface = 0;

			if (l == 0)
			{
				F_snow = 100.0 * snow_pack;
				if (F_snow < 1.0) F_snow = 1.0;

				//heat transfer between air and first layer

				if (snow_pack > 0.0)
					//outQ[l-1] = a * K[l] * (Surf_Temp - temp[l]) / Z[l] / F_snow;//J/(cm2*day)
					outQ_surface += a * K[l] * (Surf_Temp - temp[l]) / Z[l] / F_snow; //J/(cm2*day)
				else
					//outQ[l-1] = a * K[l] * (Surf_Temp - temp[l]) / Z[l];
					outQ_surface += a * K[l] * (Surf_Temp - temp[l]) / Z[l];
			}

			if (l<qq - 1)
			{
				Kave = (K[l] + K[l + 1]) / 2.0;
				//heat from layer l to l+1
				outQ[l] = 2000.0 * Kave * (temp[l] - temp[l + 1]) / (Z[l + 1] - Z[l]);
			}
			else
			{
				//heat from bottom layer to deeper soil
				outQ[l] = a * K[l] * (temp[l] - yr_avetj) / (200.0 - Z[l]);
			}


			if (l == 0)
			{
				dQ = outQ_surface - outQ[l];
			}
			else
			{
				dQ = outQ[l - 1] - outQ[l];
			}


			dT = dQ / C[l];

			temp[l] += dT;


			if (Surf_Temp >= yr_avetj) temp[l] = std::min(Surf_Temp, std::max(yr_avetj, temp[l]));
			else temp[l] = std::min(yr_avetj, std::max(Surf_Temp, temp[l]));


		} // l loop

	} // n

	PyObject *pylist, *item;
	pylist = PyList_New(length);
	if (pylist != NULL)
	{
		for (int nn = 0; nn<length; nn++)
		{
			item = PyFloat_FromDouble(temp[nn]);
			PyList_SET_ITEM(pylist, nn, item);
		}
	}
	return pylist;


}
// This function used in the model...
static PyObject* Heat_Transfer_New(PyObject* self, PyObject* args)

{
    int qq;
    double snow_pack;
    double Surf_Temp;
    double yr_avetj;

	PyObject *K_list;
	PyObject *Z_list;
	PyObject *C_list;
	PyObject *temp_list;

	

//    PyArg_ParseTuple(args, "iidddOOOO", &qq,&WV,&snow_pack,&yr_avetj,&Surf_Temp,&K_list,&Z_list,&C_list,&temp_list);
	PyArg_ParseTuple(args, "idddOOOO", &qq, &snow_pack, &yr_avetj, &Surf_Temp, &K_list, &Z_list, &C_list, &temp_list);
	

//	if (!PyArg_ParseTuple(args, "idddOOOO", &qq, &snow_pack, &yr_avetj, &Surf_Temp, &K_list, &Z_list, &C_list, &temp_list))
//	{
//		goto error;
//	}
//error:
//	return 0;
	


    if (PyList_Check(K_list) == false)
    {
        std::cout << " K should be a list "<< std::endl;
        return NULL;
    }

    if (PyList_Check(Z_list) == false)
    {
        std::cout << " Z should be a list "<< std::endl;
        return NULL;
    }

    if (PyList_Check(C_list) == false)
    {
        std::cout << " C should be a list "<< std::endl;
        return NULL;
    }

    if (PyList_Check(temp_list) == false)
    {
        std::cout << " temp should be a list "<< std::endl;
        return NULL;
    }

	// since VC not support variable-length arrays, use this const variable in here.
	const long int max_length = 50000;
    long int length = PyObject_Length(temp_list);
    //int length = 10000;
    //int length = malloc(PyObject_Length(temp_list));
    //    std::cout << "object length -->" << length << std::endl;


    //     long length = PyNumber_Long(PyTuple_Size(temp_list));

//    vector<double>K(length);
//	vector<double> K[length];
//    vector<double> Z[length];
//    vector<double> C[length];
//    vector<double> temp[length];
//	vector<double> outQ[length];

    double outQ[max_length];

    double K[max_length];
    double Z[max_length];
    double C[max_length];
    double temp[max_length];

    //double outQ[max_length];

    double Kave, dQ;
    double a = 10000.0; //5000

    for (int bbb=0; bbb<length; bbb++)
    {


            K[bbb] = PyFloat_AsDouble(PyList_GetItem(K_list,bbb));
            Z[bbb] = PyFloat_AsDouble(PyList_GetItem(Z_list,bbb));
            C[bbb] = PyFloat_AsDouble(PyList_GetItem(C_list,bbb));
            temp[bbb] = PyFloat_AsDouble(PyList_GetItem(temp_list,bbb));

            //std::cout << C[bbb] << " " << Z[bbb] << " " << K[bbb] << " "<< temp[bbb] << std::endl;

    }

    //Heat flux from layer L-1 down to L

    int WV = 200;
    float outQ_surface;
    float F_snow;
    float dT ;

    for (int n=0; n<WV; n++)
    {

        for (int l=0; l<qq; l++)
        {
            outQ_surface = 0;

            if (l==0)
            {
                F_snow = 100.0 * snow_pack;
                if (F_snow < 1.0) F_snow = 1.0;

                //heat transfer between air and first layer

                if(snow_pack > 0.0)
                    //outQ[l-1] = a * K[l] * (Surf_Temp - temp[l]) / Z[l] / F_snow;//J/(cm2*day)
                    outQ_surface += a * K[l] * (Surf_Temp - temp[l]) / Z[l] / F_snow; //J/(cm2*day)
                else
                    //outQ[l-1] = a * K[l] * (Surf_Temp - temp[l]) / Z[l];
                    outQ_surface += a * K[l] * (Surf_Temp - temp[l]) / Z[l];
            }

            if (l<qq-1)
            {
                Kave = (K[l] + K[l+1]) / 2.0;
                //heat from layer l to l+1
                outQ[l] = 2000.0 * Kave * (temp[l] - temp[l+1]) / (Z[l+1] - Z[l]);
            }
            else
            {
                //heat from bottom layer to deeper soil
                outQ[l] = a * K[l] * (temp[l] - yr_avetj) / (200.0 - Z[l]);
            }


            if (l == 0)
            {
                dQ = outQ_surface - outQ[l];
            }
            else
            {
                dQ = outQ[l-1] - outQ[l];
            }


            dT = dQ / C[l];

            temp[l] += dT;


            if(Surf_Temp>=yr_avetj) temp[l] = std::min(Surf_Temp, std::max(yr_avetj, temp[l]));
            else temp[l] = std::min(yr_avetj, std::max(Surf_Temp, temp[l]));


        } // l loop

    } // n


    //Py_RETURN_TRUE
    // Return value.
    PyObject *pylist, *item;
    pylist = PyList_New(length);
    if (pylist != NULL)
    {
        for (int nn=0; nn<length; nn++)
        {
            item = PyFloat_FromDouble(temp[nn]);
            PyList_SET_ITEM(pylist, nn, item);
        }
    }
    return pylist;


    //return Py_BuildValue("d", &temp);

};


/*
 * Bind Python function names to our C functions
 */



static PyMethodDef myModule_methods[] =
{
    {"myFunction", py_myFunction, METH_VARARGS},
    {"Heat_Transfer_Old", Heat_Transfer, METH_VARARGS},
    {"Heat_Transfer_New", Heat_Transfer_New, METH_VARARGS},
	{ "O2_diffusion", O2_diffusion, METH_VARARGS },
	{ "testfunc", test_func, METH_VARARGS },
    {NULL, NULL}
};


/*
 * Python calls this to let us initialize our module
 */
//void initDNDC_MODULE()
//{
//    (void) Py_InitModule("DNDC_MODULE", myModule_methods);
//};

#if PY_MAJOR_VERSION >= 3
static struct PyModuleDef myextension_methods =
{
    PyModuleDef_HEAD_INIT,
    "dndclib", /* name of module */
    "",          /* module documentation, may be NULL */
    -1,          /* size of per-interpreter state of the module, or -1 if the module keeps state in global variables. */
    myModule_methods
};
#endif


#if PY_MAJOR_VERSION >= 3
PyMODINIT_FUNC PyInit_dndclib()
{
    
    #if PY_MAJOR_VERSION >= 3
        PyObject *module = PyModule_Create(&myextension_methods);
        if (!module) return NULL;
    #else
        PyObject *m = Py_InitModule("dndclib",myModule_methods);
    #endif
    
        
    #if PY_MAJOR_VERSION >= 3
        return module;
    #else
        if (m == NULL)
        {
            return;
        }
    #endif

}
#endif


PyMODINIT_FUNC initdndclib()
{
    
#if PY_MAJOR_VERSION >= 3
    PyObject *module = PyModule_Create(&myextension_methods);
    if (!module) return NULL;
#else
    PyObject *m = Py_InitModule("dndclib",myModule_methods);
#endif
    
    
#if PY_MAJOR_VERSION >= 3
    return module;
#else
    if (m == NULL)
    {
        return;
    }
#endif
    
}

int main(int argc, char *argv[])
{
    
    /* These have to be wchar_t */
    char *str_program_name = argv[0];
    
    
    #if PY_MAJOR_VERSION >= 3
        wchar_t *_program_name = (wchar_t*)str_program_name;
    #else
        char *_program_name = str_program_name;
    #endif
    
    
    /* Pass argv[0] to the Python interpreter */
    Py_SetProgramName(_program_name);
    /* Initialize the Python interpreter.  Required. */
    Py_Initialize();

    /* Add a static module */
    #if PY_MAJOR_VERSION >= 3
         PyInit_dndclib();
    #else
        initdndclib();
    #endif

    
    Py_Finalize();
    
}
