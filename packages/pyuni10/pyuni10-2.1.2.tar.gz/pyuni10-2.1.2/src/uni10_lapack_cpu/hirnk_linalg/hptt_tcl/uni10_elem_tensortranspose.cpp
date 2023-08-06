#include "uni10_env_info.h"
#include "uni10_lapack_cpu/uni10_elem_hirnk_linalg.h"

#if defined(UNI_TCL)

namespace uni10{

  namespace hirnk_linalg_unielem_internal{

    void TensorTranspose(const UniElemDouble* ka, const uni10_int *newbdidx, const uni10_int rank, const uni10_int* oribonddims, UniElemDouble* b){

#if defined(UNI_DEBUG)
      printf(" @@@@@@@@ HPTT Permutation @@@@@@@ \n");
#endif
      
      uni10_int threads_num = env_variables.GetSysInfo().threads_num_;
      uni10_int row_major = 1;

      double alpha = 1.0;
      double beta  = 0.0;
      double* elem_t1 = ka->elem_ptr_;
      double* elem_t2 = b->elem_ptr_; 

      dTensorTranspose(newbdidx, rank, 
          alpha, elem_t1, oribonddims, NULL,\
          beta, elem_t2, NULL,\
          threads_num, row_major);

    }

    void TensorTranspose(const UniElemComplex* ka, const uni10_int *newbdidx, const uni10_int rank, const uni10_int* oribonddims, UniElemComplex* b){

#if defined(UNI_DEBUG)
      printf(" @@@@@@@@ HPTT Permutation @@@@@@@ \n");
#endif

      uni10_int threads_num = env_variables.GetSysInfo().threads_num_;
      uni10_int row_major = 1;

      double _Complex alpha = 1.;
      double _Complex beta = 0.;

      double _Complex* elem_t1 = (double _Complex*)ka->elem_ptr_;
      double _Complex* elem_t2 = (double _Complex*)b->elem_ptr_; 

      zTensorTranspose(newbdidx, rank, 
          alpha, false, elem_t1, oribonddims, NULL,\
          beta, elem_t2, NULL,\
          threads_num, row_major);

    }

  }

};

#endif
