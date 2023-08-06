#ifndef __UNI10_HIGH_RANK_LINALG_INPLACE_OTIMESS_H__
#define __UNI10_HIGH_RANK_LINALG_INPLACE_OTIMESS_H__

#include "uni10_api/uni10_hirnk_linalg_inplace/uni10_hirnk_linalg_inplace_otimes.h"

namespace uni10{

  // OTIMES ( T, T )
  inline void Otimes_dd(void* m3, const void* m1, const void* m2){

    Otimes( *((UniTensor<uni10_double64>*)m3), *((UniTensor<uni10_double64>*)m1), *((UniTensor<uni10_double64>*)m2), INPLACE);

  }

  inline void Otimes_dz(void* m3, const void* m1, const void* m2){

    Otimes( *((UniTensor<uni10_complex128 >*)m3), *((UniTensor<uni10_double64>*)m1), *((UniTensor<uni10_complex128 >*)m2), INPLACE);

  }

  inline void Otimes_zd(void* m3, const void* m1, const void* m2){

    Otimes( *((UniTensor<uni10_complex128 >*)m3), *((UniTensor<uni10_complex128 >*)m1), *((UniTensor<uni10_double64>*)m2), INPLACE);

  }

  inline void Otimes_zz(void* m3, const void* m1, const void* m2){

    Otimes( *((UniTensor<uni10_complex128 >*)m3), *((UniTensor<uni10_complex128 >*)m1), *((UniTensor<uni10_complex128 >*)m2), INPLACE);

  }

  // Function pointers of vector of Otimess' driver functions.
  static void (*OtimesDriver[])(void* m3, const void* m1, const void* m2) = {Otimes_dd, Otimes_zd, Otimes_dz, Otimes_zz};


  template<typename T>
    void OtimessMix(UniTensor<T>& Tout, const std::vector< std::pair<void*, int> >& _ulist, UNI10_INPLACE on);

  template<typename T> 
    void OtimessPure(UniTensor<T>& Tout, const std::vector< std::pair<void*, int> >& _ulist, UNI10_INPLACE on);

  template<typename T> 
    void Otimess(UniTensor<T>& Tout, const std::vector< UniTensor<T>* >& _ulist, UNI10_INPLACE on);

  // OTIMES ( M, M )
  inline void Otimes_dd_m(void* m3, const void* m1, const void* m2){

    Otimes( *((Matrix<uni10_double64>*)m3), *((Matrix<uni10_double64>*)m1), *((Matrix<uni10_double64>*)m2), INPLACE);

  }

  inline void Otimes_dz_m(void* m3, const void* m1, const void* m2){

    Otimes( *((Matrix<uni10_complex128 >*)m3), *((Matrix<uni10_double64>*)m1), *((Matrix<uni10_complex128 >*)m2), INPLACE);

  }

  inline void Otimes_zd_m(void* m3, const void* m1, const void* m2){

    Otimes( *((Matrix<uni10_complex128 >*)m3), *((Matrix<uni10_complex128 >*)m1), *((Matrix<uni10_double64>*)m2), INPLACE);

  }

  inline void Otimes_zz_m(void* m3, const void* m1, const void* m2){

    Otimes( *((Matrix<uni10_complex128 >*)m3), *((Matrix<uni10_complex128 >*)m1), *((Matrix<uni10_complex128 >*)m2), INPLACE);

  }

  // Function pointers of vector of Otimess' driver functions.
  static void (*OtimesDriver_m[])(void* m3, const void* m1, const void* m2) = {Otimes_dd_m, Otimes_zd_m, Otimes_dz_m, Otimes_zz_m};

  template<typename T>
    void OtimessMix(Matrix<T>& Tout, const std::vector< std::pair<void*, int> >& _ulist, UNI10_INPLACE on);

  template<typename T> 
    void OtimessPure(Matrix<T>& Tout, const std::vector< std::pair<void*, int> >& _ulist, UNI10_INPLACE on);
  
  template<typename T> 
    void Otimess(Matrix<T>& Tout, const std::vector< Matrix<T>* >& _ulist, UNI10_INPLACE on);


