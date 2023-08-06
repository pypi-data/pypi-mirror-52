#ifndef __UNI10_LINALG_CUSOLVER_GPU_Z_H__
#define __UNI10_LINALG_CUSOLVER_GPU_Z_H__

#include <limits.h>

#include "uni10_type.h"
#include "uni10_error.h"
#include "uni10_cusolver_gpu/tools_cusolver_gpu/uni10_tools_cusolver_gpu.h"
#include "uni10_cusolver_gpu/tools_cusolver_gpu/uni10_linalg_cusolver_gpu_dz.h"

namespace uni10{

  namespace linalg_driver_internal{

    // Blas
    //
    void VectorAdd_gpu(uni10_complex128 a, uni10_complex128* X, uni10_int incx, uni10_complex128* Y, uni10_int incy, uni10_uint64 N);   // Y = a*X + Y

    void VectorAdd_gpu(uni10_complex128* Y, uni10_complex128* X, uni10_uint64 N);// Y = Y + X

    void VectorSub_gpu(uni10_complex128* Y, uni10_complex128* X, uni10_uint64 N);// Y = Y - X

    void VectorMul_gpu(uni10_complex128* Y, uni10_complex128* X, uni10_uint64 N); // Y = Y * X, element-wise multiplication;

    void VectorScal_gpu(uni10_complex128 a, uni10_complex128* X, uni10_uint64 N);// X = a * X

    void VectorExp_gpu(uni10_complex128 a, uni10_complex128* X, uni10_uint64 N);

    uni10_complex128 VectorSum_gpu(uni10_complex128* X, uni10_uint64 N, uni10_int inc);

    uni10_double64 Norm_gpu(uni10_complex128* X, uni10_uint64 N, uni10_int inc);

    void MatrixDot_gpu(uni10_complex128* A, uni10_complex128* B, uni10_int M, uni10_int N, uni10_int K, uni10_complex128* C);

    void DiagRowMul_gpu(uni10_complex128* mat, uni10_complex128* diag, uni10_uint64 M, uni10_uint64 N);

    void DiagColMul_gpu(uni10_complex128* mat, uni10_complex128* diag, uni10_uint64 M, uni10_uint64 N);

    void Transpose_gpu(uni10_complex128* A, uni10_uint64 M, uni10_uint64 N, uni10_complex128* AT);

    void Transpose_gpu(uni10_complex128* A, uni10_uint64 M, uni10_uint64 N);

    void Dagger_gpu(uni10_complex128* A, uni10_uint64 M, uni10_uint64 N, uni10_complex128* AT);

    void Dagger_gpu(uni10_complex128* A, uni10_uint64 M, uni10_uint64 N);

    void Conjugate_gpu(uni10_complex128 *A, uni10_uint64 N, uni10_complex128 *A_conj);

    void Conjugate_gpu(uni10_complex128 *A, uni10_uint64 N);

    void Identity_gpu(uni10_complex128* A, uni10_uint64 M, uni10_uint64 N);

    // Lapack
    //
    void Svd_gpu(uni10_complex128* Mij_ori, uni10_int M, uni10_int N, uni10_complex128* U, uni10_complex128* S, uni10_complex128* vT);

    void Sdd_gpu(uni10_complex128* Mij_ori, uni10_int M, uni10_int N, uni10_complex128* U, uni10_complex128* S, uni10_complex128* vT);

    void Qr_gpu(uni10_complex128* Mij_ori, uni10_int M, uni10_int N, uni10_complex128* Q, uni10_complex128* R);

    void Rq_gpu(uni10_complex128* Mij_ori, uni10_int M, uni10_int N, uni10_complex128* R, uni10_complex128* Q);

    void Ql_gpu(uni10_complex128* Mij_ori, uni10_int M, uni10_int N, uni10_complex128* Q, uni10_complex128* L);

    void Lq_gpu(uni10_complex128* Mij_ori, uni10_int M, uni10_int N, uni10_complex128* L, uni10_complex128* Q);

    void Qdr_gpu(uni10_complex128* Mij_ori, uni10_int M, uni10_int N, uni10_complex128* Q, uni10_complex128* D, uni10_complex128* R);

    void Ldq_gpu(uni10_complex128* Mij_ori, uni10_int M, uni10_int N, uni10_complex128* L, uni10_complex128* D, uni10_complex128* Q);

    void QdrColPivot_gpu(uni10_complex128* Mij_ori, uni10_int M, uni10_int N, uni10_complex128* Q, uni10_complex128* D, uni10_complex128* R);

    void Inverse_gpu(uni10_complex128* A, uni10_int N);

    uni10_complex128 Det_gpu(uni10_complex128* A, uni10_int N);

    //=================================================================================//

    void EigDecompose_gpu(uni10_complex128* Kij, uni10_int N, uni10_complex128* Eig, uni10_complex128 *EigVec);

    //
    // function overload for operators + - * += -= *=
    // 
    void DiagMatAddDenseMat_gpu(const uni10_complex128* D, const uni10_complex128* a, uni10_uint64 m, uni10_uint64 n, uni10_complex128* b);

    void DiagMatSubDenseMat_gpu(const uni10_complex128* D, const uni10_complex128* a, uni10_uint64 m, uni10_uint64 n, uni10_complex128* b);

    void DiagMatMulDenseMat_gpu(const uni10_complex128* D, const uni10_complex128* a, uni10_uint64 m, uni10_uint64 n, uni10_complex128* b);

    void DenseMatAddDiagMat_gpu(uni10_complex128* a, const uni10_complex128* D, uni10_uint64 m, uni10_uint64 n);

    void DenseMatSubDiagMat_gpu(uni10_complex128* a, const uni10_complex128* D, uni10_uint64 m, uni10_uint64 n);

    void DiagMatMulDenseMat_gpu(uni10_complex128* D, const uni10_complex128* a, uni10_uint64 m, uni10_uint64 n);
   
    void DenseMatAddDiagMat_gpu(const uni10_complex128* a, const uni10_complex128* D, uni10_uint64 m, uni10_uint64 n, uni10_complex128* b);

    void DenseMatSubDiagMat_gpu(const uni10_complex128* a, const uni10_complex128* D, uni10_uint64 m, uni10_uint64 n, uni10_complex128* b);

    void DenseMatMulDiagMat_gpu(const uni10_complex128* a, const uni10_complex128* D, uni10_uint64 m, uni10_uint64 n, uni10_complex128* b);

  };/* namespace uni10_linalg */

};/* namespace uni10 */

#endif
