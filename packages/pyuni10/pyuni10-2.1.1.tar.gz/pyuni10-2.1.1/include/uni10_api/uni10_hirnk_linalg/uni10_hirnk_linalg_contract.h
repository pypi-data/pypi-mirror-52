#ifndef __UNI10_HIGH_RANK_LINALG_CONTRACT_H__
#define __UNI10_HIGH_RANK_LINALG_CONTRACT_H__

#include "uni10_api/uni10_hirnk_linalg_inplace/uni10_hirnk_linalg_inplace_contract.h"

namespace uni10{

  /// @ingroup hirnklin
  /// @brief Contract two tensors.
  /// 
  /// Contract the bonds of with same labels.
  /// @param[in] Ta, Tb Input tensor.
  /// @return The resulting tensor.
  template<typename T>
    UniTensor<T> Contract(const UniTensor<uni10_double64>& Ta, const UniTensor<T>& Tb);

  template<typename T>
    UniTensor<uni10_complex128> Contract(const UniTensor<uni10_complex128>& Ta, const UniTensor<T>& Tb);

  template<typename T>
    UniTensor<T> Contract(const UniTensor<uni10_double64>& Ta, const UniTensor<T>& Tb){

      UniTensor<T> Tout;
      Contract(Tout, Ta, Tb, INPLACE);
      return Tout;

    }

  template<typename T>
    UniTensor<uni10_complex128> Contract(const UniTensor<uni10_complex128>& Ta, const UniTensor<T>& Tb){

      UniTensor<uni10_complex128> Tout;
      Contract(Tout, Ta, Tb, INPLACE);
      return Tout;

    }

};

#endif
