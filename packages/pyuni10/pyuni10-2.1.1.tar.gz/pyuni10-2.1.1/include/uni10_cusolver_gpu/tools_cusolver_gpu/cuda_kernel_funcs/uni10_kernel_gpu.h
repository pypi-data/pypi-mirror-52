#ifndef __UNI10_KERNEL_GPU_H__
#define __UNI10_KERNEL_GPU_H__

#include "uni10_type.h"
#include "uni10_error.h"
#include "uni10_env_info.h"
#include "uni10_env_info/uni10_cusolver_gpu/uni10_env_info_cusolver_gpu.h"

namespace uni10{

#ifdef __UNI10_ENV_CUSOLVER_GPU_H__
#ifndef THREADSPERBLK_X
#define THREADSPERBLK_X env_variables.GetSysInfo().host_const.BlockSize_x
#endif
#ifndef THREADSPERBLK_Y
#define THREADSPERBLK_Y env_variables.GetSysInfo().host_const.BlockSize_y
#endif
#ifndef THREADSPERBLK_Z
#define THREADSPERBLK_Z env_variables.GetSysInfo().host_const.BlockSize_z
#endif

#ifndef MAXGRIDSIZE_X_H
#define MAXGRIDSIZE_X_H env_variables.GetSysInfo().maxgridsize_x
#endif
#ifndef MAXGRIDSIZE_Y_H
#define MAXGRIDSIZE_Y_H env_variables.GetSysInfo().maxgridsize_y
#endif
#ifndef MAXGRIDSIZE_Z_H
#define MAXGRIDSIZE_Z_H env_variables.GetSysInfo().maxgridsize_z
#endif
#ifndef MAXTHREADSPERBLOCK_H
#define MAXTHREADSPERBLOCK_H env_variables.GetSysInfo().maxthreadsperblock
#endif
#endif

  namespace linalg_driver_internal{

    // uni10_double64
    void VectorExp_kernel(uni10_double64 a, uni10_double64* X, uni10_uint64 N);

    //element-wise multiplication.
    void VectorMul_kernel(uni10_double64* Y, uni10_double64* X, uni10_uint64 N);

    void VectorSum_kernel(uni10_double64 a, uni10_double64* X, uni10_uint64 N);

    void SetDiag_kernel(uni10_double64* ori_elem, uni10_double64* diag_elem, uni10_uint64 M, uni10_uint64 N, uni10_uint64 diag_N);

    void SetDiag_kernel(uni10_double64* ori_elem, uni10_double64* diag_elem, uni10_uint64 M, uni10_uint64 N, uni10_uint64 diag_N);

    void GetUpTri_kernel(uni10_double64* ori_elem, uni10_double64* tri_elem, uni10_uint64 m, uni10_uint64 n); // elem -> tri_elem

    void GetDnTri_kernel(uni10_double64* ori_elem, uni10_double64* tri_elem, uni10_uint64 m, uni10_uint64 n);

    // uni10_complex128
    void VectorExp_kernel(uni10_complex128 a, uni10_complex128* X, uni10_uint64 N);

    //element-wise multiplication.
    void VectorMul_kernel(uni10_complex128 a, uni10_complex128* X, uni10_uint64 N);

    void VectorSum_kernel(uni10_complex128 a, uni10_complex128* X, uni10_uint64 N);

    void SetDiag_kernel(uni10_complex128* ori_elem, uni10_complex128* diag_elem, uni10_uint64 M, uni10_uint64 N, uni10_uint64 diag_N);

    void GetDiag_kernel(uni10_complex128* ori_elem, uni10_complex128* diag_elem, uni10_uint64 M, uni10_uint64 N, uni10_uint64 diag_N);

    void GetUpTri_kernel(uni10_complex128* ori_elem, uni10_complex128* tri_elem, uni10_uint64 m, uni10_uint64 n); // elem -> tri_elem

    void GetDnTri_kernel(uni10_complex128* ori_elem, uni10_complex128* tri_elem, uni10_uint64 m, uni10_uint64 n);

    // Auxiliary double64-complex128 || complex128-double64
    void UniElemCastkernel(uni10_complex128* new_elem, uni10_double64* raw_elem, uni10_uint64 elemNum);

    void UniElemCastkernel(uni10_double64* new_elem, uni10_complex128* raw_elem, uni10_uint64 elemNum);

    void Reshape_kernel(double* oldElem, int bondNum, size_t elemNum, size_t* offset, double* newElem);

    void Reshape_kernel(uni10_complex128* oldElem, int bondNum, size_t elemNum, size_t* offset, uni10_complex128* newElem);

  }

}

#endif
