#include "uni10_cusolver_gpu/uni10_elem_linalg_cusolver_gpu.h"

namespace uni10{

  namespace linalg_unielem_internal{

    void VectorScal(uni10_double64* a, UniElemDouble* X, uni10_uint64* N){

      linalg_driver_internal::VectorScal(*a, X->elem_ptr_, *N);

    }

    void VectorScal(uni10_complex128* a, UniElemComplex* X, uni10_uint64* N){

      linalg_driver_internal::VectorScal(*a, X->elem_ptr_, *N);

    }

    void VectorScal(uni10_double64* a, UniElemComplex* X, uni10_uint64* N){

      linalg_driver_internal::VectorScal(*a, X->elem_ptr_, *N);

    }


  }

}
