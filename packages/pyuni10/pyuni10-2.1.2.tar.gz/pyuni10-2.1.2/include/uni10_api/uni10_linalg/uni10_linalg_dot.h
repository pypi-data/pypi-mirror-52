#ifndef __UNI10_LINALG_DOT_H__
#define __UNI10_LINALG_DOT_H__

#include "uni10_api/uni10_linalg_inplace/uni10_linalg_inplace_dot.h"

namespace uni10{

  template<typename T> 
    Matrix<uni10_complex128> Dot( const Block<uni10_complex128>& kblk1, const Block<T>& kblk2 );

  /// @ingroup linalg
  /// @brief Perform matrix multiplication.
  /// 
  /// @param[in] kblk1 Input matrix.
  /// @param[in] kblk2 Input matrix.
  /// @return Result matrix of \c kblk1*kblk2.
  template<typename T> 
    Matrix<T> Dot( const Block<uni10_double64>& kblk1, const Block<T>& kblk2 );

  template<typename T> 
    Matrix<uni10_complex128> Dot( const Block<uni10_complex128>& kblk1, const Block<T>& kblk2 ){

      Matrix<uni10_complex128> matout;
      Dot(matout, kblk1, kblk2, INPLACE);
      return matout;

    }

  template<typename T> 
    Matrix<T> Dot( const Block<uni10_double64>& kblk1, const Block<T>& kblk2 ){

      Matrix<T> matout;
      Dot(matout, kblk1, kblk2, INPLACE);
      return matout;

    }

}

#endif
