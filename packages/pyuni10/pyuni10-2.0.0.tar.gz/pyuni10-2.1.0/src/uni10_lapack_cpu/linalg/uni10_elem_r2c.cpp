#include "uni10_lapack_cpu/uni10_elem_linalg.h"

namespace uni10{

  void Real2Complex(const UniElemDouble* d, UniElemComplex* z){

    tools_internal::UniElemCast(z->elem_ptr_, d->elem_ptr_, d->elem_num_);

  }

  void Real2Complex(const UniElemComplex* _z, UniElemComplex* z){

    uni10_error_msg(true, "%s", "Developing.");

  }
  
}
