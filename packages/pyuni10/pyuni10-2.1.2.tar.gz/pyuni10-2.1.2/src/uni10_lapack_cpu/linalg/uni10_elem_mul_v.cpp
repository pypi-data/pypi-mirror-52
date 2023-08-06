#include "uni10_lapack_cpu/uni10_elem_linalg.h"

namespace uni10{

  namespace linalg_unielem_internal{

    void VectorMul(UniElemDouble* Y, const UniElemDouble* X, const uni10_uint64* N){

      linalg_driver_internal::VectorMul(Y->elem_ptr_, X->elem_ptr_, *N);

    }

    void VectorMul(UniElemComplex* Y, const UniElemDouble* X, const uni10_uint64* N){

      linalg_driver_internal::VectorMul(Y->elem_ptr_, X->elem_ptr_, *N);

    }

    void VectorMul(UniElemComplex* Y, const UniElemComplex* X, const uni10_uint64* N){

      linalg_driver_internal::VectorMul(Y->elem_ptr_, X->elem_ptr_, *N);

    }  

  }

}
