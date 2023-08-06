#include "uni10_sys_info/uni10_cusolver_gpu/uni10_device_const_cusolver_gpu.cuh"
#include "uni10_cusolver_gpu/tools_cusolver_gpu/cuda_kernel_funcs/uni10_kernel_gpu.h"

namespace uni10{

  namespace linalg_driver_internal{

    __global__ void _VectorExp_kernel(uni10_double64 a, uni10_double64* X, uni10_uint64 N){

      uni10_uint64 idx = (blockIdx.y*(gridDim.x) +  blockIdx.x) * DCnst.block + threadIdx.x;

      if(idx < N)
        X[idx] = exp( a * X[idx]);

    }

    void VectorExp_kernel(uni10_double64 a, uni10_double64* X, uni10_uint64 N){
      const MemoryConst &host_const = env_variables.GetSysInfo().host_const;
      uni10_uint64 NBlk = (N + host_const.block - 1) / host_const.block;
      dim3 grid(NBlk%MAXGRIDSIZE_X_H, (NBlk + MAXGRIDSIZE_X_H - 1)/MAXGRIDSIZE_X_H);

      //dim3 gridSize(blockNum % MAXGRIDSIZE_X_H, (blockNum + MAXGRIDSIZE_X_H - 1) / MAXGRIDSIZE_X_H);

      _VectorExp_kernel<<<grid, host_const.block>>>(a, X, N);

    }

    __global__ void _VectorExp_kernel(uni10_complex128 a, uni10_complex128* X, uni10_uint64 N){

      //uni10_uint64 idx = blockIdx.y * MAXGRIDSIZE_X * MAXTHREADSPERBLOCK + blockIdx.x * blockDim.x + threadIdx.x;

      //if(idx < N)
      //  X[idx] = exp( a * X[idx]);

    }

    void VectorExp_kernel(uni10_complex128 a, uni10_complex128* X, uni10_uint64 N){


      uni10_error_msg(true, "%s", "Developing");

      const MemoryConst &host_const = env_variables.GetSysInfo().host_const;
      uni10_uint64 NBlk = (N + host_const.block - 1) / host_const.block;
      dim3 grid(NBlk%MAXGRIDSIZE_X_H, (NBlk + MAXGRIDSIZE_X_H - 1)/MAXGRIDSIZE_X_H);

      //dim3 gridSize(blockNum % MAXGRIDSIZE_X_H, (blockNum + MAXGRIDSIZE_X_H - 1) / MAXGRIDSIZE_X_H);
      _VectorExp_kernel<<<grid, host_const.block>>>(a, X, N);


    }

  }

}
