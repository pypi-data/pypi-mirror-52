#ifndef __UNI10_LINALG_RQ_H__
#define __UNI10_LINALG_RQ_H__

#include <vector>

#include "uni10_api/uni10_linalg_inplace/uni10_linalg_inplace_rq.h"

namespace uni10{

  /// @ingroup linalg
  /// @brief Compute the RQ decomposition of a matrix.
  /// 
  /// Factor the matrix \c kblk as \c r*q, where \c r is upper-triangular and \c q is orthonormal.
  /// @param[in] kblk Matrix to be factored.
  /// @return Vector of result matrices. The elements are (in sequence): \c r The upper-triangular matrix, \c q A matrix with orthonoraml columns.
  template<typename UniType>
    std::vector< Matrix<UniType> > Rq( const Block<UniType>& kblk );

  template<typename UniType>
    std::vector< Matrix<UniType> > Rq( const Block<UniType>& kblk ){

      std::vector<Matrix<UniType> > rq(2);
      Rq(kblk, rq[0], rq[1], INPLACE);

      return rq;

    }

}

#endif
