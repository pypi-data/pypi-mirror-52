#ifndef __UNI10_LINALG_INVERSE_H__
#define __UNI10_LINALG_INVERSE_H__

#include <vector>

#include "uni10_api/uni10_linalg_inplace/uni10_linalg_inplace_inverse.h"

namespace uni10{

  /// @ingroup linalg
  /// @brief Compute the inverse of a matrix.
  /// 
  /// @param[in] kblk The matrix to be inverted.
  /// @return Inverse matrix of \c kblk.
  template<typename UniType>
    Matrix<UniType> Inverse( const Block<UniType>& kblk );

  template<typename UniType>
    Matrix<UniType> Inverse( const Block<UniType>& kblk ){

      Matrix<UniType> invmat(kblk);

      uni10_error_msg(!(kblk.row_ == kblk.col_), "%s", "Cannot perform inversion on a non-square matrix." );

      linalg_unielem_internal::Inverse(&invmat.elem_, &kblk.row_, &kblk.diag_);

      return invmat;

    }

}

#endif
