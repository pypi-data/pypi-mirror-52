#include "uni10_scalapack_mpi/uni10_elem_linalg_scalapack_mpi.h"

namespace uni10{

  void matrixQL(const uni10_elem_double64* Mij_ori, uni10_const_bool* isMdiag, const uni10_uint64* M, const uni10_uint64* N, 
      uni10_elem_double64* Q, uni10_elem_double64* L){

    if(!*isMdiag)
      uni10_linalg::matrixQL(Mij_ori->elem_ptr_, Mij_ori->blockrow, Mij_ori->blockcol, Mij_ori->desc, *M, *N, Q->elem_ptr_, Q->desc, L->elem_ptr_, L->desc);
    else
      uni10_error_msg(true, "%s", "Developping!!!");

  }

  void matrixQL(const uni10_elem_complex128* Mij_ori, uni10_const_bool* isMdiag, const uni10_uint64* M, const uni10_uint64* N, 
      uni10_elem_complex128* Q, uni10_elem_complex128* L){

    if(!*isMdiag)
      uni10_linalg::matrixQL(Mij_ori->elem_ptr_, *M, *N, Q->elem_ptr_, L->elem_ptr_);
    else
      uni10_error_msg(true, "%s", "Developping!!!");

  }

}
