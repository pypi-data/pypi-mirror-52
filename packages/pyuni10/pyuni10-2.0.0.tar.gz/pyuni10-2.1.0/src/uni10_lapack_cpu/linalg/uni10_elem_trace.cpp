#include "uni10_lapack_cpu/uni10_elem_linalg.h"

namespace uni10{

  namespace linalg_unielem_internal{

    uni10_double64 Trace(const UniElemDouble* Mij_ori, uni10_const_bool* isMdiag, const uni10_uint64* M, const uni10_uint64* N){

      uni10_uint64 min = std::min(*M, *N);
      uni10_int32 inc = 1;
      uni10_double64 res = 0.;
      if(!*isMdiag){
        for(uni10_uint64 i = 0; i < min; i++){
          res += Mij_ori->elem_ptr_[i*(*N)+i];
        }
      }
      else
        res = linalg_driver_internal::VectorSum(Mij_ori->elem_ptr_, min, inc);
      return res;

    }

    uni10_complex128 Trace(const UniElemComplex* Mij_ori, uni10_const_bool* isMdiag, const uni10_uint64* M, const uni10_uint64* N){

      uni10_uint64 min = std::min(*M, *N);
      uni10_int32 inc = 1;
      uni10_complex128 res = 0.;
      if(!*isMdiag){
        for(uni10_uint64 i = 0; i < min; i++){
          res += Mij_ori->elem_ptr_[i*(*N)+i];
        }
      }
      else
        res = linalg_driver_internal::VectorSum(Mij_ori->elem_ptr_, min, inc);
      return res;
    }

  }

}
