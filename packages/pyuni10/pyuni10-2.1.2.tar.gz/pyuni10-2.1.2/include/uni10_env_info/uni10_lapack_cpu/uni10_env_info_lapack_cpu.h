#ifndef __UNI10_ENV_LAPACK_CPU_H__
#define __UNI10_ENV_LAPACK_CPU_H__ 

#include <stdio.h>

#include "uni10_sys_info/uni10_lapack_cpu/uni10_sys_info_lapack_cpu.h"

namespace uni10{

  class UniEnvInfoCpu{

    public:

      UniEnvInfoCpu(): etype_(cpu){};

      ~UniEnvInfoCpu(){};

      void Clear();

      void UsedMemory(const uni10_uint64& memsize);

      bool LoadUni10Rc();

      void PrintEnvInfo() const;

      const SysInfoCpu& GetSysInfo() const;

      friend void Uni10Create(int argc, char** argv);

    private:

      uni10_exu_type    etype_;

      SysInfoCpu  uni10_sys_info_;

      void Init_(int argc=0, char** argv=NULL);

  };

  extern UniEnvInfoCpu env_variables;

};

#endif
