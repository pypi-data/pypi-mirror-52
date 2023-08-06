#ifndef __UNI10_LINALG_INPLACE_QDRCPIVOT_H__
#define __UNI10_LINALG_INPLACE_QDRCPIVOT_H__

#include "uni10_api/Matrix.h"

namespace uni10{

  template<typename UniType>
    void QdrColPivot( const Block<UniType>& kblk, Matrix<UniType>& q, Matrix<UniType>& d, Matrix<UniType>& r, UNI10_INPLACE on );

  template<typename UniType>
    void QdrColPivot( const Block<UniType>& kblk, Matrix<UniType>& q, Matrix<UniType>& d, Matrix<UniType>& r, UNI10_INPLACE on ){

      uni10_error_msg(on != 1, "%s", "Setting a wrong flag of uni10_Inplace." );
      uni10_error_msg(kblk.row_ != kblk.col_, "%s", "Cannot perform QDRCOLPIVOT decomposition when row_ != col_. Nothing to do." );

      q.Assign(kblk.row_, kblk.col_);
      d.Assign(kblk.col_, kblk.col_, true);
      r.Assign(kblk.col_, kblk.col_);

      linalg_unielem_internal::QdrColPivot(&kblk.elem_, &kblk.diag_, &kblk.row_, &kblk.col_, &q.elem_, &d.elem_, &r.elem_);

    }

}

#endif
