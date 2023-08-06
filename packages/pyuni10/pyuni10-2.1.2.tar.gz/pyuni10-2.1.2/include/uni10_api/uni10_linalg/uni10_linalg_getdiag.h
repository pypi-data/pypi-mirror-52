#ifndef __UNI10_LINALG_GETDIAG_H__
#define __UNI10_LINALG_GETDIAG_H__

#include <vector>

#include "uni10_api/Block.h"
#include "uni10_api/Matrix.h"

namespace uni10{

  /// @ingroup linalg
  /// @brief Get the diaongal elements of a matrix.
  /// 
  /// @param[in] kblk Input matrix.
  /// @return A matrix with same diagonal element with \c kblk and other elements are zero.
  template<typename UniType> 
    Matrix<UniType> GetDiag( const Block<UniType>& kblk );

  template<typename UniType> 
    Matrix<UniType> GetDiag( const Block<UniType>& kblk ){

      if(kblk.diag_){
        Matrix<UniType> diagmat(kblk);
        return diagmat;
      }
      else{
        Matrix<UniType> diagmat(kblk.row_, kblk.col_, true);
        uni10_error_msg(true, "%s", "Developping!!!");
        return diagmat;
      }

    }

}

#endif
