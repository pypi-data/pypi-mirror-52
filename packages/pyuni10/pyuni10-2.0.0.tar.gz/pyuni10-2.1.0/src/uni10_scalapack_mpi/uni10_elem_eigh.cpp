#include "uni10_scalapack_mpi/uni10_elem_linalg_scalapack_mpi.h"

namespace uni10{

  void matrixEigh(const uni10_elem_double64* Mij_ori, uni10_const_bool *isMdiag, const uni10_uint64* N, uni10_elem_double64* Eig, uni10_elem_double64* EigVec){

    if(!*isMdiag)
      uni10_linalg::eigSyDecompose(Mij_ori->elem_ptr_, Mij_ori->blockrow, Mij_ori->blockcol, Mij_ori->desc,  *N, Eig->elem_ptr_, EigVec->elem_ptr_, EigVec->desc);
    else
      uni10_error_msg(true, "%s", "Developping!!!");

  }

  void matrixEigh(const uni10_elem_complex128* Mij_ori, uni10_const_bool *isMdiag, const uni10_uint64* N, uni10_elem_double64* Eig, uni10_elem_complex128* EigVec){

    if(!*isMdiag)
      uni10_linalg::eigSyDecompose(Mij_ori->elem_ptr_, *N, Eig->elem_ptr_, EigVec->elem_ptr_);
    else
      uni10_error_msg(true, "%s", "Developping!!!");

  }

  void matrixEigh(const uni10_elem_complex128* Mij_ori, uni10_const_bool *isMdiag, const uni10_uint64* N, uni10_elem_complex128* Eig, uni10_elem_complex128* EigVec){

    uni10_double64* tmp = (uni10_double64*)malloc((*N)*sizeof(uni10_double64));
    if(!*isMdiag){
      uni10_linalg::eigSyDecompose(Mij_ori->elem_ptr_, *N, tmp, EigVec->elem_ptr_);
      uni10_elem_cast(Eig->elem_ptr_, tmp, (*N));
    }
    else
      uni10_error_msg(true, "%s", "Developping!!!");

  }

}
