#ifndef __UNI10_HIGH_RANK_LINALG_PSEUDOPERMUTE_H__
#define __UNI10_HIGH_RANK_LINALG_PSEUDOPERMUTE_H__

#include "uni10_api/uni10_hirnk_linalg_inplace/uni10_hirnk_linalg_inplace_pseudoPermute.h"

namespace uni10{

  // It's a temporary version of pseudo permute.
  // Treat the input tensor as bosonic and perform permutation.
  // Tensor would retain the original style after pseudo permute.
  
  template<typename UniType>
	UniTensor<UniType> PseudoPermute( const UniTensor<UniType>& T, const std::vector<uni10_int>& newLabels, uni10_int rowBondNum);

  template<typename UniType>
	UniTensor<UniType> PseudoPermute( const UniTensor<UniType>& T, uni10_int* newLabels, uni10_int rowBondNum);

  template<typename UniType>
    UniTensor<UniType> PseudoPermute( const UniTensor<UniType>& T, uni10_int rowBondNum);

  template<typename UniType>
	UniTensor<UniType> PseudoPermute( const UniTensor<UniType>& T, const std::vector<uni10_int>& newLabels, uni10_int rowBondNum){
	  uni10_error_msg((*T.status) & UniTensor<UniType>::GET_HAVEBOND == 0, "%s", "There is no bond in the tensor(scalar) to Permute.");
      uni10_error_msg((T.labels->size() == newLabels.size()) == 0, "%s", "The size of the input new labels does not match for the number of bonds.");

      uni10_int bondNum = T.bonds->size();
      std::vector<uni10_int> rsp_outin(bondNum);
      uni10_int cnt = 0;
      for(uni10_int i = 0; i < bondNum; i++)
        for(uni10_int j = 0; j < bondNum; j++)
          if((*T.labels)[i] == newLabels[j]){
            rsp_outin[j] = i;
            cnt++;
          }
      uni10_error_msg((cnt == newLabels.size()) == 0, "%s", "The input new labels do not 1-1 correspond to the labels of the tensor.");

      uni10_bool inorder = true;

      for(uni10_int i = 1; i < bondNum; i++)
        if(rsp_outin[i] != i){
          inorder = false;
          break;
        }
      if(inorder && (*T.RBondNum) == rowBondNum) {
        return T;
      }
      else{
        std::vector<Bond> outBonds;
        for(uni10_int b = 0; b < T.bonds->size(); b++){
          outBonds.push_back((*T.bonds)[rsp_outin[b]]);
        }
        for(uni10_uint64 b = 0; b < T.bonds->size(); b++){
          if(b < (uni10_uint64)rowBondNum)
            outBonds[b].change(BD_IN);
          else
            outBonds[b].change(BD_OUT);
        }
        UniTensor<UniType> Tout(outBonds, (*T.name));
        Tout.SetLabel(newLabels);

        // The version of one node gpu is Developping
        if((*T.status) & UniTensor<UniType>::GET_HAVEELEM())
          (T.style == no_sym) ? tensor_tools::permute(T.paras, rsp_outin, Tout.paras, inorder, T.style) : tensor_tools::permute(T.paras, rsp_outin, Tout.paras, inorder, bs_sym);

        Tout.SetStyle(T.style);
        *Tout.status |= UniTensor<UniType>::GET_HAVEELEM();

        return Tout;

      }

	}

  template<typename UniType>
	UniTensor<UniType> PseudoPermute( const UniTensor<UniType>& T, uni10_int* newLabels, uni10_int rowBondNum){

		std::vector<uni10_int> _labels(newLabels, newLabels + T.bond().size());
		return PseudoPermute(T, _labels, rowBondNum);

	}

  template<typename UniType>
    UniTensor<UniType> PseudoPermute( const UniTensor<UniType>& T, uni10_int rowBondNum){

    	std::vector<uni10_int> ori_labels = T.label();
    	return PseudoPermute(T, ori_labels, rowBondNum);
    	
    }


};

#endif
