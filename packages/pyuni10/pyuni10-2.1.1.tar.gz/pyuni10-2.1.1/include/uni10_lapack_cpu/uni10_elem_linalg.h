#ifndef __UNI10_ELEM_LINALG_LAPACK_CPU_H__
#define __UNI10_ELEM_LINALG_LAPACK_CPU_H__

#include "uni10_type.h"
#include "uni10_lapack_cpu/uni10_elem_lapack_cpu.h"
#include "uni10_lapack_cpu/tools_lapack_cpu/uni10_tools_lapack_cpu.h"
#include "uni10_lapack_cpu/tools_lapack_cpu/uni10_linalg_lapack_cpu_d.h"
#include "uni10_lapack_cpu/tools_lapack_cpu/uni10_linalg_lapack_cpu_dz.h"
#include "uni10_lapack_cpu/tools_lapack_cpu/uni10_linalg_lapack_cpu_z.h"
#include "uni10_lapack_cpu/tools_lapack_cpu/uni10_resize_lapack_cpu.h"

typedef uni10::UniElemLapackCpu<uni10_double64>     UniElemDouble;
typedef uni10::UniElemLapackCpu<uni10_complex128>   UniElemComplex;

namespace uni10{

  namespace linalg_unielem_internal{

    // Blas 
    //
    // UNI10_DOUBLE64
    void VectorScal(uni10_double64* a, UniElemDouble* X, uni10_uint64* N);   // X = a * X

    void VectorAdd(UniElemDouble* Y, const UniElemDouble* X, const uni10_uint64* N);

    void MatrixAdd(UniElemDouble* A, uni10_bool* Aisdag, const UniElemDouble* B, uni10_const_bool* Bisdiag, 
        const uni10_uint64* M, const uni10_uint64* N );

    void MatrixAdd(const UniElemDouble* A, uni10_const_bool* Aisdag, const UniElemDouble* B, uni10_const_bool* Bisdiag, 
        const uni10_uint64* M, const uni10_uint64* N, UniElemDouble* C);

    void VectorSub(UniElemDouble* Y, const UniElemDouble* X, const uni10_uint64* N);

    void MatrixSub(UniElemDouble* A, uni10_bool* Aisdag, const UniElemDouble* B, uni10_const_bool* Bisdiag, 
        const uni10_uint64* M, const uni10_uint64* N );

    void MatrixSub(const UniElemDouble* A, uni10_const_bool* Aisdag, const UniElemDouble* B, uni10_const_bool* Bisdiag, 
        const uni10_uint64* M, const uni10_uint64* N, UniElemDouble* C);

    void VectorMul(UniElemDouble* Y, const UniElemDouble* X, const uni10_uint64* N);   // Y = Y * X, element-wise multiplication;

    void MatrixMul(UniElemDouble* A, uni10_bool* Aisdag, const UniElemDouble* B, uni10_const_bool* Bisdiag, 
        const uni10_uint64* M, const uni10_uint64* N );

    void MatrixMul(const UniElemDouble* A, uni10_const_bool* Aisdag, const UniElemDouble* B, uni10_const_bool* Bisdiag, 
        const uni10_uint64* M, const uni10_uint64* N, UniElemDouble* C);

    void Conjugate(const UniElemDouble* A, const uni10_uint64* N, UniElemDouble* A_conj);

    void Conjugate(UniElemDouble* A, uni10_uint64* N);

    void Dagger(const UniElemDouble* A, const uni10_uint64* M, const uni10_uint64* N, UniElemDouble* AT);

    void Dagger(UniElemDouble* A, uni10_uint64* M, uni10_uint64* N);

    uni10_double64 Det(const UniElemDouble* A, const uni10_uint64* N, uni10_const_bool* isdiag);

    void Dot(const UniElemDouble* A, uni10_const_bool* Aisdag, const UniElemDouble* B, uni10_const_bool* Bisdiag, 
        const uni10_uint64* M, const uni10_uint64* N, const uni10_uint64* K, UniElemDouble* C);

    void VectorExp(uni10_double64* a, UniElemDouble* X, uni10_uint64* N);

    void Inverse(const UniElemDouble* A, const uni10_uint64* N, uni10_const_bool* isdiag);

    uni10_double64 Norm(const UniElemDouble* X, const uni10_uint64* N, uni10_int32* inc);

    uni10_double64 VectorSum (const UniElemDouble* X, const uni10_uint64* N, uni10_int32* inc);

    void Ldq(const UniElemDouble* Mij_ori, uni10_const_bool* isdiag, const uni10_uint64* M, const uni10_uint64* N, 
        UniElemDouble* L, UniElemDouble* D, UniElemDouble* Q);

