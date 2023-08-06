#include "uni10_lapack_cpu/uni10_elem_linalg.h"

namespace uni10{

  namespace linalg_unielem_internal{

    void EigDecompose(const UniElemDouble* Mij_ori, uni10_const_bool *isMdiag, const uni10_uint64* N, UniElemComplex* Eig, UniElemComplex* EigVec){

      if(!*isMdiag)
        linalg_driver_internal::EigDecompose(Mij_ori->elem_ptr_, *N, Eig->elem_ptr_, EigVec->elem_ptr_);
      else
        uni10_error_msg(true, "%s", "Developping!!!");

    }

    void EigDecompose(const UniElemComplex* Mij_ori, uni10_const_bool *isMdiag, const uni10_uint64* N, UniElemComplex* Eig, UniElemComplex* EigVec){

      if(!*isMdiag)
        linalg_driver_internal::EigDecompose(Mij_ori->elem_ptr_, *N, Eig->elem_ptr_, EigVec->elem_ptr_);
      else
        uni10_error_msg(true, "%s", "Developping!!!");

    }

  }

}
