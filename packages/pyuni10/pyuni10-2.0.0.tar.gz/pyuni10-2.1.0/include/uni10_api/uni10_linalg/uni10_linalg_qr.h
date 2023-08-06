#ifndef __UNI10_LINALG_QR_H__
#define __UNI10_LINALG_QR_H__

#include <vector>

#include "uni10_api/uni10_linalg_inplace/uni10_linalg_inplace_qr.h"

namespace uni10{

  /// @ingroup linalg
  /// @brief Compute the QR decomposition of a matrix.
  /// 
  /// Factor the matrix \c kblk as \c q*r, where \c q is orthonormal and \c r is upper-triangular.
  /// @param[in] kblk Matrix to be factored.
  /// @return Vector of result matrices. \c q A matrix with orthonoraml columns, \c r The upper-triangular matrix.
  template<typename UniType>
    std::vector< Matrix<UniType> > Qr( const Block<UniType>& kblk );

  template<typename UniType>
    std::vector< Matrix<UniType> > Qr( const Block<UniType>& kblk ){

      std::vector<Matrix<UniType> > qr(2);
      Qr(kblk, qr[0], qr[1], INPLACE);

      return qr;

    }

}

#endif
