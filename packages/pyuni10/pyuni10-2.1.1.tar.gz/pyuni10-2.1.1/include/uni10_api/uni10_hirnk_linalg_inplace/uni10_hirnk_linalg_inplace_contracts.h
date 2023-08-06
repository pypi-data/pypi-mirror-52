#ifndef __UNI10_HIGH_RANK_LINALG_INPLACE_CONTRACTS_H__
#define __UNI10_HIGH_RANK_LINALG_INPLACE_CONTRACTS_H__

#include "uni10_api/uni10_hirnk_linalg_inplace/uni10_hirnk_linalg_inplace_contract.h"

namespace uni10{

  // The driver fucntions of Non-type UniTensor contraction.
  inline void Contract_dd(void* m3, void* m1, void* m2){

    Contract( *((UniTensor<uni10_double64>*)m3), *((UniTensor<uni10_double64>*)m1), *((UniTensor<uni10_double64>*)m2), INPLACE);

  }

  inline void Contract_dz(void* m3, void* m1, void* m2){

    Contract( *((UniTensor<uni10_complex128 >*)m3), *((UniTensor<uni10_double64>*)m1), *((UniTensor<uni10_complex128 >*)m2), INPLACE);

  }

  inline void Contract_zd(void* m3, void* m1, void* m2){

    Contract( *((UniTensor<uni10_complex128 >*)m3), *((UniTensor<uni10_complex128 >*)m1), *((UniTensor<uni10_double64>*)m2), INPLACE);

  }

  inline void Contract_zz(void* m3, void* m1, void* m2){

    Contract( *((UniTensor<uni10_complex128 >*)m3), *((UniTensor<uni10_complex128 >*)m1), *((UniTensor<uni10_complex128 >*)m2), INPLACE);

  }

  // Function pointers of vector of Contracts' driver functions.
  static void (*ContractDriver[])(void* m3, void* m1, void* m2) = {Contract_dd, Contract_zd, Contract_dz, Contract_zz};


  // Contract with mix type.
  template<typename T>
    void ContractsMix(UniTensor<T>& mout, std::vector< std::pair<void*, int> >& _ulist, UNI10_INPLACE on);

  template<typename T> 
    void ContractsPure(UniTensor<T>& mout, std::vector< std::pair<void*, int> >& _ulist, UNI10_INPLACE on);

  // Uni10_API level.
  template<typename T> 
    void Contracts(UniTensor<T>& mout, std::vector< UniTensor<T>* >& _ulist, std::pair<bool, uni10_int>& isMix_TrLen, UNI10_INPLACE on);

