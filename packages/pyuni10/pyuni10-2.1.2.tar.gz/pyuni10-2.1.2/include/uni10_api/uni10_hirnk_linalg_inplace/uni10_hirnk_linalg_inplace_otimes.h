#ifndef __UNI10_HIGH_RANK_LINALG_INPLACE_OTIMES_H__
#define __UNI10_HIGH_RANK_LINALG_INPLACE_OTIMES_H__

#include "uni10_api/uni10_hirnk_linalg_inplace/uni10_hirnk_linalg_inplace_contract.h"

namespace uni10{

  /// @ingroup hirnklin_inplace
  /// @brief Take direct product of two tensors.
  /// 
  /// @param[in] kten1, kten2 Input tensor.
  /// @param[out] outten The resulting tensor.
  template<typename To, typename T, typename U>
    void Otimes( UniTensor<To>& outten, const UniTensor<T>& kten1, const UniTensor<U>& kten2, UNI10_INPLACE on);

  /// @ingroup hirnklin_inplace
  /// @brief Take direct product of two matrices.
  /// 
  /// @param[in] kten1, ketn2 Input matrices.
  /// @param[out] outmat The resulting matrix.
  template<typename To, typename T, typename U>
    void Otimes( Matrix<To>& outmat, const Block<T>& kten1, const Block<U>& kten2, UNI10_INPLACE on);

  template<typename To, typename T, typename U>
    void Otimes( UniTensor<To>& outten, const UniTensor<T>& kten1, const UniTensor<U>& kten2, UNI10_INPLACE on){

      uni10_error_msg(on != 1, "%s", "Setting a wrong flag of uni10_Inplace." );
      
      UniTensor<T> ten1 = kten1;
      UniTensor<U> ten2 = kten2;
      std::vector<uni10_int> label1(ten1.BondNum());
      std::vector<uni10_int> label2(ten2.BondNum());
      for(uni10_uint64 i = 0; i < ten1.BondNum(); i++){
        if(i < ten1.InBondNum())
          label1[i] = i;
        else
          label1[i] = ten2.InBondNum() + i;
      }
      for(uni10_uint64 i = 0; i < ten2.BondNum(); i++){
        if(i < ten2.InBondNum())
          label2[i] = i + ten1.InBondNum();
        else
          label2[i] = i + ten1.BondNum();
      }
      ten1.SetLabel(label1);
      ten2.SetLabel(label2);

      Contract(outten, ten1, ten2, on);

    }

  template<typename To, typename T, typename U>
    void Otimes( Matrix<To>& outmat, const Block<T>& kten1, const Block<U>& kten2, UNI10_INPLACE on){

      uni10_error_msg(on != 1, "%s", "Setting a wrong flag of uni10_Inplace." );

      UniTensor<T> ten1(kten1);
      UniTensor<U> ten2(kten2);
      std::vector<uni10_int> label1(ten1.BondNum());
      std::vector<uni10_int> label2(ten2.BondNum());
      for(uni10_uint64 i = 0; i < ten1.BondNum(); i++){
        if(i < ten1.InBondNum())
          label1[i] = i;
        else
          label1[i] = ten2.InBondNum() + i;
      }
      for(uni10_uint64 i = 0; i < ten2.BondNum(); i++){
        if(i < ten2.InBondNum())
          label2[i] = i + ten1.InBondNum();
        else
          label2[i] = i + ten1.BondNum();
      }
      ten1.SetLabel(label1);
      ten2.SetLabel(label2);

      UniTensor<To> outten;
      Contract(outten, ten1, ten2, INPLACE);
      outmat = outten.ConstGetBlock();

    }

};

#endif
