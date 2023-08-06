#ifndef __UNI10_LINALG_INPLACE_CONJ_H__
#define __UNI10_LINALG_INPLACE_CONJ_H__

#include "uni10_api/Matrix.h"

/// @defgroup linalg_inplace linear algebra inplace
/// @brief The functions in linear algebra inplace provide the overloaded functions of those in linear algebra. The difference is that user should declare the result as a variable before calling the function and pass them as an argument. It will be overwritten by the result on exit. The last augument should set to \c UNI10_INPLACE when calling these functions.
namespace uni10{

  /// @ingroup linalg_inplace
  /// @brief Takes complex conjugate of a matrix.
  /// 
  /// @param[out] matout Complex conjugate of \c kmat. Original contents of \c matout will be replaced.
  /// @param[in] kamt Input matrix.
  template<typename UniType>
    void Conj( Matrix<UniType>& matout, const Block<UniType>& kblk, UNI10_INPLACE on );

  /// @ingroup linalg_inplace
  /// @brief Takes complex conjugate of a matrix.
  /// 
  /// @param[in,out] matout On entry, \c matout is the input matrix. On exit, \c matout is overwritten by its complex cojugate.
  template<typename UniType>
    void Conj( Matrix<UniType>& matout, UNI10_INPLACE on );

  template<typename UniType>
    void Conj( Matrix<UniType>& matout, const Block<UniType>& kblk, UNI10_INPLACE on ){

      uni10_error_msg(on != 1, "%s", "Setting a wrong flag of uni10_Inplace." );

      matout.Assign(kblk.row_, kblk.col_);
      linalg_unielem_internal::Conjugate(&kblk.elem_, &matout.elem_.elem_num_, &matout.elem_);

    }

  template<typename UniType>
    void Conj( Matrix<UniType>& matout, UNI10_INPLACE on ){

      uni10_error_msg(on != 1, "%s", "Setting a wrong flag of uni10_Inplace." );

      linalg_unielem_internal::Conjugate(&matout.elem_, &matout.elem_.elem_num_);

    }

};

#endif
