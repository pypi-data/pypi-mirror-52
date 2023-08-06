#include "uni10_cusolver_gpu/uni10_elem_linalg_cusolver_gpu.h"

namespace uni10{

  namespace linalg_unielem_internal{

    void Rq(const UniElemDouble* Mij_ori, uni10_const_bool* isMdiag, const uni10_uint64* M, const uni10_uint64* N, 
        UniElemDouble* R, UniElemDouble* Q){

      //uni10_error_msg(true, "Developping!!!(Have bugs)");
      if(!*isMdiag)
        linalg_driver_internal::Rq(Mij_ori->elem_ptr_, *M, *N, R->elem_ptr_, Q->elem_ptr_);
      else
        uni10_error_msg(true, "%s", "Developping!!!");

    }

    void Rq(const UniElemComplex* Mij_ori, uni10_const_bool* isMdiag, const uni10_uint64* M, const uni10_uint64* N, 
        UniElemComplex* R, UniElemComplex* Q){

      if(!*isMdiag)
        linalg_driver_internal::Rq(Mij_ori->elem_ptr_, *M, *N, R->elem_ptr_, Q->elem_ptr_);
      else
        uni10_error_msg(true, "%s", "Developping!!!");

    }

  }

}
