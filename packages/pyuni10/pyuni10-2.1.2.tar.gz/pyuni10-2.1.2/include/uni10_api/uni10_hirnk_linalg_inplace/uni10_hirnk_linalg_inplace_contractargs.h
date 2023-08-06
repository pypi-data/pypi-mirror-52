#ifndef __UNI10_HIGH_RANK_LINALG_INPLACE_CONTRACT_ARGS_H__
#define __UNI10_HIGH_RANK_LINALG_INPLACE_CONTRACT_ARGS_H__

#include "uni10_api/UniTensor.h"
#include "uni10_api/Network.h"

#include "uni10_api/uni10_hirnk_linalg_inplace/uni10_hirnk_linalg_inplace_contracts.h"

namespace uni10{

  template<typename UniTo>
    void _ContractArgs( UniTo& outten, Network& ctr_net, uni10_uint64& idx);

  template<typename UniTo, typename UniTi, typename ... Args>
    void _ContractArgs( UniTo& outten, Network& ctr_net, uni10_uint64& idx, const UniTi& T1, const Args&... args);

  /// @ingroup hirnklin_inplace
  /// @brief Contract an array of tensors with given Network.
  ///
  /// Contract the whole tensor network as specified in Network object. The order of passing tensors should be the same as written in Network files.
  /// @see Network
  /// @param[out] outten The resulting tensor.
  /// @param[in] ctr_net Network object.
  /// @param[in] T1 The first tensor.
  /// @param[in] Args The other tensors.
  template<typename UniTo, typename UniTi, typename ... Args>
    void ContractArgs( UniTo& outten, Network& ctr_net, const UniTi& T1, const Args&... args);

  //
  // ContractArgs without Network. Before using this function, users have to set the suitable labers on each UniTensors' bonds.
  // 
  template<typename UniTo>
    void _ContractArgs( UniTo& outten, std::vector< std::pair<void*, int> >& ulist);

  template<typename UniTo, typename UniTi, typename ... Args>
    void _ContractArgs( UniTo& outten, std::vector< std::pair<void*, int> >& ulist, const UniTi& T1, const Args&... args);

  template<typename UniTo, typename UniTi, typename ... Args>
    void ContractArgs( UniTo& outten, const UniTi& T1, const Args&... args);

  template<typename UniTo>
    void _ContractArgs( UniTo& outten, Network& ctr_net, uni10_uint64& idx){
      ctr_net.Launch(outten);
    }

  template<typename UniTo, typename UniTi, typename ... Args>
    void _ContractArgs( UniTo& outten, Network& ctr_net, uni10_uint64& idx, const UniTi& T1, const Args&... args){
      ctr_net.PutTensor(idx, T1);
      idx++;
      _ContractArgs(outten, ctr_net, idx, args...);
    }

  template<typename UniTo, typename UniTi, typename ... Args>
    void ContractArgs( UniTo& outten, Network& ctr_net, const UniTi& T1, const Args&... args){
      uni10_uint64 idx = 0;
      _ContractArgs(outten, ctr_net, idx, T1, args...);
    }

  template<typename UniTo>
    void _ContractArgs( UniTo& outten, std::vector< std::pair<void*, int> >& ulist){

      std::pair<bool, uni10_int> isMix_TrLen(false, 0);

      bool isTc = false;

      uni10_int cnt_Tr = 0;

      for(uni10_uint64 i = 0; i < ulist.size(); i++){

        if(ulist[i].second == 2)
          isTc = true;

        if(ulist[i].second == 1 && !isTc)
          cnt_Tr++;

        if(i == 0)
          continue;

        else if(ulist[i-1].second != ulist[i].second){

          isMix_TrLen = std::pair<bool, uni10_int>(true, cnt_Tr);

        }

      }

      if(isMix_TrLen.first == false){

        ContractsPure(outten, ulist, INPLACE);

      }
      else{

        ContractsMix(outten, ulist, isMix_TrLen, INPLACE);
      }

    }

  template<typename UniTo, typename UniTi, typename ... Args>
    void _ContractArgs( UniTo& outten, std::vector< std::pair<void*, int> >& ulist, const UniTi& T1, const Args&... args){

      ulist.push_back(std::pair<void*, int>((void*)&T1, T1.TypeId()));
      _ContractArgs(outten, ulist, args...);

    }


  template<typename UniTo, typename UniTi, typename ... Args>
    void ContractArgs( UniTo& outten, const UniTi& T1, const Args&... args){

      std::vector< std::pair<void*, int> > ulist;
      _ContractArgs(outten, ulist, T1, args...);

    }

};

#endif
