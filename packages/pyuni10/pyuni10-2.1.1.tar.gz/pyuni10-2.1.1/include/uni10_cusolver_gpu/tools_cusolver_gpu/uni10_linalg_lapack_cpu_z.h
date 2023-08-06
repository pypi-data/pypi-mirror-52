#ifndef __UNI10_LINALG_LAPACK_CPU_Z_H__
#define __UNI10_LINALG_LAPACK_CPU_Z_H__

#include <limits.h>

#include "uni10_type.h"
#include "uni10_error.h"
#include "uni10_cusolver_gpu/tools_cusolver_gpu/uni10_tools_cusolver_gpu.h"
#include "uni10_cusolver_gpu/tools_cusolver_gpu/uni10_linalg_lapack_cpu_dz.h"

#ifdef UNI_MKL
#include "mkl.h"
#else
#include "uni10_cusolver_gpu/tools_cusolver_gpu/uni10_lapack_wrapper_cpu.h"
#endif

namespace uni10{

  namespace linalg_driver_internal{

    // Blas
    //
    void VectorAdd_cpu(uni10_complex128 a, uni10_complex128* X, uni10_int incx, uni10_complex128* Y, uni10_int incy, uni10_uint64 N);   // Y = a*X + Y

    void VectorAdd_cpu(uni10_complex128* Y, uni10_complex128* X, uni10_uint64 N);// Y = Y + X

    void VectorSub_cpu(uni10_complex128* Y, uni10_complex128* X, uni10_uint64 N);// Y = Y - X

    void VectorMul_cpu(uni10_complex128* Y, uni10_complex128* X, uni10_uint64 N); // Y = Y * X, element-wise multiplication;

    void VectorScal_cpu(uni10_complex128 a, uni10_complex128* X, uni10_uint64 N);// X = a * X

    void VectorExp_cpu(uni10_complex128 a, uni10_complex128* X, uni10_uint64 N);

    uni10_complex128 VectorSum_cpu(uni10_complex128* X, uni10_uint64 N, uni10_int inc);

    uni10_double64 Norm_cpu(uni10_complex128* X, uni10_uint64 N, uni10_int inc);

    void MatrixDot_cpu(uni10_complex128* A, uni10_complex128* B, uni10_int M, uni10_int N, uni10_int K, uni10_complex128* C);

    void DiagRowMul_cpu(uni10_complex128* mat, uni10_complex128* diag, uni10_uint64 M, uni10_uint64 N);

    void DiagColMul_cpu(uni10_complex128* mat, uni10_complex128* diag, uni10_uint64 M, uni10_uint64 N);

    void Transpose_cpu(uni10_complex128* A, uni10_uint64 M, uni10_uint64 N, uni10_complex128* AT);

    void Transpose_cpu(uni10_complex128* A, uni10_uint64 M, uni10_uint64 N);

    void Dagger_cpu(uni10_complex128* A, uni10_uint64 M, uni10_uint64 N, uni10_complex128* AT);

    void Dagger_cpu(uni10_complex128* A, uni10_uint64 M, uni10_uint64 N);

    void Conjugate_cpu(uni10_complex128 *A, uni10_uint64 N, uni10_complex128 *A_conj);

    void Conjugate_cpu(uni10_complex128 *A, uni10_uint64 N);

    void Identity_cpu(uni10_complex128* A, uni10_uint64 M, uni10_uint64 N);

    // Lapack
    //
    void Svd_cpu(uni10_complex128* Mij_ori, uni10_int M, uni10_int N, uni10_complex128* U, uni10_complex128* S, uni10_complex128* vT);

    void Sdd_cpu(uni10_complex128* Mij_ori, uni10_int M, uni10_int N, uni10_complex128* U, uni10_complex128* S, uni10_complex128* vT);

    void Qr_cpu(uni10_complex128* Mij_ori, uni10_int M, uni10_int N, uni10_complex128* Q, uni10_complex128* R);

    void Rq_cpu(uni10_complex128* Mij_ori, uni10_int M, uni10_int N, uni10_complex128* R, uni10_complex128* Q);

    void Ql_cpu(uni10_complex128* Mij_ori, uni10_int M, uni10_int N, uni10_complex128* Q, uni10_complex128* L);

    void Lq_cpu(uni10_complex128* Mij_ori, uni10_int M, uni10_int N, uni10_complex128* L, uni10_complex128* Q);

    void Qdr_cpu(uni10_complex128* Mij_ori, uni10_int M, uni10_int N, uni10_complex128* Q, uni10_complex128* D, uni10_complex128* R);

    void Ldq_cpu(uni10_complex128* Mij_ori, uni10_int M, uni10_int N, uni10_complex128* L, uni10_complex128* D, uni10_complex128* Q);

    void QdrColPivot_cpu(uni10_complex128* Mij_ori, uni10_int M, uni10_int N, uni10_complex128* Q, uni10_complex128* D, uni10_complex128* R);

    void Inverse_cpu(uni10_complex128* A, uni10_int N);

    uni10_complex128 Det_cpu(uni10_complex128* A, uni10_int N);

    //=================================================================================//

    void EigDecompose_cpu(uni10_complex128* Kij, uni10_int N, uni10_complex128* Eig, uni10_complex128 *EigVec);

    //
    // function overload for operators + - * += -= *=
    // 
    void DiagMatAddDenseMat_cpu(const uni10_complex128* D, const uni10_complex128* a, uni10_uint64 m, uni10_uint64 n, uni10_complex128* b);

    void DiagMatSubDenseMat_cpu(const uni10_complex128* D, const uni10_complex128* a, uni10_uint64 m, uni10_uint64 n, uni10_complex128* b);

    void DiagMatMulDenseMat_cpu(const uni10_complex128* D, const uni10_complex128* a, uni10_uint64 m, uni10_uint64 n, uni10_complex128* b);

    void DenseMatAddDiagMat_cpu(uni10_complex128* a, const uni10_complex128* D, uni10_uint64 m, uni10_uint64 n);

    void DenseMatSubDiagMat_cpu(uni10_complex128* a, const uni10_complex128* D, uni10_uint64 m, uni10_uint64 n);

    void DiagMatMulDenseMat_cpu(uni10_complex128* D, const uni10_complex128* a, uni10_uint64 m, uni10_uint64 n);
   
    void DenseMatAddDiagMat_cpu(const uni10_complex128* a, const uni10_complex128* D, uni10_uint64 m, uni10_uint64 n, uni10_complex128* b);

    void DenseMatSubDiagMat_cpu(const uni10_complex128* a, const uni10_complex128* D, uni10_uint64 m, uni10_uint64 n, uni10_complex128* b);

    void DenseMatMulDiagMat_cpu(const uni10_complex128* a, const uni10_complex128* D, uni10_uint64 m, uni10_uint64 n, uni10_complex128* b);


  };/* namespace uni10_linalg */

};/* namespace uni10 */

#endif
