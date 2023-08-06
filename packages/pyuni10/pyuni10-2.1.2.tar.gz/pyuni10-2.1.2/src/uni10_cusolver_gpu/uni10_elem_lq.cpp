#include "uni10_cusolver_gpu/uni10_elem_linalg_cusolver_gpu.h"

namespace uni10{

  namespace linalg_unielem_internal{

    void Lq(const UniElemDouble* Mij_ori, uni10_const_bool* isMdiag, const uni10_uint64* M, const uni10_uint64* N, 
        UniElemDouble* L, UniElemDouble* Q){

      if(!*isMdiag)
        linalg_driver_internal::Lq(Mij_ori->elem_ptr_, *M, *N, L->elem_ptr_, Q->elem_ptr_);
      else
        uni10_error_msg(true, "%s", "Developping!!!");

    }

    void Lq(const UniElemComplex* Mij_ori, uni10_const_bool* isMdiag, const uni10_uint64* M, const uni10_uint64* N, 
        UniElemComplex* L, UniElemComplex* Q){

      if(!*isMdiag)
        linalg_driver_internal::Lq(Mij_ori->elem_ptr_, *M, *N, L->elem_ptr_, Q->elem_ptr_);
      else
        uni10_error_msg(true, "%s", "Developping!!!");

    }


  }

}
