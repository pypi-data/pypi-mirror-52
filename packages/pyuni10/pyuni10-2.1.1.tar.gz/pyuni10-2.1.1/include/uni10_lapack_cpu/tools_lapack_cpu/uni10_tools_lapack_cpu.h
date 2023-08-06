#ifndef __UNI10_TOOLS_CPU_H__
#define __UNI10_TOOLS_CPU_H__

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <limits.h>

#include "uni10_type.h"
#include "uni10_error.h"

#ifdef UNI_MKL
#include "mkl.h"
#else
#include "uni10_lapack_cpu/tools_lapack_cpu/uni10_lapack_wrapper_cpu.h"
#endif

namespace uni10{

  namespace tools_internal{

    void* UniElemAlloc(uni10_uint64 memsize);

    void* UniElemCopy(void* des, const void* src, uni10_uint64 memsize);

    void UniElemFree(void* ptr, uni10_uint64 memsize);

    void UniElemZeros(void* ptr, uni10_uint64 memsize);

    //For double ptr.
    //
    void Ones(uni10_double64* elem, uni10_uint64 elem_num);

    void SetDiag(uni10_double64* elem, uni10_double64* diag_elem, uni10_uint64 M, uni10_uint64 N, uni10_uint64 diag_N);

    void GetDiag(uni10_double64* elem, uni10_double64* diag_elem, uni10_uint64 M, uni10_uint64 N, uni10_uint64 diag_N);

    void PrintElem_I(const uni10_double64& elem_i);

    void GetUpTri(uni10_double64* elem, uni10_double64* tri_elem, uni10_uint64 m, uni10_uint64 n);

    void GetDnTri(uni10_double64* elem, uni10_double64* tri_elem, uni10_uint64 m, uni10_uint64 n);

    //For complex ptr.
    //
    void Ones(uni10_complex128* elem, uni10_uint64 elem_num);

    void SetDiag(uni10_complex128* elem, uni10_complex128* diag_elem, uni10_uint64 M, uni10_uint64 N, uni10_uint64 diag_N);

    void GetDiag(uni10_complex128* elem, uni10_complex128* diag_elem, uni10_uint64 M, uni10_uint64 N, uni10_uint64 diag_N);

    void PrintElem_I(const uni10_complex128& elem_i);

    void GetUpTri(uni10_complex128* elem, uni10_complex128* tri_elem, uni10_uint64 m, uni10_uint64 n);

    void GetDnTri(uni10_complex128* elem, uni10_complex128* tri_elem, uni10_uint64 m, uni10_uint64 n);

    void UniElemCast(uni10_complex128* des, const uni10_double64* src, uni10_uint64 N);

    void UniElemCast(uni10_double64 *des, const uni10_complex128 *src, uni10_uint64 N);

    void ToReal(uni10_double64& M_i, uni10_double64 val);

    void ToReal(uni10_complex128& M_i, uni10_double64 val);

    void ToComplex(uni10_double64& M_i, uni10_double64 val);

    void ToComplex(uni10_complex128& M_i, uni10_double64 val);

    void ShrinkWithoutFree(uni10_uint64 memsize);

  }

}/* namespace uni10 */
#endif /* UNI10_TOOLS_H */
