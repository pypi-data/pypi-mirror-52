#include "uni10_cusolver_gpu/uni10_elem_linalg_cusolver_gpu.h"

namespace uni10{

  namespace linalg_unielem_internal{

    uni10_double64 Norm(const UniElemDouble* X, const uni10_uint64* N, uni10_int32* inc){

      return linalg_driver_internal::Norm(X->elem_ptr_, *N, *inc);

    }

    uni10_double64 Norm(const UniElemComplex* X, const uni10_uint64* N, uni10_int32* inc){

      return linalg_driver_internal::Norm(X->elem_ptr_, *N, *inc);

    }

  }

}
