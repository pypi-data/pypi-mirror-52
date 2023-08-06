#ifndef __UNI10_LINALG_CONJ_H__
#define __UNI10_LINALG_CONJ_H__

#include <vector>

#include "uni10_api/uni10_linalg_inplace/uni10_linalg_inplace_conj.h"

  /// @defgroup linalg linear algebra
  /// @brief Auxiliary linear algebra functions.
  
namespace uni10{
  
  /// @ingroup linalg
  /// @brief Takes complex conjugate of a matrix.
  /// 
  /// @param[in] kblk Input matrix.
  /// @return The complex conjugate of \c kblk
  template<typename UniType>
    Matrix<UniType> Conj( const Block<UniType>& kblk );

  template<typename UniType>
    Matrix<UniType> Conj( const Block<UniType>& kblk ){

      Matrix<UniType> matout(kblk.row(), kblk.col(), kblk.diag());
      Conj(matout, kblk, INPLACE);

      return matout;

    }

}

#endif
