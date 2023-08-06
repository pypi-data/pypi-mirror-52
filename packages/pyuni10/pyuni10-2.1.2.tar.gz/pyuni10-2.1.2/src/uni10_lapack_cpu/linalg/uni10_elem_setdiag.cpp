#include "uni10_lapack_cpu/uni10_elem_linalg.h"

namespace uni10{

  namespace linalg_unielem_internal{

    void SetDiag(UniElemDouble* _elem, const UniElemDouble* diag_elem, const uni10_uint64* M, const uni10_uint64* N ){

      tools_internal::SetDiag(_elem->elem_ptr_, diag_elem->elem_ptr_, *M, *N, std::min(*M, *N));

    }

    void SetDiag(UniElemComplex* _elem, const UniElemComplex* diag_elem, const uni10_uint64* M, const uni10_uint64* N ){

      tools_internal::SetDiag(_elem->elem_ptr_, diag_elem->elem_ptr_, *M, *N, std::min(*M, *N));

    }

  }

}
