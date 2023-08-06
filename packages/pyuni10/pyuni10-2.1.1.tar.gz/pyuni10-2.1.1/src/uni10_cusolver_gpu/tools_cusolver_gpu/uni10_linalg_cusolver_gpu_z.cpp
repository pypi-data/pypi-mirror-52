#include "uni10_cusolver_gpu/tools_cusolver_gpu/uni10_linalg_cusolver_gpu_z.h"

namespace uni10{

  namespace linalg_driver_internal{

    void VectorAdd_gpu(std::complex<double> a, std::complex<double>* X, uni10_int incx, std::complex<double>* Y, uni10_int incy, uni10_uint64 N){   // Y = aX + Y
      
      uni10_error_msg(true, "%s", "Developing");

    }

    // Blas
    void VectorAdd_gpu(std::complex<double>* Y, std::complex<double>* X, uni10_uint64 N){

      uni10_error_msg(true, "%s", "Developing");

    }

    void VectorSub_gpu(std::complex<double>* Y, std::complex<double>* X, uni10_uint64 N){

      uni10_error_msg(true, "%s", "Developing");

    }

    void VectorMul_gpu(std::complex<double>* Y, std::complex<double>* X, uni10_uint64 N){ 

      uni10_error_msg(true, "%s", "Developing");

    }

    void VectorScal_gpu(std::complex<double> a, std::complex<double>* X, uni10_uint64 N){

      uni10_error_msg(true, "%s", "Developing");

    }

    void VectorExp_gpu(std::complex<double> a, std::complex<double>* X, uni10_uint64 N){

      uni10_error_msg(true, "%s", "Developing");

    }

    std::complex<double> VectorSum_gpu(std::complex<double>* X, uni10_uint64 N, uni10_int inc){

      uni10_error_msg(true, "%s", "Developing");

    }

    double Norm_gpu(std::complex<double>* X, uni10_uint64 N, uni10_int inc){

      uni10_error_msg(true, "%s", "Developing");

    }

    void MatrixDot_gpu(std::complex<double>* A, std::complex<double>* B, uni10_int M, uni10_int N, uni10_int K, std::complex<double>* C){

      uni10_error_msg(true, "%s", "Developing");

    }

    void DiagRowMul_gpu(std::complex<double>* mat, std::complex<double>* diag, uni10_uint64 M, uni10_uint64 N){

      uni10_error_msg(true, "%s", "Developing");

    }

    void DiagColMul_gpu(std::complex<double> *mat, std::complex<double>* diag, uni10_uint64 M, uni10_uint64 N){

      uni10_error_msg(true, "%s", "Developing");

    }

    void Transpose_gpu(std::complex<double>* A, uni10_uint64 M, uni10_uint64 N, std::complex<double>* AT){

      uni10_error_msg(true, "%s", "Developing");

    }

    void Transpose_gpu(std::complex<double>* A, uni10_uint64 M, uni10_uint64 N){

      uni10_error_msg(true, "%s", "Developing");

    }

    void Dagger_gpu(std::complex<double>* A, uni10_uint64 M, uni10_uint64 N, std::complex<double> *AT){

      uni10_error_msg(true, "%s", "Developing");

    }

    void Dagger_gpu(std::complex<double>* A, uni10_uint64 M, uni10_uint64 N){

      uni10_error_msg(true, "%s", "Developing");

    }

    void Conjugate_gpu(std::complex<double> *A, uni10_uint64 N, std::complex<double> *A_conj){

      uni10_error_msg(true, "%s", "Developing");

    }

    void Conjugate_gpu(std::complex<double> *A, uni10_uint64 N){

      uni10_error_msg(true, "%s", "Developing");

    }

    //LAPACK
    //
    void Svd_gpu(std::complex<double>* Mij_ori, uni10_int M, uni10_int N, std::complex<double>* U, std::complex<double>* S_ori, std::complex<double>* vT){

      uni10_error_msg(true, "%s", "Developing");

    }

    void Sdd_gpu(std::complex<double>* Mij_ori, uni10_int M, uni10_int N, std::complex<double>* U, std::complex<double>* S_ori, std::complex<double>* vT){

      uni10_error_msg(true, "%s", "Developing");

    }

    void Qr_gpu(std::complex<double>* Mij_ori, uni10_int M, uni10_int N, std::complex<double>* Q, std::complex<double>* R){

      uni10_error_msg(true, "%s", "Developing");

    }

