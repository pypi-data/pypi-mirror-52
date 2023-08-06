#ifndef __UNI10_LINALG_EIGH_H__
#define __UNI10_LINALG_EIGH_H__

#include <vector>

#include "uni10_api/uni10_linalg_inplace/uni10_linalg_inplace_eigh.h"

namespace uni10{

  template<typename UniType>
    std::vector< Matrix<UniType> > EigH( const Block<UniType >& kblk );

  template<typename UniType>
    std::vector< Matrix<UniType> > EigH( const Block<UniType >& kblk ){

      Matrix<uni10_double64> w;
      Matrix<UniType> v;

      EigH(kblk, w, v, INPLACE);

      std::vector<Matrix<UniType>> wv(2);
      wv[0] = w;
      wv[1] = v;

      return wv;

    }

}

#endif
