#ifndef __UNI10_LINALG_LAPACK_CPU_Z_H__
#define __UNI10_LINALG_LAPACK_CPU_Z_H__

#include <limits.h>

#include "uni10_type.h"
#include "uni10_error.h"
#include "uni10_lapack_cpu/tools_lapack_cpu/uni10_tools_lapack_cpu.h"
#include "uni10_lapack_cpu/tools_lapack_cpu/uni10_linalg_lapack_cpu_dz.h"

#ifdef UNI_MKL
#include "mkl.h"
#else
#include "uni10_lapack_cpu/tools_lapack_cpu/uni10_lapack_wrapper_cpu.h"
#endif

namespace uni10{

  namespace linalg_driver_internal{

    // Blas
    //
    void VectorAdd(uni10_complex128 a, uni10_complex128* X, uni10_int incx, uni10_complex128* Y, uni10_int incy, uni10_uint64 N);   // Y = a*X + Y

    void VectorAdd(uni10_complex128* Y, uni10_complex128* X, uni10_uint64 N);// Y = Y + X

    void VectorSub(uni10_complex128* Y, uni10_complex128* X, uni10_uint64 N);// Y = Y - X

    void VectorMul(uni10_complex128* Y, uni10_complex128* X, uni10_uint64 N); // Y = Y * X, element-wise multiplication;

    void VectorScal(uni10_complex128 a, uni10_complex128* X, uni10_uint64 N);// X = a * X

    void VectorExp(uni10_complex128 a, uni10_complex128* X, uni10_uint64 N);

    uni10_complex128 VectorSum(uni10_complex128* X, uni10_uint64 N, uni10_int inc);

    uni10_double64 Norm(uni10_complex128* X, uni10_uint64 N, uni10_int inc);

    void MatrixDot(uni10_complex128* A, uni10_complex128* B, uni10_int M, uni10_int N, uni10_int K, uni10_complex128* C);

    void DiagRowMul(uni10_complex128* mat, uni10_complex128* diag, uni10_uint64 M, uni10_uint64 N);

    void DiagColMul(uni10_complex128* mat, uni10_complex128* diag, uni10_uint64 M, uni10_uint64 N);

    void Transpose(uni10_complex128* A, uni10_uint64 M, uni10_uint64 N, uni10_complex128* AT);

    void Transpose(uni10_complex128* A, uni10_uint64 M, uni10_uint64 N);

    void Dagger(uni10_complex128* A, uni10_uint64 M, uni10_uint64 N, uni10_complex128* AT);

    void Dagger(uni10_complex128* A, uni10_uint64 M, uni10_uint64 N);

    void Conjugate(uni10_complex128 *A, uni10_uint64 N, uni10_complex128 *A_conj);

    void Conjugate(uni10_complex128 *A, uni10_uint64 N);

    void Identity(uni10_complex128* A, uni10_uint64 M, uni10_uint64 N);

    // Lapack
    //
    void Svd(uni10_complex128* Mij_ori, uni10_int M, uni10_int N, uni10_complex128* U, uni10_complex128* S, uni10_complex128* vT);

    void Sdd(uni10_complex128* Mij_ori, uni10_int M, uni10_int N, uni10_complex128* U, uni10_complex128* S, uni10_complex128* vT);

    void Qr(uni10_complex128* Mij_ori, uni10_int M, uni10_int N, uni10_complex128* Q, uni10_complex128* R);

    void Rq(uni10_complex128* Mij_ori, uni10_int M, uni10_int N, uni10_complex128* R, uni10_complex128* Q);

    void Ql(uni10_complex128* Mij_ori, uni10_int M, uni10_int N, uni10_complex128* Q, uni10_complex128* L);

    void Lq(uni10_complex128* Mij_ori, uni10_int M, uni10_int N, uni10_complex128* L, uni10_complex128* Q);

    void Qdr(uni10_complex128* Mij_ori, uni10_int M, uni10_int N, uni10_complex128* Q, uni10_complex128* D, uni10_complex128* R);

    void Ldq(uni10_complex128* Mij_ori, uni10_int M, uni10_int N, uni10_complex128* L, uni10_complex128* D, uni10_complex128* Q);

    void QdrColPivot(uni10_complex128* Mij_ori, uni10_int M, uni10_int N, uni10_complex128* Q, uni10_complex128* D, uni10_complex128* R);

    void Inverse(uni10_complex128* A, uni10_int N);

    uni10_complex128 Det(uni10_complex128* A, uni10_int N);

    //=================================================================================//

    void EigDecompose(uni10_complex128* Kij, uni10_int N, uni10_complex128* Eig, uni10_complex128 *EigVec);

    //
    // function overload for operators + - * += -= *=
    // 
    void DiagMatAddDenseMat(const uni10_complex128* D, const uni10_complex128* a, uni10_uint64 m, uni10_uint64 n, uni10_complex128* b);

    void DiagMatSubDenseMat(const uni10_complex128* D, const uni10_complex128* a, uni10_uint64 m, uni10_uint64 n, uni10_complex128* b);

    void DiagMatMulDenseMat(const uni10_complex128* D, const uni10_complex128* a, uni10_uint64 m, uni10_uint64 n, uni10_complex128* b);

    void DenseMatAddDiagMat(uni10_complex128* a, const uni10_complex128* D, uni10_uint64 m, uni10_uint64 n);
                                                                                      
    void DenseMatSubDiagMat(uni10_complex128* a, const uni10_complex128* D, uni10_uint64 m, uni10_uint64 n);

    void DiagMatMulDenseMat(uni10_complex128* D, const uni10_complex128* a, uni10_uint64 m, uni10_uint64 n);
   
    void DenseMatAddDiagMat(const uni10_complex128* a, const uni10_complex128* D, uni10_uint64 m, uni10_uint64 n, uni10_complex128* b);
                                                                                                                                                    
    void DenseMatSubDiagMat(const uni10_complex128* a, const uni10_complex128* D, uni10_uint64 m, uni10_uint64 n, uni10_complex128* b);
                                                                                                                                                    
    void DenseMatMulDiagMat(const uni10_complex128* a, const uni10_complex128* D, uni10_uint64 m, uni10_uint64 n, uni10_complex128* b);

  };/* namespace uni10_linalg */

};/* namespace uni10 */

#endif
