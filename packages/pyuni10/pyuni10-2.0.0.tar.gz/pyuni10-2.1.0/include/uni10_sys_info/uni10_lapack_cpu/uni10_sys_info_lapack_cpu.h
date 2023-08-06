#ifndef __UNI10_SYS_INFO_LAPACK_CPU_H__
#define __UNI10_SYS_INFO_LAPACK_CPU_H__

#if defined(LINUX)
#include <sys/sysinfo.h>
#include <sys/sysctl.h>
#elif defined(OSX)
#include <sys/vmmeter.h>
#endif

#include <sys/types.h>


#include <unistd.h>

#include "uni10_type.h"
#include "uni10_error.h"

namespace uni10{


  struct SysInfoCpu{

    SysInfoCpu(): total_memsize_(0), free_memsize_(0), swap_memsize_(0), mem_unit_(0), core_num_(0), status_(false){

      Init();

    }

    void Clear(){
      total_memsize_  = 0;
      free_memsize_   = 0;
      swap_memsize_   = 0;
      mem_unit_       = 0;
      core_num_       = 0;
      status_         = false;
    };

    void Init(){

#if defined(LINUX)
      struct sysinfo tmp_info;
      sysinfo( & tmp_info );
      total_memsize_    = (uni10_uint64)tmp_info.totalram;
      free_memsize_     = (uni10_uint64)tmp_info.freeram;
      swap_memsize_     = (uni10_uint64)tmp_info.freeswap;
      mem_unit_         = (uni10_uint64)tmp_info.mem_unit;
      core_num_         = sysconf(_SC_NPROCESSORS_ONLN);
      threads_num_      = 8;
#elif defined(OXS)

#endif
      status_ = true;

    }

    void PrintSysInfo() const{

      uni10_double64 total_memsize   = total_memsize_  / 1024. / 1024. * mem_unit_;
      uni10_double64 free_memsize    = free_memsize_   / 1024. / 1024. * mem_unit_;
      uni10_double64 swap_memsize    = swap_memsize_ / 1024. / 1024. * mem_unit_;
      uni10_uint64 max_len           = floor(log(total_memsize_));

#if defined(LINUX)
      fprintf(stdout, "\n#######  Uni10 environment information  #######\n");
      fprintf(stdout, "# CPU   cores   : %*d \n"    , (int)max_len, core_num_);
      fprintf(stdout, "# Threads number: %*d \n"    , (int)max_len, threads_num_);
      fprintf(stdout, "# Total memory  : %*.2f MB\n", (int)max_len, total_memsize);
      fprintf(stdout, "# Free  memory  : %*.2f MB\n", (int)max_len, free_memsize);
      fprintf(stdout, "# Swap  memory  : %*.2f MB\n", (int)max_len, swap_memsize);
      fprintf(stdout, "###############################################\n\n");

#elif defined(OXS)
      system("vm_stat");
#endif

    }

    uni10_uint64 total_memsize_;
    uni10_uint64 free_memsize_;
    uni10_uint64 swap_memsize_;
    uni10_uint64 mem_unit_;
    uni10_int core_num_;
    uni10_int threads_num_;

    bool status_;

  };

}

#endif
