#ifndef __UNI10_LINALG_SDD_H__
#define __UNI10_LINALG_SDD_H__

#include <vector>

#include "uni10_api/uni10_linalg_inplace/uni10_linalg_inplace_sdd.h"

namespace uni10{

  /// @ingroup linalg
  /// @brief Perform singular value decomposition
  /// 
  /// Factor the matrix \c kblk as \c u*s*vt. The difference between this function and Svd() is the lapack function they call.
  /// @param[in] kblk Matrix to be factored.
  /// @return Vector of result matrices. The elements are (in sequence): \c u A unitary matrix, \c s A diagonal matrix with singular values at diagonal element stored in descending order, \c vt The transpose of a unitary matrix \c v.
  template<typename UniType>
    std::vector< Matrix<UniType> > Sdd( const Block<UniType>& kblk );

  template<typename UniType>
    std::vector< Matrix<UniType> > Sdd( const Block<UniType>& kblk ){

      std::vector<Matrix<UniType> > svd(3);
      Sdd(kblk, svd[0], svd[1], svd[2], INPLACE);

      return svd;

    }


}

#endif
