#ifndef __UNI10_LINALG_NORM_H__
#define __UNI10_LINALG_NORM_H__

#include <vector>

#include "uni10_api/Block.h"
#include "uni10_api/Matrix.h"

namespace uni10{

  /// @ingroup linalg
  /// @brief Compute the Frobenius norm of a matrix.
  /// 
  /// @param[in] kblk Matrix to compute Frobenius norm for.
  /// @return The Frobenius norm of \c kblk.
  template<typename UniType>
    uni10_double64 Norm( const Block<UniType>& kblk );

  template<typename UniType>
    uni10_double64 Norm( const Block<UniType>& kblk ){

      uni10_int32 inc = 1;
      uni10_uint64 elem_num = kblk.diag_ ? std::min(kblk.row_, kblk.col_) : kblk.row_ * kblk.col_;
      return linalg_unielem_internal::Norm(&kblk.elem_, &elem_num, &inc);

    }

}

#endif
