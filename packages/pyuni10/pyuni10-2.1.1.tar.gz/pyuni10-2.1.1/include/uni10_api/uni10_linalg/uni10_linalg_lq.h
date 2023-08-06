#ifndef __UNI10_LINALG_LQ_H__
#define __UNI10_LINALG_LQ_H__

#include <vector>

#include "uni10_api/uni10_linalg_inplace/uni10_linalg_inplace_lq.h"

namespace uni10{

  /// @ingroup linalg
  /// @brief Compute the LQ decomposition of a matrix.
  /// 
  /// Factor the matrix \c kblk as \c l*q, where \c l is lower-triangular, and \c q is orthonormal.
  /// @param[in] kblk Matrix to be factored.
  /// @return Vector of result matrices. The elements are (in sequence): \c l The lower-triangular matrix, \c q A matrix with orthonoraml rows.
  template<typename UniType>
    std::vector< Matrix<UniType> > Lq( const Block<UniType>& kblk );

  template<typename UniType>
    std::vector< Matrix<UniType> > Lq( const Block<UniType>& kblk ){

      std::vector<Matrix<UniType> > lq(2);
      Lq(kblk, lq[0], lq[1], INPLACE);

      return lq;

    }

}

#endif
