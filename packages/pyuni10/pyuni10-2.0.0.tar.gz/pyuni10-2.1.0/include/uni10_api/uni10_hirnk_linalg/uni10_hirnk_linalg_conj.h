#ifndef __UNI10_HIGH_RANK_LINALG_CONJ_H__
#define __UNI10_HIGH_RANK_LINALG_CONJ_H__

#include "uni10_api/uni10_hirnk_linalg_inplace/uni10_hirnk_linalg_inplace_conj.h"

namespace uni10{

  /// @ingroup hirnklin
  /// @brief Take complex conjugate of a tensor.
  ///
  /// Take complex conjugate of each elements of a tensor. 
  /// @param[in] kten Input tensor.
  /// @return The resulting tensor.
  template<typename UniType>
    UniTensor<UniType> Conj( const UniTensor<UniType>& kten );

  template<typename UniType>
    UniTensor<UniType> Conj( const UniTensor<UniType>& kten ){

      UniTensor<UniType> outten;
      Conj(outten, kten, INPLACE);
      return outten;

    }

};

#endif
