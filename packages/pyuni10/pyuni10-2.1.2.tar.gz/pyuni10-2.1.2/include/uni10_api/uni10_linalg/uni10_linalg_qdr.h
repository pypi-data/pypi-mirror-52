#ifndef __UNI10_LINALG_QDR_H__
#define __UNI10_LINALG_QDR_H__

#include <vector>

#include "uni10_api/uni10_linalg_inplace/uni10_linalg_inplace_qdr.h"

namespace uni10{

  /// @ingroup linalg
  /// @brief Compute the QR decomposition of a matrix.
  /// 
  /// Factor the matrix \c kblk as \c q*d*r, where \c q is orthonormal, \c d is diagonal and \c r is upper-triangular.
  /// @param[in] kblk Matrix to be factored.
  /// @return Vector of result matrices. The elements are (in sequence): \c q A matrix with orthonoraml columns, \c d The diagonal matrix. \c r The upper-triangular matrix.\c d*r is equivalent to the upper triangular matrix in the conventional QR decomposition.
  template<typename UniType>
    std::vector< Matrix<UniType> > Qdr( const Block<UniType>& kblk );

  template<typename UniType>
    std::vector< Matrix<UniType> > Qdr( const Block<UniType>& kblk ){

      std::vector<Matrix<UniType> > qdr(3);
      Qdr(kblk, qdr[0], qdr[1], qdr[2], INPLACE);

      return qdr;

    }

}

#endif
