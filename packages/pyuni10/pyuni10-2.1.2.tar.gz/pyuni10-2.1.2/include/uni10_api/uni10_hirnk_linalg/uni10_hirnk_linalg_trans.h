#ifndef __UNI10_HIGH_RANK_LINALG_TRANS_H__
#define __UNI10_HIGH_RANK_LINALG_TRANS_H__

#include "uni10_api/uni10_hirnk_linalg_inplace/uni10_hirnk_linalg_inplace_trans.h"

namespace uni10{

  /// @ingroup hirnklin
  /// @brief Take transpose of a tensor.
  /// 
  /// Take transpose of the incoming and outgoing bonds. 
  /// @param[in] T Input tensor.
  /// @return The resulting tensor.
  template<typename UniType>
    UniTensor<UniType> Transpose( const UniTensor<UniType>& kten );

  template<typename UniType>
    UniTensor<UniType> Transpose( const UniTensor<UniType>& kten ){

      UniTensor<UniType> outten;
      Transpose(outten, kten, INPLACE);
      return outten;

    }

};

#endif
