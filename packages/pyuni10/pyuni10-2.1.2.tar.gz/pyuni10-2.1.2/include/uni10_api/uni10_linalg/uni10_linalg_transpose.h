#ifndef __UNI10_LINALG_TRANS_H__
#define __UNI10_LINALG_TRANS_H__

#include <vector>

#include "uni10_api/uni10_linalg_inplace/uni10_linalg_inplace_transpose.h"

namespace uni10{

  /// @ingroup linalg
  /// @brief Takes transpose of a matrix.
  /// 
  /// @param[in] kblk Input matrix.
  /// @return transpose of \c kblk. 
  template<typename UniType>
    Matrix<UniType> Transpose( const Block<UniType>& kblk ){

      Matrix<UniType> transmat;
      Transpose(transmat, kblk, INPLACE);

      return transmat;

    }

}

#endif