  // Contract with mix type.
  template<typename T>
    void ContractsMix(UniTensor<T>& _Tout, std::vector< std::pair<void*, int> >& _ulist, std::pair<bool, uni10_int>& isMix_TrLen, UNI10_INPLACE on){

      uni10_error_msg(on != 1, "%s", "Setting a wrong flag of uni10_Inplace");
      uni10_error_msg(_ulist.size() < 2, "%s", "Too few UniTensors in the Contraction list [N >= 2]. ");
      uni10_error_msg(_Tout.TypeId() == 1, "%s", 
          "There are complex matrices in the input arguments. Hence, the type of output matrix must be complex.");

      //
      // Check Tout is in the ulist or not.
      //
      
      bool inlist = false;
      for(uni10_uint64 i = 0; i < _ulist.size(); i++)
        if(_ulist[i].first == &_Tout){
          inlist = true;
          break;
        }

      UniTensor<T>* Tout = NULL;

      if(inlist){
        Tout = new UniTensor<T>(UniTensor<T>());
      }else{
        Tout = &_Tout;
      }

      uni10_uint64 complex1st = isMix_TrLen.second;

      if(isMix_TrLen.second > 1){

        UniTensor<uni10_double64> Tr1, Tr2;

        ContractDriver[0]((void*)&Tr1, _ulist[0].first, _ulist[1].first);

        uni10_int i = 2;

        for( i = 2; i < isMix_TrLen.second; i++){

          Tr2 = *(UniTensor<uni10_double64>*)_ulist[i].first;

          if(i % 2 == 0)
            ContractDriver[0]((void*)&Tr2, (void*)&Tr1, _ulist[i].first);
          else
            ContractDriver[0]((void*)&Tr1, (void*)&Tr2, _ulist[i].first);

        }

        if(i % 2 == 0){
          ContractDriver[2]((void*)Tout, (void*)&Tr1, _ulist[complex1st].first);
        }

        if(i % 2 == 1){
          ContractDriver[2]((void*)Tout, (void*)&Tr2, _ulist[complex1st].first);
        }

      }else{

        uni10_int rest_idx = isMix_TrLen.second == 0 ? 1 : 0;

        if(_ulist[rest_idx].second == 1){

          ContractDriver[1]((void*)Tout, _ulist[complex1st].first, _ulist[rest_idx].first);

        }else{

          ContractDriver[3]((void*)Tout, _ulist[complex1st].first, _ulist[rest_idx].first);

        }

      }

      uni10_uint64 offset = (isMix_TrLen.second > 1) ? isMix_TrLen.second + 1 : 2;
      uni10_uint64 j = 0;

      UniTensor<uni10_complex128> tmpT1;

      for( ; j < _ulist.size()-offset; j++){

        int driver_type = _ulist[j+offset].second == 1 ? 1 : 3;

        if(j % 2 == 0)
          ContractDriver[driver_type]((void*)&tmpT1, (void*)Tout, _ulist[j+offset].first);
        else
          ContractDriver[driver_type]((void*)Tout, (void*)&tmpT1, _ulist[j+offset].first);

      }

      if(j % 2 == 1){

        *Tout = tmpT1;

      }

      if(inlist){
        _Tout = *Tout;
        delete Tout;
      }

    }


  template<typename T> 
    void ContractsPure(UniTensor<T>& _Tout, std::vector< std::pair<void*, int> >& _ulist, UNI10_INPLACE on){

      uni10_error_msg(on != 1, "%s", "Setting a wrong flag of uni10_Inplace");
      uni10_error_msg(_Tout.TypeId() != _ulist[0].second, "%s", "Set a wrong type to the output UniTensor.");
      
      //
      // Check Tout is in the ulist or not.
      //
      bool inlist = false;

      for(uni10_uint64 i = 0; i < _ulist.size(); i++)
        if(_ulist[i].first == &_Tout){
          inlist = true;
          break;
        }

      UniTensor<T>* Tout = NULL;

      if(inlist){
        Tout = new UniTensor<T>(UniTensor<T>());
      }else{
        Tout = &_Tout;
      }
           
      int driver_type = (Tout->TypeId() == 1) ? 0 : 3;

      ContractDriver[driver_type]((void*)Tout, _ulist[0].first, _ulist[1].first);

      UniTensor<T> tmpT1;

      uni10_uint64 i = 2;

      for( ; i < _ulist.size(); i++){

        if(i % 2 == 0)
          ContractDriver[driver_type]((void*)&tmpT1, (void*)Tout, _ulist[i].first);
        else
          ContractDriver[driver_type]((void*)Tout, (void*)&tmpT1, _ulist[i].first);

      }

      if(i % 2 == 1){

        *Tout = tmpT1;

      }

      if(inlist){
        _Tout = *Tout;
        delete Tout;
      }

    };

  template<typename T> 
    void Contracts(UniTensor<T>& Tout, std::vector< UniTensor<T>* >& _ulist, UNI10_INPLACE on){

      uni10_error_msg(on != 1, "%s", "Setting a wrong flag of uni10_Inplace");

      Contract(Tout, *_ulist[0], *_ulist[1], on);

      uni10_uint64 i;

      UniTensor<T> tmpT1;

      for( i = 2; i < _ulist.size(); i++){

        if(i % 2 == 0)
          Contract(tmpT1, Tout, *_ulist[i], on);
        else
          Contract(Tout, tmpT1, *_ulist[i], on);

      }

      if(i % 2 == 1){

        Tout = tmpT1;

      }

    }

}; /* End of namespace. */

#endif