  // OTIMES(T, T)
  template<typename T>
    void OtimessMix(UniTensor<T>& Tout, const std::vector< std::pair<void*, int> >& _ulist, UNI10_INPLACE on){

      uni10_error_msg(on != 1, "%s", "Setting a wrong flag of uni10_Inplace");
      uni10_error_msg(Tout.typeID() == 1, "%s", 
          "There are complex matrices in the input arguments. Hence, the output matrix must be complex.");

      if(_ulist.size() == 1){

        if(_ulist[0].second == 1)
          Tout = *(UniTensor<uni10_double64>*)(_ulist[0].first);
        else
          Tout = *(UniTensor<uni10_complex128>*)(_ulist[0].first);
        return;

      }

      std::vector<std::pair<void*, int> > ulist = _ulist;

      if(ulist.size() == 2){

        int driver_type = (ulist[0].second - 1) + (2 * (ulist[1].second - 1));
        if(driver_type == 0){
          UniTensor<uni10_double64> _Tout;
          OtimesDriver[driver_type]((void*)&_Tout, ulist[0].first, ulist[1].first);
          Tout = _Tout;
        }else
          OtimesDriver[driver_type]((void*)&Tout, ulist[0].first, ulist[1].first);

        return;

      }

      std::vector<std::pair<void*, int> > sub_ulist;
      int driver_type;
      std::vector<UniTensor<uni10_double64> > buf_r(ulist.size()/2);
      std::vector<UniTensor<uni10_complex128> > buf_c(ulist.size()/2);

      int offset = (ulist.size() % 2 == 0) ? 0 : 1;  

      if(offset == 1)
        sub_ulist.push_back(ulist[0]);

      for(int b = 0 ; b < (int)ulist.size()/2; b++){
        driver_type = (ulist[2*b+offset].second -1) + (2 * (ulist[2*b+1+offset].second - 1));
        if(driver_type == 0){
          OtimesDriver[driver_type]((void*)&buf_r[b], ulist[2*b+offset].first, ulist[2*b+1+offset].first);
          sub_ulist.push_back(std::pair<void*, int>((void*)&buf_r[b], 1));
        }else{
          OtimesDriver[driver_type]((void*)&buf_c[b], ulist[2*b+offset].first, ulist[2*b+1+offset].first);
          sub_ulist.push_back(std::pair<void*, int>((void*)&buf_c[b], 2));
        }

      }

      OtimessMix(Tout, sub_ulist, on);

    }


  template<typename T> 
    void OtimessPure(UniTensor<T>& Tout, const std::vector< std::pair<void*, int> >& _ulist, UNI10_INPLACE on){

      uni10_error_msg(on != 1, "%s", "Setting a wrong flag of uni10_Inplace");

      if(_ulist.size() == 1){

        Tout = *(UniTensor<T>*)(_ulist[0].first);
        return;

      }

      std::vector<std::pair<void*, int> > ulist = _ulist;
      int driver_type = Tout.typeID() == 1 ? 0 : 3;

      if(ulist.size() == 2){

        OtimesDriver[driver_type]((void*)&Tout, ulist[0].first, ulist[1].first);
        return;

      }

      std::vector<std::pair<void*, int> > sub_ulist;
      std::vector< UniTensor<T> > buf(ulist.size()/2);

      int offset = (ulist.size() % 2 == 0) ? 0 : 1;  

      if(offset == 1)
        sub_ulist.push_back(ulist[0]);

      for(int b = 0 ; b < (int)ulist.size()/2; b++){
        OtimesDriver[driver_type]((void*)&buf[b], ulist[2*b+offset].first, ulist[2*b+1+offset].first);
        sub_ulist.push_back(std::pair<void*, int>((void*)&buf[b], Tout.typeID()));
      }

      OtimessPure(Tout, sub_ulist, on);


    }

  template<typename T> 
    void Otimess(UniTensor<T>& Tout, const std::vector< UniTensor<T>* >& _ulist, UNI10_INPLACE on){

      uni10_error_msg(on != 1, "%s", "Setting a wrong flag of uni10_Inplace");

      if(_ulist.size() == 1){

        Tout = (*_ulist[0]);
        return;

      }

      std::vector< UniTensor<T>* > ulist = _ulist;

      if(ulist.size() == 2){

          Otimes(Tout, *ulist[0], *ulist[1], INPLACE);

        return;

      }

      std::vector< UniTensor<T>* > sub_ulist;
      int driver_type;
      std::vector< UniTensor<T> > buf_ten(ulist.size()/2);

      int offset = (ulist.size() % 2 == 0) ? 0 : 1;  

      if(offset == 1)
        sub_ulist.push_back(ulist[0]);

      for(int b = 0 ; b < (int)ulist.size()/2; b++){

        Otimes(buf_ten[b], *ulist[2*b+offset], *ulist[2*b+1+offset], INPLACE);
        sub_ulist.push_back(&buf_ten[b]);

      }

      Otimess(Tout, sub_ulist, on);

    }

