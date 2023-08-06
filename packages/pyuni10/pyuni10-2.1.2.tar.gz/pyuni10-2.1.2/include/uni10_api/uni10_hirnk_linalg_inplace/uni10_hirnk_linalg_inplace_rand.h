#ifndef __UNI10_HIGH_RANK_LINALG_INPLACE_RAND_H__
#define __UNI10_HIGH_RANK_LINALG_INPLACE_RAND_H__

#include "uni10_api/tensor_tools/tensor_tools.h"

namespace uni10{

  /// @ingroup hirnklin_inplace
  /// @brief Set elements of a tensor with random numbers.
  ///
  /// @param[in/out] Tensor to be randomize.
  template<typename uni10_type> 
    void Randomize( UniTensor<uni10_type>& A );

  template<typename uni10_type> 
    void Randomize( UniTensor<uni10_type>& A ){

      tensor_tools::randomize(A.paras, A.style);

    }

};

#endif
