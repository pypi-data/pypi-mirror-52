#ifndef __UNI10_LINALG_DET_H__
#define __UNI10_LINALG_DET_H__

#include <vector>

#include "uni10_api/Block.h"

namespace uni10{

  /// @ingroup linalg
  /// @brief Compute the determinant of a matrix.
  /// 
  /// @param[in] kblk Input matrix to compute determinants for.
  /// @return Determinant of \c kblk.
  template<typename UniType>
    UniType Det( const Block<UniType>& kblk );

  template<typename UniType>
    UniType Det( const Block<UniType>& kblk ){

      UniType res = linalg_unielem_internal::Det(&kblk.elem_, &kblk.row_, &kblk.diag_);

      return res;

    }

}

#endif
