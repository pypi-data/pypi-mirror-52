#include <limits.h>

#include "uni10_error.h"
#include "uni10_cusolver_gpu/tools_cusolver_gpu/uni10_tools_cusolver_gpu.h"
#include "uni10_cusolver_gpu/tools_cusolver_gpu/uni10_linalg_hybrid_z.h"
#include "uni10_cusolver_gpu/tools_cusolver_gpu/uni10_linalg_hybrid_dz.h"

namespace uni10{

  namespace linalg_driver_internal{

    void VectorAdd(std::complex<double> a, std::complex<double>* X, uni10_int incx, std::complex<double>* Y, uni10_int incy, uni10_uint64 N){   // Y = aX + Y

      if(RUNTIMETYPE == only_cpu){

        VectorAdd_cpu(a, X, incx, Y, incy, N);

      }

      else if(RUNTIMETYPE == only_gpu){

        VectorAdd_gpu(a, X, incx, Y, incy, N);

      }

      else if(RUNTIMETYPE == hybrid){

        uni10_error_msg(true, "%s", "Developing");

      }
      
    }

    // Blas
    void VectorAdd(std::complex<double>* Y, std::complex<double>* X, uni10_uint64 N){

      if(RUNTIMETYPE == only_cpu){

        VectorAdd_cpu(Y, X, N);

      }

      else if(RUNTIMETYPE == only_gpu){

        VectorAdd_gpu(Y, X, N);

      }

      else if(RUNTIMETYPE == hybrid){

        uni10_error_msg(true, "%s", "Developing");

      }

    }

    void VectorSub(std::complex<double>* Y, std::complex<double>* X, uni10_uint64 N){

      if(RUNTIMETYPE == only_cpu){

        VectorSub_cpu(Y, X, N);

      }

      else if(RUNTIMETYPE == only_gpu){

        VectorSub_gpu(Y, X, N);

      }

      else if(RUNTIMETYPE == hybrid){

        uni10_error_msg(true, "%s", "Developing");

      }

    }

    void VectorMul(std::complex<double>* Y, std::complex<double>* X, uni10_uint64 N){ 

      if(RUNTIMETYPE == only_cpu){

        VectorMul_cpu(Y, X, N);

      }

      else if(RUNTIMETYPE == only_gpu){

        VectorMul_gpu(Y, X, N);

      }

      else if(RUNTIMETYPE == hybrid){

        uni10_error_msg(true, "%s", "Developing");

      }

    }

    void VectorScal(std::complex<double> a, std::complex<double>* X, uni10_uint64 N){

      if(RUNTIMETYPE == only_cpu){

        VectorScal_cpu(a, X, N);

      }

      else if(RUNTIMETYPE == only_gpu){

        VectorScal_gpu(a, X, N);

      }

      else if(RUNTIMETYPE == hybrid){

        uni10_error_msg(true, "%s", "Developing");

      }

    }

    void VectorExp(std::complex<double> a, std::complex<double>* X, uni10_uint64 N){

      if(RUNTIMETYPE == only_cpu){

        VectorExp_cpu(a, X, N);

      }

      else if(RUNTIMETYPE == only_gpu){

        VectorExp_gpu(a, X, N);

      }

      else if(RUNTIMETYPE == hybrid){

        uni10_error_msg(true, "%s", "Developing");

      }

    }

    std::complex<double> VectorSum(std::complex<double>* X, uni10_uint64 N, uni10_int inc){

      if(RUNTIMETYPE == only_cpu){

        VectorSum_cpu(X, N, inc);

      }

      else if(RUNTIMETYPE == only_gpu){

        VectorSum_gpu(X, N, inc);

      }

      else if(RUNTIMETYPE == hybrid){

        uni10_error_msg(true, "%s", "Developing");

      }

    }

    double Norm(std::complex<double>* X, uni10_uint64 N, uni10_int inc){

      if(RUNTIMETYPE == only_cpu){

        Norm_cpu(X, N, inc);

      }

      else if(RUNTIMETYPE == only_gpu){

        Norm_gpu(X, N, inc);

      }

      else if(RUNTIMETYPE == hybrid){

        uni10_error_msg(true, "%s", "Developing");

      }

    }

