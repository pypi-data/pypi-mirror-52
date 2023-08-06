#ifndef __UNI10_LINALG_INPLACE_EIGH_H__
#define __UNI10_LINALG_INPLACE_EIGH_H__

#include "uni10_api/Matrix.h"

namespace uni10{

  template<typename UniType>
    void EigH( const Block<UniType>& kblk, Matrix<uni10_double64>& z, Matrix<UniType>& w, UNI10_INPLACE on );

  template<typename UniType>
    void EigH( const Block<UniType>& kblk, Matrix<uni10_double64>& z, Matrix<UniType>& w, UNI10_INPLACE on ){

      uni10_error_msg(on != 1, "%s", "Setting a wrong flag of uni10_Inplace." );
      uni10_error_msg(kblk.row_ != kblk.col_, "%s", "For doing symmetric eigenvalue decomposition, the matrix have to be square and symmetric." );

      //GPU_NOT_READY
      z.Assign(kblk.row_, kblk.col_, true);
      w.Assign(kblk.row_, kblk.col_);

      linalg_unielem_internal::SyEigDecompose(&kblk.elem_, &kblk.diag_, &kblk.col_, &z.elem_, &w.elem_);

    }

}

#endif
