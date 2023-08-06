#ifndef __UNI10_HIGH_RANK_LINALG_INPLACE_PSEUDOPERMUTE_H__
#define __UNI10_HIGH_RANK_LINALG_INPLACE_PSEUDOPERMUTE_H__

#include "uni10_api/tensor_tools/tensor_tools.h"

namespace uni10{

  // It's a temporary version of pseudo permute.
  // Treat the input tensor as bosonic and perform permutation.
  // Tensor would retain the original style after pseudo permute.

  template<typename UniType>
	 void PseudoPermute( UniTensor<UniType>& Tout, const UniTensor<UniType>& T, const std::vector<uni10_int>& newLabels, uni10_int rowBondNum, UNI10_INPLACE on);

  template<typename UniType>
	 void PseudoPermute( UniTensor<UniType>& Tout, const UniTensor<UniType>& T, uni10_int* newLabels, uni10_int rowBondNum, UNI10_INPLACE on);

  template<typename UniType>
	 void PseudoPermute( UniTensor<UniType>& Tout, const UniTensor<UniType>& T, uni10_int rowBondNum, UNI10_INPLACE on);

  template<typename UniType>
	 void PseudoPermute( UniTensor<UniType>& T, const std::vector<uni10_int>& newLabels, uni10_int rowBondNum, UNI10_INPLACE on);

  template<typename UniType>
	 void PseudoPermute( UniTensor<UniType>& T, uni10_int* newLabels, uni10_int rowBondNum, UNI10_INPLACE on);

  template<typename UniType>
	 void PseudoPermute( UniTensor<UniType>& T, uni10_int rowBondNum, UNI10_INPLACE on);

  template<typename UniType>
	 void PseudoPermute( UniTensor<UniType>& Tout, const UniTensor<UniType>& T, const std::vector<uni10_int>& newLabels, uni10_int rowBondNum, UNI10_INPLACE on){
	  uni10_error_msg(on != 1, "%s", "Setting a wrong flag of uni10_Inplace." );
      uni10_error_msg(*T.status & (UniTensor<UniType>::GET_HAVEBOND == 0), "%s", "There is no bond in the tensor(scalar) to Permute.");
      uni10_error_msg((T.labels->size() == newLabels.size()) == 0, "%s", "The size of the input new labels does not match for the number of bonds.");

      uni10_int bondNum = T.bonds->size();
      std::vector<uni10_int> rsp_idx(bondNum);
      uni10_int cnt = 0;
      for(uni10_int i = 0; i < bondNum; i++)
        for(uni10_int j = 0; j < bondNum; j++)
          if((*T.labels)[i] == newLabels[j]){
            rsp_idx[j] = i;
            cnt++;
          }

      uni10_error_msg((cnt == (uni10_int)newLabels.size()) == 0, "%s", "The input new labels do not 1-1 correspond to the labels of the tensor.");

      uni10_bool inorder = true;

      for(uni10_int i = 1; i < bondNum; i++)
        if(rsp_idx[i] != i){
          inorder = false;
          break;
        }

      if(inorder && (*T.RBondNum) == rowBondNum) {
        Tout = T;
        return ;
      } 
      else{

        std::vector<Bond> outBonds;
        for(uni10_int b = 0; b < (uni10_int)T.bonds->size(); b++){
          outBonds.push_back((*T.bonds)[rsp_idx[b]]);
        }
        for(uni10_int b = 0; b < (uni10_int)T.bonds->size(); b++){
          if(b < rowBondNum)
            outBonds[b].change(BD_IN);
          else
            outBonds[b].change(BD_OUT);
        }
        Tout.Assign(outBonds);
        Tout.SetName(*T.name);

        if((*T.status) & UniTensor<UniType>::GET_HAVEELEM())
          (T.style == no_sym) ? tensor_tools::permute(T.paras, rsp_idx, Tout.paras, inorder, T.style) : tensor_tools::permute(T.paras, rsp_idx, Tout.paras, inorder, bs_sym);

        *Tout.status |= UniTensor<UniType>::GET_HAVEELEM();
        Tout.SetStyle(T.style);
        Tout.SetLabel(newLabels);

      }

	}

  template<typename UniType>
	 void PseudoPermute( UniTensor<UniType>& Tout, const UniTensor<UniType>& T, uni10_int* newLabels, uni10_int rowBondNum, UNI10_INPLACE on){
		std::vector<uni10_int> _labels(newLabels, newLabels + T.bond().size());
		PseudoPermute( Tout, T, _labels, rowBondNum, on);

	}

  template<typename UniType>
	 void PseudoPermute( UniTensor<UniType>& Tout, const UniTensor<UniType>& T, uni10_int rowBondNum, UNI10_INPLACE on){
		std::vector<uni10_int> ori_labels = T.label();
		PseudoPermute( Tout, T, ori_labels, rowBondNum, on);
	
	}

  template<typename UniType>
	 void PseudoPermute( UniTensor<UniType>& T, const std::vector<uni10_int>& newLabels, uni10_int rowBondNum, UNI10_INPLACE on){
		UniTensor<UniType> Tout;
		PseudoPermute( Tout, T, newLabels, rowBondNum, on);
		T = Tout;

	}

  template<typename UniType>
	 void PseudoPermute( UniTensor<UniType>& T, uni10_int* newLabels, uni10_int rowBondNum, UNI10_INPLACE on){
		UniTensor<UniType> Tout;
		PseudoPermute( Tout, T, newLabels, rowBondNum, on);
		T = Tout;

	}

  template<typename UniType>
	 void PseudoPermute( UniTensor<UniType>& T, uni10_int rowBondNum, UNI10_INPLACE on){
		UniTensor<UniType> Tout;
		PseudoPermute( Tout, T, rowBondNum, on);
		T = Tout;

	}


};

#endif
