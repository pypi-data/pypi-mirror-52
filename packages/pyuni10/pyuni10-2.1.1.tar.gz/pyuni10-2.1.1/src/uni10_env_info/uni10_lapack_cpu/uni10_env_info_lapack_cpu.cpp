#include "uni10_error.h"
#include "uni10_env_info/uni10_lapack_cpu/uni10_env_info_lapack_cpu.h"

namespace uni10{

  UniEnvInfoCpu env_variables;

  void UniEnvInfoCpu::Init_(int argc, char** argv){
    
    argc   = 0;
    argv   = NULL;

    this->etype_  = cpu;
    this->uni10_sys_info_.Init();
    this->LoadUni10Rc();

  }

  void UniEnvInfoCpu::Clear(){

    this->etype_   = no;
    this->uni10_sys_info_.Clear();

  }

  void UniEnvInfoCpu::UsedMemory(const uni10_uint64& memsize){

    this->uni10_sys_info_.free_memsize_ -= memsize;

  }

  bool UniEnvInfoCpu::LoadUni10Rc(){

    bool exsist_rc = true;
    FILE* rcfp = fopen("~/.uni10rc", "r");

    if(!rcfp)
      exsist_rc = false;
    else{
      this->etype_ = cpu;
      uni10_error_msg(true, "%s", "Developping !!!");
    }

    return exsist_rc;
    
  }

  const SysInfoCpu& UniEnvInfoCpu::GetSysInfo() const{

    return uni10_sys_info_;

  }

  void UniEnvInfoCpu::PrintEnvInfo() const{

    uni10_sys_info_.PrintSysInfo();

  }

}