    void Rq_gpu(std::complex<double>* Mij_ori, uni10_int M, uni10_int N, std::complex<double>* R, std::complex<double>* Q){

      uni10_error_msg(true, "%s", "Developing");

    }

    void Lq_gpu(std::complex<double>* Mij_ori, uni10_int M, uni10_int N, std::complex<double>* L, std::complex<double>* Q){

      uni10_error_msg(true, "%s", "Developing");

    }

    void Ql_gpu(std::complex<double>* Mij_ori, uni10_int M, uni10_int N, std::complex<double>* Q, std::complex<double>* L){

      uni10_error_msg(true, "%s", "Developing");

    }

    void Qdr_gpu(std::complex<double>* Mij_ori, uni10_int M, uni10_int N, std::complex<double>* Q, std::complex<double>* D, std::complex<double>* R){

      uni10_error_msg(true, "%s", "Developing");

    }


    void Ldq_gpu(std::complex<double>* Mij_ori, uni10_int M, uni10_int N, std::complex<double>* L, std::complex<double>* D, std::complex<double>* Q){

      uni10_error_msg(true, "%s", "Developing");

    }

    void QdrColPivot_gpu(std::complex<double>* Mij_ori, uni10_int M, uni10_int N, std::complex<double>* Q, std::complex<double>* D, std::complex<double>* R){

      uni10_error_msg(true, "%s", "Developing");

    }


    void Inverse_gpu(std::complex<double>* A, uni10_int N){

      uni10_error_msg(true, "%s", "Developing");
    }


    std::complex<double> Det_gpu(std::complex<double>* A, uni10_int N){

      uni10_error_msg(true, "%s", "Developing");

    }

    void EigDecompose_gpu(std::complex<double>* Kij, uni10_int N, std::complex<double>* Eig, std::complex<double>* EigVec){
      uni10_uint64 memsize = N * N * sizeof(std::complex<double>);

      uni10_error_msg(true, "%s", "Developing");

    }

    void Identity_gpu(std::complex<double>* elem, uni10_uint64 M, uni10_uint64 N){

      uni10_error_msg(true, "%s", "Developing");

    }

    //
    // function overload for operators + - * += -= *=
    // 
    void DiagMatAddDenseMat_gpu(const std::complex<double>* D, const std::complex<double>* a, uni10_uint64 m, uni10_uint64 n, std::complex<double>* b){

      uni10_error_msg(true, "%s", "Developing");

    }

    void DiagMatSubDenseMat_gpu(const std::complex<double>* D, const std::complex<double>* a, uni10_uint64 m, uni10_uint64 n, std::complex<double>* b){

      uni10_error_msg(true, "%s", "Developing");

    }

    void DiagMatMulDenseMat_gpu(const std::complex<double>* D, const std::complex<double>* a, uni10_uint64 m, uni10_uint64 n, std::complex<double>* b){

      uni10_error_msg(true, "%s", "Developing");

    }

    void DenseMatAddDiagMat_gpu(std::complex<double>* a, const std::complex<double>* D, uni10_uint64 m, uni10_uint64 n){

      uni10_error_msg(true, "%s", "Developing");

    }

    void DenseMatSubDiagMat_gpu(std::complex<double>* a, const std::complex<double>* D, uni10_uint64 m, uni10_uint64 n){

      uni10_error_msg(true, "%s", "Developing");

    }

    void DiagMatMulDenseMat_gpu(std::complex<double>* D, const std::complex<double>* a, uni10_uint64 m, uni10_uint64 n){

      uni10_error_msg(true, "%s", "Developing");

    }
   
    void DenseMatAddDiagMat_gpu(const std::complex<double>* a, const std::complex<double>* D, uni10_uint64 m, uni10_uint64 n, std::complex<double>* b){

      uni10_error_msg(true, "%s", "Developing");

    }

    void DenseMatSubDiagMat_gpu(const std::complex<double>* a, const std::complex<double>* D, uni10_uint64 m, uni10_uint64 n, std::complex<double>* b){

      uni10_error_msg(true, "%s", "Developing");

    }

    void DenseMatMulDiagMat_gpu(const std::complex<double>* a, const std::complex<double>* D, uni10_uint64 m, uni10_uint64 n, std::complex<double>* b){

      uni10_error_msg(true, "%s", "Developing");

    }

  } /* namespace linalg_driver_internal */

}
