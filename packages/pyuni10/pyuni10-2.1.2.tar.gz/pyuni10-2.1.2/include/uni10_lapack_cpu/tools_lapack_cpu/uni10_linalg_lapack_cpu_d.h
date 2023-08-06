#ifndef __UNI10_LINALG_LAPACK_CPU_D_H__
#define __UNI10_LINALG_LAPACK_CPU_D_H__

#include <limits.h>

#include "uni10_type.h"
#include "uni10_error.h"
#include "uni10_lapack_cpu/tools_lapack_cpu/uni10_tools_lapack_cpu.h"

#ifdef UNI_MKL
#include "mkl.h"
#else
#include "uni10_lapack_cpu/tools_lapack_cpu/uni10_lapack_wrapper_cpu.h"
#endif

namespace uni10{

  namespace linalg_driver_internal{

    // Blas 
    //
    void VectorAdd(uni10_double64 a, uni10_double64* X, uni10_int incx, uni10_double64* Y, uni10_int incy, uni10_uint64 N);   // Y = a*X + Y

    void VectorAdd(uni10_double64* Y, uni10_double64* X, uni10_uint64 N);   // Y = Y + X

    void VectorSub(uni10_double64* Y, uni10_double64* X, uni10_uint64 N);   // Y = Y - X

    void VectorMul(uni10_double64* Y, uni10_double64* X, uni10_uint64 N);   // Y = Y * X, element-wise multiplication;

    void VectorScal(uni10_double64 a, uni10_double64* X, uni10_uint64 N);  // X = a * X

    void VectorExp(uni10_double64 a, uni10_double64* X, uni10_uint64 N);

    uni10_double64 VectorSum(uni10_double64* X, uni10_uint64 N, uni10_int inc);

    uni10_double64 Norm(uni10_double64* X, uni10_uint64 N, uni10_int inc);

    void MatrixDot(uni10_double64* A, uni10_double64* B, uni10_int M, uni10_int N, uni10_int K, uni10_double64* C);

    void DiagRowMul(uni10_double64* mat, uni10_double64* diag, uni10_uint64 M, uni10_uint64 N);

    void DiagColMul(uni10_double64* mat, uni10_double64* diag, uni10_uint64 M, uni10_uint64 N);

    void Transpose(uni10_double64* A, uni10_uint64 M, uni10_uint64 N, uni10_double64* AT);

    void Transpose(uni10_double64* A, uni10_uint64 M, uni10_uint64 N);

    void Dagger(uni10_double64* A, uni10_uint64 M, uni10_uint64 N, uni10_double64 *AT);

    void Dagger(uni10_double64* A, uni10_uint64 M, uni10_uint64 N);

    void Identity(uni10_double64* A, uni10_uint64 M, uni10_uint64 N);

    void SyTriMatEigDecompose(uni10_double64* D, uni10_double64* E, uni10_int N, 
        uni10_double64* z=NULL, uni10_int LDZ=1);

    // Lapack
    //
    /*Generate a set of row vectors which form a othonormal basis
     *For the incoming matrix "elem", the number of row <= the number of column, M <= N
     */
    void Svd(uni10_double64* Mij_ori, uni10_int M, uni10_int N, uni10_double64* U, uni10_double64* S, uni10_double64* vT);

    void Sdd(uni10_double64* Mij_ori, uni10_int M, uni10_int N, uni10_double64* U, uni10_double64* S, uni10_double64* vT);

    void Qr(uni10_double64* Mij_ori, uni10_int M, uni10_int N, uni10_double64* Q, uni10_double64* R);

    void Rq(uni10_double64* Mij_ori, uni10_int M, uni10_int N, uni10_double64* R, uni10_double64* Q);

    void Ql(uni10_double64* Mij_ori, uni10_int M, uni10_int N, uni10_double64* Q, uni10_double64* L);

    void Lq(uni10_double64* Mij_ori, uni10_int M, uni10_int N, uni10_double64* L, uni10_double64* Q);

    void Qdr(uni10_double64* Mij_ori, uni10_int M, uni10_int N, uni10_double64* Q, uni10_double64* D, uni10_double64* R);

    void Ldq(uni10_double64* Mij_ori, uni10_int M, uni10_int N, uni10_double64* L, uni10_double64* D, uni10_double64* Q);

    void QdrColPivot(uni10_double64* Mij_ori, uni10_int M, uni10_int N, uni10_double64* Q, uni10_double64* D, uni10_double64* R);

    void Inverse(uni10_double64* A, uni10_int N);

    uni10_double64 Det(uni10_double64* A, uni10_int N);

    //=====================================================================================//
    //
    void reshapeElem(uni10_double64* elem, uni10_uint64* transOffset);

    void SyEigDecompose(uni10_double64* Kij, uni10_int N, uni10_double64* Eig, uni10_double64* EigVec);

    //
    // function overload for operator + - * += -= *= 
    //
    void DiagMatAddDenseMat(const double* D, const double* a, uni10_uint64 m, uni10_uint64 n, double* b);

    void DiagMatSubDenseMat(const double* D, const double* a, uni10_uint64 m, uni10_uint64 n, double* b);

    void DiagMatMulDenseMat(const double* D, const double* a, uni10_uint64 m, uni10_uint64 n, double* b);

    void DenseMatAddDiagMat(double* a, const double* D, uni10_uint64 m, uni10_uint64 n);
                                                                                         
    void DenseMatSubDiagMat(double* a, const double* D, uni10_uint64 m, uni10_uint64 n);

    void DiagMatMulDenseMat(double* D, const double* a, uni10_uint64 m, uni10_uint64 n);
                                                                                         
    void DenseMatAddDiagMat(const double* a, const double* D, uni10_uint64 m, uni10_uint64 n, double* b);

    void DenseMatSubDiagMat(const double* a, const double* D, uni10_uint64 m, uni10_uint64 n, double* b);

    void DenseMatMulDiagMat(const double* a, const double* D, uni10_uint64 m, uni10_uint64 n, double* b);

  };/* namespace uni10_linalg */

};/* namespace uni10 */

#endif
