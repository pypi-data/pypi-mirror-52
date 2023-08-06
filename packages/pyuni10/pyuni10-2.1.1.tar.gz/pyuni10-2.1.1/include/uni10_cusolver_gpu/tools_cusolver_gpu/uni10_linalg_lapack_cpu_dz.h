#ifndef __UNI10_LINALG_LAPACK_CPU_DZ_H__
#define __UNI10_LINALG_LAPACK_CPU_DZ_H__

#include <limits.h>

#include "uni10_type.h"
#include "uni10_error.h"
#include "uni10_cusolver_gpu/tools_cusolver_gpu/uni10_tools_cusolver_gpu.h"
#include "uni10_cusolver_gpu/tools_cusolver_gpu/uni10_linalg_lapack_cpu_z.h"

#ifdef UNI_MKL
#include "mkl.h"
#else
#include "uni10_cusolver_gpu/tools_cusolver_gpu/uni10_lapack_wrapper_cpu.h"
#endif

namespace uni10{

  namespace linalg_driver_internal{

    //Blas
    //
    void VectorAdd_cpu(uni10_double64 a, uni10_double64* X, uni10_int incx, uni10_complex128* Y, uni10_int incy, uni10_uint64 N);   // Y = a*X + Y

    void VectorAdd_cpu(uni10_complex128* Y, uni10_double64* X, uni10_uint64 N);

    void VectorSub_cpu(uni10_complex128* Y, uni10_double64* X, uni10_uint64 N);

    void VectorMul_cpu(uni10_complex128* Y, uni10_double64* X, uni10_uint64 N);
    
    void VectorScal_cpu(uni10_double64 a, uni10_complex128* X, uni10_uint64 N);

    void VectorExp_cpu(uni10_double64 a, uni10_complex128* X, uni10_uint64 N);
 
    void MatrixDot_cpu(uni10_double64* A, uni10_complex128* B, uni10_int M, uni10_int N, uni10_int K, uni10_complex128* C);

    void MatrixDot_cpu(uni10_complex128* A, uni10_double64* B, uni10_int M, uni10_int N, uni10_int K, uni10_complex128* C);

    void DiagRowMul_cpu(uni10_complex128* mat, uni10_double64* diag, uni10_uint64 M, uni10_uint64 N);

    void DiagColMul_cpu(uni10_complex128* mat, uni10_double64* diag, uni10_uint64 M, uni10_uint64 N);

    //Lapack
    //

    //====================================================================//

    void EigDecompose_cpu(uni10_double64* Kij, uni10_int N, uni10_complex128* Eig, uni10_complex128 *EigVec);

    void SyEigDecompose_cpu(uni10_complex128* Kij, uni10_int N, uni10_double64* Eig, uni10_complex128* EigVec);

    void Svd_cpu(uni10_complex128* Mij_ori, uni10_int M, uni10_int N, uni10_complex128* U, uni10_double64 *S, uni10_complex128* vT);

    void Sdd_cpu(uni10_complex128* Mij_ori, uni10_int M, uni10_int N, uni10_complex128* U, uni10_double64 *S, uni10_complex128* vT);

    //
    // function overload for operators + - * += -= *=
    // 
    // r operator(+,-,*,+=,-=,*=) z
    void DiagMatAddDenseMat_cpu(const double* D, const uni10_complex128* a, uni10_uint64 m, uni10_uint64 n, uni10_complex128* b);

    void DiagMatSubDenseMat_cpu(const double* D, const uni10_complex128* a, uni10_uint64 m, uni10_uint64 n, uni10_complex128* b);

    void DiagMatMulDenseMat_cpu(const double* D, const uni10_complex128* a, uni10_uint64 m, uni10_uint64 n, uni10_complex128* b);
   
    void DenseMatAddDiagMat_cpu(const double* a, const uni10_complex128* D, uni10_uint64 m, uni10_uint64 n, uni10_complex128* b);

    void DenseMatSubDiagMat_cpu(const double* a, const uni10_complex128* D, uni10_uint64 m, uni10_uint64 n, uni10_complex128* b);

    void DenseMatMulDiagMat_cpu(const double* a, const uni10_complex128* D, uni10_uint64 m, uni10_uint64 n, uni10_complex128* b);

    // z operator(+,-,*,+=,-=,*=) r

    void DiagMatAddDenseMat_cpu(const uni10_complex128* D, const double* a, uni10_uint64 m, uni10_uint64 n, uni10_complex128* b);

    void DiagMatSubDenseMat_cpu(const uni10_complex128* D, const double* a, uni10_uint64 m, uni10_uint64 n, uni10_complex128* b);

    void DiagMatMulDenseMat_cpu(const uni10_complex128* D, const double* a, uni10_uint64 m, uni10_uint64 n, uni10_complex128* b);

    void DenseMatAddDiagMat_cpu(uni10_complex128* a, const double* D, uni10_uint64 m, uni10_uint64 n);

    void DenseMatSubDiagMat_cpu(uni10_complex128* a, const double* D, uni10_uint64 m, uni10_uint64 n);

    void DiagMatMulDenseMat_cpu(uni10_complex128* D, const double* a, uni10_uint64 m, uni10_uint64 n);
   
    void DenseMatAddDiagMat_cpu(const uni10_complex128* a, const double* D, uni10_uint64 m, uni10_uint64 n, uni10_complex128* b);

    void DenseMatSubDiagMat_cpu(const uni10_complex128* a, const double* D, uni10_uint64 m, uni10_uint64 n, uni10_complex128* b);

    void DenseMatMulDiagMat_cpu(const uni10_complex128* a, const double* D, uni10_uint64 m, uni10_uint64 n, uni10_complex128* b);

  };/* namespace uni10_linalg */

};/* namespace uni10 */

#endif
