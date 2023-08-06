#include "uni10_cusolver_gpu/uni10_elem_linalg_cusolver_gpu.h"

namespace uni10{

  namespace linalg_unielem_internal{

    void SyTriMatEigDecompose(UniElemDouble* D, UniElemDouble* E, uni10_uint64* N, 
        UniElemDouble* z, uni10_uint64* LDZ){

      if(z==NULL && LDZ==NULL)
        linalg_driver_internal::SyTriMatEigDecompose(D->elem_ptr_, E->elem_ptr_, *N);
      else
        linalg_driver_internal::SyTriMatEigDecompose(D->elem_ptr_, E->elem_ptr_, *N, z->elem_ptr_, *LDZ);

    }

    void SyTriMatEigDecompose(UniElemComplex* D, UniElemComplex* E, uni10_uint64* N, 
        UniElemComplex* z, uni10_uint64* LDZ){

      uni10_error_msg(true, "%s", "developping!!");

    }

  }

}
