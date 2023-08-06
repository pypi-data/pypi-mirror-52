#include "uni10_cusolver_gpu/uni10_elem_linalg_cusolver_gpu.h"

namespace uni10{

  namespace linalg_unielem_internal{

    void Ql(const UniElemDouble* Mij_ori, uni10_const_bool* isMdiag, const uni10_uint64* M, const uni10_uint64* N, 
        UniElemDouble* Q, UniElemDouble* L){

      if(!*isMdiag)
        linalg_driver_internal::Ql(Mij_ori->elem_ptr_, *M, *N, Q->elem_ptr_, L->elem_ptr_);
      else
        uni10_error_msg(true, "%s", "Developping!!!");

    }

    void Ql(const UniElemComplex* Mij_ori, uni10_const_bool* isMdiag, const uni10_uint64* M, const uni10_uint64* N, 
        UniElemComplex* Q, UniElemComplex* L){

      if(!*isMdiag)
        linalg_driver_internal::Ql(Mij_ori->elem_ptr_, *M, *N, Q->elem_ptr_, L->elem_ptr_);
      else
        uni10_error_msg(true, "%s", "Developping!!!");

    }


  }

}
