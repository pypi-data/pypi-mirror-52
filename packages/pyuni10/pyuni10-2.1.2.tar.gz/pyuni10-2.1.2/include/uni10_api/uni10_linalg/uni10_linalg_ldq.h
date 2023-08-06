#ifndef __UNI10_LINALG_LDQ_H__
#define __UNI10_LINALG_LDQ_H__

#include <vector>

#include "uni10_api/uni10_linalg_inplace/uni10_linalg_inplace_ldq.h"

namespace uni10{

  /// @ingroup linalg
  /// @brief Compute the LQ decomposition of a matrix.
  /// 
  /// Factor the matrix \c kblk as \c l*d*q, where \c l is lower-triangular, \c d is diagonal and \c q is orthonormal.
  /// @param[in] kblk Matrix to be factored.
  /// @return Vector of result matrices. The elements are (in sequence): \c l The lower-triangular matrix, \c d The diagonal matrix. \c q A matrix with orthonoraml rows. \c l*d is equivalent to the lower triangular matrix in the conventional LQ decomposition. 
  template<typename UniType>
    std::vector< Matrix<UniType> > Ldq( const Block<UniType>& kblk );

  template<typename UniType>
    std::vector< Matrix<UniType> > Ldq( const Block<UniType>& kblk ){

      std::vector<Matrix<UniType> > ldq(3);
      Ldq(kblk, ldq[0], ldq[1], ldq[2], INPLACE);

      return ldq;

    }

}

#endif
