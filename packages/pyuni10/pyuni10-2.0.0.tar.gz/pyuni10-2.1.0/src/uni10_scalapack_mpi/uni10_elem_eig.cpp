#include "uni10_scalapack_mpi/uni10_elem_linalg_scalapack_mpi.h"

namespace uni10{

  void matrixEig(const uni10_elem_double64* Mij_ori, uni10_const_bool *isMdiag, const uni10_uint64* N, uni10_elem_complex128* Eig, uni10_elem_complex128* EigVec){

    if(!*isMdiag)
      uni10_linalg::eigDecompose(Mij_ori->elem_ptr_, *N, Eig->elem_ptr_, EigVec->elem_ptr_);
    else
      uni10_error_msg(true, "%s", "Developping!!!");

  }

  void matrixEig(const uni10_elem_complex128* Mij_ori, uni10_const_bool *isMdiag, const uni10_uint64* N, uni10_elem_complex128* Eig, uni10_elem_complex128* EigVec){

    if(!*isMdiag)
      uni10_linalg::eigDecompose(Mij_ori->elem_ptr_, *N, Eig->elem_ptr_, EigVec->elem_ptr_);
    else
      uni10_error_msg(true, "%s", "Developping!!!");

  }

}
