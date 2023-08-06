#ifndef __UNI10_HIGH_RANK_LINALG_INPLACE_PARTIALTRA_H__
#define __UNI10_HIGH_RANK_LINALG_INPLACE_PARTIALTRA_H__

#include "uni10_api/uni10_hirnk_linalg_inplace/uni10_hirnk_linalg_inplace_permute.h"
#include "uni10_api/tensor_tools/tensor_tools.h"

namespace uni10{

  /// @ingroup hirnklin_inplace
  /// @brief Take partial trace of given pair of bonds of a tensor.
  /// 
  /// @param[in] kten Input tensor.
  /// @param[in] la, lb Labels of bonds.
  /// @param[out] outten The resulting tensor.
  template<typename uni10_type>
    void ParticalTrace(UniTensor<uni10_type>& outten, const UniTensor<uni10_type>& kten, uni10_int32 la, uni10_int32 lb, UNI10_INPLACE on);

  /// @ingroup hirnklin_inplace
  /// @overload
  template<typename uni10_type>
    void ParticalTrace(UniTensor<uni10_type>& outten, uni10_int32 la, uni10_int32 lb, UNI10_INPLACE on);

  template<typename uni10_type>
    void ParticalTrace(UniTensor<uni10_type>& outten, uni10_int32 la, uni10_int32 lb, UNI10_INPLACE on){

      UniTensor<uni10_type> tmp;
      ParticalTrace(tmp, outten, la, lb, on);
      outten = tmp;

    }

  template<typename uni10_type>
    void ParticalTrace(UniTensor<uni10_type>& outten, const UniTensor<uni10_type>& kten, uni10_int32 la, uni10_int32 lb, UNI10_INPLACE on){

      uni10_error_msg(on != 1, "%s", "Setting a wrong flag of uni10_Inplace." );
      uni10_error_msg(!((*kten.status) & kten.HAVEELEM), "%s" ,"Cannot perform contraction of two tensors before setting their elements.");
      uni10_error_msg(!(kten.bonds->size() > 2), "%s", "The number of bonds must larger than 2 for performing ParticalTrace.");
      uni10_error_msg(&outten == &kten, "%s", 
          "The address of kten and outten are the same. Please use void ParticalTrace(UniTensor<uni10_type>& T, uni10_int32 la, uni10_int32 lb, UNI10_INPLACE on) instead.");


      uni10_int32 bondNum = kten.bonds->size();
      std::vector<Bond> newBonds;
      std::vector<uni10_int32>newLabels(bondNum - 2, 0);
      std::vector<uni10_int32>rsp_labels(bondNum);
      uni10_int32 ia, ib;
      uni10_int32 enc = 0;

      for(uni10_uint64 l = 0; l < kten.labels->size(); l++){
        if((*kten.labels)[l] == la)
          ia = l;
        else if((*kten.labels)[l] == lb)
          ib = l;
        else{
          newBonds.push_back((*kten.bonds)[l]);
          newLabels[enc] = (*kten.labels)[l];
          rsp_labels[enc] = (*kten.labels)[l];
          enc++;
        }
      }

      uni10_error_msg(!(enc == newLabels.size()), "%s", "Cannot find the two bonds with the given two labels.");

      outten.assign(newBonds);
      outten.setLabel(newLabels);
      rsp_labels[bondNum - 2] = (*kten.labels)[ia];
      rsp_labels[bondNum - 1] = (*kten.labels)[ib];
      ia = bondNum - 2;
      ib = bondNum - 1;

      UniTensor<uni10_type> pkten;
      Permute(pkten, kten, rsp_labels, *outten.RBondNum, INPLACE);

      tensor_tools::traceByRow(outten.paras, pkten.paras, ia, ib, pkten.style);

      *outten.status |= UniTensor<uni10_type>::GET_HAVEELEM();

    }

};

#endif
