#include "uni10_lapack_cpu/uni10_elem_linalg.h"

namespace uni10{

  namespace linalg_unielem_internal{

    void MatrixSub(UniElemDouble* A, uni10_bool* isAdiag, const UniElemDouble* B, uni10_const_bool* isBdiag, 
        const uni10_uint64* M, const uni10_uint64* N){

      if(*isAdiag && !*isBdiag){

        UniElemDouble DA(*A);
        A->Init(*M, *N, false);
        linalg_driver_internal::DiagMatSubDenseMat(DA.elem_ptr_, B->elem_ptr_, *M, *N, A->elem_ptr_);

      }
      else if(!*isAdiag && *isBdiag){

        linalg_driver_internal::DenseMatSubDiagMat(A->elem_ptr_, B->elem_ptr_, *M, *N);

      }
      else
        linalg_driver_internal::VectorSub(A->elem_ptr_, B->elem_ptr_, B->elem_num_);

    }

    void MatrixSub(UniElemComplex* A, uni10_bool* isAdiag, const UniElemComplex* B, uni10_const_bool* isBdiag, 
        const uni10_uint64* M, const uni10_uint64* N){

      if(*isAdiag && !*isBdiag){

        UniElemComplex DA(*A);
        A->Init(*M, *N, false);
        linalg_driver_internal::DiagMatSubDenseMat(DA.elem_ptr_, B->elem_ptr_, *M, *N, A->elem_ptr_);

      }
      else if(!*isAdiag && *isBdiag){

        linalg_driver_internal::DenseMatSubDiagMat(A->elem_ptr_, B->elem_ptr_, *M, *N);

      }
      else
        linalg_driver_internal::VectorSub(A->elem_ptr_, B->elem_ptr_, B->elem_num_);

    }

    void MatrixSub(UniElemComplex* A, uni10_bool* isAdiag, const UniElemDouble* B, uni10_const_bool* isBdiag, 
        const uni10_uint64* M, const uni10_uint64* N){

      if(*isAdiag && !*isBdiag){

        UniElemComplex DA(*A);
        A->Init(*M, *N, false);
        linalg_driver_internal::DiagMatSubDenseMat(DA.elem_ptr_, B->elem_ptr_, *M, *N, A->elem_ptr_);

      }
      else if(!*isAdiag && *isBdiag){

        linalg_driver_internal::DenseMatSubDiagMat(A->elem_ptr_, B->elem_ptr_, *M, *N);

      }
      else
        linalg_driver_internal::VectorSub(A->elem_ptr_, B->elem_ptr_, B->elem_num_);

    }

    void MatrixSub(const UniElemDouble* A, uni10_const_bool* isAdiag, const UniElemDouble* B, uni10_const_bool* isBdiag, 
        const uni10_uint64* M, const uni10_uint64* N, UniElemDouble* C){

      if( *isAdiag && !*isBdiag ){

        linalg_driver_internal::DiagMatSubDenseMat(A->elem_ptr_, B->elem_ptr_, *M, *N, C->elem_ptr_);

      }
      else if( !*isAdiag && *isBdiag ){

        linalg_driver_internal::DenseMatSubDiagMat(A->elem_ptr_, B->elem_ptr_, *M, *N, C->elem_ptr_);

      }
      else{

        tools_internal::UniElemCopy(C->elem_ptr_, A->elem_ptr_,  C->elem_num_*sizeof(uni10_double64));
        linalg_driver_internal::VectorSub(C->elem_ptr_, B->elem_ptr_, C->elem_num_);

      }

    }

    void MatrixSub(const UniElemComplex* A, uni10_const_bool* isAdiag, const UniElemComplex* B, uni10_const_bool* isBdiag, 
        const uni10_uint64* M, const uni10_uint64* N, UniElemComplex* C){

      if( *isAdiag && !*isBdiag ){

        linalg_driver_internal::DiagMatSubDenseMat(A->elem_ptr_, B->elem_ptr_, *M, *N, C->elem_ptr_);

      }
      else if( !*isAdiag && *isBdiag ){

        linalg_driver_internal::DenseMatSubDiagMat(A->elem_ptr_, B->elem_ptr_, *M, *N, C->elem_ptr_);

      }
      else{

        tools_internal::UniElemCopy(C->elem_ptr_, A->elem_ptr_,  A->elem_num_*sizeof(uni10_complex128));
        linalg_driver_internal::VectorSub(C->elem_ptr_, B->elem_ptr_, C->elem_num_);

      }

    }

    void MatrixSub(const UniElemDouble* A, uni10_const_bool* isAdiag, const UniElemComplex* B, uni10_const_bool* isBdiag, 
        const uni10_uint64* M, const uni10_uint64* N, UniElemComplex* C){

      if( *isAdiag && !*isBdiag ){

        linalg_driver_internal::DiagMatSubDenseMat(A->elem_ptr_, B->elem_ptr_, *M, *N, C->elem_ptr_);

      }
      else if( !*isAdiag && *isBdiag ){

        linalg_driver_internal::DenseMatSubDiagMat(A->elem_ptr_, B->elem_ptr_, *M, *N, C->elem_ptr_);

      }
      else{

        tools_internal::UniElemCast(C->elem_ptr_, A->elem_ptr_, C->elem_num_);
        linalg_driver_internal::VectorSub(C->elem_ptr_, B->elem_ptr_, C->elem_num_);

      }

    }

    void MatrixSub(const UniElemComplex* A, uni10_const_bool* isAdiag, const UniElemDouble* B, uni10_const_bool* isBdiag, 
        const uni10_uint64* M, const uni10_uint64* N, UniElemComplex* C){

      if( *isAdiag && !*isBdiag ){

        linalg_driver_internal::DiagMatSubDenseMat(A->elem_ptr_, B->elem_ptr_, *M, *N, C->elem_ptr_);

      }
      else if( !*isAdiag && *isBdiag ){

        linalg_driver_internal::DenseMatSubDiagMat(A->elem_ptr_, B->elem_ptr_, *M, *N, C->elem_ptr_);

      }
      else{

        tools_internal::UniElemCopy(C->elem_ptr_, A->elem_ptr_, A->elem_num_*sizeof(uni10_complex128));
        linalg_driver_internal::VectorSub(C->elem_ptr_, B->elem_ptr_, C->elem_num_);

      }

    }

  }

}
