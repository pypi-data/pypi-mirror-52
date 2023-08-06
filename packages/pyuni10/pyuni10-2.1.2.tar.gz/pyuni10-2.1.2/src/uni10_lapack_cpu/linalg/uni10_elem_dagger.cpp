#include "uni10_lapack_cpu/uni10_elem_linalg.h"

namespace uni10{

  namespace linalg_unielem_internal{

    void Dagger(const UniElemDouble* A, const uni10_uint64* M, const uni10_uint64* N, UniElemDouble* AT){

      linalg_driver_internal::Dagger(A->elem_ptr_, *M, *N, AT->elem_ptr_);

    }

    void Dagger(UniElemDouble* A, uni10_uint64* M, uni10_uint64* N){

      linalg_driver_internal::Dagger(A->elem_ptr_, *M, *N);

    }

    void Dagger(const UniElemComplex* A, const uni10_uint64* M, const uni10_uint64* N, UniElemComplex* AT){

      linalg_driver_internal::Dagger(A->elem_ptr_, *M, *N, AT->elem_ptr_);

    }

    void Dagger(UniElemComplex* A, uni10_uint64* M, uni10_uint64* N){

      linalg_driver_internal::Dagger(A->elem_ptr_, *M, *N);

    }

  }

}
