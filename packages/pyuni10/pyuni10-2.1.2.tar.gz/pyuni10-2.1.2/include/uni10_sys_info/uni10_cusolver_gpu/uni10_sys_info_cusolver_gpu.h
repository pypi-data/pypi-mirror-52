#ifndef __UNI10_SYS_INFO_CUSOLVER_GPU_H__
#define __UNI10_SYS_INFO_CUSOLVER_GPU_H__

#if defined(LINUX)
#include <sys/sysinfo.h>
#elif defined(OSX)
#include <sys/vmmeter.h>
#endif

#include <sys/types.h>
#include <sys/sysctl.h>

#include <unistd.h>

#include "uni10_type.h"
#include "uni10_error.h"
#include "uni10_sys_info/uni10_cusolver_gpu/uni10_memory_const_cusolver_gpu.h"

namespace uni10{

    enum Uni10RunTimeType{
        only_cpu   =   0,
        hybrid     =   1,
        only_gpu   =   2
    };

    struct SysInfoGpu{

        // Developping
        SysInfoGpu(): device(0), status(0){
        }

        void DefaultInit(){

          status = 1;
          device = 0;

          cudaGetDeviceProperties(&dev_prop, device);


          globalMem          = dev_prop.totalGlobalMem;
          maxgridsize_x      = dev_prop.maxGridSize[0];
          maxgridsize_y      = dev_prop.maxGridSize[1];
          maxgridsize_z      = dev_prop.maxGridSize[2];
          maxthreadsperblock = dev_prop.maxThreadsPerBlock;
          maxthreadsdim_x    = dev_prop.maxThreadsDim[0];
          maxthreadsdim_y    = dev_prop.maxThreadsDim[1];
          maxthreadsdim_z    = dev_prop.maxThreadsDim[2];
          regsperblock       = dev_prop.regsPerBlock;

          // May be modified by the paramters in uni10rc.
          runtime_type       = only_gpu;

          host_const.blocksize_x = 8;
          host_const.blocksize_y = 8;
          host_const.blocksize_z = 4;
          host_const.gridsize_x = host_const.gridsize_y = host_const.gridsize_z = 1;

          host_const.grid = host_const.gridsize_x*host_const.gridsize_y*host_const.gridsize_z;
          host_const.block = host_const.blocksize_x*host_const.blocksize_y*host_const.blocksize_z;

          //threadsPerBlock_x  = 32;
          //threadsPerBlock_y  = 32;

          checkCudaErrors(cudaMemGetInfo(&free_byte, &total_byte));

        }


        void Clear(){


        };

        void PrintSysInfo() const{

          // Get device properties
          printf("\nCUDA Device #%d\n", device);
          cudaDeviceProp dev_prop;
          cudaGetDeviceProperties(&dev_prop, device);
          printf("Major revision number:         %d\n",  dev_prop.major);
          printf("Minor revision number:         %d\n",  dev_prop.minor);
          printf("Name:                          %s\n",  dev_prop.name);

          printf("Total global memory:           %ld\n",  dev_prop.totalGlobalMem);
#ifdef GPUDEBUG
          printf("Total shared memory per block: %ld\n",  dev_prop.sharedMemPerBlock);
          printf("Total registers per block:     %d\n",  dev_prop.regsPerBlock);
          printf("Warp size:                     %d\n",  dev_prop.warpSize);
          printf("Maximum memory pitch:          %ld\n",  dev_prop.memPitch);
          printf("Maximum threads per block:     %d\n",  dev_prop.maxThreadsPerBlock);
          for (int j = 0; j < 3; ++j)
            printf("Maximum dimension %d of block:  %d\n", j, dev_prop.maxThreadsDim[j]);
          for (int j = 0; j < 3; ++j)
            printf("Maximum dimension %d of grid:   %d\n", j, dev_prop.maxGridSize[j]);
          printf("Clock rate:                    %d\n",  dev_prop.clockRate);
          printf("Total constant memory:         %ld\n",  dev_prop.totalConstMem);
          printf("Texture alignment:             %ld\n",  dev_prop.textureAlignment);
          printf("Concurrent copy and execution: %s\n",  (dev_prop.deviceOverlap ? "Yes" : "No"));
          printf("Number of multiprocessors:     %d\n",  dev_prop.multiProcessorCount);
          printf("Kernel execution timeout:      %s\n",  (dev_prop.kernelExecTimeoutEnabled ? "Yes" : "No"));
#endif
          printf("Compute:                       %d\n",  (dev_prop.computeMode));

        };

        //device ID
        uni10_int device;

        //device property
        cudaDeviceProp dev_prop;

        //redundant vars: (?
        uni10_uint64 globalMem, maxgridsize_x, maxgridsize_y, maxgridsize_z, maxthreadsperblock, maxthreadsdim_x, maxthreadsdim_y, maxthreadsdim_z, regsperblock;
        uni10_uint64 free_byte, total_byte;

        //Constant on CPU :
        MemoryConst host_const;

        // The variable to handle the context of cublas.
        Uni10RunTimeType runtime_type;

        //uni10_int threadsPerBlock_x, threadsPerBlock_y;

        uni10_int status;  // status = 0. Has not initialized.

    };

}

#endif
