#include "uni10_lapack_cpu/uni10_elem_linalg.h"

namespace uni10{

  namespace linalg_unielem_internal{

    void QdrColPivot(const UniElemDouble* Mij_ori, uni10_const_bool* isMdiag, const uni10_uint64* M, const uni10_uint64* N, 
        UniElemDouble* Q, UniElemDouble* D, UniElemDouble* R){

      if(!*isMdiag)
        linalg_driver_internal::QdrColPivot(Mij_ori->elem_ptr_, *M, *N, Q->elem_ptr_, D->elem_ptr_, R->elem_ptr_);
      else
        uni10_error_msg(true, "%s", "Developping!!!");

    }

    void QdrColPivot(const UniElemComplex* Mij_ori, uni10_const_bool* isMdiag, const uni10_uint64* M, const uni10_uint64* N, 
        UniElemComplex* Q,UniElemComplex* D, UniElemComplex* R){

      if(!*isMdiag)
        linalg_driver_internal::QdrColPivot(Mij_ori->elem_ptr_, *M, *N, Q->elem_ptr_, D->elem_ptr_, R->elem_ptr_);
      else
        uni10_error_msg(true, "%s", "Developping!!!");

    }

  }

}