    void Lq(const UniElemDouble* Mij_ori, uni10_const_bool* isdiag, const uni10_uint64* M, const uni10_uint64* N, 
        UniElemDouble* L, UniElemDouble* Q);

    void QdrColPivot(const UniElemDouble* Mij_ori, uni10_const_bool* isdiag, const uni10_uint64* M, const uni10_uint64* N, 
        UniElemDouble* Q, UniElemDouble* D, UniElemDouble* R);

    void Qdr(const UniElemDouble* Mij_ori, uni10_const_bool* isdiag, const uni10_uint64* M, const uni10_uint64* N, 
        UniElemDouble* Q, UniElemDouble* D, UniElemDouble* R);

    void Qr(const UniElemDouble* Mij_ori, uni10_const_bool* isdiag, const uni10_uint64* M, const uni10_uint64* N, 
        UniElemDouble* Q, UniElemDouble* R);

    void Ql(const UniElemDouble* Mij_ori, uni10_const_bool* isdiag, const uni10_uint64* M, const uni10_uint64* N, 
        UniElemDouble* Q, UniElemDouble* L);

    void Rq(const UniElemDouble* Mij_ori, uni10_const_bool* isdiag, const uni10_uint64* M, const uni10_uint64* N, 
        UniElemDouble* R, UniElemDouble* Q);

    void Sdd(const UniElemDouble* Mij_ori, uni10_const_bool* isdiag, const uni10_uint64* M, const uni10_uint64* N, 
        UniElemDouble* U, UniElemDouble* S, UniElemDouble* vT);

    void Svd(const UniElemDouble* Mij_ori, uni10_const_bool* isdiag, const uni10_uint64* M, const uni10_uint64* N, 
        UniElemDouble* U, UniElemDouble* S, UniElemDouble* vT);

    void SyEigDecompose(const UniElemDouble* Mij_ori, uni10_const_bool *isMdiag, const uni10_uint64* N, 
        UniElemDouble* Eig, UniElemDouble* EigVec);

    void SyTriMatEigDecompose(UniElemDouble* D, UniElemDouble* E, uni10_uint64* N, 
        UniElemDouble* z=NULL, uni10_uint64* LDZ=NULL);

    uni10_double64 Trace(const UniElemDouble* Mij_ori, uni10_const_bool* isdiag, const uni10_uint64* M, const uni10_uint64* N);

    void Transpose(const UniElemDouble* A, const uni10_uint64* M, const uni10_uint64* N, UniElemDouble* AT);

    void Transpose(UniElemDouble* A, uni10_uint64* M, uni10_uint64* N);

    void SetDiag(UniElemDouble* _elem, const UniElemDouble* src_elem, const uni10_uint64* M, const uni10_uint64* N);

    void Identity(UniElemDouble* A, const uni10_bool* is_diag, const uni10_uint64* M, const uni10_uint64* N);

    void NormalRandomize(UniElemDouble* A, const uni10_bool* is_diag, const uni10_uint64* M, const uni10_uint64* N, 
        const uni10_double64* mu, const uni10_double64* var, const uni10_int64* seed);

    void UniformRandomize(UniElemDouble* A, const uni10_bool* is_diag, const uni10_uint64* M, const uni10_uint64* N, 
        const uni10_double64* up, const uni10_double64* dn, const uni10_int64* seed);

    // Blas 
    //
    // UNI10_COMPLEX128
    void VectorScal(uni10_complex128* a, UniElemComplex* X, uni10_uint64* N);   // X = a * X

    void VectorAdd(UniElemComplex* Y, const UniElemComplex* X, const uni10_uint64* N);

    void MatrixAdd(UniElemComplex* A, uni10_bool* Aisdag, const UniElemComplex* B, uni10_const_bool* Bisdiag, 
        const uni10_uint64* M, const uni10_uint64* N);

    void MatrixAdd(const UniElemComplex* A, uni10_const_bool* Aisdag, const UniElemComplex* B, uni10_const_bool* Bisdiag, 
        const uni10_uint64* M, const uni10_uint64* N, UniElemComplex* C);

    void VectorSub(UniElemComplex* Y, const UniElemComplex* X, const uni10_uint64* N);

    void MatrixSub(UniElemComplex* A, uni10_bool* Aisdag, const UniElemComplex* B, uni10_const_bool* Bisdiag, 
        const uni10_uint64* M, const uni10_uint64* N);

    void MatrixSub(const UniElemComplex* A, uni10_const_bool* Aisdag, const UniElemComplex* B, uni10_const_bool* Bisdiag, const uni10_uint64* M, const uni10_uint64* N, UniElemComplex* C); 

