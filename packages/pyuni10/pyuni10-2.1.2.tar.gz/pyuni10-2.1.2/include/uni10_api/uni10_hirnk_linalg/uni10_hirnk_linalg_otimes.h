#ifndef __UNI10_HIGH_RANK_LINALG_OTIMES_H__
#define __UNI10_HIGH_RANK_LINALG_OTIMES_H__

#include "uni10_api/uni10_hirnk_linalg_inplace/uni10_hirnk_linalg_inplace_otimes.h"
namespace uni10{

  template<typename T>
    UniTensor<uni10_complex128> Otimes(const UniTensor<uni10_complex128>& Ta, const UniTensor<T>& Tb);

  /// @ingroup hirnklin
  /// @brief Take direct product of two tensors.
  /// 
  /// @param[in] Ta, Tb Input tensor.
  /// @return The resulting tensor.
  template<typename T>
    UniTensor<T> Otimes(const UniTensor<uni10_double64>& Ta, const UniTensor<T>& Tb);

  template<typename T>
    Matrix<uni10_complex128> Otimes(const Block<uni10_complex128>& Ta, const Block<T>& Tb);

  /// @ingroup hirnklin
  /// @brief Take direct product of two matrices.
  /// 
  /// @param[in] Ta, Tb Input matrices.
  /// @return The resulting matrices.
  template<typename T>
    Matrix<T> Otimes(const Block<uni10_double64>& Ta, const Block<T>& Tb);


  template<typename T>
    UniTensor<uni10_complex128> Otimes(const UniTensor<uni10_complex128>& Ta, const UniTensor<T>& Tb){

      UniTensor<uni10_complex128> Tout;
      Otimes(Tout, Ta, Tb, INPLACE);
      return Tout;

    }

  template<typename T>
    UniTensor<T> Otimes(const UniTensor<uni10_double64>& Ta, const UniTensor<T>& Tb){

      UniTensor<T> Tout;
      Otimes(Tout, Ta, Tb, INPLACE);
      return Tout;

    }

  template<typename T>
    Matrix<uni10_complex128> Otimes(const Block<uni10_complex128>& Ma, const Block<T>& Mb){

      Matrix<uni10_complex128> Mout;
      Otimes(Mout, Ma, Mb, INPLACE);
      return Mout;

    }

  template<typename T>
    Matrix<T> Otimes(const Block<uni10_double64>& Ma, const Block<T>& Mb){

      Matrix<T> Mout;
      Otimes(Mout, Ma, Mb, INPLACE);
      return Mout;

    }

};

#endif
