#ifndef __UNI10_CUSOLVER_GPU_DCONST_CUH__
#define __UNI10_CUSOLVER_GPU_DCONST_CUH__
#include "uni10/uni10_sys_info/uni10_cusolver_gpu/uni10_gpu_Mem.h"

//extern __constant__ uni10::MemCnst DCnst;

namespace uni10{

    extern __device__ __constant__ MemCnst DCnst;
}

#endif