    void MatrixDot(std::complex<double>* A, std::complex<double>* B, uni10_int M, uni10_int N, uni10_int K, std::complex<double>* C){

      if(RUNTIMETYPE == only_cpu){

        MatrixDot_cpu(A, B, M, N, K, C);

      }

      else if(RUNTIMETYPE == only_gpu){

        MatrixDot_gpu(A, B, M, N, K, C);

      }

      else if(RUNTIMETYPE == hybrid){

        uni10_error_msg(true, "%s", "Developing");

      }

    }

    void DiagRowMul(std::complex<double>* mat, std::complex<double>* diag, uni10_uint64 M, uni10_uint64 N){

      if(RUNTIMETYPE == only_cpu){

        DiagRowMul_cpu(mat, diag, M, N);

      }

      else if(RUNTIMETYPE == only_gpu){

        DiagRowMul_gpu(mat, diag, M, N);

      }

      else if(RUNTIMETYPE == hybrid){

        uni10_error_msg(true, "%s", "Developing");

      }

    }

    void DiagColMul(std::complex<double> *mat, std::complex<double>* diag, uni10_uint64 M, uni10_uint64 N){

      if(RUNTIMETYPE == only_cpu){

        DiagColMul_cpu(mat, diag, M, N);

      }

      else if(RUNTIMETYPE == only_gpu){

        DiagColMul_gpu(mat, diag, M, N);

      }

      else if(RUNTIMETYPE == hybrid){

        uni10_error_msg(true, "%s", "Developing");

      }

    }

    void Transpose(std::complex<double>* A, uni10_uint64 M, uni10_uint64 N, std::complex<double>* AT){

      if(RUNTIMETYPE == only_cpu){

        Transpose_cpu(A, M, N, AT);

      }

      else if(RUNTIMETYPE == only_gpu){

        Transpose_gpu(A, M, N, AT);

      }

      else if(RUNTIMETYPE == hybrid){

        uni10_error_msg(true, "%s", "Developing");

      }

    }

    void Transpose(std::complex<double>* A, uni10_uint64 M, uni10_uint64 N){

      if(RUNTIMETYPE == only_cpu){

        Transpose_cpu(A, M, N);

      }

      else if(RUNTIMETYPE == only_gpu){

        Transpose_gpu(A, M, N);

      }

      else if(RUNTIMETYPE == hybrid){

        uni10_error_msg(true, "%s", "Developing");

      }

    }

    void Dagger(std::complex<double>* A, uni10_uint64 M, uni10_uint64 N, std::complex<double> *AT){

      if(RUNTIMETYPE == only_cpu){

        Dagger_cpu(A, M, N, AT);

      }

      else if(RUNTIMETYPE == only_gpu){

        Dagger_gpu(A, M, N, AT);

      }

      else if(RUNTIMETYPE == hybrid){

        uni10_error_msg(true, "%s", "Developing");

      }

    }

    void Dagger(std::complex<double>* A, uni10_uint64 M, uni10_uint64 N){

      if(RUNTIMETYPE == only_cpu){

        Dagger_cpu(A, M, N);

      }

      else if(RUNTIMETYPE == only_gpu){

        Dagger_gpu(A, M, N);

      }

      else if(RUNTIMETYPE == hybrid){

        uni10_error_msg(true, "%s", "Developing");

      }

    }

    void Conjugate(std::complex<double> *A, uni10_uint64 N, std::complex<double> *A_conj){

      if(RUNTIMETYPE == only_cpu){

        Conjugate_cpu(A, N, A_conj);

      }

      else if(RUNTIMETYPE == only_gpu){

        Conjugate_gpu(A, N, A_conj);

      }

      else if(RUNTIMETYPE == hybrid){

        uni10_error_msg(true, "%s", "Developing");

      }

    }

