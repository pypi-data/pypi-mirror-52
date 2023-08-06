#ifndef __UNI10_RNG_H__
#define __UNI10_RNG_H__

#include <chrono>

#include "uni10_elem_rng.h"
#include "uni10_api/linalg_inplace.h"

#define uni10_rand(M, eng, dis, up, dn, seed)\
  do{ \
    uni10_int32  seed1 = seed;\
    uni10_uint64 num = M.ElemNum();\
    if(seed1 == -1)\
      seed1 = std::chrono::system_clock::now().time_since_epoch().count();\
    uni10_elem_rng(M, num, eng, dis, up, dn, seed1);\
  }while(0);

#define uni10_orthoRand(M, eng, dis, up, dn, seed)\
  do{ \
    uni10_int32 seed1 = seed;\
    uni10_uint64 num = M.ElemNum();\
    if(seed1 == -1)\
      seed1 = std::chrono::system_clock::now().time_since_epoch().count();\
    uni10_elem_rng(M, num, eng, dis, up, dn, seed1);\
    M = uni10::svd(M)[0];\
  }while(0);

#endif
