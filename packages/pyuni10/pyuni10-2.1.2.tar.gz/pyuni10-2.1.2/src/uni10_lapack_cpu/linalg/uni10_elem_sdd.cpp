#include "uni10_lapack_cpu/uni10_elem_linalg.h"

namespace uni10{

  namespace linalg_unielem_internal{

    void Sdd(const UniElemDouble* Mij_ori, uni10_const_bool* isMdiag, const uni10_uint64* M, const uni10_uint64* N, 
        UniElemDouble* U, UniElemDouble* S, UniElemDouble* vT){

      uni10_double64* U_elem  = (U  == NULL) ? NULL : U->elem_ptr_;
      uni10_double64* vT_elem = (vT == NULL) ? NULL : vT->elem_ptr_;

      if(!*isMdiag)
        linalg_driver_internal::Sdd(Mij_ori->elem_ptr_, *M, *N, U_elem, S->elem_ptr_, vT_elem);
      else
        uni10_error_msg(true, "%s", "Developping!!!");

    }

    void Sdd(const UniElemComplex* Mij_ori, uni10_const_bool* isMdiag, const uni10_uint64* M, const uni10_uint64* N, 
        UniElemComplex* U, UniElemComplex* S, UniElemComplex* vT){

      uni10_complex128* U_elem  = (U  == NULL) ? NULL : U->elem_ptr_;
      uni10_complex128* vT_elem = (vT == NULL) ? NULL : vT->elem_ptr_;

      if(!*isMdiag)
        linalg_driver_internal::Sdd(Mij_ori->elem_ptr_, *M, *N, U_elem, S->elem_ptr_, vT_elem);
      else
        uni10_error_msg(true, "%s", "Developping!!!");

    }


  }

}
