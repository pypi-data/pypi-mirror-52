#include "uni10_sys_info/uni10_cusolver_gpu/uni10_memory_const_cusolver_gpu.h"
#include "uni10_sys_info/uni10_cusolver_gpu/uni10_device_const_cusolver_gpu.cuh"

#include "uni10_error.h"


namespace uni10{

    //gpu device instance
    __device__ __constant__ MemoryConst DCnst;

    void MemConstToGPU(const MemoryConst &HCnst){
        checkCudaErrors( cudaMemcpyToSymbol(DCnst,&HCnst,sizeof(MemoryConst)) );
    }
    void MemConstFromGPU(MemoryConst &HCnst){
        checkCudaErrors( cudaMemcpyFromSymbol(&HCnst,DCnst,sizeof(MemoryConst)) );
    }

}; // End of uni10 namespace

