#include "uni10_cusolver_gpu/uni10_elem_linalg_cusolver_gpu.h"

namespace uni10{

  namespace linalg_unielem_internal{

    void Transpose(const UniElemDouble* A, const uni10_uint64* M, const uni10_uint64* N, UniElemDouble* AT){

      linalg_driver_internal::Transpose(A->elem_ptr_, *M, *N, AT->elem_ptr_);

    }

    void Transpose(UniElemDouble* A, uni10_uint64* M, uni10_uint64* N){

      linalg_driver_internal::Transpose(A->elem_ptr_, *M, *N);

    }

    void Transpose(const UniElemComplex* A, const uni10_uint64* M, const uni10_uint64* N, UniElemComplex* AT){

      linalg_driver_internal::Transpose(A->elem_ptr_, *M, *N, AT->elem_ptr_);

    }

    void Transpose(UniElemComplex* A, uni10_uint64* M, uni10_uint64* N){

      linalg_driver_internal::Transpose(A->elem_ptr_, *M, *N);

    }


  }

}
