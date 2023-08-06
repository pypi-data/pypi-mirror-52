#include "uni10_type.h"
#include "uni10_error.h"
#include "uni10_auxiliary.h"

namespace uni10{

  //env_type(env_info, _type) env_variables;

  void Uni10Create(int argc, char** argv){

    env_variables.Init_(argc, argv);

  }

  void Uni10Destroy(){

    env_variables.Clear();

  }

  void Uni10PrintEnvInfo(){

    env_variables.PrintEnvInfo();

  }


}; // End of namespace