    void VectorMul(UniElemComplex* Y, const UniElemComplex* X, const uni10_uint64* N);   // Y = Y * X, element-wise multiplication; 

    void MatrixMul(UniElemComplex* A, uni10_bool* Aisdag, const UniElemComplex* B, uni10_const_bool* Bisdag, const uni10_uint64* M, const uni10_uint64* N ); 

    void MatrixMul(const UniElemComplex* A, uni10_const_bool* Aisdag, const UniElemComplex* B, uni10_const_bool* Bisdag, const uni10_uint64* M, const uni10_uint64* N, UniElemComplex* C); 

    void Conjugate(const UniElemComplex* A, const uni10_uint64* N, UniElemComplex* A_conj);

    void Conjugate(UniElemComplex* A, uni10_uint64* N);

    void Dagger(const UniElemComplex* A, const uni10_uint64* M, const uni10_uint64* N, UniElemComplex* AT);

    void Dagger(UniElemComplex* A, uni10_uint64* M, uni10_uint64* N);

    uni10_complex128 Det(const UniElemComplex* A, const uni10_uint64* N, uni10_const_bool* isdiag);

    void Dot(const UniElemComplex* A, uni10_const_bool* Aisdag, const UniElemComplex* B, uni10_const_bool* Bisdag, 
        const uni10_uint64* M, const uni10_uint64* N, const uni10_uint64* K, UniElemComplex* C);

    void VectorExp(uni10_complex128* a, UniElemComplex* X, uni10_uint64* N);

    void Inverse(const UniElemComplex* A, const uni10_uint64* N, uni10_const_bool* isdiag);

    uni10_double64   Norm(const UniElemComplex* X, const uni10_uint64* N, uni10_int32* inc);

    uni10_complex128 VectorSum (const UniElemComplex* X, const uni10_uint64* N, uni10_int32* inc);

    void EigDecompose(const UniElemComplex* Mij_ori, uni10_const_bool *isMdiag, const uni10_uint64* N, 
        UniElemComplex* Eig, UniElemComplex* EigVec);

    void Ldq(const UniElemComplex* Mij_ori, uni10_const_bool* isdiag, const uni10_uint64* M, const uni10_uint64* N, 
        UniElemComplex* L, UniElemComplex* D, UniElemComplex* Q);

    void Lq(const UniElemComplex* Mij_ori, uni10_const_bool* isdiag, const uni10_uint64* M, const uni10_uint64* N, 
        UniElemComplex* L, UniElemComplex* Q);

    void QdrColPivot(const UniElemComplex* Mij_ori, uni10_const_bool* isdiag, const uni10_uint64* M, const uni10_uint64* N, 
        UniElemComplex* Q, UniElemComplex* D, UniElemComplex* R);

    void Qdr(const UniElemComplex* Mij_ori, uni10_const_bool* isdiag, const uni10_uint64* M, const uni10_uint64* N, 
        UniElemComplex* Q, UniElemComplex* D, UniElemComplex* R);

    void Qr(const UniElemComplex* Mij_ori, uni10_const_bool* isdiag, const uni10_uint64* M, const uni10_uint64* N, 
        UniElemComplex* Q, UniElemComplex* R);

    void Ql(const UniElemComplex* Mij_ori, uni10_const_bool* isdiag, const uni10_uint64* M, const uni10_uint64* N, 
        UniElemComplex* Q, UniElemComplex* L);

    void Rq(const UniElemComplex* Mij_ori, uni10_const_bool* isdiag, const uni10_uint64* M, const uni10_uint64* N, 
        UniElemComplex* R, UniElemComplex* Q);

    void Sdd(const UniElemComplex* Mij_ori, uni10_const_bool* isdiag, const uni10_uint64* M, const uni10_uint64* N, 
        UniElemComplex* U, UniElemComplex* S, UniElemComplex* vT);

    void Svd(const UniElemComplex* Mij_ori, uni10_const_bool* isdiag, const uni10_uint64* M, const uni10_uint64* N, 
        UniElemComplex* U, UniElemComplex* S, UniElemComplex* vT);

    void SyEigDecompose(const UniElemComplex* Mij_ori, uni10_const_bool *isMdiag, const uni10_uint64* N, 
        UniElemComplex* Eig, UniElemComplex* EigVec);

    void SyTriMatEigDecompose(UniElemComplex* D, UniElemComplex* E, uni10_uint64* N, 
        UniElemComplex* z=NULL, uni10_uint64* LDZ=NULL);

    uni10_complex128 Trace(const UniElemComplex* Mij_ori, uni10_const_bool* isdiag, const uni10_uint64* M, const uni10_uint64* N);

