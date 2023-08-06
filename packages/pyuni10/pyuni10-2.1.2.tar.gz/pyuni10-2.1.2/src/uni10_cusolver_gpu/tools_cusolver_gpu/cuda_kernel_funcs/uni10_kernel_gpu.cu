#include "uni10_sys_info/uni10_cusolver_gpu/uni10_device_const_cusolver_gpu.cuh"
#include "uni10_cusolver_gpu/tools_cusolver_gpu/cuda_kernel_funcs/uni10_kernel_gpu.h"

namespace uni10{

  namespace linalg_driver_internal{

    // uni10_double64
    __global__ void _VectorMul_kernel(uni10_double64* Y, uni10_double64* X, uni10_uint64 N){

      size_t idx = (blockIdx.y*(gridDim.x) +  blockIdx.x) * DCnst.block + threadIdx.x;

      if(idx < N)
        Y[idx] *= X[idx];

    }

    void VectorMul_kernel(uni10_double64* Y, uni10_double64* X, uni10_uint64 N){

      const MemoryConst &host_const = env_variables.GetSysInfo().host_const;
      uni10_uint64 NBlk = (N + host_const.block - 1) / host_const.block;
      dim3 grid(NBlk%MAXGRIDSIZE_X_H, (NBlk + MAXGRIDSIZE_X_H - 1)/MAXGRIDSIZE_X_H);

      _VectorMul_kernel<<< grid, host_const.block >>>(Y , X , N);


    }

    __global__ void _VectorSum_kernel(uni10_double64 a, uni10_double64* X, uni10_uint64 N){

    }

    void VectorSum_kernel(uni10_double64 a, uni10_double64* X, uni10_uint64 N){

    }

    __global__ void _SetDiag_kernel(uni10_double64* ori_elem, uni10_double64* diag_elem, uni10_uint64 M, uni10_uint64 N, uni10_uint64 diag_N){


    }

    void SetDiag_kernel(uni10_double64* ori_elem, uni10_double64* diag_elem, uni10_uint64 M, uni10_uint64 N, uni10_uint64 diag_N){

    }

    __global__ void _GetDiag_kernel(uni10_double64* ori_elem, uni10_double64* diag_elem, uni10_uint64 M, uni10_uint64 N, uni10_uint64 diag_N){

    }

    void GetDiag_kernel(uni10_double64* ori_elem, uni10_double64* diag_elem, uni10_uint64 M, uni10_uint64 N, uni10_uint64 diag_N){

    }

    __global__ void _GetUpTri_kernel(uni10_double64* ori_elem, uni10_double64* tri_elem, uni10_uint64 m, uni10_uint64 n){

    }

    void GetUpTri_kernel(uni10_double64* ori_elem, uni10_double64* tri_elem, uni10_uint64 m, uni10_uint64 n){

    }

    __global__ void _GetDnTri_kernel(uni10_double64* ori_elem, uni10_double64* tri_elem, uni10_uint64 m, uni10_uint64 n){

    }

    void GetDnTri_kernel(uni10_double64* ori_elem, uni10_double64* tri_elem, uni10_uint64 m, uni10_uint64 n){

    }

    // uni10_complex128
    __global__ void _VectorMul_kernel(uni10_complex128 a, uni10_complex128* X, uni10_uint64 N){

    }

    void VectorMul_kernel(uni10_complex128 a, uni10_complex128* X, uni10_uint64 N){

    }

    __global__ void _VectorSum_kernel(uni10_complex128 a, uni10_complex128* X, uni10_uint64 N){

    }

    void VectorSum_kernel(uni10_complex128 a, uni10_complex128* X, uni10_uint64 N){

    }

    __global__ void _SetDiag_kernel(uni10_complex128* ori_elem, uni10_complex128* diag_elem, uni10_uint64 M, uni10_uint64 N, uni10_uint64 diag_N){

    }

    void SetDiag_kernel(uni10_complex128* ori_elem, uni10_complex128* diag_elem, uni10_uint64 M, uni10_uint64 N, uni10_uint64 diag_N){

    }

    __global__ void _GetDiag_kernel(uni10_complex128* ori_elem, uni10_complex128* diag_elem, uni10_uint64 M, uni10_uint64 N, uni10_uint64 diag_N){

    }

    void GetDiag_kernel(uni10_complex128* ori_elem, uni10_complex128* diag_elem, uni10_uint64 M, uni10_uint64 N, uni10_uint64 diag_N){

    }

    __global__ void _GetUpTri_kernel(uni10_complex128* ori_elem, uni10_complex128* tri_elem, uni10_uint64 m, uni10_uint64 n){

    }

    void GetUpTri_kernel(uni10_complex128* ori_elem, uni10_complex128* tri_elem, uni10_uint64 m, uni10_uint64 n){

    }

    __global__ void _GetDnTri_kernel(uni10_complex128* ori_elem, uni10_complex128* tri_elem, uni10_uint64 m, uni10_uint64 n){

    }

    void GetDnTri_kernel(uni10_complex128* ori_elem, uni10_complex128* tri_elem, uni10_uint64 m, uni10_uint64 n){

    }

    // Auxiliary double64-complex128 || complex128-double64
    __global__ void _UniElemCast_kernel(uni10_complex128* new_elem, uni10_double64* raw_elem, uni10_uint64 elemNum){

    }

    void UniElemCast_kernel(uni10_complex128* new_elem, uni10_double64* raw_elem, uni10_uint64 elemNum){

    }

    __global__ void _UniElemCast_kernel(uni10_double64* new_elem, uni10_complex128* raw_elem, uni10_uint64 elemNum){

    }

    void UniElemCast_kernel(uni10_double64* new_elem, uni10_complex128* raw_elem, uni10_uint64 elemNum){

    }

  }

}
