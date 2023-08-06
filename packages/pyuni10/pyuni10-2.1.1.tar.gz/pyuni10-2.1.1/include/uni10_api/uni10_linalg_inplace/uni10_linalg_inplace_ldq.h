#ifndef __UNI10_LINALG_INPLACE_LDQ_H__
#define __UNI10_LINALG_INPLACE_LDQ_H__

#include "uni10_api/Matrix.h"

namespace uni10{

  /// @ingroup linalg_inplace
  /// @brief Compute the LQ decomposition of a matrix.
  /// 
  /// Factor the matrix \c kblk as \c l*d*q, where \c l is lower-triangular, \c d is diagonal and \c q is orthonormal.
  /// @param[in] kblk Matrix to be factored.
  /// @param[out] l The lower-triangular matrix.
  /// @param[out] d The diagonal matrix. \c l*d is equivalent to the lower triangular matrix in the conventional LQ decomposition.
  /// @param[out] q A matrix with orthonoraml rows.
  template<typename UniType>
    void Ldq( const Block<UniType>& kblk, Matrix<UniType>& l, Matrix<UniType>& d, Matrix<UniType>& q, UNI10_INPLACE on  );

  template<typename UniType>
    void Ldq( const Block<UniType>& kblk, Matrix<UniType>& l, Matrix<UniType>& d, Matrix<UniType>& q, UNI10_INPLACE on  ){

      uni10_error_msg(on != 1, "%s", "Setting a wrong flag of uni10_Inplace." );

      uni10_error_msg(kblk.row_ > kblk.col_, "%s", "Cannot perform LDQ decomposition when row_ > col_. Nothing to do." );

      l.Assign(kblk.row_, kblk.row_);
      d.Assign(kblk.row_, kblk.row_, true);
      q.Assign(kblk.row_, kblk.col_);

      linalg_unielem_internal::Ldq(&kblk.elem_, &kblk.diag_, &kblk.row_, &kblk.col_, &l.elem_, &d.elem_, &q.elem_);

    }

}

#endif
