#include "uni10_sys_info/uni10_cusolver_gpu/uni10_device_const_cusolver_gpu.cuh"
#include "uni10_cusolver_gpu/tools_cusolver_gpu/cuda_kernel_funcs/uni10_kernel_gpu.h"

namespace uni10{

  namespace linalg_driver_internal{

    __global__ void _Reshape_kernel(double* oldElem, int bondNum, size_t elemNum, size_t* offset, double* newElem){

      //size_t oldIdx = blockIdx.y * MAXGRIDSIZE_X * MAXTHREADSPERBLOCK +  blockIdx.x * blockDim.x + threadIdx.x;
      size_t oldIdx = (blockIdx.y*(gridDim.x) +  blockIdx.x) * DCnst.block + threadIdx.x;
      size_t idx = oldIdx;
      size_t newIdx = 0;

      if(idx < elemNum){
        for(int i = 0; i < bondNum; i++){
          newIdx += (idx/offset[i]) * offset[bondNum + i];
          idx = idx % offset[i];
        }
        newElem[newIdx] = oldElem[oldIdx];
      }

    }

    void Reshape_kernel(double* oldElem, int bondNum, size_t elemNum, size_t* offset, double* newElem){

      size_t* D_offset;
      checkCudaErrors(cudaMalloc((void**)&D_offset, 2 * sizeof(size_t) * bondNum));
      checkCudaErrors(cudaMemcpy(D_offset, offset, 2 * sizeof(size_t) * bondNum, cudaMemcpyHostToDevice));

      const MemoryConst &host_const = env_variables.GetSysInfo().host_const;
      uni10_uint64 NBlk = (elemNum + host_const.block - 1) / host_const.block;
      dim3 grid(NBlk%MAXGRIDSIZE_X_H, (NBlk + MAXGRIDSIZE_X_H - 1)/MAXGRIDSIZE_X_H);

      _Reshape_kernel<<<grid, host_const.block>>>(oldElem, bondNum, elemNum, D_offset, newElem);

      cudaFree(D_offset);


    }

    __global__ void _Reshape_kernel(std::complex<double>* oldElem, int bondNum, size_t elemNum, size_t* offset, std::complex<double>* newElem){

      size_t oldIdx = (blockIdx.y*(gridDim.x) +  blockIdx.x) * DCnst.block + threadIdx.x;
      size_t idx = oldIdx;
      size_t newIdx = 0;

      if(idx < elemNum){
        for(int i = 0; i < bondNum; i++){
          newIdx += (idx/offset[i]) * offset[bondNum + i];
          idx = idx % offset[i];
        }
        newElem[newIdx] = oldElem[oldIdx];
      }

    }

    void Reshape_kernel(std::complex<double>* oldElem, int bondNum, size_t elemNum, size_t* offset, std::complex<double>* newElem){

      size_t* D_offset;
      checkCudaErrors(cudaMalloc((void**)&D_offset, 2 * sizeof(size_t) * bondNum));
      checkCudaErrors(cudaMemcpy(D_offset, offset, 2 * sizeof(size_t) * bondNum, cudaMemcpyHostToDevice));


      const MemoryConst &host_const = env_variables.GetSysInfo().host_const;
      uni10_uint64 NBlk = (elemNum + host_const.block - 1) / host_const.block;
      dim3 grid(NBlk%MAXGRIDSIZE_X_H, (NBlk + MAXGRIDSIZE_X_H - 1)/MAXGRIDSIZE_X_H);

      _Reshape_kernel<<<grid, host_const.block>>>(oldElem, bondNum, elemNum, D_offset, newElem);


      cudaFree(D_offset);

    }

  }

}
