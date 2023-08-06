#ifndef __UNI10_LINALG_HYBRID_DZ_H__
#define __UNI10_LINALG_HYBRID_DZ_H__

#include "uni10_cusolver_gpu/tools_cusolver_gpu/uni10_linalg_lapack_cpu_dz.h"
#include "uni10_cusolver_gpu/tools_cusolver_gpu/uni10_linalg_cusolver_gpu_dz.h"

namespace uni10{

  namespace linalg_driver_internal{

    //Blas
    //
    void VectorAdd(uni10_double64 a, uni10_double64* X, uni10_int incx, uni10_complex128* Y, uni10_int incy, uni10_uint64 N);   // Y = a*X + Y

    void VectorAdd(uni10_complex128* Y, uni10_double64* X, uni10_uint64 N);

    void VectorSub(uni10_complex128* Y, uni10_double64* X, uni10_uint64 N);

    void VectorMul(uni10_complex128* Y, uni10_double64* X, uni10_uint64 N);
    
    void VectorScal(uni10_double64 a, uni10_complex128* X, uni10_uint64 N);

    void VectorExp(uni10_double64 a, uni10_complex128* X, uni10_uint64 N);
 
    void MatrixDot(uni10_double64* A, uni10_complex128* B, uni10_int M, uni10_int N, uni10_int K, uni10_complex128* C);

    void MatrixDot(uni10_complex128* A, uni10_double64* B, uni10_int M, uni10_int N, uni10_int K, uni10_complex128* C);

    void DiagRowMul(uni10_complex128* mat, uni10_double64* diag, uni10_uint64 M, uni10_uint64 N);

    void DiagColMul(uni10_complex128* mat, uni10_double64* diag, uni10_uint64 M, uni10_uint64 N);

    //Lapack
    //

    //====================================================================//

    void EigDecompose(uni10_double64* Kij, uni10_int N, uni10_complex128* Eig, uni10_complex128 *EigVec);

    void SyEigDecompose(uni10_complex128* Kij, uni10_int N, uni10_double64* Eig, uni10_complex128* EigVec);

    void Svd(uni10_complex128* Mij_ori, uni10_int M, uni10_int N, uni10_complex128* U, uni10_double64 *S, uni10_complex128* vT);

    void Sdd(uni10_complex128* Mij_ori, uni10_int M, uni10_int N, uni10_complex128* U, uni10_double64 *S, uni10_complex128* vT);

    //
    // function overload for operators + - * += -= *=
    // 
    // r operator(+,-,*,+=,-=,*=) z
    void DiagMatAddDenseMat(const double* D, const uni10_complex128* a, uni10_uint64 m, uni10_uint64 n, uni10_complex128* b);

    void DiagMatSubDenseMat(const double* D, const uni10_complex128* a, uni10_uint64 m, uni10_uint64 n, uni10_complex128* b);

    void DiagMatMulDenseMat(const double* D, const uni10_complex128* a, uni10_uint64 m, uni10_uint64 n, uni10_complex128* b);
   
    void DenseMatAddDiagMat(const double* a, const uni10_complex128* D, uni10_uint64 m, uni10_uint64 n, uni10_complex128* b);
                                                                                                                                      
    void DenseMatSubDiagMat(const double* a, const uni10_complex128* D, uni10_uint64 m, uni10_uint64 n, uni10_complex128* b);
                                                                                                                                      
    void DenseMatMulDiagMat(const double* a, const uni10_complex128* D, uni10_uint64 m, uni10_uint64 n, uni10_complex128* b);

    // z operator(+,-,*,+=,-=,*=) r

    void DiagMatAddDenseMat(const uni10_complex128* D, const double* a, uni10_uint64 m, uni10_uint64 n, uni10_complex128* b);

    void DiagMatSubDenseMat(const uni10_complex128* D, const double* a, uni10_uint64 m, uni10_uint64 n, uni10_complex128* b);

    void DiagMatMulDenseMat(const uni10_complex128* D, const double* a, uni10_uint64 m, uni10_uint64 n, uni10_complex128* b);

    void DenseMatAddDiagMat(uni10_complex128* a, const double* D, uni10_uint64 m, uni10_uint64 n);
                                                                                                       
    void DenseMatSubDiagMat(uni10_complex128* a, const double* D, uni10_uint64 m, uni10_uint64 n);
                                                                                                       
    void DiagMatMulDenseMat(uni10_complex128* D, const double* a, uni10_uint64 m, uni10_uint64 n);
   
    void DenseMatAddDiagMat(const uni10_complex128* a, const double* D, uni10_uint64 m, uni10_uint64 n, uni10_complex128* b);
                                                                                                                                       
    void DenseMatSubDiagMat(const uni10_complex128* a, const double* D, uni10_uint64 m, uni10_uint64 n, uni10_complex128* b);
                                                                                                                                       
    void DenseMatMulDiagMat(const uni10_complex128* a, const double* D, uni10_uint64 m, uni10_uint64 n, uni10_complex128* b);

  };/* namespace uni10_linalg */

};/* namespace uni10 */

#endif
