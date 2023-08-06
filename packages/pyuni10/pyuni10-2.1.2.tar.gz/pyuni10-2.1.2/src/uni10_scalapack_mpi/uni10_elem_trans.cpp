#include "uni10_scalapack_mpi/uni10_elem_linalg_scalapack_mpi.h"

namespace uni10{

  void setTranspose(const uni10_elem_double64* A, const uni10_uint64* M, const uni10_uint64* N, uni10_elem_double64* AT){

    uni10_linalg::setTranspose(A->elem_ptr_, A->desc, *M, *N, AT->elem_ptr_, AT->desc);

  }

  void setTranspose(uni10_elem_double64* A, uni10_uint64* M, uni10_uint64* N){
    
    const uni10_elem_double64 _A(*A);
    uni10_elem_double64 AT(*N, *M, false);
    uni10_linalg::setTranspose(_A.elem_ptr_, _A.desc, _A.Cnum_, _A.Rnum_, AT.elem_ptr_, AT.desc);
    //*A = AT;

  }

  void setTranspose(const uni10_elem_complex128* A, const uni10_uint64* M, const uni10_uint64* N, uni10_elem_complex128* AT){

    uni10_linalg::setTranspose(A->elem_ptr_, *M, *N, AT->elem_ptr_);

  }

  void setTranspose(uni10_elem_complex128* A, uni10_uint64* M, uni10_uint64* N){

    uni10_linalg::setTranspose(A->elem_ptr_, *M, *N);

  }

}
