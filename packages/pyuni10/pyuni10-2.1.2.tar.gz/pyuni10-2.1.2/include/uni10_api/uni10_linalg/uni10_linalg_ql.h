#ifndef __UNI10_LINALG_QL_H__
#define __UNI10_LINALG_QL_H__

#include <vector>

#include "uni10_api/uni10_linalg_inplace/uni10_linalg_inplace_conj.h"

namespace uni10{

  /// @ingroup linalg
  /// @brief Compute the QL decomposition of a matrix.
  /// 
  /// Factor the matrix \c kblk as \c q*l, where \c q is orthonormal and \c l is lower-triangular.
  /// @param[in] kblk Matrix to be factored.
  /// @return Vector of result matrices. The elements are (in sequence): q \c A matrix with orthonoraml columns, \c l The lower-triangular matrix.
  template<typename UniType>
    std::vector< Matrix<UniType> > Ql( const Block<UniType>& kblk );

  template<typename UniType>
    std::vector< Matrix<UniType> > Ql( const Block<UniType>& kblk ){

      std::vector<Matrix<UniType> > ql(2);
      Ql(kblk, ql[0], ql[1], INPLACE);

      return ql;

    }

}

#endif
