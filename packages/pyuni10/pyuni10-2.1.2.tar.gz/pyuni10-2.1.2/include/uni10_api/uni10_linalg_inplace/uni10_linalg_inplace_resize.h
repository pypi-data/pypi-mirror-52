#ifndef __UNI10_LINALG_INPLACE_RESIZE_H__
#define __UNI10_LINALG_INPLACE_RESIZE_H__

#include "uni10_api/Matrix.h"

namespace uni10{

  /// @ingroup linalg_inplace
  /// @brief Change shape and size of a matrix.
  /// 
  /// @param[in,out] M On entry, \c M is the matrix to be resized. On exit, \c M is the output matrix.
  /// @param[in] row Number of rows of output matrix.
  /// @param[in] col Number of columns of output matrix.
  template<typename _uni10_type> 
    void Resize( Matrix<_uni10_type>& M , uni10_uint64 row, uni10_uint64 col, UNI10_INPLACE on);

  /// @ingroup linalg_inplace
  /// @brief Change shape and size of a matrix.
  /// 
  /// @param[out] Mout On exit, \c Mout is the output matrix.
  /// @param[in] Min On entry, \c Min is the matrix to be resized.
  /// @param[in] row Number of rows of output matrix.
  /// @param[in] col Number of columns of output matrix.
  template<typename _uni10_type> 
    void Resize( Matrix<_uni10_type>& Mout , const Matrix<_uni10_type>& Min, uni10_uint64 row, uni10_uint64 col, UNI10_INPLACE on);

  template<typename _uni10_type> 
    void Resize( Matrix<_uni10_type>& M , uni10_uint64 row, uni10_uint64 col, UNI10_INPLACE on){ 

      uni10_error_msg(on != 1, "%s", "Setting a wrong flag of uni10_Inplace." );

      Matrix<_uni10_type> Mout;
      Resize(Mout, M, row,  col, on);
      M = Mout;

    }

  template<typename _uni10_type> 
    void Resize( Matrix<_uni10_type>& Mout , const Matrix<_uni10_type>& Min, uni10_uint64 row, uni10_uint64 col, UNI10_INPLACE on){ 

      uni10_error_msg(on != 1, "%s", "Setting a wrong flag of uni10_Inplace." );

      Mout.Assign(row, col, Min.diag_);
      uni10_bool fixHead = true;
      resize(Mout.elem_, Mout.row_, Mout.col_, Min.elem_, Min.row_, Min.col_, fixHead);

    }

}

#endif
