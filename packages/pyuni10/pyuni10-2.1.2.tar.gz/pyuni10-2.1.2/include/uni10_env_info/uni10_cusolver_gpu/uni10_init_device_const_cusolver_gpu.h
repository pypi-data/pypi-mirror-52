#ifndef __UNI10_CUSOLVER_GPU_INITDCONST_H__
#define __UNI10_CUSOLVER_GPU_INITDCONST_H__

#include <map>
#include <string>

#include "uni10_type.h"
#include "uni10_error.h"
#include "uni10_sys_info/uni10_cusolver_gpu/uni10_sys_info_cusolver_gpu.h"

namespace uni10{

  void Uni10InitDeviceConst(SysInfoGpu& uni10_sys_info);

  std::map<std::string, uni10_int> uni10_get_device_const();

}

#endif
