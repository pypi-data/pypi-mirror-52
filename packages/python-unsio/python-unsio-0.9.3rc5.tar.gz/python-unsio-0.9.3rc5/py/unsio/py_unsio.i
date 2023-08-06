//-*- C -*-
// ============================================================================
// Copyright Jean-Charles LAMBERT - 2008-2019
//           Centre de donneeS Astrophysiques de Marseille (CeSAM)
// e-mail:   Jean-Charles.Lambert@lam.fr
// address:  Aix Marseille Universite, CNRS, LAM
//           Laboratoire d'Astrophysique de Marseille
//           Pole de l'Etoile, site de Chateau-Gombert
//           38, rue Frederic Joliot-Curie
//           13388 Marseille cedex 13 France
//           CNRS UMR 7326
// ============================================================================
// Swig python interface for UNSIO
// ============================================================================

// python module name
%module py_unsio

%{
#define SWIG_FILE_WITH_INIT
#include "uns.h"
%}

%include "numpy.i"
%include "std_string.i"

%init %{
 import_array();
%}

// below we change the type of dimension of numpy array.
// By default it's an "int", but we have std::vector object returning size()
// method as dimension, and which are of type "unsigned int"
// This may cause a problem with BIG simulations. Indeed a simulation with 1.1 billions particles
// store in a xyz positions array a size of 3.3 billions which overtake size of SIGNED int, which go
// only to 2^31 bits = 2.14 billons !!!!! (damn nasty bug....)
%numpy_typemaps(double, NPY_DOUBLE, unsigned int)
%numpy_typemaps(float , NPY_FLOAT , unsigned int)
%numpy_typemaps(int   , NPY_INT   , unsigned int)

// getArrayX return 1D numpy float array
%apply (unsigned int* DIM1, float ** ARGOUTVIEW_ARRAY1  )
      {( unsigned int* size, float ** farray             )};

//%apply ( int* DIM1, int   ** ARGOUTVIEW_ARRAY1  )
//      {( int* size, int   ** iarray             )};

// getArrayX return 1D numpy double array
%apply (unsigned int* DIM1, double ** ARGOUTVIEW_ARRAY1  )
      {( unsigned int* size, double ** farray             )};

// getArrayX return 1D numpy int array
%apply (unsigned int* DIM1, int   ** ARGOUTVIEW_ARRAY1  )
      {( unsigned int* size, int   ** iarray             )};


// getValueX return float/double/int value
%apply float  *OUTPUT { float  * fvalue };
%apply double *OUTPUT { double * fvalue };
%apply int    *OUTPUT { int    * ivalue };

// rename methods because of overloading limitations with swig c++
// IMPORTANT :
// rename statement MUST be placed before inclusion of the header "%include uns.h"
// in order to be renamed

//float
%rename(getValueF) getData(const std::string,float *);
%rename(getArrayF) getData(const std::string,const std::string,unsigned int *,float **);
%rename(getArrayF) getData(const std::string,unsigned int *,float **);
//double
%rename(getValueF) getData(const std::string,double *);
%rename(getArrayF) getData(const std::string,const std::string,unsigned int *,double **);
%rename(getArrayF) getData(const std::string,unsigned int *, double **);
//int
%rename(getValueI) getData(const std::string,int *);
%rename(getArrayI) getData(const std::string,const std::string,unsigned int *,int **);
%rename(getArrayI) getData(const std::string,unsigned int *,int **);


%apply (unsigned int DIM1  , float * INPLACE_ARRAY1) {(unsigned int size, float * farray)};
%apply (unsigned int DIM1  , double* INPLACE_ARRAY1) {(unsigned int size, double* farray)};
%apply (unsigned int DIM1  , int   * INPLACE_ARRAY1) {(unsigned int size, int   * iarray)};

// rename methods because of overloading limitations with swig c++
// float
%rename(setValueF) setData(const std::string,float);
%rename(setArrayF_do_not_used) setData(const std::string,const std::string,unsigned int ,float *,const bool _addr=false);
%rename(setArrayF_do_not_used) setData(const std::string,unsigned int ,float *,const bool _addr=false);
// double
%rename(setValueF) setData(const std::string,double);
%rename(setArrayF_do_not_used) setData(const std::string,const std::string, unsigned int ,double *,const bool _addr=false);
%rename(setArrayF_do_not_used) setData(const std::string,unsigned int ,double *,const bool _addr=false);
// int
%rename(setValueI) setData(const std::string,int,const bool _addr=false);
%rename(setArrayI) setData(const std::string,const std::string,unsigned int ,int *,const bool _addr=false);
%rename(setArrayI) setData(const std::string,unsigned int ,int *);

// Parse the original header file
%include "uns.h"

%extend uns::CunsOut2 {
  // we rewrite setArrayF because numpy array size is different from nbody for 3D arrays
  int setArrayF(const std::string  comp,const std::string  prop,
		unsigned int  size,T * farray, const bool _addr=false) {
    if (prop=="pos" || prop=="vel" || prop=="acc") size /= 3;
    int status = $self->snapshot->setData(comp,prop,size,farray,_addr);
    return status;
  }
  // we rewrite setArrayF because numpy array size is different from nbody for 3D arrays
  int setArrayF(const std::string  prop,
		unsigned int  size,T * farray, const bool _addr=false) {
    if (prop=="pos" || prop=="vel" || prop=="acc") size /= 3;
    int status = $self->snapshot->setData(prop,size,farray,_addr);
    return status;
  }
 };


// rename templates
// INPUT
%template(CunsIn)  uns::CunsIn2<float>;
//%template(CunsInF) uns::CunsIn2<float>;
%template(CunsInD) uns::CunsIn2<double>;
// OUTPUT
//%template(CunsOutF) uns::CunsOut2<float>;
%template(CunsOut)  uns::CunsOut2<float>;
%template(CunsOutD) uns::CunsOut2<double>;
