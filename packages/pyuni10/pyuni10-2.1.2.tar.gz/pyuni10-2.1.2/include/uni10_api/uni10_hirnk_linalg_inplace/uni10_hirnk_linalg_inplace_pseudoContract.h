#ifndef __UNI10_HIGH_RANK_LINALG_INPLACE_PSEUDOCONTRACT_H__
#define __UNI10_HIGH_RANK_LINALG_INPLACE_PSEUDOCONTRACT_H__

#include "uni10_api/uni10_hirnk_linalg/uni10_hirnk_linalg_pseudoPermute.h"
#include "uni10_api/tensor_tools/tensor_tools.h"

namespace uni10{

	// It's a temporary version of pseudo contract.
	// Treat the input tensor as bosonic and perform permutation.
	// Tensor would retain the original style after pseudo contract.

	template<typename To, typename T, typename U>
		void PseudoContract( UniTensor<To>& t3, const UniTensor<T>& t1, const UniTensor<U>& t2, UNI10_INPLACE on);

	template<typename To, typename T, typename U>
		void PseudoContract( UniTensor<To>& t3, const UniTensor<T>& t1, const UniTensor<U>& t2, UNI10_INPLACE on){

			uni10_error_msg(on != 1, "%s", "Setting a wrong flag of uni10_Inplace." );
			uni10_error_msg(!((*t1.status) & (*t2.status) & t1.HAVEELEM), "%s" ,"Cannot perform Contraction of two tensors before setting their elements.");

			if((void*)&t1 == (void*)&t2 || (void*)&t3 == (void*)&t2){
        UniTensor<U> tmp(t2);
        PseudoContract(t3, t1, tmp, on);
        return ;
      }

      if((void*)&t3 == (void*)&t1){
        UniTensor<T> tmp(t1);
        PseudoContract(t3, tmp, t2, on);
        return ;
      }

      if((*t1.status) & t1.HAVEBOND && (*t2.status) & t1.HAVEBOND){

        uni10_int crossbondnum = (t1.style == no_sym) ? tensor_tools::contract( t1.paras, t2.paras, t3, t1.style) : tensor_tools::contract( t1.paras, t2.paras, t3, bs_sym );

        if(crossbondnum == 0){

          UniTensor<To> tmp(t3);

          std::vector<uni10_int> t1_labels = t1.label();
          std::vector<uni10_int> t2_labels = t2.label();
          std::vector<uni10_int> t3_rsplabels(t3.BondNum());
          
          uni10_int idx = 0;
          for(uni10_int i = 0; i < t1.InBondNum(); i++){
            t3_rsplabels[idx] = t1_labels[i];
            idx++;
          }
          for(uni10_int i = 0; i < t2.InBondNum(); i++){
            t3_rsplabels[idx] = t2_labels[i];
            idx++;
          }
          for(uni10_int i = t1.InBondNum(); i < t1.BondNum(); i++){
            t3_rsplabels[idx] = t1_labels[i];
            idx++;
          }
          for(uni10_int i = t2.InBondNum(); i < t2.BondNum(); i++){
            t3_rsplabels[idx] = t2_labels[i];
            idx++;
          }

          PseudoPermute(t3, tmp, t3_rsplabels, t1.InBondNum()+t2.InBondNum(), INPLACE);

        }

      }
      else if((*t1.status) & t1.HAVEBOND)
        t3 = t1 * t2[0];
      else if((*t2.status) & t2.HAVEBOND)
        t3 = t1[0] * t2;
      else
        t3 = UniTensor<To>(t1[0] * t2[0]);

		}

};

#endif
