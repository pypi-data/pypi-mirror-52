#include "uni10_cusolver_gpu/tools_cusolver_gpu/uni10_linalg_cusolver_gpu_dz.h"

namespace uni10{

  namespace linalg_driver_internal{

    void VectorAdd_gpu(double a, double* X, uni10_int incx, std::complex<double>* Y, uni10_int incy, uni10_uint64 N){   // Y = aX + Y

    }

    void VectorAdd_gpu(std::complex<double>* Y, double* X, uni10_uint64 N){

    }

    void VectorSub_gpu(std::complex<double>* Y, double* X, uni10_uint64 N){

    }

    void VectorMul_gpu(std::complex<double>* Y, double* X, uni10_uint64 N){

    }

    void VectorScal_gpu(double a, std::complex<double>* X, uni10_uint64 N){

    }

    void VectorExp_gpu(double a, std::complex<double>* X, uni10_uint64 N){

    }

    void MatrixDot_gpu(double* A, std::complex<double>* B, uni10_int M, uni10_int N, uni10_int K, std::complex<double>* C){

    }

    void MatrixDot_gpu(std::complex<double>* A, double* B, uni10_int M, uni10_int N, uni10_int K, std::complex<double>* C){

    }

    void DiagRowMul_gpu(std::complex<double>* mat, double* diag, uni10_uint64 M, uni10_uint64 N){

    }

    void DiagColMul_gpu(std::complex<double>* mat, double* diag, uni10_uint64 M, uni10_uint64 N){

    }

    void EigDecompose_gpu(double* Kij_ori, uni10_int N, std::complex<double>* Eig, std::complex<double>* EigVec){

    }

    void SyEigDecompose_gpu(std::complex<double>* Kij, uni10_int N, double* Eig, std::complex<double>* EigVec){

    }

    void Svd_gpu(std::complex<double>* Mij_ori, uni10_int M, uni10_int N, std::complex<double>* U, double *S, std::complex<double>* vT){

    }

    void Sdd_gpu(std::complex<double>* Mij_ori, uni10_int M, uni10_int N, std::complex<double>* U, double *S, std::complex<double>* vT){

    }

    // r operator() z

    void DiagMatAddDenseMat_gpu(const double* D, const std::complex<double>* a, uni10_uint64 m, uni10_uint64 n, std::complex<double>* b){


    }

    void DiagMatSubDenseMat_gpu(const double* D, const std::complex<double>* a, uni10_uint64 m, uni10_uint64 n, std::complex<double>* b){

    }

    void DiagMatMulDenseMat_gpu(const double* D, const std::complex<double>* a, uni10_uint64 m, uni10_uint64 n, std::complex<double>* v){


    }
   
    void DenseMatAddDiagMat_gpu(const double* a, const std::complex<double>* D, uni10_uint64 m, uni10_uint64 n, std::complex<double>* b){


    }
                                                                                                                                      
    void DenseMatSubDiagMat_gpu(const double* a, const std::complex<double>* D, uni10_uint64 m, uni10_uint64 n, std::complex<double>* b){


    }
                                                                                                                                      
    void DenseMatMulDiagMat_gpu(const double* a, const std::complex<double>* D, uni10_uint64 m, uni10_uint64 n, std::complex<double>* v){

    }

    // z operator() r

    void DiagMatAddDenseMat_gpu(const std::complex<double>* D, const double* a, uni10_uint64 m, uni10_uint64 n, std::complex<double>* b){

    }

    void DiagMatSubDenseMat_gpu(const std::complex<double>* D, const double* a, uni10_uint64 m, uni10_uint64 n, std::complex<double>* b){

    }

    void DiagMatMulDenseMat_gpu(const std::complex<double>* D, const double* a, uni10_uint64 m, uni10_uint64 n, std::complex<double>* v){


    }

    void DenseMatAddDiagMat_gpu(std::complex<double>* a, const double* D, uni10_uint64 m, uni10_uint64 n){


    }
                                                                                                       
    void DenseMatSubDiagMat_gpu(std::complex<double>* a, const double* D, uni10_uint64 m, uni10_uint64 n){


    }
                                                                                                       
    void DiagMatMulDenseMat_gpu(std::complex<double>* D, const double* a, uni10_uint64 m, uni10_uint64 n){


    }
   
    void DenseMatAddDiagMat_gpu(const std::complex<double>* a, const double* D, uni10_uint64 m, uni10_uint64 n, std::complex<double>* b){


    }
                                                                                                                                       
    void DenseMatSubDiagMat_gpu(const std::complex<double>* a, const double* D, uni10_uint64 m, uni10_uint64 n, std::complex<double>* b){


    }
                                                                                                                                       
    void DenseMatMulDiagMat_gpu(const std::complex<double>* a, const double* D, uni10_uint64 m, uni10_uint64 n, std::complex<double>* v){


    }


  };/* namespace linalg_driver_internal */

};/* namespace uni10 */

