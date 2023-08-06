#include "uni10_cusolver_gpu/uni10_elem_linalg_cusolver_gpu.h"

namespace uni10{

  namespace linalg_unielem_internal{

    void Dot(const UniElemDouble* A, uni10_const_bool* isAdiag, const UniElemDouble* B, uni10_const_bool* isBdiag, 
        const uni10_uint64* M, const uni10_uint64* N, const uni10_uint64* K, UniElemDouble* C){

      if( !*isAdiag && !*isBdiag ){

        linalg_driver_internal::MatrixDot(A->elem_ptr_, B->elem_ptr_, *M, *N, *K, C->elem_ptr_);

      }
      else if( *isAdiag && !*isBdiag ){

        tools_internal::UniElemCopy(C->elem_ptr_, B->elem_ptr_, B->elem_num_*sizeof(uni10_double64));
        linalg_driver_internal::DiagRowMul(C->elem_ptr_, A->elem_ptr_, std::min(*M, *K), *N);

      }
      else if( !*isAdiag && *isBdiag ){

        uni10_uint64 data_col = std::min(*K, *N);

        for(int r = 0; r < (int)*M; r++)
          tools_internal::UniElemCopy(&C->elem_ptr_[r*(*N)], &A->elem_ptr_[r*(*K)], data_col *sizeof(uni10_double64));

        linalg_driver_internal::DiagColMul(C->elem_ptr_, B->elem_ptr_, *M, data_col);

      }
      else{

        uni10_uint64 min = std::min(A->elem_num_, B->elem_num_);
        tools_internal::UniElemCopy(C->elem_ptr_, A->elem_ptr_, min*sizeof(uni10_double64));

        linalg_driver_internal::VectorMul(C->elem_ptr_, B->elem_ptr_, min);

      }

    }

    void Dot(const UniElemComplex* A, uni10_const_bool* isAdiag, const UniElemComplex* B, uni10_const_bool* isBdiag, 
        const uni10_uint64* M, const uni10_uint64* N, const uni10_uint64* K, UniElemComplex* C){

      if( !*isAdiag && !*isBdiag ){

        linalg_driver_internal::MatrixDot(A->elem_ptr_, B->elem_ptr_, *M, *N, *K, C->elem_ptr_);

      }
      else if( *isAdiag && !*isBdiag ){

        tools_internal::UniElemCopy(C->elem_ptr_, B->elem_ptr_, B->elem_num_*sizeof(uni10_complex128));
        linalg_driver_internal::DiagRowMul(C->elem_ptr_, A->elem_ptr_, std::min(*M, *K), *N);

      }
      else if( !*isAdiag && *isBdiag ){

        uni10_uint64 data_col = std::min(*K, *N);

        for(int r = 0; r < (int)*M; r++)
          tools_internal::UniElemCopy(&C->elem_ptr_[r*(*N)], &A->elem_ptr_[r*(*K)], data_col*sizeof(uni10_complex128));

        linalg_driver_internal::DiagColMul(C->elem_ptr_, B->elem_ptr_, *M, data_col);

      }
      else{

        uni10_uint64 min = std::min(A->elem_num_, B->elem_num_);
        tools_internal::UniElemCopy(C->elem_ptr_, A->elem_ptr_, min*sizeof(uni10_complex128));

        linalg_driver_internal::VectorMul(C->elem_ptr_, B->elem_ptr_, min);

      }

    }

    void Dot(const UniElemDouble* A, uni10_const_bool* isAdiag, const UniElemComplex* B, uni10_const_bool* isBdiag, 
        const uni10_uint64* M, const uni10_uint64* N, const uni10_uint64* K, UniElemComplex* C){

      if( !*isAdiag && !*isBdiag ){

        linalg_driver_internal::MatrixDot(A->elem_ptr_, B->elem_ptr_, *M, *N, *K, C->elem_ptr_);

      }
      else if( *isAdiag && !*isBdiag ){

        tools_internal::UniElemCopy(C->elem_ptr_, B->elem_ptr_, B->elem_num_*sizeof(uni10_complex128));
        linalg_driver_internal::DiagRowMul(C->elem_ptr_, A->elem_ptr_, std::min(*M, *K), *N);

      }
      else if( !*isAdiag && *isBdiag ){

        uni10_uint64 data_col = std::min(*K, *N);

        for(int r = 0; r < (int)*M; r++)
          tools_internal::UniElemCast(&C->elem_ptr_[r*(*N)], &A->elem_ptr_[r*(*K)], data_col);

        linalg_driver_internal::DiagColMul(C->elem_ptr_, B->elem_ptr_, *M, data_col);

      }
      else{

        uni10_uint64 min = std::min(A->elem_num_, B->elem_num_);
        tools_internal::UniElemCopy(C->elem_ptr_, A->elem_ptr_, min*sizeof(uni10_complex128));

        linalg_driver_internal::VectorMul(C->elem_ptr_, B->elem_ptr_, min);

      }

    }

    void Dot(const UniElemComplex* A, uni10_const_bool* isAdiag, const UniElemDouble* B, uni10_const_bool* isBdiag, 
        const uni10_uint64* M, const uni10_uint64* N, const uni10_uint64* K, UniElemComplex* C){

      if( !*isAdiag && !*isBdiag ){

        linalg_driver_internal::MatrixDot(A->elem_ptr_, B->elem_ptr_, *M, *N, *K, C->elem_ptr_);

      }
      else if( *isAdiag && !*isBdiag ){

        tools_internal::UniElemCast(C->elem_ptr_, B->elem_ptr_, B->elem_num_);
        linalg_driver_internal::DiagRowMul(C->elem_ptr_, A->elem_ptr_, std::min(*M, *K), *N);

      }
      else if( !*isAdiag && *isBdiag ){

        uni10_uint64 data_col = std::min(*K, *N);

        for(int r = 0; r < (int)*M; r++)
          tools_internal::UniElemCopy(&C->elem_ptr_[r*(*N)], &A->elem_ptr_[r*(*K)], data_col*sizeof(uni10_complex128));

        linalg_driver_internal::DiagColMul(C->elem_ptr_, B->elem_ptr_, *M, data_col);

      }
      else{

        uni10_uint64 min = std::min(A->elem_num_, B->elem_num_);
        tools_internal::UniElemCopy(C->elem_ptr_, A->elem_ptr_, min*sizeof(uni10_complex128));

        linalg_driver_internal::VectorMul(C->elem_ptr_, B->elem_ptr_, min);

      }

    }

  }

}