    void Conjugate(std::complex<double> *A, uni10_uint64 N){

      if(RUNTIMETYPE == only_cpu){

        Conjugate_cpu(A, N);

      }

      else if(RUNTIMETYPE == only_gpu){

        Conjugate_gpu(A, N);

      }

      else if(RUNTIMETYPE == hybrid){

        uni10_error_msg(true, "%s", "Developing");

      }

    }

    //LAPACK
    //
    void Svd(std::complex<double>* Mij_ori, uni10_int M, uni10_int N, std::complex<double>* U, std::complex<double>* S, std::complex<double>* vT){

      if(RUNTIMETYPE == only_cpu){

        Svd_cpu(Mij_ori, M, N, U, S, vT);

      }

      else if(RUNTIMETYPE == only_gpu){

        Svd_gpu(Mij_ori, M, N, U, S, vT);

      }

      else if(RUNTIMETYPE == hybrid){

        uni10_error_msg(true, "%s", "Developing");

      }

    }

    void Sdd(std::complex<double>* Mij_ori, uni10_int M, uni10_int N, std::complex<double>* U, std::complex<double>* S, std::complex<double>* vT){

      if(RUNTIMETYPE == only_cpu){

        Sdd_cpu(Mij_ori, M, N, U, S, vT);

      }

      else if(RUNTIMETYPE == only_gpu){

        Sdd_gpu(Mij_ori, M, N, U, S, vT);

      }

      else if(RUNTIMETYPE == hybrid){

        uni10_error_msg(true, "%s", "Developing");

      }

    }

    void Qr(std::complex<double>* Mij_ori, uni10_int M, uni10_int N, std::complex<double>* Q, std::complex<double>* R){

      if(RUNTIMETYPE == only_cpu){

        Qr_cpu(Mij_ori, M, N, Q, R);

      }

      else if(RUNTIMETYPE == only_gpu){

        Qr_gpu(Mij_ori, M, N, Q, R);

      }

      else if(RUNTIMETYPE == hybrid){

        uni10_error_msg(true, "%s", "Developing");

      }

    }

    void Rq(std::complex<double>* Mij_ori, uni10_int M, uni10_int N, std::complex<double>* R, std::complex<double>* Q){

      if(RUNTIMETYPE == only_cpu){

        Rq_cpu(Mij_ori, M, N, R, Q);

      }

      else if(RUNTIMETYPE == only_gpu){

        Rq_gpu(Mij_ori, M, N, R, Q);

      }

      else if(RUNTIMETYPE == hybrid){

        uni10_error_msg(true, "%s", "Developing");

      }

    }

    void Lq(std::complex<double>* Mij_ori, uni10_int M, uni10_int N, std::complex<double>* L, std::complex<double>* Q){

      if(RUNTIMETYPE == only_cpu){

        Lq_cpu(Mij_ori, M, N, L, Q);

      }

      else if(RUNTIMETYPE == only_gpu){

        Lq_gpu(Mij_ori, M, N, L, Q);

      }

      else if(RUNTIMETYPE == hybrid){

        uni10_error_msg(true, "%s", "Developing");

      }

    }

    void Ql(std::complex<double>* Mij_ori, uni10_int M, uni10_int N, std::complex<double>* Q, std::complex<double>* L){

      if(RUNTIMETYPE == only_cpu){

        Ql_cpu(Mij_ori, M, N, Q, L);

      }

      else if(RUNTIMETYPE == only_gpu){

        Ql_gpu(Mij_ori, M, N, Q, L);

      }

      else if(RUNTIMETYPE == hybrid){

        uni10_error_msg(true, "%s", "Developing");

      }

    }

    void Qdr(std::complex<double>* Mij_ori, uni10_int M, uni10_int N, std::complex<double>* Q, std::complex<double>* D, std::complex<double>* R){

      if(RUNTIMETYPE == only_cpu){

        Qdr_cpu(Mij_ori, M, N, Q, D, R);

      }

      else if(RUNTIMETYPE == only_gpu){

        Qdr_gpu(Mij_ori, M, N, Q, D, R);

      }

      else if(RUNTIMETYPE == hybrid){

        uni10_error_msg(true, "%s", "Developing");

      }

    }


