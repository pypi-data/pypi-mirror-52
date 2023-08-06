#ifndef __UNI10_LINALG_INPLACE_DOTARGS_H__
#define __UNI10_LINALG_INPLACE_DOTARGS_H__

#include "uni10_api/Matrix.h"
#include "uni10_linalg_inplace_dots.h"

namespace uni10{

  // DOES NOT OPTIMIZE.
  template<typename Res> 
    void _DotArgs(Res& matout, std::vector<std::pair<void*, int> >& matptrs);

  template<typename Res, typename Obj, typename... Args> 
    void _DotArgs(Res& matout, std::vector<std::pair<void*, int> >& matptrs, const Obj& kmat, const Args&... args);

  /// @ingroup linalg_inplace
  /// @brief Compute multiplication of array of an matrix <tt> T=A*B*...*N.
  /// 
  /// @param[out] mout On exit, \c matout is overwritten by the result of matrix multiplication.
  /// @param[in] _m1 The leftmost matrix \c A.
  /// @param[in] args The matrices \c B, \c C, ... \c N. The order of matrices must follow the matrix multiplication.
  // DotsArgs (API level)
  template<typename Res, typename Obj, typename... Args> 
    void DotArgs(Res& matout, const Obj& kmat, const Args&... args);



  template<typename Res> 
    void _DotArgs(Res& matout, std::vector<std::pair<void*, int> >& matptrs){

      bool is_pure = true;
      for(int i = 0; i < matptrs.size()-1; i++)
        if(matptrs[i].second != matptrs[i+1].second){
          is_pure = false;
          break;
        }

      if(is_pure)
        DotsPure(matout, matptrs, INPLACE);
      else{
        DotsMix(matout, matptrs, INPLACE);
      }

    }

  template<typename Res, typename Obj, typename... Args> 
    void _DotArgs(Res& matout, std::vector<std::pair<void*, int> >& matptrs, const Obj& kmat, const Args&... args) {

      matptrs.push_back(std::pair<void*, int>((void*)&kmat, kmat.TypeId()));
      _DotArgs(matout, matptrs, args...);

    }

  template<typename Res, typename Obj, typename... Args> 
    void DotArgs(Res& matout, const Obj& kmat, const Args&... args) {

      std::vector<std::pair<void*, int> > matptrs;
      matptrs.push_back(std::pair<void*, int>((void*)&kmat, kmat.TypeId()));
      _DotArgs(matout, matptrs, args...);

    }

}

#endif
