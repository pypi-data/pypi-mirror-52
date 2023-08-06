#include "uni10_lapack_cpu/uni10_elem_linalg.h"

namespace uni10{

  namespace linalg_unielem_internal{

    void Inverse(const UniElemDouble* A, const uni10_uint64* N, uni10_const_bool* isMdiag){

      if(!*isMdiag)
        linalg_driver_internal::Inverse(A->elem_ptr_, *N);
      else
        uni10_error_msg(true, "%s", "Developping!!!");

    }

    void Inverse(const UniElemComplex* A, const uni10_uint64* N, uni10_const_bool* isMdiag){

      if(!*isMdiag)
        linalg_driver_internal::Inverse(A->elem_ptr_, *N);
      else
        uni10_error_msg(true, "%s", "Developping!!!");

    }

  }

}
