#include "uni10_api/uni10_linalg_inplace/uni10_linalg_inplace_dot.h"

namespace uni10{

  void Dot( Matrix<uni10_double64>& matout, const Block<uni10_double64>& kblk, UNI10_INPLACE on ){

    uni10_error_msg(on != 1, "%s", "Setting a wrong flag of uni10_Inplace." );

    uni10_error_msg(matout.col_ != kblk.row_, "%s", "The dimensions of the two matrices do not match for matrix multiplication.");

    Matrix<uni10_double64> tmpmat(matout.row_, kblk.col_, matout.diag_ && kblk.diag_);

    linalg_unielem_internal::Dot(&matout.elem_, &matout.diag_, &kblk.elem_, &kblk.diag_, &matout.row_, &kblk.col_, &matout.col_, &tmpmat.elem_);

    matout = tmpmat;

  }

}

