#ifndef __UNI10_LINALG_INPLACE_INVERSE_H__
#define __UNI10_LINALG_INPLACE_INVERSE_H__

#include "uni10_api/Matrix.h"

namespace uni10{

  /// @ingroup linalg_inplace
  /// @brief Compute the inverse of a matrix.
  /// 
  /// @param[in,out] matout On entry, \c matout is the matrix to be inverted. On exit, \c matout is overwritten by its inverse.
  template<typename UniType>
    void Inverse( Matrix<UniType>& matout, UNI10_INPLACE on );

  template<typename UniType>
    void Inverse( Matrix<UniType>& matout, UNI10_INPLACE on ){

      uni10_error_msg(on != 1, "%s", "Setting a wrong flag of uni10_Inplace." );

      uni10_error_msg(!(matout.row_ == matout.col_), "%s", "Cannot perform inversion on a non-square matrix." );

      linalg_unielem_internal::Inverse(&matout.elem_, &matout.row_, &matout.diag_);

    }

}

#endif
