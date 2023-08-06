#ifndef __UNI10_HIGH_RANK_LINALG_INPLACE_TRANS_H__
#define __UNI10_HIGH_RANK_LINALG_INPLACE_TRANS_H__

#include "uni10_api/tensor_tools/tensor_tools.h"

namespace uni10{

  /// @ingroup hirnklin_inplace
  /// @brief Take transpose of a tensor.
  /// 
  /// Take transpose of the incoming and outgoing bonds. 
  /// @param[in] kten Input tensor.
  /// @param[out] The resulting tensor.
  template<typename uni10_type>
    void Transpose( UniTensor<uni10_type>& outten, const UniTensor<uni10_type>& kten, UNI10_INPLACE on );

  /// @ingroup hirnklin_inplace
  /// @overload
  template<typename uni10_type>
    void Transpose( UniTensor<uni10_type>& T, UNI10_INPLACE on );

  template<typename uni10_type>
    void Transpose( UniTensor<uni10_type>& outten, const UniTensor<uni10_type>& kten, UNI10_INPLACE on ){

      uni10_error_msg(on != 1, "%s", "Setting a wrong flag of uni10_Inplace." );
      uni10_error_msg(!(*kten.status & UniTensor<uni10_type>::GET_HAVEBOND()), 
          "%s", "There is no bond in the tensor(scalar) to perform transposition.");

      uni10_uint64 bondNum = kten.bonds->size();
      std::vector<uni10_int32> rsp_outin(bondNum);
      uni10_int32 rbondNum = 0;
      for(uni10_uint64 b = 0; b < bondNum; b++)
        if((*kten.bonds)[b].type() == BD_IN)
          rbondNum++;
        else
          break;
      uni10_uint64 cbondNum = bondNum - rbondNum;
      for(uni10_uint64 b = 0; b < bondNum; b++)
        if(b < cbondNum)
          rsp_outin[b] = rbondNum + b;
        else
          rsp_outin[b] = b - cbondNum;
      std::vector<uni10_int32> outLabels(bondNum, 0);
      std::vector<Bond> outBonds;
      for(uni10_uint64 b = 0; b < kten.bonds->size(); b++){
        outBonds.push_back((*kten.bonds)[rsp_outin[b]]);
        outLabels[b] = (*kten.labels)[rsp_outin[b]];
      }
      for(uni10_uint64 b = 0; b < bondNum; b++){
        if(b < cbondNum)
          outBonds[b].type_enforce() = BD_IN;
        else
          outBonds[b].type_enforce() = BD_OUT;
      }
      
      outten.Assign(outBonds);
      outten.SetName(*kten.name);
      outten.SetLabel(outLabels);

      if((*kten.status) & UniTensor<uni10_type>::GET_HAVEELEM())
        tensor_tools::transpose(outten.paras, kten.paras, kten.style);

      *outten.status |= UniTensor<uni10_type>::GET_HAVEELEM();

    }

  template<typename uni10_type>
    void Transpose( UniTensor<uni10_type>& T, UNI10_INPLACE on ){

      UniTensor<uni10_type> Tt;
      Transpose(Tt, T, on);
      T = Tt;

    }


};

#endif
