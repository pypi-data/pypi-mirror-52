#ifndef __UNI10_HIGH_RANK_LINALG_INPLACE_CONTRACT_H__
#define __UNI10_HIGH_RANK_LINALG_INPLACE_CONTRACT_H__

#include "uni10_api/uni10_hirnk_linalg/uni10_hirnk_linalg_permute.h"
#include "uni10_api/tensor_tools/tensor_tools.h"

namespace uni10{

  /// @ingroup hirnklin_inplace
  /// @brief Contract two tensors.
  ///
  /// Contract the bonds of with same labels.
  /// @param[in] t1, t2 Input tensor.
  /// @param[out] t3 The resulting tensor.
  template<typename To, typename T, typename U>
    void Contract( UniTensor<To>& t3, const UniTensor<T>& t1, const UniTensor<U>& t2, UNI10_INPLACE on);

  template<typename To, typename T, typename U>
    void Contract( UniTensor<To>& t3, const UniTensor<T>& t1, const UniTensor<U>& t2, UNI10_INPLACE on){

      uni10_error_msg(on != 1, "%s", "Setting a wrong flag of uni10_Inplace." );
      uni10_error_msg(!((*t1.status) & (*t2.status) & t1.HAVEELEM), "%s" ,"Cannot perform Contraction of two tensors before setting their elements.");

      if((void*)&t1 == (void*)&t2 || (void*)&t3 == (void*)&t2){
        UniTensor<U> tmp(t2);
        Contract(t3, t1, tmp, on);
        return ;
      }

      if((void*)&t3 == (void*)&t1){
        UniTensor<T> tmp(t1);
        Contract(t3, tmp, t2, on);
        return ;
      }

      if((*t1.status) & t1.HAVEBOND && (*t2.status) & t1.HAVEBOND){

        uni10_int crossbondnum = tensor_tools::contract( t1.paras, t2.paras, t3, t1.style );

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

          Permute(t3, tmp, t3_rsplabels, t1.InBondNum()+t2.InBondNum(), INPLACE);

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
