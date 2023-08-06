#ifndef __UNI10_LINALG_EXPH_H__
#define __UNI10_LINALG_EXPH_H__

#include "uni10_api/uni10_linalg_inplace/uni10_linalg_inplace_dot.h"
#include "uni10_api/uni10_linalg/uni10_linalg_eigh.h"

namespace uni10{

  template<typename UniType>
    Matrix<UniType> ExpH( uni10_double64 a, const Block<UniType>& kblk);

  template<typename UniType>
    Matrix<uni10_complex128> ExpH( uni10_complex128 a, const Block<UniType>& kblk);

  template<typename UniType>
    Matrix<UniType> ExpH( uni10_double64 a, const Block<UniType>& kblk){

      std::vector< Matrix<UniType> > rets = EigH( kblk );

      Matrix<UniType> UT, EXPT;
      Dagger(UT, rets[1], INPLACE);

      linalg_unielem_internal::VectorExp( &a, &rets[0].elem_, &rets[0].row_ );

      DotArgs(EXPT, UT, rets[0], rets[1]);

      return EXPT;

    }

  template<typename UniType>
    Matrix<uni10_complex128> ExpH( uni10_complex128 a, const Block<UniType>& kblk){

      std::vector< Matrix<UniType> > rets = EigH( kblk );

      Matrix<UniType> UT;
      Dagger(UT, rets[1], INPLACE);

      Matrix<uni10_complex128> cret0(rets[0]);

      linalg_unielem_internal::VectorExp( &a, &cret0.elem_, &cret0.row_ );

      Matrix<uni10_complex128> EXPT;

      DotArgs(EXPT, UT, cret0, rets[1]);

      return EXPT;

    }

}

#endif
