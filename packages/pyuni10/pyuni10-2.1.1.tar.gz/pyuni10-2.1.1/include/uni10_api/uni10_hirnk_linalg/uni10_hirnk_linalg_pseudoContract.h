#ifndef __UNI10_HIGH_RANK_LINALG_PSEUDOCONTRACT_H__
#define __UNI10_HIGH_RANK_LINALG_PSEUDOCONTRACT_H__

#include "uni10_api/uni10_hirnk_linalg_inplace/uni10_hirnk_linalg_inplace_pseudoContract.h"

namespace uni10{

	// It's a temporary version of pseudo permute.
  // Treat the input tensor as bosonic and perform permutation.
  // Tensor would retain the original style after pseudo permute.

  template<typename T>
    UniTensor<T> PseudoContract(const UniTensor<uni10_double64>& Ta, const UniTensor<T>& Tb);

  template<typename T>
    UniTensor<uni10_complex128> PseudoContract(const UniTensor<uni10_complex128>& Ta, const UniTensor<T>& Tb);

  template<typename T>
    UniTensor<T> PseudoContract(const UniTensor<uni10_double64>& Ta, const UniTensor<T>& Tb){

      UniTensor<T> Tout;
      PseudoContract(Tout, Ta, Tb, INPLACE);
      return Tout;

    }

  template<typename T>
    UniTensor<uni10_complex128> PseudoContract(const UniTensor<uni10_complex128>& Ta, const UniTensor<T>& Tb){

      UniTensor<uni10_complex128> Tout;
      PseudoContract(Tout, Ta, Tb, INPLACE);
      return Tout;

    }

};

#endif
