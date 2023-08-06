#ifndef __UNI10_LINALG_INPLACE_DOTS_H__
#define __UNI10_LINALG_INPLACE_DOTS_H__

#include <utility>

#include "uni10_api/Matrix.h"
#include "uni10_linalg_inplace_dot.h"

namespace uni10{

  // The driver fucntions of Dots.
  inline void dot_dd(void* m3, const void* m1, const void* m2){

    Dot( *((Matrix<double>*)m3), *((Matrix<double>*)m1), *((Matrix<double>*)m2), INPLACE);

  }

  inline void dot_dz(void* m3, const void* m1, const void* m2){

    Dot( *((Matrix<uni10_complex128 >*)m3), *((Matrix<double>*)m1), *((Matrix<uni10_complex128 >*)m2), INPLACE);

  }

  inline void dot_zd(void* m3, const void* m1, const void* m2){

    Dot( *((Matrix<uni10_complex128 >*)m3), *((Matrix<uni10_complex128 >*)m1), *((Matrix<double>*)m2), INPLACE);

  }

  inline void dot_zz(void* m3, const void* m1, const void* m2){

    Dot( *((Matrix<uni10_complex128 >*)m3), *((Matrix<uni10_complex128 >*)m1), *((Matrix<uni10_complex128 >*)m2), INPLACE);

  }

  // Function pointers of vector of Dots' driver functions.
  static void (*dot_driver[])(void* m3, const void* m1, const void* m2) = {dot_dd, dot_zd, dot_dz, dot_zz};

  // Dots with mix type.
  template<typename T>
    void DotsMix(Matrix<T>& matout, const std::vector< std::pair<void*, int> >& matptrs, UNI10_INPLACE on);

  // Matrices in the mlist have same type.
  template<typename T> 
    void DotsPure(Matrix<T>& matout, const std::vector< std::pair<void*, int> >& matptrs, UNI10_INPLACE on);


  // Dots with pure type (User API level).
  template<typename uni10_type> 
    void Dots(Matrix<uni10_type>& matout, const std::vector< Matrix<uni10_type>* >& matptrs, UNI10_INPLACE on);

  template<typename T>
    void DotsMix(Matrix<T>& matout, const std::vector< std::pair<void*, int> >& matptrs, UNI10_INPLACE on){

      uni10_error_msg(on != 1, "%s", "Setting a wrong flag of uni10_Inplace");
      uni10_error_msg(matout.TypeId() == 1, "%s", 
          "There are complex matrices in the input arguments. Hence, the output matrix must be complex.");

      if(matptrs.size() == 1){

        if(matptrs[0].second == 1)
          matout = *(Matrix<uni10_double64>*)(matptrs[0].first);
        else
          matout = *(Matrix<uni10_complex128>*)(matptrs[0].first);
        return;

      }

      std::vector<std::pair<void*, int> > mlist = matptrs;

      if(mlist.size() == 2){

        int driver_type = (mlist[0].second - 1) + (2 * (mlist[1].second - 1));
        if(driver_type == 0){
          Matrix<uni10_double64> _matout;
          dot_driver[driver_type]((void*)&_matout, mlist[0].first, mlist[1].first);
          matout = _matout;
        }else
          dot_driver[driver_type]((void*)&matout, mlist[0].first, mlist[1].first);

        return;

      }

      std::vector<std::pair<void*, int> > submatptrs;
      int driver_type;
      std::vector<Matrix<uni10_double64> > buf_r(mlist.size()/2);
      std::vector<Matrix<uni10_complex128> > buf_c(mlist.size()/2);

      int offset = (mlist.size() % 2 == 0) ? 0 : 1;  

      if(offset == 1)
        submatptrs.push_back(mlist[0]);

      for(int b = 0 ; b < (int)mlist.size()/2; b++){
        driver_type = (mlist[2*b+offset].second -1) + (2 * (mlist[2*b+1+offset].second - 1));
        if(driver_type == 0){
          dot_driver[driver_type]((void*)&buf_r[b], mlist[2*b+offset].first, mlist[2*b+1+offset].first);
          submatptrs.push_back(std::pair<void*, int>((void*)&buf_r[b], 1));
        }else{
          dot_driver[driver_type]((void*)&buf_c[b], mlist[2*b+offset].first, mlist[2*b+1+offset].first);
          submatptrs.push_back(std::pair<void*, int>((void*)&buf_c[b], 2));
        }

      }

      DotsMix(matout, submatptrs, on);

    }

  template<typename T> 
    void DotsPure(Matrix<T>& matout, const std::vector< std::pair<void*, int> >& matptrs, UNI10_INPLACE on){

      uni10_error_msg(on != 1, "%s", "Setting a wrong flag of uni10_Inplace");

      if(matptrs.size() == 1){

        matout = *(Matrix<T>*)(matptrs[0].first);
        return;

      }

      std::vector<std::pair<void*, int> > mlist = matptrs;
      int driver_type = matout.TypeId() == 1 ? 0 : 3;

      if(mlist.size() == 2){

        dot_driver[driver_type]((void*)&matout, mlist[0].first, mlist[1].first);
        return;

      }

      std::vector<std::pair<void*, int> > submatptrs;
      std::vector< Matrix<T> > buf(mlist.size()/2);

      int offset = (mlist.size() % 2 == 0) ? 0 : 1;  

      if(offset == 1)
        submatptrs.push_back(mlist[0]);

      for(int b = 0 ; b < (int)mlist.size()/2; b++){
        dot_driver[driver_type]((void*)&buf[b], mlist[2*b+offset].first, mlist[2*b+1+offset].first);
        submatptrs.push_back(std::pair<void*, int>((void*)&buf[b], matout.TypeId()));
      }

      DotsPure(matout, submatptrs, on);

    }

  template<typename uni10_type> 
    void Dots(Matrix<uni10_type>& matout, const std::vector< Matrix<uni10_type>* >& matptrs, UNI10_INPLACE on) {

      uni10_error_msg(on != 1, "%s", "Setting a wrong flag of uni10_Inplace." );

      if(matptrs.size() == 1){

        matout = (*matptrs[0]);
        return;

      }

      std::vector< Matrix<uni10_type>* > mlist = matptrs;

      if(mlist.size() == 2){

          Dot(matout, *mlist[0], *mlist[1], INPLACE);

        return;

      }

      std::vector< Matrix<uni10_type>* > submatptrs;
      int driver_type;
      std::vector<Matrix<uni10_type> > buf_mat(mlist.size()/2);

      int offset = (mlist.size() % 2 == 0) ? 0 : 1;  

      if(offset == 1)
        submatptrs.push_back(mlist[0]);

      for(int b = 0 ; b < (int)mlist.size()/2; b++){

        Dot(buf_mat[b], *mlist[2*b+offset], *mlist[2*b+1+offset], INPLACE);
        submatptrs.push_back(&buf_mat[b]);

      }

      Dots(matout, submatptrs, on);

    }

}

#endif