    void Transpose(const UniElemComplex* A, const uni10_uint64* M, const uni10_uint64* N, UniElemComplex* AT);

    void Transpose(UniElemComplex* A, uni10_uint64* M, uni10_uint64* N);

    void NormalRandomize(UniElemComplex* A, const uni10_bool* is_diag, const uni10_uint64* M, const uni10_uint64* N, 
        const uni10_double64* mu, const uni10_double64* var, const uni10_int64* seed);

    void UniformRandomize(UniElemComplex* A, const uni10_bool* is_diag, const uni10_uint64* M, const uni10_uint64* N, 
        const uni10_double64* up, const uni10_double64* dn, const uni10_int64* seed);

    void Identity(UniElemComplex* A, const uni10_bool* is_diag, const uni10_uint64* M, const uni10_uint64* N);

    void SetDiag(UniElemComplex* _elem, const UniElemComplex* src_elem, const uni10_uint64* M, const uni10_uint64* N);

    // Blas 
    //
    // MIX
    void VectorScal(uni10_double64* a, UniElemComplex* X, uni10_uint64* N); 

    void VectorAdd(UniElemComplex* Y, const UniElemDouble* X, const uni10_uint64* N);

    void MatrixAdd(const UniElemDouble* A, uni10_const_bool* Aisdag, const UniElemComplex* B, uni10_const_bool* Bisdag, 
        const uni10_uint64* M, const uni10_uint64* N, UniElemComplex* C);

    void MatrixAdd(UniElemComplex* A, uni10_bool* Aisdag, const UniElemDouble* B, uni10_const_bool* Bisdag, 
        const uni10_uint64* M, const uni10_uint64* N );

    void MatrixAdd(const UniElemComplex* A, uni10_const_bool* Aisdag, const UniElemDouble* B, uni10_const_bool* Bisdag, 
        const uni10_uint64* M, const uni10_uint64* N, UniElemComplex* C);

    void VectorSub(UniElemComplex* Y, const UniElemDouble* X, const uni10_uint64* N);

    void MatrixSub(const UniElemDouble* A, uni10_const_bool* Aisdag, const UniElemComplex* B, uni10_const_bool* Bisdag, 
        const uni10_uint64* M, const uni10_uint64* N, UniElemComplex* C);

    void MatrixSub(UniElemComplex* A, uni10_bool* Aisdag, const UniElemDouble* B, uni10_const_bool* Bisdag, 
        const uni10_uint64* M, const uni10_uint64* N );

    void MatrixSub(const UniElemComplex* A, uni10_const_bool* Aisdag, const UniElemDouble* B, uni10_const_bool* Bisdag, 
        const uni10_uint64* M, const uni10_uint64* N, UniElemComplex* C);

    void VectorMul(UniElemComplex* Y, const UniElemDouble* X, const uni10_uint64* N);   // Y = Y * X, element-wise multiplication;

    void MatrixMul(UniElemComplex* A, uni10_bool* Aisdag, const UniElemDouble* B, uni10_const_bool* Bisdag, 
        const uni10_uint64* M, const uni10_uint64* N);

    void MatrixMul(const UniElemDouble* A, uni10_const_bool* Aisdag, const UniElemComplex* B, uni10_const_bool* Bisdag, 
        const uni10_uint64* M, const uni10_uint64* N, UniElemComplex* C);

    void MatrixMul(const UniElemComplex* A, uni10_const_bool* Aisdag, const UniElemDouble* B, uni10_const_bool* Bisdag, 
        const uni10_uint64* M, const uni10_uint64* N, UniElemComplex* C);

    void Dot(const UniElemDouble* A, uni10_const_bool* Aisdag, const UniElemComplex* B, uni10_const_bool* Bisdag, 
        const uni10_uint64* M, const uni10_uint64* N, const uni10_uint64* K, UniElemComplex* C);

    void Dot(const UniElemComplex* A, uni10_const_bool* Aisdag, const UniElemDouble* B, uni10_const_bool* Bisdag, 
        const uni10_uint64* M, const uni10_uint64* N, const uni10_uint64* K, UniElemComplex* C);

    void EigDecompose(const UniElemDouble* Mij_ori, uni10_const_bool *isMdiag, const uni10_uint64* N, 
        UniElemComplex* Eig, UniElemComplex* EigVec);

    void SyEigDecompose(const UniElemComplex* Mij_ori, uni10_const_bool *isMdiag, const uni10_uint64* N, 
        UniElemDouble* Eig, UniElemComplex* EigVec);

    void VectorExp(uni10_double64* a, UniElemComplex* X, uni10_uint64* N);

  }

}

#endif

