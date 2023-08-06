#include "uni10_scalapack_mpi/uni10_elem_linalg_scalapack_mpi.h"

namespace uni10{

  void trimatrixEigh(uni10_elem_double64* D, uni10_elem_double64* E, uni10_uint64* N, 
      uni10_elem_double64* z, uni10_uint64* LDZ){

    if(z==NULL && LDZ==NULL)
      uni10_linalg::trimatrixEigH(D->elem_ptr_, E->elem_ptr_, *N);
    else
      uni10_linalg::trimatrixEigH(D->elem_ptr_, E->elem_ptr_, *N, z->elem_ptr_, *LDZ);

  }

  void trimatrixEigh(uni10_elem_complex128* D, uni10_elem_complex128* E, uni10_uint64* N, 
      uni10_elem_complex128* z, uni10_uint64* LDZ){

    uni10_error_msg(true, "%s", "developping!!");

  }

}
