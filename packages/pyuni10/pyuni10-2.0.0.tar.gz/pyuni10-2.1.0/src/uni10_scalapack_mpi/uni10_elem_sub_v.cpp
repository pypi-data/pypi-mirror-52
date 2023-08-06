#include "uni10_scalapack_mpi/uni10_elem_linalg_scalapack_mpi.h"

namespace uni10{

  void vectorSub(uni10_elem_double64* Y, const uni10_elem_double64* X, const uni10_uint64* N){

    uni10_error_msg(*N != Y->Rnum_*Y->Cnum_, "%s", "Input length is wrong.");
    uni10_linalg::vectorSub(Y->elem_ptr_, X->elem_ptr_, Y->blockrow*Y->blockcol);

  }

  void vectorSub(uni10_elem_complex128* Y, const uni10_elem_complex128* X, const uni10_uint64* N){

    uni10_linalg::vectorSub(Y->elem_ptr_, X->elem_ptr_, *N);

  }

  void vectorSub(uni10_elem_complex128* Y, const uni10_elem_double64* X, const uni10_uint64* N){

    uni10_linalg::vectorSub(Y->elem_ptr_, X->elem_ptr_, *N);

  }

}
