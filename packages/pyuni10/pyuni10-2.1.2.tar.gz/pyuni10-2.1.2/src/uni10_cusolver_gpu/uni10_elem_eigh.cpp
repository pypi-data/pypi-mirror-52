#include "uni10_cusolver_gpu/uni10_elem_linalg_cusolver_gpu.h"

namespace uni10{

  namespace linalg_unielem_internal{

    void SyEigDecompose(const UniElemDouble* Mij_ori, uni10_const_bool *isMdiag, const uni10_uint64* N, UniElemDouble* Eig, UniElemDouble* EigVec){

      if(!*isMdiag)
        linalg_driver_internal::SyEigDecompose(Mij_ori->elem_ptr_, *N, Eig->elem_ptr_, EigVec->elem_ptr_);
      else
        uni10_error_msg(true, "%s", "Developping!!!");

    }

    void SyEigDecompose(const UniElemComplex* Mij_ori, uni10_const_bool *isMdiag, const uni10_uint64* N, UniElemDouble* Eig, UniElemComplex* EigVec){

      if(!*isMdiag)
        linalg_driver_internal::SyEigDecompose(Mij_ori->elem_ptr_, *N, Eig->elem_ptr_, EigVec->elem_ptr_);
      else
        uni10_error_msg(true, "%s", "Developping!!!");

    }

    void SyEigDecompose(const UniElemComplex* Mij_ori, uni10_const_bool *isMdiag, const uni10_uint64* N, UniElemComplex* Eig, UniElemComplex* EigVec){

      uni10_double64* tmp = (uni10_double64*)malloc((*N)*sizeof(uni10_double64));
      if(!*isMdiag){
        linalg_driver_internal::SyEigDecompose(Mij_ori->elem_ptr_, *N, tmp, EigVec->elem_ptr_);
        tools_internal::UniElemCast(Eig->elem_ptr_, tmp, (*N));
      }
      else
        uni10_error_msg(true, "%s", "Developping!!!");

    }

  }

}
