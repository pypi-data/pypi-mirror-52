#include "uni10_cusolver_gpu/uni10_elem_linalg_cusolver_gpu.h"

namespace uni10{

  namespace linalg_unielem_internal{

    uni10_double64 Det(const UniElemDouble* A, const uni10_uint64* N, uni10_const_bool* isMdiag){

      uni10_double64 det = 0.;
      if(!*isMdiag)
        det = linalg_driver_internal::Det(A->elem_ptr_, *N);
      else
        uni10_error_msg(true, "%s", "Developping!!!");

      return det;  

    }

    uni10_complex128 Det(const UniElemComplex* A, const uni10_uint64* N, uni10_const_bool* isMdiag){

      uni10_complex128 det = 0.;
      if(!*isMdiag)
        det = linalg_driver_internal::Det(A->elem_ptr_, *N);
      else
        uni10_error_msg(true, "%s", "Developping!!!");

      return det;  

    }

  }

}