    void Ldq(std::complex<double>* Mij_ori, uni10_int M, uni10_int N, std::complex<double>* L, std::complex<double>* D, std::complex<double>* Q){

      if(RUNTIMETYPE == only_cpu){

        Ldq_cpu(Mij_ori, M, N, L, D, Q);

      }

      else if(RUNTIMETYPE == only_gpu){

        Ldq_gpu(Mij_ori, M, N, L, D, Q);

      }

      else if(RUNTIMETYPE == hybrid){

        uni10_error_msg(true, "%s", "Developing");

      }

    }

    void QdrColPivot(std::complex<double>* Mij_ori, uni10_int M, uni10_int N, std::complex<double>* Q, std::complex<double>* D, std::complex<double>* R){

      if(RUNTIMETYPE == only_cpu){

        QdrColPivot_cpu(Mij_ori, M, N, Q, D, R);

      }

      else if(RUNTIMETYPE == only_gpu){

        QdrColPivot_gpu(Mij_ori, M, N, Q, D, R);

      }

      else if(RUNTIMETYPE == hybrid){

        uni10_error_msg(true, "%s", "Developing");

      }

    }


    void Inverse(std::complex<double>* A, uni10_int N){

      if(RUNTIMETYPE == only_cpu){

        Inverse_cpu(A, N);

      }

      else if(RUNTIMETYPE == only_gpu){

        Inverse_gpu(A, N);

      }

      else if(RUNTIMETYPE == hybrid){

        uni10_error_msg(true, "%s", "Developing");

      }

    }

    std::complex<double> Det(std::complex<double>* A, uni10_int N){

      if(RUNTIMETYPE == only_cpu){

        Det_cpu(A, N);

      }

      else if(RUNTIMETYPE == only_gpu){

        Det_gpu(A, N);

      }

      else if(RUNTIMETYPE == hybrid){

        uni10_error_msg(true, "%s", "Developing");

      }

    }

    void EigDecompose(std::complex<double>* Kij, uni10_int N, std::complex<double>* Eig, std::complex<double>* EigVec){

      if(RUNTIMETYPE == only_cpu){

        EigDecompose_cpu(Kij, N, Eig, EigVec);

      }

      else if(RUNTIMETYPE == only_gpu){

        EigDecompose_gpu(Kij, N, Eig, EigVec);

      }

      else if(RUNTIMETYPE == hybrid){

        uni10_error_msg(true, "%s", "Developing");

      }

    }

    void Identity(std::complex<double>* elem, uni10_uint64 M, uni10_uint64 N){

      if(RUNTIMETYPE == only_cpu){

        Identity_cpu(elem, M, N);

      }

      else if(RUNTIMETYPE == only_gpu){

        Identity_gpu(elem, M, N);

      }

      else if(RUNTIMETYPE == hybrid){

        uni10_error_msg(true, "%s", "Developing");

      }

    }

    //
    // function overload for operators + - * += -= *=
    // 
    void DiagMatAddDenseMat(const std::complex<double>* D, const std::complex<double>* a, uni10_uint64 m, uni10_uint64 n, std::complex<double>* b){

      if(RUNTIMETYPE == only_cpu){

        DiagMatAddDenseMat_cpu(D, a, m, n, b);

      }

      else if(RUNTIMETYPE == only_gpu){

        DiagMatAddDenseMat_gpu(D, a, m, n, b);

      }

      else if(RUNTIMETYPE == hybrid){

        uni10_error_msg(true, "%s", "Developing");

      }

    }

    void DiagMatSubDenseMat(const std::complex<double>* D, const std::complex<double>* a, uni10_uint64 m, uni10_uint64 n, std::complex<double>* b){

      if(RUNTIMETYPE == only_cpu){

        DiagMatSubDenseMat_cpu(D, a, m, n, b);

      }

      else if(RUNTIMETYPE == only_gpu){

        DiagMatSubDenseMat_gpu(D, a, m, n, b);

      }

      else if(RUNTIMETYPE == hybrid){

        uni10_error_msg(true, "%s", "Developing");

      }

    }

