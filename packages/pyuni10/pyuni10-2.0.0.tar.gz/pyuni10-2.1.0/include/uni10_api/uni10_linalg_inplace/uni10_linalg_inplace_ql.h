#ifndef __UNI10_LINALG_INPLACE_QL_H__
#define __UNI10_LINALG_INPLACE_QL_H__

#include "uni10_api/Matrix.h"

namespace uni10{

  /// @ingroup linalg_inplace
  /// @brief Compute the QL decomposition of a matrix.
  /// 
  /// Factor the matrix \c kblk as \c q*l, where \c q is orthonormal and \c l is lower-triangular.
  /// @param[in] kblk Matrix to be factored.
  /// @param[out] q A matrix with orthonoraml columns.
  /// @param[out] l The lower-triangular matrix.
  template<typename UniType>
    void Ql( const Block<UniType>& kblk, Matrix<UniType>& q, Matrix<UniType>& l, UNI10_INPLACE on  );

  template<typename UniType>
    void Ql( const Block<UniType>& kblk, Matrix<UniType>& q, Matrix<UniType>& l, UNI10_INPLACE on  ){

      uni10_error_msg(on != 1, "%s", "Setting a wrong flag of uni10_Inplace." );

      uni10_error_msg(kblk.row_ < kblk.col_, "%s", "Cannot perform QL decomposition when row_ < col_. Nothing to do." );

      q.Assign(kblk.row_, kblk.col_);
      l.Assign(kblk.col_, kblk.col_);

      linalg_unielem_internal::Ql(&kblk.elem_, &kblk.diag_, &kblk.row_, &kblk.col_, &q.elem_, &l.elem_);

    }

}

#endif
