#include "uni10_cusolver_gpu/uni10_elem_linalg_cusolver_gpu.h"

namespace uni10{

  namespace linalg_unielem_internal{

    void MatrixMul(UniElemDouble* A, uni10_bool* isAdiag, const UniElemDouble* B, uni10_const_bool* isBdiag, 
        const uni10_uint64*M, const uni10_uint64* N){

      if(*isAdiag && !*isBdiag){

        linalg_driver_internal::DiagMatMulDenseMat(A->elem_ptr_, B->elem_ptr_, *M, *N);

      }
      else if(!*isAdiag && *isBdiag){

        UniElemDouble MA(*A);
        A->Init(*M, *N, true);
        linalg_driver_internal::DenseMatMulDiagMat(MA.elem_ptr_, B->elem_ptr_, *M, *N, A->elem_ptr_);

      }
      else
        linalg_driver_internal::VectorMul(A->elem_ptr_, B->elem_ptr_, B->elem_num_);

    }

    void MatrixMul(UniElemComplex* A, uni10_bool* isAdiag, const UniElemComplex* B, uni10_const_bool* isBdiag, 
        const uni10_uint64 *M, const uni10_uint64* N){

      if(*isAdiag && !*isBdiag){

        linalg_driver_internal::DiagMatMulDenseMat(A->elem_ptr_, B->elem_ptr_, *M, *N);

      }
      else if(!*isAdiag && *isBdiag){

        UniElemComplex MA(*A);
        A->Init(*M, *N, true);
        linalg_driver_internal::DenseMatMulDiagMat(MA.elem_ptr_, B->elem_ptr_, *M, *N, A->elem_ptr_);

      }
      else
        linalg_driver_internal::VectorMul(A->elem_ptr_, B->elem_ptr_, B->elem_num_);


    }

    void MatrixMul(UniElemComplex* A, uni10_bool* isAdiag, const UniElemDouble* B, uni10_const_bool* isBdiag, 
        const uni10_uint64 *M, const uni10_uint64* N){

      if(*isAdiag && !*isBdiag){

        linalg_driver_internal::DiagMatMulDenseMat(A->elem_ptr_, B->elem_ptr_, *M, *N);

      }
      else if(!*isAdiag && *isBdiag){

        UniElemComplex MA(*A);
        A->Init(*M, *N, true);
        linalg_driver_internal::DenseMatMulDiagMat(MA.elem_ptr_, B->elem_ptr_, *M, *N, A->elem_ptr_);

      }
      else
        linalg_driver_internal::VectorMul(A->elem_ptr_, B->elem_ptr_, B->elem_num_);


    }

    void MatrixMul(const UniElemDouble* A, uni10_const_bool* isAdiag, const UniElemDouble* B, uni10_const_bool* isBdiag, 
        const uni10_uint64* M, const uni10_uint64* N, UniElemDouble* C){

      if( *isAdiag && !*isBdiag ){

        linalg_driver_internal::DiagMatMulDenseMat(A->elem_ptr_, B->elem_ptr_, *M, *N, C->elem_ptr_);

      }
      else if( !*isAdiag && *isBdiag ){

        linalg_driver_internal::DenseMatMulDiagMat(A->elem_ptr_, B->elem_ptr_, *M, *N, C->elem_ptr_);

      }
      else{

        tools_internal::UniElemCopy(C->elem_ptr_, A->elem_ptr_,  A->elem_num_*sizeof(uni10_double64));
        linalg_driver_internal::VectorMul(C->elem_ptr_, B->elem_ptr_, C->elem_num_);

      }

    }

    void MatrixMul(const UniElemComplex* A, uni10_const_bool* isAdiag, const UniElemComplex* B, uni10_const_bool* isBdiag, 
        const uni10_uint64* M, const uni10_uint64* N, UniElemComplex* C){

      if( *isAdiag && !*isBdiag ){

        linalg_driver_internal::DiagMatMulDenseMat(A->elem_ptr_, B->elem_ptr_, *M, *N, C->elem_ptr_);

      }
      else if( !*isAdiag && *isBdiag ){

        linalg_driver_internal::DenseMatMulDiagMat(A->elem_ptr_, B->elem_ptr_, *M, *N, C->elem_ptr_);

      }
      else{

        tools_internal::UniElemCopy(C->elem_ptr_, A->elem_ptr_,  A->elem_num_*sizeof(uni10_complex128));
        linalg_driver_internal::VectorMul(C->elem_ptr_, B->elem_ptr_, C->elem_num_);

      }

    }

    void MatrixMul(const UniElemDouble* A, uni10_const_bool* isAdiag, const UniElemComplex* B, uni10_const_bool* isBdiag, 
        const uni10_uint64* M, const uni10_uint64* N, UniElemComplex* C){

      if( *isAdiag && !*isBdiag ){

        linalg_driver_internal::DiagMatMulDenseMat(A->elem_ptr_, B->elem_ptr_, *M, *N, C->elem_ptr_);

      }
      else if( !*isAdiag && *isBdiag ){

        linalg_driver_internal::DenseMatMulDiagMat(A->elem_ptr_, B->elem_ptr_, *M, *N, C->elem_ptr_);

      }
      else{

        tools_internal::UniElemCopy(C->elem_ptr_, B->elem_ptr_,  B->elem_num_*sizeof(uni10_complex128));
        linalg_driver_internal::VectorMul(C->elem_ptr_, A->elem_ptr_, C->elem_num_);

      }

    }

    void MatrixMul(const UniElemComplex* A, uni10_const_bool* isAdiag, const UniElemDouble* B, uni10_const_bool* isBdiag, 
        const uni10_uint64* M, const uni10_uint64* N, UniElemComplex* C){

      if( *isAdiag && !*isBdiag ){

        linalg_driver_internal::DiagMatMulDenseMat(A->elem_ptr_, B->elem_ptr_, *M, *N, C->elem_ptr_);

      }
      else if( !*isAdiag && *isBdiag ){

        linalg_driver_internal::DenseMatMulDiagMat(A->elem_ptr_, B->elem_ptr_, *M, *N, C->elem_ptr_);

      }
      else{

        tools_internal::UniElemCopy(C->elem_ptr_, A->elem_ptr_,  A->elem_num_*sizeof(uni10_complex128));
        linalg_driver_internal::VectorMul(C->elem_ptr_, B->elem_ptr_, C->elem_num_);

      }

    }

  }

}