    void DiagMatMulDenseMat(const std::complex<double>* D, const std::complex<double>* a, uni10_uint64 m, uni10_uint64 n, std::complex<double>* b){

      if(RUNTIMETYPE == only_cpu){

        DiagMatMulDenseMat_cpu(D, a, m, n, b);

      }

      else if(RUNTIMETYPE == only_gpu){

        DiagMatMulDenseMat_gpu(D, a, m, n, b);

      }

      else if(RUNTIMETYPE == hybrid){

        uni10_error_msg(true, "%s", "Developing");

      }

    }

    void DenseMatAddDiagMat(std::complex<double>* a, const std::complex<double>* D, uni10_uint64 m, uni10_uint64 n){

      if(RUNTIMETYPE == only_cpu){

        DenseMatAddDiagMat_cpu(a, D, m, n);

      }

      else if(RUNTIMETYPE == only_gpu){

        DenseMatAddDiagMat_gpu(a, D, m, n);

      }

      else if(RUNTIMETYPE == hybrid){

        uni10_error_msg(true, "%s", "Developing");

      }

    }
                                                                                      
    void DenseMatSubDiagMat(std::complex<double>* a, const std::complex<double>* D, uni10_uint64 m, uni10_uint64 n){

      if(RUNTIMETYPE == only_cpu){

        DenseMatSubDiagMat_cpu(a, D, m, n);

      }

      else if(RUNTIMETYPE == only_gpu){

        DenseMatSubDiagMat_gpu(a, D, m, n);

      }

      else if(RUNTIMETYPE == hybrid){

        uni10_error_msg(true, "%s", "Developing");

      }

    }

    void DiagMatMulDenseMat(std::complex<double>* D, const std::complex<double>* a, uni10_uint64 m, uni10_uint64 n){

      if(RUNTIMETYPE == only_cpu){

        DiagMatMulDenseMat_cpu(D, a, m, n);

      }

      else if(RUNTIMETYPE == only_gpu){

        DiagMatMulDenseMat_gpu(D, a, m, n);

      }

      else if(RUNTIMETYPE == hybrid){

        uni10_error_msg(true, "%s", "Developing");

      }

    }
   
    void DenseMatAddDiagMat(const std::complex<double>* a, const std::complex<double>* D, uni10_uint64 m, uni10_uint64 n, std::complex<double>* b){

      if(RUNTIMETYPE == only_cpu){

        DenseMatAddDiagMat_cpu(a, D, m, n, b);

      }

      else if(RUNTIMETYPE == only_gpu){

        DenseMatAddDiagMat_gpu(a, D, m, n, b);

      }

      else if(RUNTIMETYPE == hybrid){

        uni10_error_msg(true, "%s", "Developing");

      }

    }
                                                                                                                                                    
    void DenseMatSubDiagMat(const std::complex<double>* a, const std::complex<double>* D, uni10_uint64 m, uni10_uint64 n, std::complex<double>* b){

      if(RUNTIMETYPE == only_cpu){

        DenseMatSubDiagMat_cpu(a, D, m, n, b);

      }

      else if(RUNTIMETYPE == only_gpu){

        DenseMatSubDiagMat_gpu(a, D, m, n, b);

      }

      else if(RUNTIMETYPE == hybrid){

        uni10_error_msg(true, "%s", "Developing");

      }

    }
                                                                                                                                                    
    void DenseMatMulDiagMat(const std::complex<double>* a, const std::complex<double>* D, uni10_uint64 m, uni10_uint64 n, std::complex<double>* b){

      if(RUNTIMETYPE == only_cpu){

        DenseMatMulDiagMat_cpu(a, D, m, n, b);

      }

      else if(RUNTIMETYPE == only_gpu){

        DenseMatMulDiagMat_gpu(a, D, m, n, b);

      }

      else if(RUNTIMETYPE == hybrid){

        uni10_error_msg(true, "%s", "Developing");

      }

    }

  } /* namespace linalg_driver_internal */

}
