#include "uni10_error.h"
#include "uni10_sys_info/uni10_cusolver_gpu/uni10_memory_const_cusolver_gpu.h"
#include "uni10_env_info/uni10_cusolver_gpu/uni10_env_info_cusolver_gpu.h"
#include "uni10_parser.hpp"

namespace uni10{

  UniEnvInfoGpu env_variables;

  void UniEnvInfoGpu::Init_(int argc, char** argv){

    this->uni10_sys_info_.DefaultInit();


    if(!this->LoadUni10Rc(uni10_sys_info_)){
       //(?

    }

    this->ConstHostToDevice_();


  }

  void UniEnvInfoGpu::UsedMemory(const uni10_uint64& memsize){

    this->uni10_sys_info_.free_byte -= memsize;

  }

  void UniEnvInfoGpu::Clear(){

    this->etype_         = gpu;
    this->uni10_sys_info_.Clear();

  }

  bool UniEnvInfoGpu::DefaultOngpuFlag(){

    bool ongpu;

    if(uni10_sys_info_.runtime_type == only_cpu){

      ongpu = false;

    }

    else if(uni10_sys_info_.runtime_type == only_gpu){

      ongpu = true;

    }

    else if(uni10_sys_info_.runtime_type == hybrid){

      uni10_error_msg(true, "%s", "Developing");
      ongpu = false;

    }

    return ongpu;

  }

  bool UniEnvInfoGpu::LoadUni10Rc(SysInfoGpu& uni10_sys_info){

        bool exists_rc = true;
        Parser pars;

        //tmp vars:
        int mode;
        unsigned int Bsx=0,Bsy=0,Bsz=0,block;

        pars.Bind("mode", mode);
        pars.Bind("blocksize_x",Bsx);
        pars.Bind("blocksize_y",Bsy);
        pars.Bind("blocksize_z",Bsz);

        std::string rcpath = "~/.uni10rc";
        if( access(rcpath.c_str(),R_OK) ){
            rcpath = ".uni10rc";
            if(access(rcpath.c_str(),R_OK)){
                exists_rc = false;
            }
        }

        if(exists_rc){
            pars.Parse(rcpath);
            pars.CheckAll(); // check if all keys are set and read.

            block = Bsx*Bsy*Bsz;

            //checking ...
            if( mode > 2 || mode < 0) uni10_error_msg(true, "%s", "[Read RC] Invalid mode.");
            if( block > 1024 ) uni10_error_msg(true, "%s", "[Read RC] total threads in a block cannot exceed 2014.");
            if( block % 32 ) uni10_error_msg(true, "%s", "[Read RC] total threads in a block should be multiple of 32.");

            //Fill-in
            if(mode == 0)
              uni10_sys_info_.runtime_type = only_cpu;
            else if(mode == 1)
              uni10_sys_info_.runtime_type = hybrid;
            else if(mode == 2)
              uni10_sys_info_.runtime_type = only_gpu;

            uni10_sys_info_.host_const.blocksize_x = Bsx;
            uni10_sys_info_.host_const.blocksize_y = Bsy;
            uni10_sys_info_.host_const.blocksize_z = Bsz;
            uni10_sys_info_.host_const.block       = block;
        }

        return exists_rc;




    }

  const SysInfoGpu& UniEnvInfoGpu::GetSysInfo() const{

    return uni10_sys_info_;

  }


  void UniEnvInfoGpu::PrintEnvInfo() {

    uni10_sys_info_.PrintSysInfo();

    MemoryConst& tmp_dev_info = uni10_sys_info_.host_const;
    ConstDeviceToHost_();

    fprintf(stdout,"\n----- DEVICE CONSTANT -----\n");
    fprintf(stdout," # of threads per block = %d \n",tmp_dev_info.block);
    fprintf(stdout,"blocksize_x = %d\n",tmp_dev_info.blocksize_x);
    fprintf(stdout,"blocksize_y = %d\n",tmp_dev_info.blocksize_y);
    fprintf(stdout,"blocksize_z = %d\n",tmp_dev_info.blocksize_z);
    fprintf(stdout,"\n");

    fprintf(stdout,"# of blocks per grid = %d \n",tmp_dev_info.grid);
    fprintf(stdout,"gridsize_x  = %d\n",tmp_dev_info.gridsize_x);
    fprintf(stdout,"gridsize_y  = %d\n",tmp_dev_info.gridsize_y);
    fprintf(stdout,"gridsize_z  = %d\n",tmp_dev_info.gridsize_z);
    fprintf(stdout,"\n");

    fprintf(stdout,"---------------------------\n");

  }

  void UniEnvInfoGpu::ConstDeviceToHost_(){

    MemConstFromGPU(uni10_sys_info_.host_const);

  }

  void UniEnvInfoGpu::ConstHostToDevice_(){

    MemConstToGPU(uni10_sys_info_.host_const);

  }

}
