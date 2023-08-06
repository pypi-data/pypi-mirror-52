#ifndef __UNI10_HIGH_RANK_LINALG_INPLACE_COJ_H__
#define __UNI10_HIGH_RANK_LINALG_INPLACE_COJ_H__

#include "uni10_api/tensor_tools/tensor_tools.h"

/// @defgroup hirnklin_inplace high-rank linear algebra inplace
/// @brief The functions in high linear algebra inplace provide the overloaded functions of those in high-rank linear algebra. The difference is that user should declare the result as a variable before calling the function and pass them as an argument. It will be overwritten by the result on exit. The last augument should set to \c UNI10_INPLACE when calling these functions.
namespace uni10{

  /// @ingroup hirnklin_inplace
  /// @brief Take complex conjugate of a tensor.
  ///
  /// Take complex conjugate of each elements of a tensor. 
  /// @param[in] kten Input tensor.
  /// @param[out] outten The resulting tensor.
  template<typename UniType>
    void Conj( UniTensor<UniType>& outten, const UniTensor<UniType>& kten, UNI10_INPLACE on);

  /// @ingroup hirnklin_inplace
  /// @overload
  template<typename UniType>
    void Conj( UniTensor<UniType>& outten, UNI10_INPLACE on);

  template<typename UniType>
    void Conj( UniTensor<UniType>& outten, const UniTensor<UniType>& kten, UNI10_INPLACE on){

      uni10_error_msg(on != 1, "%s", "Setting a wrong flag of uni10_Inplace." );
      uni10_error_msg(!(*kten.status & UniTensor<UniType>::GET_HAVEBOND()), 
          "%s", "There is no bond in the tensor(scalar) to perform transposition.");

      outten.Assign(*kten.bonds);
      outten.SetName(*kten.name);
      outten.SetLabel(*kten.labels);

      if((*kten.status) & UniTensor<UniType>::GET_HAVEELEM())
        tensor_tools::conj(outten.paras, kten.paras, kten.style);
        

      *outten.status |= UniTensor<UniType>::GET_HAVEELEM();

    }

  template<typename UniType>
    void Conj( UniTensor<UniType>& outten, UNI10_INPLACE on){

      UniTensor<UniType> tmpten;
      conj(tmpten, outten, on);
      outten = tmpten;

    }

};

#endif
