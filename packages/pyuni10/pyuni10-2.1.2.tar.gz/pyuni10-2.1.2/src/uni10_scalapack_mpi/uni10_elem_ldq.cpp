#include "uni10_scalapack_mpi/uni10_elem_linalg_scalapack_mpi.h"

namespace uni10{

  void matrixLDQ(const uni10_elem_double64* Mij_ori, uni10_const_bool* isMdiag, const uni10_uint64* M, const uni10_uint64* N, 
      uni10_elem_double64* L, uni10_elem_double64* D, uni10_elem_double64* Q){
    
    if(!*isMdiag)
      uni10_linalg::matrixLDQ(Mij_ori->elem_ptr_, *M, *N, L->elem_ptr_, D->elem_ptr_, Q->elem_ptr_);
    else
      uni10_error_msg(true, "%s", "Developping!!!");

  }

  void matrixLDQ(const uni10_elem_complex128* Mij_ori, uni10_const_bool* isMdiag, const uni10_uint64* M, const uni10_uint64* N, 
      uni10_elem_complex128* L,uni10_elem_complex128* D, uni10_elem_complex128* Q){

    if(!*isMdiag)
      uni10_linalg::matrixLDQ(Mij_ori->elem_ptr_, *M, *N, L->elem_ptr_, D->elem_ptr_, Q->elem_ptr_);
    else
      uni10_error_msg(true, "%s", "Developping!!!");

  }

}
