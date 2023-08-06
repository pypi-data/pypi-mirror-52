#ifndef __UNI10_LINALG_CUSOLVER_GPU_D_H__
#define __UNI10_LINALG_CUSOLVER_GPU_D_H__

#include <limits.h>

#include "uni10_type.h"
#include "uni10_error.h"
#include "uni10_cusolver_gpu/tools_cusolver_gpu/uni10_tools_cusolver_gpu.h"
#include "uni10_cusolver_gpu/tools_cusolver_gpu/cuda_kernel_funcs/uni10_kernel_gpu.h"
#include "uni10_env_info/uni10_cusolver_gpu/uni10_env_info_cusolver_gpu.h"
namespace uni10{

  namespace linalg_driver_internal{

    // Blas
    //
    void VectorAdd_gpu(uni10_double64 a, uni10_double64* X, uni10_int incx, uni10_double64* Y, uni10_int incy, uni10_uint64 N);   // Y = a*X + Y

    void VectorAdd_gpu(uni10_double64* Y, uni10_double64* X, uni10_uint64 N);   // Y = Y + X

    void VectorSub_gpu(uni10_double64* Y, uni10_double64* X, uni10_uint64 N);   // Y = Y - X

    void VectorMul_gpu(uni10_double64* Y, uni10_double64* X, uni10_uint64 N);   // Y = Y * X, element-wise multiplication;

    void VectorScal_gpu(uni10_double64 a, uni10_double64* X, uni10_uint64 N);  // X = a * X

    void VectorExp_gpu(uni10_double64 a, uni10_double64* X, uni10_uint64 N);

    uni10_double64 VectorSum_gpu(uni10_double64* X, uni10_uint64 N, uni10_int inc);

    uni10_double64 Norm_gpu(uni10_double64* X, uni10_uint64 N, uni10_int inc);

    void MatrixDot_gpu(uni10_double64* A, uni10_double64* B, uni10_int M, uni10_int N, uni10_int K, uni10_double64* C);

    void DiagRowMul_gpu(uni10_double64* mat, uni10_double64* diag, uni10_uint64 M, uni10_uint64 N);

    void DiagColMul_gpu(uni10_double64* mat, uni10_double64* diag, uni10_uint64 M, uni10_uint64 N);

    void Transpose_gpu(uni10_double64* A, uni10_uint64 M, uni10_uint64 N, uni10_double64* AT);

    void Transpose_gpu(uni10_double64* A, uni10_uint64 M, uni10_uint64 N);

    void Dagger_gpu(uni10_double64* A, uni10_uint64 M, uni10_uint64 N, uni10_double64 *AT);

    void Dagger_gpu(uni10_double64* A, uni10_uint64 M, uni10_uint64 N);

    void Identity_gpu(uni10_double64* A, uni10_uint64 M, uni10_uint64 N);

    void SyTriMatEigDecompose_gpu(uni10_double64* D, uni10_double64* E, uni10_int N,
        uni10_double64* z=NULL, uni10_int LDZ=1);

    // Lapack
    //
    /*Generate a set of row Vectors which form a othonormal basis
     *For the incoming Matrix "elem", the number of row <= the number of column, M <= N
     */
    void Svd_gpu(uni10_double64* Mij_ori, uni10_int M, uni10_int N, uni10_double64* U, uni10_double64* S, uni10_double64* vT);

    void Sdd_gpu(uni10_double64* Mij_ori, uni10_int M, uni10_int N, uni10_double64* U, uni10_double64* S, uni10_double64* vT);

    void Qr_gpu(uni10_double64* Mij_ori, uni10_int M, uni10_int N, uni10_double64* Q, uni10_double64* R);

    void Rq_gpu(uni10_double64* Mij_ori, uni10_int M, uni10_int N, uni10_double64* R, uni10_double64* Q);

    void Ql_gpu(uni10_double64* Mij_ori, uni10_int M, uni10_int N, uni10_double64* Q, uni10_double64* L);

    void Lq_gpu(uni10_double64* Mij_ori, uni10_int M, uni10_int N, uni10_double64* L, uni10_double64* Q);

    void Qdr_gpu(uni10_double64* Mij_ori, uni10_int M, uni10_int N, uni10_double64* Q, uni10_double64* D, uni10_double64* R);

    void Ldq_gpu(uni10_double64* Mij_ori, uni10_int M, uni10_int N, uni10_double64* L, uni10_double64* D, uni10_double64* Q);

    void QdrColPivot_gpu(uni10_double64* Mij_ori, uni10_int M, uni10_int N, uni10_double64* Q, uni10_double64* D, uni10_double64* R);

    void Inverse_gpu(uni10_double64* A, uni10_int N);

    uni10_double64 Det_gpu(uni10_double64* A, uni10_int N);

    //=====================================================================================//
    //
    void reshapeElem_gpu(uni10_double64* elem, uni10_uint64* transOffset);

    void SyEigDecompose_gpu(uni10_double64* Kij, uni10_int N, uni10_double64* Eig, uni10_double64* EigVec);

    //
    // function overload for operator + - * += -= *=
    //
    void DiagMatAddDenseMat_gpu(const double* D, const double* a, uni10_uint64 m, uni10_uint64 n, double* b);

    void DiagMatSubDenseMat_gpu(const double* D, const double* a, uni10_uint64 m, uni10_uint64 n, double* b);

    void DiagMatMulDenseMat_gpu(const double* D, const double* a, uni10_uint64 m, uni10_uint64 n, double* b);

    void DenseMatAddDiagMat_gpu(double* a, const double* D, uni10_uint64 m, uni10_uint64 n);

    void DenseMatSubDiagMat_gpu(double* a, const double* D, uni10_uint64 m, uni10_uint64 n);

    void DiagMatMulDenseMat_gpu(double* D, const double* a, uni10_uint64 m, uni10_uint64 n);

    void DenseMatAddDiagMat_gpu(const double* a, const double* D, uni10_uint64 m, uni10_uint64 n, double* b);

    void DenseMatSubDiagMat_gpu(const double* a, const double* D, uni10_uint64 m, uni10_uint64 n, double* b);

    void DenseMatMulDiagMat_gpu(const double* a, const double* D, uni10_uint64 m, uni10_uint64 n, double* b);

  };/* namespace uni10_linalg */

};/* namespace uni10 */

#endif
