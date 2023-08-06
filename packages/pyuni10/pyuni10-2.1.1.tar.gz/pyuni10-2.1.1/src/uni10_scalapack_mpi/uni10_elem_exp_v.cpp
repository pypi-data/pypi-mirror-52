#include "uni10_scalapack_mpi/uni10_elem_linalg_scalapack_mpi.h"

namespace uni10{

  void vectorExp(uni10_double64* a, uni10_elem_double64* X, uni10_uint64* N){

    uni10_linalg::vectorExp(*a, X->elem_ptr_, *N);

  }

  void vectorExp(uni10_complex128* a, uni10_elem_complex128* X, uni10_uint64* N){

    uni10_linalg::vectorExp(*a, X->elem_ptr_, *N);

  }
  
  void vectorExp(uni10_double64* a, uni10_elem_complex128* X, uni10_uint64* N){

    uni10_linalg::vectorExp(*a, X->elem_ptr_, *N);

  }

}
