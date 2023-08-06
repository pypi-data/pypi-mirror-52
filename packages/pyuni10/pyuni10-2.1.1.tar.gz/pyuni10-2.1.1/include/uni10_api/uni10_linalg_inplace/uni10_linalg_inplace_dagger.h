#ifndef __UNI10_LINALG_INPLACE_DAGGER_H__
#define __UNI10_LINALG_INPLACE_DAGGER_H__

#include "uni10_api/Matrix.h"

namespace uni10{


  /// @ingroup linalg_inplace
  /// @brief Takes complex conjugate transpose of a matrix.
  /// 
  /// @param[out] matout Complex conjugate transpose of \c kmat. Original contents of \c matout will be overwritten.
  /// @param[in] kblk Input matrix.
  template<typename UniType>
    void Dagger( Matrix<UniType>& matout, const Block<UniType>& kblk, UNI10_INPLACE on );

  /// @ingroup linalg_inplace
  /// @brief Takes complex conjugate transpose of a matrix.
  /// 
  /// @param[in,out] matout On entry, \c matout is the input matrix. On exit, \c matout is overwritten by its complex cojugate transpose.
  template<typename UniType>
    void Dagger( Matrix<UniType>& matout, UNI10_INPLACE on );

  template<typename UniType>
    void Dagger( Matrix<UniType>& matout, const Block<UniType>& kblk, UNI10_INPLACE on ){

      uni10_error_msg(on != 1, "%s", "Setting a wrong flag of uni10_Inplace." );

      matout.Assign(kblk.col_, kblk.row_, kblk.diag_);
      linalg_unielem_internal::Dagger(&kblk.elem_, &kblk.row_, &kblk.col_, &matout.elem_);

    }

  template<typename UniType>
    void Dagger( Matrix<UniType>& matout, UNI10_INPLACE on ){

      uni10_error_msg(on != 1, "%s", "Setting a wrong flag of uni10_Inplace." );

      linalg_unielem_internal::Dagger(&matout.elem_, &matout.row_, &matout.col_);

      uni10_uint64 tmp = matout.row_;
      matout.row_ = matout.col_;
      matout.col_ = tmp;

    }

}

#endif
