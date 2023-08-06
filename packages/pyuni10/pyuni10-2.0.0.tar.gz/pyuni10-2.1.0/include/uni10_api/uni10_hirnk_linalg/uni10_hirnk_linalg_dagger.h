#ifndef __UNI10_HIGH_RANK_LINALG_DAGGER_H__
#define __UNI10_HIGH_RANK_LINALG_DAGGER_H__

#include "uni10_api/uni10_hirnk_linalg_inplace/uni10_hirnk_linalg_inplace_dagger.h"

namespace uni10{

  /// @ingroup hirnklin
  /// @brief Take conjugate transpose of a tensor.
  ///
  /// Take complex conjugate of each elements of a tensor, and take transpose of the incoming and outgoing bonds. 
  /// @param[in] kten Input tensor.
  /// @return The resulting tensor.
  template<typename UniType>
    UniTensor<UniType> Dagger( const UniTensor<UniType>& kten );

  template<typename UniType>
    UniTensor<UniType> Dagger( const UniTensor<UniType>& kten ){

      UniTensor<UniType> outten;
      Dagger(outten, kten, INPLACE);
      return outten;

    }

};

#endif
