#ifndef __UNI10_LINALG_SUM_H__
#define __UNI10_LINALG_SUM_H__

#include <vector>

#include "uni10_api/Block.h"
#include "uni10_api/Matrix.h"

namespace uni10{

  /// @ingroup linalg
  /// @brief Compute the sum of all elements of the matrix.
  /// 
  /// @param[in] kblk Input matrix.
  /// @return Sum of all elements.
  template<typename UniType>
    UniType Sum( const Block<UniType>& kblk );

  template<typename UniType>
    UniType Sum( const Block<UniType>& kblk ){

      uni10_int32 inc = 1;
      return linalg_unielem_internal::VectorSum(&kblk.elem_, &kblk.elem_.elem_num_, &inc);

    }

}

#endif
