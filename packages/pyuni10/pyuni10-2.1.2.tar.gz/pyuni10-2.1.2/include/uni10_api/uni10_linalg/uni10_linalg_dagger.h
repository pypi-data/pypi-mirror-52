#ifndef __UNI10_LINALG_DAGGER_H__
#define __UNI10_LINALG_DAGGER_H__

#include <vector>

#include "uni10_api/uni10_linalg_inplace/uni10_linalg_inplace_dagger.h"

namespace uni10{

  /// @ingroup linalg
  /// @brief Takes complex conjugate transpose of a matrix.
  /// 
  /// @param[in] kblk Input matrix.
  /// @return The complex conjugate transpose of \c kblk.
  template<typename UniType>
    Matrix<UniType> Dagger( const Block<UniType>& kblk );

  template<typename UniType>
    Matrix<UniType> Dagger( const Block<UniType>& kblk ){

      Matrix<UniType> matout(kblk.col(), kblk.row(), kblk.diag());
      Dagger(matout, kblk, INPLACE);

      return matout;

    }

}

#endif
