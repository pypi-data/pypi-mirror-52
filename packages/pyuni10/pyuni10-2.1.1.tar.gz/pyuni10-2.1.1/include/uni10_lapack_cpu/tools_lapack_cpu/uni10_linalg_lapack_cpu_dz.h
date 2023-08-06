#ifndef __UNI10_LINALG_LAPACK_CPU_DZ_H__
#define __UNI10_LINALG_LAPACK_CPU_DZ_H__

#include <limits.h>

#include "uni10_type.h"
#include "uni10_error.h"
#include "uni10_lapack_cpu/tools_lapack_cpu/uni10_tools_lapack_cpu.h"
#include "uni10_lapack_cpu/tools_lapack_cpu/uni10_linalg_lapack_cpu_z.h"

#ifdef UNI_MKL
#include "mkl.h"
#else
#include "uni10_lapack_cpu/tools_lapack_cpu/uni10_lapack_wrapper_cpu.h"
#endif

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
    void DiagMatAddDenseMat(const double* D, const std::complex<double>* a, uni10_uint64 m, uni10_uint64 n, std::complex<double>* b);

    void DiagMatSubDenseMat(const double* D, const std::complex<double>* a, uni10_uint64 m, uni10_uint64 n, std::complex<double>* b);

    void DiagMatMulDenseMat(const double* D, const std::complex<double>* a, uni10_uint64 m, uni10_uint64 n, std::complex<double>* b);
   
    void DenseMatAddDiagMat(const double* a, const std::complex<double>* D, uni10_uint64 m, uni10_uint64 n, std::complex<double>* b);
                                                                                                                                      
    void DenseMatSubDiagMat(const double* a, const std::complex<double>* D, uni10_uint64 m, uni10_uint64 n, std::complex<double>* b);
                                                                                                                                      
    void DenseMatMulDiagMat(const double* a, const std::complex<double>* D, uni10_uint64 m, uni10_uint64 n, std::complex<double>* b);

    // z operator(+,-,*,+=,-=,*=) r

    void DiagMatAddDenseMat(const std::complex<double>* D, const double* a, uni10_uint64 m, uni10_uint64 n, std::complex<double>* b);

    void DiagMatSubDenseMat(const std::complex<double>* D, const double* a, uni10_uint64 m, uni10_uint64 n, std::complex<double>* b);

    void DiagMatMulDenseMat(const std::complex<double>* D, const double* a, uni10_uint64 m, uni10_uint64 n, std::complex<double>* b);

    void DenseMatAddDiagMat(std::complex<double>* a, const double* D, uni10_uint64 m, uni10_uint64 n);
                                                                                                       
    void DenseMatSubDiagMat(std::complex<double>* a, const double* D, uni10_uint64 m, uni10_uint64 n);
                                                                                                       
    void DiagMatMulDenseMat(std::complex<double>* D, const double* a, uni10_uint64 m, uni10_uint64 n);
   
    void DenseMatAddDiagMat(const std::complex<double>* a, const double* D, uni10_uint64 m, uni10_uint64 n, std::complex<double>* b);
                                                                                                                                       
    void DenseMatSubDiagMat(const std::complex<double>* a, const double* D, uni10_uint64 m, uni10_uint64 n, std::complex<double>* b);
                                                                                                                                       
    void DenseMatMulDiagMat(const std::complex<double>* a, const double* D, uni10_uint64 m, uni10_uint64 n, std::complex<double>* b);

  };/* namespace uni10_linalg */

};/* namespace uni10 */

#endif