  // OTIMES ( M, M )
  // Dirty version. It will be optimized as soon as possibly.
  template<typename T>
    void OtimessMix(Matrix<T>& Mout, const std::vector< std::pair<void*, int> >& _mlist, UNI10_INPLACE on){

      uni10_error_msg(on != 1, "%s", "Setting a wrong flag of uni10_Inplace");
      uni10_error_msg(Mout.typeID() == 1, "%s", 
          "There are complex matrices in the input arguments. Hence, the output matrix must be complex.");

      if(_mlist.size() == 1){

        if(_mlist[0].second == 1)
          Mout = *(Matrix<uni10_double64>*)(_mlist[0].first);
        else
          Mout = *(Matrix<uni10_complex128>*)(_mlist[0].first);
        return;

      }

      std::vector<std::pair<void*, int> > mlist = _mlist;

      if(mlist.size() == 2){

        int driver_type = (mlist[0].second - 1) + (2 * (mlist[1].second - 1));
        if(driver_type == 0){
          Matrix<uni10_double64> _Mout;
          OtimesDriver_m[driver_type]((void*)&_Mout, mlist[0].first, mlist[1].first);
          Mout = _Mout;
        }else
          OtimesDriver_m[driver_type]((void*)&Mout, mlist[0].first, mlist[1].first);

        return;

      }

      std::vector<std::pair<void*, int> > sub_mlist;
      int driver_type;
      std::vector<Matrix<uni10_double64> > buf_r(mlist.size()/2);
      std::vector<Matrix<uni10_complex128> > buf_c(mlist.size()/2);

      int offset = (mlist.size() % 2 == 0) ? 0 : 1;  

      if(offset == 1)
        sub_mlist.push_back(mlist[0]);

      for(int b = 0 ; b < (int)mlist.size()/2; b++){
        driver_type = (mlist[2*b+offset].second -1) + (2 * (mlist[2*b+1+offset].second - 1));
        if(driver_type == 0){
          OtimesDriver_m[driver_type]((void*)&buf_r[b], mlist[2*b+offset].first, mlist[2*b+1+offset].first);
          sub_mlist.push_back(std::pair<void*, int>((void*)&buf_r[b], 1));
        }else{
          OtimesDriver_m[driver_type]((void*)&buf_c[b], mlist[2*b+offset].first, mlist[2*b+1+offset].first);
          sub_mlist.push_back(std::pair<void*, int>((void*)&buf_c[b], 2));
        }

      }

      OtimessMix(Mout, sub_mlist, on);

    }


  template<typename T> 
    void OtimessPure(Matrix<T>& Mout, const std::vector< std::pair<void*, int> >& _mlist, UNI10_INPLACE on){

      uni10_error_msg(on != 1, "%s", "Setting a wrong flag of uni10_Inplace");

      if(_mlist.size() == 1){

        Mout = *(Matrix<T>*)(_mlist[0].first);
        return;

      }

      std::vector<std::pair<void*, int> > mlist = _mlist;
      int driver_type = Mout.typeID() == 1 ? 0 : 3;

      if(mlist.size() == 2){

        OtimesDriver_m[driver_type]((void*)&Mout, mlist[0].first, mlist[1].first);
        return;

      }

      std::vector<std::pair<void*, int> > sub_mlist;
      std::vector< Matrix<T> > buf(mlist.size()/2);

      int offset = (mlist.size() % 2 == 0) ? 0 : 1;  

      if(offset == 1)
        sub_mlist.push_back(mlist[0]);

      for(int b = 0 ; b < (int)mlist.size()/2; b++){
        OtimesDriver_m[driver_type]((void*)&buf[b], mlist[2*b+offset].first, mlist[2*b+1+offset].first);
        sub_mlist.push_back(std::pair<void*, int>((void*)&buf[b], Mout.typeID()));
      }

      OtimessPure(Mout, sub_mlist, on);

    }

  template<typename T> 
    void Otimess(Matrix<T>& Mout, const std::vector< Matrix<T>* >& _mlist, UNI10_INPLACE on){

      uni10_error_msg(on != 1, "%s", "Setting a wrong flag of uni10_Inplace");

      if(_mlist.size() == 1){

        Mout = (*_mlist[0]);
        return;

      }

      std::vector< Matrix<T>* > mlist = _mlist;

      if(mlist.size() == 2){

          Otimes(Mout, *mlist[0], *mlist[1], INPLACE);

        return;

      }

      std::vector< Matrix<T>* > sub_mlist;
      int driver_type;
      std::vector< Matrix<T> > buf_ten(mlist.size()/2);

      int offset = (mlist.size() % 2 == 0) ? 0 : 1;  

      if(offset == 1)
        sub_mlist.push_back(mlist[0]);

      for(int b = 0 ; b < (int)mlist.size()/2; b++){

        Otimes(buf_ten[b], *mlist[2*b+offset], *mlist[2*b+1+offset], INPLACE);
        sub_mlist.push_back(&buf_ten[b]);

      }

      Otimess(Mout, sub_mlist, on);

    }

}; /* End of namespace. */

#endif
