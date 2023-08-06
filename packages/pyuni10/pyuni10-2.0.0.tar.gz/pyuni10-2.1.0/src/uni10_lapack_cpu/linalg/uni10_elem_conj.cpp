#include "uni10_lapack_cpu/uni10_elem_linalg.h"

namespace uni10{

  namespace linalg_unielem_internal{

    void Conjugate(const UniElemDouble* A, const uni10_uint64* N, UniElemDouble* A_conj){

      tools_internal::UniElemCopy(A_conj->elem_ptr_, A->elem_ptr_, (*N) *sizeof(uni10_double64));

    }

    void Conjugate(UniElemDouble* A, uni10_uint64* N){

      //For function overload. Nothing to do.
      //
    }

    void Conjugate(const UniElemComplex* A, const uni10_uint64* N, UniElemComplex* A_conj){

      linalg_driver_internal::Conjugate(A->elem_ptr_, *N, A_conj->elem_ptr_);

    }

    void Conjugate(UniElemComplex* A, uni10_uint64* N){

      linalg_driver_internal::Conjugate(A->elem_ptr_, *N);

    }

  }

}
