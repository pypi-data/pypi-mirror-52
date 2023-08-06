#ifndef __UNI10_LINALG_INPLACE_DOT_H__
#define __UNI10_LINALG_INPLACE_DOT_H__

#include "uni10_api/Matrix.h"

namespace uni10{

  void Dot( Matrix<uni10_double64>& matout, const Block<uni10_double64>& kblk, UNI10_INPLACE on );

  /// @ingroup linalg_inplace
  /// @brief Perform matrix multiplication \c A=A*B.
  /// 
  /// @param[in,out] matout On entry, \c matout is the original matrix \c A. On exit, \c matout is overwritten by \c A*B.
  /// @param[in] kblk Matrix \c B.
  template<typename T> 
    void Dot( Matrix<uni10_complex128>& matout, const Block<T>& kblk, UNI10_INPLACE on );

  /// @ingroup linalg_inplace
  /// @brief Perform matrix multiplication \c A*B.
  /// 
  /// @param[out] matout On exit, \c matout is overwritten by \c A*B.
  /// @param[in] kblk1 Matrix \c A.
  /// @param[in] kblk2 Matrix \c B.
  template<typename To, typename T, typename U> 
    void Dot( Matrix<To>& matout, const Block<T>& kblk1, const Block<U>& kblk2, UNI10_INPLACE on );

  template<typename T> 
    void Dot( Matrix<uni10_complex128>& matout, const Block<T>& kblk, UNI10_INPLACE on ){

      uni10_error_msg(on != 1, "%s", "Setting a wrong flag of uni10_Inplace." );

      uni10_error_msg(matout.col_ != kblk.row_, "%s", "The dimensions of the two matrices do not match for matrix multiplication.");

      Matrix<uni10_complex128> tmpmat(matout.row_, kblk.col_, matout.diag_ && kblk.diag_);

      linalg_unielem_internal::Dot(&matout.elem_, &matout.diag_, &kblk.elem_, &kblk.diag_, &matout.row_, &kblk.col_, &matout.col_, &tmpmat.elem_);

      matout = tmpmat;

    }

  template<typename To, typename T, typename U> 
    void Dot( Matrix<To>& matout, const Block<T>& kblk1, const Block<U>& kblk2, UNI10_INPLACE on ){
      
      uni10_error_msg(on != 1, "%s", "Setting a wrong flag of uni10_Inplace." );

      uni10_error_msg(kblk1.col_ != kblk2.row_, "%s", "The dimensions of the two matrices do not match for matrix multiplication.");
      //Lack of error msgs.
      //
      matout.Assign(kblk1.row_, kblk2.col_, kblk1.diag_ && kblk2.diag_);

      linalg_unielem_internal::Dot(&kblk1.elem_, &kblk1.diag_, &kblk2.elem_, &kblk2.diag_, &kblk1.row_, &kblk2.col_, &kblk1.col_, &matout.elem_);

    }

}

#endif
