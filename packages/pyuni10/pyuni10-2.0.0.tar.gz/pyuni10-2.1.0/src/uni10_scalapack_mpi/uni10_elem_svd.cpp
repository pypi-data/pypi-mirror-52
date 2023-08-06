#include "uni10_scalapack_mpi/uni10_elem_linalg_scalapack_mpi.h"

namespace uni10{

  void matrixSVD(const uni10_elem_double64* Mij_ori, uni10_const_bool* isMdiag, const uni10_uint64* M, const uni10_uint64* N, 
      uni10_elem_double64* U, uni10_elem_double64* S, uni10_elem_double64* vT){

    uni10_double64* U_elem  = (U  == NULL) ? NULL : U->elem_ptr_;
    uni10_int* U_desc       = (U  == NULL) ? NULL : U->desc;
    uni10_double64* vT_elem = (vT == NULL) ? NULL : vT->elem_ptr_;
    uni10_int* vT_desc      = (vT == NULL) ? NULL : vT->desc;

    uni10_error_msg(std::min(*M, *N) < env_variables.get_info().blockgrid, "%s",
        "The distributed submatrix must verify the propertie, MB == NA. It also means that the environment variable, BLOCKGRID, must be smaller than min(M, N)");

    if(!*isMdiag){
      uni10_linalg::matrixSVD(Mij_ori->elem_ptr_, Mij_ori->blockrow, Mij_ori->blockcol, Mij_ori->desc, *M, *N, U_elem, U_desc, S->elem_ptr_, vT_elem, vT_desc);
    }

    else
      uni10_error_msg(true, "%s", "Developping!!!");

  }

  void matrixSVD(const uni10_elem_complex128* Mij_ori, uni10_const_bool* isMdiag, const uni10_uint64* M, const uni10_uint64* N, 
      uni10_elem_complex128* U, uni10_elem_complex128* S, uni10_elem_complex128* vT){

    //uni10_error_msg(true, "%s", "Developping!!!");
    //uni10_complex128* U_elem  = (U  == NULL) ? NULL : U->elem_ptr_;
    //uni10_complex128* vT_elem = (vT == NULL) ? NULL : vT->elem_ptr_;

    //if(!*isMdiag)
    //  uni10_linalg::matrixSVD(Mij_ori->elem_ptr_, *M, *N, U_elem, S->elem_ptr_, vT_elem);
    //else
    //  uni10_error_msg(true, "%s", "Developping!!!");

  }

}
