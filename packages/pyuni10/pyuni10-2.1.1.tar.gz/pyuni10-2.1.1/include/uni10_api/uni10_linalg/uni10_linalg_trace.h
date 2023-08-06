#ifndef __UNI10_LINALG_TRACE_H__
#define __UNI10_LINALG_TRACE_H__

#include <vector>

#include "uni10_api/Block.h"
#include "uni10_api/Matrix.h"

namespace uni10{

  /// @ingroup linalg
  /// @brief Compute the trace of a matrix.
  /// 
  /// @param[in] kblk Input matrix.
  /// @return Trace of \c kblk.
  template<typename UniType>
    UniType Trace( const Block<UniType>& kblk );

  template<typename UniType>
    UniType Trace( const Block<UniType>& kblk ){

      UniType res = linalg_unielem_internal::Trace(&kblk.elem_, &kblk.diag_, &kblk.row_, &kblk.col_);

      return res;

    }

}

#endif
