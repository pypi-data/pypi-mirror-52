#include "uni10_cusolver_gpu/uni10_elem_linalg_cusolver_gpu.h"

namespace uni10{

  namespace linalg_unielem_internal{

    void VectorSub(UniElemDouble* Y, const UniElemDouble* X, const uni10_uint64* N){

      linalg_driver_internal::VectorSub(Y->elem_ptr_, X->elem_ptr_, *N);

    }

    void VectorSub(UniElemComplex* Y, const UniElemComplex* X, const uni10_uint64* N){

      linalg_driver_internal::VectorSub(Y->elem_ptr_, X->elem_ptr_, *N);

    }

    void VectorSub(UniElemComplex* Y, const UniElemDouble* X, const uni10_uint64* N){

      linalg_driver_internal::VectorSub(Y->elem_ptr_, X->elem_ptr_, *N);

    }

  }

}
