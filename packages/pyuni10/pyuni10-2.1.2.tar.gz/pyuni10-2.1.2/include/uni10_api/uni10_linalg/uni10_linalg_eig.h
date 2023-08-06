#ifndef __UNI10_LINALG_EIG_H__
#define __UNI10_LINALG_EIG_H__

#include <vector>

#include "uni10_api/uni10_linalg_inplace/uni10_linalg_inplace_eig.h"

namespace uni10{

  template<typename UniType>
    std::vector< Matrix<uni10_complex128> > Eig( const Block<UniType>& kblk );

  template<typename UniType>
    std::vector< Matrix<uni10_complex128> > Eig( const Block<UniType>& kblk ){

      std::vector< Matrix<uni10_complex128> > wv(2);
      Eig(kblk, wv[0], wv[1], INPLACE);

      return wv;

    }

}

#endif
