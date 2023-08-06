#ifndef __UNI10_LINALG_INPLACE_SVD_H__
#define __UNI10_LINALG_INPLACE_SVD_H__

#include "uni10_api/Matrix.h"

namespace uni10{

  /// @ingroup linalg_inplace
  /// @brief Perform singular value decomposition
  /// 
  /// Factor the matrix \c kblk as \c u*s*vt.
  /// @param[in] kblk Matrix to be factored.
  /// @param[out] u A unitary matrix.
  /// @param[out] s A diagonal matrix with singular values at diagonal element stored in descending order.
  /// @param[out] vt The transpose of a unitary matrix \c v.
  template<typename uni10_type>
    void Svd( const Block<uni10_type>& kblk, Matrix<uni10_type>& u, Matrix<uni10_type>& s, Matrix<uni10_type>& vt, UNI10_INPLACE on );

  template<typename uni10_type>
    void Svd( const Block<uni10_type>& kblk, Matrix<uni10_type>& u, Matrix<uni10_type>& s, Matrix<uni10_type>& vt, UNI10_INPLACE on ){

      uni10_error_msg(on != 1, "%s", "Setting a wrong flag of uni10_Inplace." );

      uni10_uint64 min = kblk.row_ < kblk.col_ ? kblk.row_ : kblk.col_;      //min = min(row_,col_)
      s.Assign(min, min, true);

      UELEM(UniElem, _package, _type)<uni10_type>* u_elem  = NULL;     // pointer to a real matrix
      UELEM(UniElem, _package, _type)<uni10_type>* vt_elem = NULL;     // pointer to a real matrix

      if(&u != NULL){
        u.Assign(kblk.row_, min);
        u_elem = &u.elem_;
      }

      if(&vt != NULL){
        vt.Assign(min, kblk.col_);
        vt_elem = &vt.elem_;
      }

      linalg_unielem_internal::Svd(&kblk.elem_, &kblk.diag_, &kblk.row_, &kblk.col_, u_elem, &s.elem_, vt_elem);

    }

}

#endif
