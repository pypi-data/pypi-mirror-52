#ifndef __UNI10_LINALG_INPLACE_EIG_H__
#define __UNI10_LINALG_INPLACE_EIG_H__

#include "uni10_api/Matrix.h"

namespace uni10{

  /// @ingroup linalg_inplace
  /// @brief Compute the eigenvalues and right eigenvectors of a square matrix.
  /// 
  template<typename UniType>
    void Eig( const Block<UniType>& kblk, Matrix<uni10_complex128>& z, Matrix<uni10_complex128>& w, UNI10_INPLACE on );

  template<typename UniType>
    void Eig( const Block<UniType>& kblk, Matrix<uni10_complex128>& z, Matrix<uni10_complex128>& w, UNI10_INPLACE on ){

      uni10_error_msg(on != 1, "%s", "Setting a wrong flag of uni10_Inplace." );
      uni10_error_msg(kblk.row_ != kblk.col_, "%s", "For doing eigenvalue decomposition, the matrix have to be square." );

      //GPU_NOT_READY
      z.Assign(kblk.row_, kblk.col_, true);
      w.Assign(kblk.row_, kblk.col_);

      linalg_unielem_internal::EigDecompose(&kblk.elem_, &kblk.diag_, &kblk.col_, &z.elem_, &w.elem_);

    }

}

#endif
