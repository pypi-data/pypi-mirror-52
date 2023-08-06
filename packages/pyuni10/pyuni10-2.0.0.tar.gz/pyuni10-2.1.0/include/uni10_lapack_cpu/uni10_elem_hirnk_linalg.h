#ifndef __UNI10_ELEM_HIRNK_LINALG_LAPACK_CPU_H__
#define __UNI10_ELEM_HIRNK_LINALG_LAPACK_CPU_H__

#include "uni10_type.h"
#include "uni10_lapack_cpu/uni10_elem_lapack_cpu.h"

#if defined(UNI_TCL)
#include <hptt.h>
#include <tcl.h>
#endif

typedef uni10::UniElemLapackCpu<uni10_double64>     UniElemDouble;
typedef uni10::UniElemLapackCpu<uni10_complex128>   UniElemComplex;

namespace uni10{

  namespace hirnk_linalg_unielem_internal{

    // Permutation
    void TensorTranspose(const UniElemDouble* ka, const uni10_int* knewbdidx, const uni10_int krank, const uni10_int* koribonddims, UniElemDouble* b);

    void TensorTranspose(const UniElemComplex* ka, const uni10_int* knewbdidx, const uni10_int krank, const uni10_int* koribonddims, UniElemComplex* b);

    // Contraction
    void TensorContract(const UniElemDouble* a, const long* sizes_a, const uni10_int* labela, const uni10_int ranka,
        const UniElemDouble* b, const long* sizes_b, const uni10_int* labelb, const uni10_int rankb,
        UniElemDouble* c, const long* sizes_c, const uni10_int* labelc, const uni10_int rankc);

    void TensorContract(const UniElemComplex* a, const long* sizes_a, const uni10_int* labela, const uni10_int ranka,
        const UniElemComplex* b, const long* sizes_b, const uni10_int* labelb, const uni10_int rankb,
        UniElemComplex* c, const long* sizes_c, const uni10_int* labelc, const uni10_int rankc);

    void TensorContract(const UniElemDouble* a, const long* sizes_a, const uni10_int* labela, const uni10_int ranka,
        const UniElemComplex* b, const long* sizes_b, const uni10_int* labelb, const uni10_int rankb,
        UniElemComplex* c, const long* sizes_c, const uni10_int* labelc, const uni10_int rankc);

    void TensorContract(const UniElemComplex* a, const long* sizes_a, const uni10_int* labela, const uni10_int ranka,
        const UniElemDouble* b, const long* sizes_b, const uni10_int* labelb, const uni10_int rankb,
        UniElemComplex* c, const long* sizes_c, const uni10_int* labelc, const uni10_int rankc);

  }

}

#endif
