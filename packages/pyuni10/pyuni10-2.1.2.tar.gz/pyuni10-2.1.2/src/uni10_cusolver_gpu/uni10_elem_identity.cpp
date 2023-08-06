#include "uni10_cusolver_gpu/uni10_elem_linalg_cusolver_gpu.h"

namespace uni10{

  namespace linalg_unielem_internal{

    void Identity(UniElemDouble* A, const uni10_bool* is_diag, const uni10_uint64* M, const uni10_uint64* N){

      if(*is_diag == true){

        for(uni10_uint64 i = 0; i < A->elem_num_; i++)
          A->elem_ptr_[i] = 1.;

      }
      else{

        linalg_driver_internal::Identity(A->elem_ptr_, *M, *N);

      }

    }

    void Identity(UniElemComplex* A, const uni10_bool* is_diag, const uni10_uint64* M, const uni10_uint64* N){

      if(*is_diag == true){

        for(uni10_uint64 i = 0; i < A->elem_num_; i++)
          A->elem_ptr_[i] = 1.;

      }
      else{

        linalg_driver_internal::Identity(A->elem_ptr_, *M, *N);

      }

    }

  }

}
