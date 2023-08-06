#ifndef __UNI10_LINALG_INPLACE_TRANS_H__
#define __UNI10_LINALG_INPLACE_TRANS_H__

#include "uni10_api/Matrix.h"

namespace uni10{

  /// @ingroup linalg_inplace
  /// @brief Takes transpose of a matrix.
  /// 
  /// @param[out] matout Complex transpose of \c kblk. Original contents of \c matout will be replaced.
  /// @param[in] kblk Input matrix.
  template<typename UniType>
    void Transpose( Matrix<UniType>& matout, const Block<UniType>& kblk, UNI10_INPLACE on );

  /// @ingroup linalg_inplace
  /// @brief Takes transpose of a matrix.
  /// 
  /// @param[in,out] matout On entry, \c matout is the input matrix. On exit \c matout is the output matrix.
  template<typename UniType>
    void Transpose( Matrix<UniType>& matout, UNI10_INPLACE on );

  template<typename UniType>
    void Transpose( Matrix<UniType>& matout, const Block<UniType>& kblk, UNI10_INPLACE on ){

      uni10_error_msg(on != 1, "%s", "Setting a wrong flag of uni10_Inplace." );

      matout.Assign(kblk.col_, kblk.row_, kblk.diag_);
      linalg_unielem_internal::Transpose(&kblk.elem_, &kblk.row_, &kblk.col_, &matout.elem_);

    }

  template<typename UniType>
    void Transpose( Matrix<UniType>& matout, UNI10_INPLACE on ){

      uni10_error_msg(on != 1, "%s", "Setting a wrong flag of uni10_Inplace." );

      Matrix<UniType> matoutT;
      matoutT.Assign(matout.col_, matout.row_, matout.diag_);
      linalg_unielem_internal::Transpose(&matout.elem_, &matout.row_, &matout.col_, &matoutT.elem_);
      matout = matoutT;

    }

}

#endif
