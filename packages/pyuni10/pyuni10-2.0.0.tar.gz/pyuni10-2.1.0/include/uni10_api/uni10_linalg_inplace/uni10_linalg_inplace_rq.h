#ifndef __UNI10_LINALG_INPLACE_RQ_H__
#define __UNI10_LINALG_INPLACE_RQ_H__

#include "uni10_api/Matrix.h"

namespace uni10{

  /// @ingroup linalg_inplace
  /// @brief Compute the RQ decomposition of a matrix.
  /// 
  /// Factor the matrix \c kblk as \c r*q, where \c r is upper-triangular and \c q is orthonormal.
  /// @param[in] kblk Matrix to be factored.
  /// @param[out] r The upper-triangular matrix.
  /// @param[out] q A matrix with orthonoraml columns.
  template<typename UniType>
    void Rq( const Block<UniType>& kblk, Matrix<UniType>& r, Matrix<UniType>& q, UNI10_INPLACE on  );

  template<typename UniType>
    void Rq( const Block<UniType>& kblk, Matrix<UniType>& r, Matrix<UniType>& q, UNI10_INPLACE on  ){

      uni10_error_msg(on != 1, "%s", "Setting a wrong flag of uni10_Inplace." );

      uni10_error_msg(kblk.row_ > kblk.col_, "%s", "Cannot perform RQ decomposition when row_ > col_. Nothing to do." );

      r.Assign(kblk.row_, kblk.row_);
      q.Assign(kblk.row_, kblk.col_);

      linalg_unielem_internal::Rq(&kblk.elem_, &kblk.diag_, &kblk.row_, &kblk.col_, &r.elem_, &q.elem_);

    }

}

#endif
