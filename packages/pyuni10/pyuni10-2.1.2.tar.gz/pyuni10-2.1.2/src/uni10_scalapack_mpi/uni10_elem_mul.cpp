#include "uni10_scalapack_mpi/uni10_elem_linalg_scalapack_mpi.h"

namespace uni10{

  void matrixMul(uni10_elem_double64* A, uni10_bool* isAdiag, const uni10_elem_double64* B, uni10_const_bool* isBdiag, 
      const uni10_uint64* N){

    if(isAdiag && !isBdiag){
      for(uni10_uint64 i = 0; i < A->elem_num_; i++)
        A->elem_ptr_[i] *= B->elem_ptr_[i*(*N)+i];
    }
    else if(!isAdiag && isBdiag){

      *isAdiag = true;

      A->elem_num_ = B->elem_num_;

      uni10_double64* _elem = (uni10_double64*)malloc(B->elem_num_ * sizeof(uni10_double64));

      for(uni10_uint64 i = 0; i < B->elem_num_; i++)
        _elem[i] = A->elem_ptr_[i*(*N)+i] * B->elem_ptr_[i];

      if(A->elem_ptr_ != NULL)
        uni10_elem_free(A->elem_ptr_, A->elem_num_*sizeof(uni10_double64));

      A->elem_ptr_ = _elem;
    }
    else
      uni10_linalg::vectorMul(A->elem_ptr_, B->elem_ptr_, B->elem_num_);

  }

  void matrixMul(uni10_elem_complex128* A, uni10_bool* isAdiag, const uni10_elem_complex128* B, uni10_const_bool* isBdiag, 
      const uni10_uint64* N){

    if(isAdiag && !isBdiag){
      for(uni10_uint64 i = 0; i < A->elem_num_; i++)
        A->elem_ptr_[i] *= B->elem_ptr_[i*(*N)+i];
    }
    else if(!isAdiag && isBdiag){

      *isAdiag = true;

      A->elem_num_ = B->elem_num_;

      uni10_complex128* _elem = (uni10_complex128*)malloc(B->elem_num_ * sizeof(uni10_complex128));

      for(uni10_uint64 i = 0; i < B->elem_num_; i++)
        _elem[i] = A->elem_ptr_[i*(*N)+i] * B->elem_ptr_[i];

      if(A->elem_ptr_ != NULL)
        uni10_elem_free(A->elem_ptr_, A->elem_num_*sizeof(uni10_complex128));

      A->elem_ptr_ = _elem;
    }
    else
      uni10_linalg::vectorMul(A->elem_ptr_, B->elem_ptr_, B->elem_num_);


  }

  void matrixMul(const uni10_elem_double64* A, uni10_const_bool* isAdiag, const uni10_elem_double64* B, uni10_const_bool* isBdiag, 
      const uni10_uint64* M, const uni10_uint64* N, uni10_elem_double64* C){

    if( *isAdiag && !*isBdiag ){

      uni10_uint64 min = std::min(*M, *N);
      for(int i = 0; i < (int)min; i++){
        C->elem_ptr_[i] = A->elem_ptr_[i] * B->elem_ptr_[i * (*N) + i];
      }

    }
    else if( !*isAdiag && *isBdiag ){

      uni10_uint64 min = std::min(*M, *N);
      for(int i = 0; i < (int)min; i++)
        C->elem_ptr_[i] = B->elem_ptr_[i] * A->elem_ptr_[i * (*N) + i];

    }
    else{

      uni10_elem_copy(C->elem_ptr_, A->elem_ptr_,  A->elem_num_*sizeof(uni10_double64));
      uni10_linalg::vectorMul(C->elem_ptr_, B->elem_ptr_, C->elem_num_);

    }

  }

  void matrixMul(const uni10_elem_complex128* A, uni10_const_bool* isAdiag, const uni10_elem_complex128* B, uni10_const_bool* isBdiag, 
      const uni10_uint64* M, const uni10_uint64* N, uni10_elem_complex128* C){

    if( *isAdiag && !*isBdiag ){

      uni10_uint64 min = std::min(*M, *N);
      for(int i = 0; i < (int)min; i++){
        C->elem_ptr_[i] = A->elem_ptr_[i] * B->elem_ptr_[i * (*N) + i];
      }

    }
    else if( !*isAdiag && *isBdiag ){

      uni10_uint64 min = std::min(*M, *N);
      for(int i = 0; i < (int)min; i++)
        C->elem_ptr_[i] = B->elem_ptr_[i] * A->elem_ptr_[i * (*N) + i];

    }
    else{

      uni10_elem_copy(C->elem_ptr_, A->elem_ptr_,  A->elem_num_*sizeof(uni10_complex128));
      uni10_linalg::vectorMul(C->elem_ptr_, B->elem_ptr_, C->elem_num_);

    }

  }

}
