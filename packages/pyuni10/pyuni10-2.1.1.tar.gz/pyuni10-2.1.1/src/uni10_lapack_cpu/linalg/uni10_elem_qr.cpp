#include "uni10_lapack_cpu/uni10_elem_linalg.h"

namespace uni10{

  namespace linalg_unielem_internal{

    void Qr(const UniElemDouble* Mij_ori, uni10_const_bool* isMdiag, const uni10_uint64* M, const uni10_uint64* N, 
        UniElemDouble* Q, UniElemDouble* R){

      if(!*isMdiag)
        linalg_driver_internal::Qr(Mij_ori->elem_ptr_, *M, *N, Q->elem_ptr_, R->elem_ptr_);
      else
        uni10_error_msg(true, "%s", "Developping!!!");

    }

    void Qr(const UniElemComplex* Mij_ori, uni10_const_bool* isMdiag, const uni10_uint64* M, const uni10_uint64* N, 
        UniElemComplex* Q, UniElemComplex* R){

      if(!*isMdiag)
        linalg_driver_internal::Qr(Mij_ori->elem_ptr_, *M, *N, Q->elem_ptr_, R->elem_ptr_);
      else
        uni10_error_msg(true, "%s", "Developping!!!");

    }

  }

}
