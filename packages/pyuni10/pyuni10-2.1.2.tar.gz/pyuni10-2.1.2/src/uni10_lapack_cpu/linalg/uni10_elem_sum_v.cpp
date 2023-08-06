#include "uni10_lapack_cpu/uni10_elem_linalg.h"

namespace uni10{

  namespace linalg_unielem_internal{

    uni10_double64 VectorSum(const UniElemDouble* X, const uni10_uint64* N, uni10_int32* inc){

      return linalg_driver_internal::VectorSum(X->elem_ptr_, *N, *inc);

    }

    uni10_complex128 VectorSum(const UniElemComplex* X, const uni10_uint64* N, uni10_int32* inc){

      return linalg_driver_internal::VectorSum(X->elem_ptr_, *N, *inc);
    }

  }

}
