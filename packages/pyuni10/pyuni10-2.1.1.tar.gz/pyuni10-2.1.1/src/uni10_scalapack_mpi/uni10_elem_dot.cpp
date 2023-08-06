#include "uni10_scalapack_mpi/uni10_elem_linalg_scalapack_mpi.h"

namespace uni10{

  void matrixDot(const uni10_elem_double64* A, uni10_const_bool* isAdiag, const uni10_elem_double64* B, uni10_const_bool* isBdiag, 
      const uni10_uint64* M, const uni10_uint64* N, const uni10_uint64* K, uni10_elem_double64* C){

    if( !*isAdiag && !*isBdiag ){

      uni10_linalg::matrixDot(A->elem_ptr_, A->desc, B->elem_ptr_, B->desc, *M, *N, *K, C->elem_ptr_, C->desc);

    }
    else if( *isAdiag && !*isBdiag ){

      uni10_elem_copy(C->elem_ptr_, B->elem_ptr_, B->blockrow * B->blockcol*sizeof(uni10_double64));
      uni10_linalg::diagRowMul(C->elem_ptr_, A->elem_ptr_, C->blockrow, C->blockcol, C->c_head);

    }
    else if( !*isAdiag && *isBdiag ){

      uni10_elem_copy(C->elem_ptr_, A->elem_ptr_, A->blockrow * A->blockcol*sizeof(uni10_double64));
      uni10_linalg::diagColMul(C->elem_ptr_, B->elem_ptr_, C->blockrow, C->blockcol, C->r_head);

    }
    else{

      uni10_uint64 min = std::min(A->elem_num_, B->elem_num_);
      uni10_elem_copy(C->elem_ptr_, A->elem_ptr_, min*sizeof(uni10_double64));

      uni10_linalg::vectorMul(C->elem_ptr_, B->elem_ptr_, min);

    }

  }

  void matrixDot(const uni10_elem_complex128* A, uni10_const_bool* isAdiag, const uni10_elem_complex128* B, uni10_const_bool* isBdiag, 
      const uni10_uint64* M, const uni10_uint64* N, const uni10_uint64* K, uni10_elem_complex128* C){

    if( !*isAdiag && !*isBdiag ){

      //uni10_linalg::matrixDot(A->elem_ptr_, B->elem_ptr_, *M, *N, *K, C->elem_ptr_);

    }
    else if( *isAdiag && !*isBdiag ){

      //uni10_elem_copy(C->elem_ptr_, B->elem_ptr_, B->elem_num_*sizeof(uni10_complex128));
      //uni10_linalg::diagRowMul(C->elem_ptr_, A->elem_ptr_, std::min(*M, *K), *N);

    }
    else if( !*isAdiag && *isBdiag ){

      //uni10_uint64 data_col = std::min(*K, *N);

      //for(int r = 0; r < (int)*M; r++)
      //  uni10_elem_copy(&C->elem_ptr_[r*(*N)], &A->elem_ptr_[r*(*K)], data_col*sizeof(uni10_complex128));

      //uni10_linalg::diagColMul(C->elem_ptr_, B->elem_ptr_, *M, data_col);

    }
    else{

      //uni10_uint64 min = std::min(A->elem_num_, B->elem_num_);
      //uni10_elem_copy(C->elem_ptr_, A->elem_ptr_, min*sizeof(uni10_complex128));

      //uni10_linalg::vectorMul(C->elem_ptr_, B->elem_ptr_, min);

    }

  }

  void matrixDot(const uni10_elem_double64* A, uni10_const_bool* isAdiag, const uni10_elem_complex128* B, uni10_const_bool* isBdiag, 
      const uni10_uint64* M, const uni10_uint64* N, const uni10_uint64* K, uni10_elem_complex128* C){

    if( !*isAdiag && !*isBdiag ){

      //uni10_linalg::matrixDot(A->elem_ptr_, B->elem_ptr_, *M, *N, *K, C->elem_ptr_);

    }
    else if( *isAdiag && !*isBdiag ){

      //uni10_elem_copy(C->elem_ptr_, B->elem_ptr_, B->elem_num_*sizeof(uni10_complex128));
      //uni10_linalg::diagRowMul(C->elem_ptr_, A->elem_ptr_, std::min(*M, *K), *N);

    }
    else if( !*isAdiag && *isBdiag ){

      //uni10_uint64 data_col = std::min(*K, *N);

      //for(int r = 0; r < (int)*M; r++)
      //  uni10_elem_cast(&C->elem_ptr_[r*(*N)], &A->elem_ptr_[r*(*K)], data_col);

      //uni10_linalg::diagColMul(C->elem_ptr_, B->elem_ptr_, *M, data_col);

    }
    else{

      //uni10_uint64 min = std::min(A->elem_num_, B->elem_num_);
      //uni10_elem_copy(C->elem_ptr_, A->elem_ptr_, min*sizeof(uni10_complex128));

      //uni10_linalg::vectorMul(C->elem_ptr_, B->elem_ptr_, min);

    }

  }

  void matrixDot(const uni10_elem_complex128* A, uni10_const_bool* isAdiag, const uni10_elem_double64* B, uni10_const_bool* isBdiag, 
      const uni10_uint64* M, const uni10_uint64* N, const uni10_uint64* K, uni10_elem_complex128* C){

    if( !*isAdiag && !*isBdiag ){

      //uni10_linalg::matrixDot(A->elem_ptr_, B->elem_ptr_, *M, *N, *K, C->elem_ptr_);

    }
    else if( *isAdiag && !*isBdiag ){

      //uni10_elem_cast(C->elem_ptr_, B->elem_ptr_, B->elem_num_);
      //uni10_linalg::diagRowMul(C->elem_ptr_, A->elem_ptr_, std::min(*M, *K), *N);

    }
    else if( !*isAdiag && *isBdiag ){

      //uni10_uint64 data_col = std::min(*K, *N);

      //for(int r = 0; r < (int)*M; r++)
      //  uni10_elem_copy(&C->elem_ptr_[r*(*N)], &A->elem_ptr_[r*(*K)], data_col*sizeof(uni10_complex128));

      //uni10_linalg::diagColMul(C->elem_ptr_, B->elem_ptr_, *M, data_col);

    }
    else{

      //uni10_uint64 min = std::min(A->elem_num_, B->elem_num_);
      //uni10_elem_copy(C->elem_ptr_, A->elem_ptr_, min*sizeof(uni10_complex128));

      //uni10_linalg::vectorMul(C->elem_ptr_, B->elem_ptr_, min);

    }

  }

}
