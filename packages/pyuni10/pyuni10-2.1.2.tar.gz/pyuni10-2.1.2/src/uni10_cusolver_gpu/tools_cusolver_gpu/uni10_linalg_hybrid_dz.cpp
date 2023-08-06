#include <limits.h>

#include "uni10_type.h"
#include "uni10_error.h"
#include "uni10_cusolver_gpu/tools_cusolver_gpu/uni10_tools_cusolver_gpu.h"
#include "uni10_cusolver_gpu/tools_cusolver_gpu/uni10_linalg_hybrid_z.h"
#include "uni10_cusolver_gpu/tools_cusolver_gpu/uni10_linalg_hybrid_dz.h"

namespace uni10{

  namespace linalg_driver_internal{

    void VectorAdd(double a, double* X, uni10_int incx, std::complex<double>* Y, uni10_int incy, uni10_uint64 N){   // Y = aX + Y

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

    void VectorAdd(std::complex<double>* Y, double* X, uni10_uint64 N){

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

    void VectorSub(std::complex<double>* Y, double* X, uni10_uint64 N){

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

    void VectorMul(std::complex<double>* Y, double* X, uni10_uint64 N){

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

    void VectorScal(double a, std::complex<double>* X, uni10_uint64 N){
     
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

    void VectorExp(double a, std::complex<double>* X, uni10_uint64 N){

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

    void MatrixDot(double* A, std::complex<double>* B, uni10_int M, uni10_int N, uni10_int K, std::complex<double>* C){

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

    void MatrixDot(std::complex<double>* A, double* B, uni10_int M, uni10_int N, uni10_int K, std::complex<double>* C){

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

    void DiagRowMul(std::complex<double>* mat, double* diag, uni10_uint64 M, uni10_uint64 N){

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

    void DiagColMul(std::complex<double>* mat, double* diag, uni10_uint64 M, uni10_uint64 N){

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

    void EigDecompose(double* Kij_ori, uni10_int N, std::complex<double>* Eig, std::complex<double>* EigVec){

      if(RUNTIMETYPE == only_cpu){

        EigDecompose_cpu(Kij_ori, N, Eig, EigVec);

      }

      else if(RUNTIMETYPE == only_gpu){

        EigDecompose_gpu(Kij_ori, N, Eig, EigVec);

      }

      else if(RUNTIMETYPE == hybrid){

        uni10_error_msg(true, "%s", "Developing");

      }

    }

    void SyEigDecompose(std::complex<double>* Kij, uni10_int N, double* Eig, std::complex<double>* EigVec){

      if(RUNTIMETYPE == only_cpu){

        SyEigDecompose_cpu(Kij, N, Eig, EigVec);

      }

      else if(RUNTIMETYPE == only_gpu){

        SyEigDecompose_gpu(Kij, N, Eig, EigVec);

      }

      else if(RUNTIMETYPE == hybrid){

        uni10_error_msg(true, "%s", "Developing");

      }

    }

    void Svd(std::complex<double>* Mij_ori, uni10_int M, uni10_int N, std::complex<double>* U, double *S, std::complex<double>* vT){

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

    void Sdd(std::complex<double>* Mij_ori, uni10_int M, uni10_int N, std::complex<double>* U, double *S, std::complex<double>* vT){

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

    //
    // function overload for operators + - * += -= *=
    // 
    // r operator(+,-,*,+=,-=,*=) z
    void DiagMatAddDenseMat(const double* D, const std::complex<double>* a, uni10_uint64 m, uni10_uint64 n, std::complex<double>* b){

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

    void DiagMatSubDenseMat(const double* D, const std::complex<double>* a, uni10_uint64 m, uni10_uint64 n, std::complex<double>* b){

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

    void DiagMatMulDenseMat(const double* D, const std::complex<double>* a, uni10_uint64 m, uni10_uint64 n, std::complex<double>* b){

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
   
    void DenseMatAddDiagMat(const double* a, const std::complex<double>* D, uni10_uint64 m, uni10_uint64 n, std::complex<double>* b){

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
                                                                                                                                      
    void DenseMatSubDiagMat(const double* a, const std::complex<double>* D, uni10_uint64 m, uni10_uint64 n, std::complex<double>* b){

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
                                                                                                                                      
    void DenseMatMulDiagMat(const double* a, const std::complex<double>* D, uni10_uint64 m, uni10_uint64 n, std::complex<double>* b){

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

    // z operator(+,-,*,+=,-=,*=) r

    void DiagMatAddDenseMat(const std::complex<double>* D, const double* a, uni10_uint64 m, uni10_uint64 n, std::complex<double>* b){

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

    void DiagMatSubDenseMat(const std::complex<double>* D, const double* a, uni10_uint64 m, uni10_uint64 n, std::complex<double>* b){

      if(RUNTIMETYPE == only_cpu){

        DenseMatSubDiagMat_cpu(D, a, m, n, b);

      }

      else if(RUNTIMETYPE == only_gpu){

        DenseMatSubDiagMat_gpu(D, a, m, n, b);

      }

      else if(RUNTIMETYPE == hybrid){

        uni10_error_msg(true, "%s", "Developing");

      }

    }

    void DiagMatMulDenseMat(const std::complex<double>* D, const double* a, uni10_uint64 m, uni10_uint64 n, std::complex<double>* b){

      if(RUNTIMETYPE == only_cpu){

        DenseMatSubDiagMat_cpu(D, a, m, n, b);

      }

      else if(RUNTIMETYPE == only_gpu){

        DenseMatSubDiagMat_gpu(D, a, m, n, b);

      }

      else if(RUNTIMETYPE == hybrid){

        uni10_error_msg(true, "%s", "Developing");

      }

    }

    void DenseMatAddDiagMat(std::complex<double>* a, const double* D, uni10_uint64 m, uni10_uint64 n){

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
                                                                                                       
    void DenseMatSubDiagMat(std::complex<double>* a, const double* D, uni10_uint64 m, uni10_uint64 n){

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
                                                                                                       
    void DiagMatMulDenseMat(std::complex<double>* D, const double* a, uni10_uint64 m, uni10_uint64 n){

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
   
    void DenseMatAddDiagMat(const std::complex<double>* a, const double* D, uni10_uint64 m, uni10_uint64 n, std::complex<double>* b){

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

    void DenseMatSubDiagMat(const std::complex<double>* a, const double* D, uni10_uint64 m, uni10_uint64 n, std::complex<double>* b){

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

    void DenseMatMulDiagMat(const std::complex<double>* a, const double* D, uni10_uint64 m, uni10_uint64 n, std::complex<double>* b){

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


  };/* namespace linalg_driver_internal */

};/* namespace uni10 */

