#ifndef __UNI10_ENV_CUSOLVER_GPU_H__
#define __UNI10_ENV_CUSOLVER_GPU_H__

#include <stdio.h>

#include "uni10_type.h"
#include "uni10_error.h"
#include "uni10_sys_info/uni10_cusolver_gpu/uni10_sys_info_cusolver_gpu.h"
#include "uni10_sys_info/uni10_cusolver_gpu/uni10_memory_const_cusolver_gpu.h"


namespace uni10{

  class UniEnvInfoGpu{

    public:

      UniEnvInfoGpu(): etype_(gpu){};

      ~UniEnvInfoGpu(){};

      void Clear();

      void UsedMemory(const uni10_uint64& memsize);

      bool DefaultOngpuFlag();

      bool LoadUni10Rc( SysInfoGpu& _uni10_sys_info );

      void PrintEnvInfo() ;

      const SysInfoGpu& GetSysInfo() const;

      friend void Uni10Create(int argc, char** argv);

    private:

      uni10_exu_type            etype_;

      SysInfoGpu                uni10_sys_info_;

      void Init_(int argc=0, char** argv=NULL);

      // update HCnst in sys_info from DCnst on gpu
      void ConstDeviceToHost_();
      // update DCnst on gpu from HCnst un sys_info
      void ConstHostToDevice_();

  };

  extern UniEnvInfoGpu env_variables;

};

#endif
