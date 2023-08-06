#ifndef __UNI10_LINALG_QDRCPIVOT_H__
#define __UNI10_LINALG_QDRCPIVOT_H__

#include <vector>

#include "uni10_api/uni10_linalg_inplace/uni10_linalg_inplace_qdr_cpivot.h"

namespace uni10{

  template<typename uni10_type>
    std::vector< Matrix<uni10_type> > QdrColPivot( const Block<uni10_type>& kblk );

  template<typename uni10_type>
    std::vector< Matrix<uni10_type> > QdrColPivot( const Block<uni10_type>& kblk ){

      std::vector<Matrix<uni10_type> > qdr(3);
      QdrColPivot(kblk, qdr[0], qdr[1], qdr[2], INPLACE);

      return qdr;

    }

}

#endif
