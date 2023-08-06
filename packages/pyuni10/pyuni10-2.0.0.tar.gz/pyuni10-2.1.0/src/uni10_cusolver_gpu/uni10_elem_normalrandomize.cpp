#include <chrono>

#include "uni10_cusolver_gpu/uni10_elem_linalg_cusolver_gpu.h"
#include "uni10_cusolver_gpu/uni10_elem_rng_cusolver_gpu.h"

namespace uni10{

  namespace linalg_unielem_internal{

    void NormalRandomize(UniElemDouble* A, const uni10_bool* is_diag, const uni10_uint64* M, const uni10_uint64* N, 
        const uni10_double64* mu, const uni10_double64* var, const uni10_int64* _seed){

      uni10_uint64 seed = (*_seed < 0) ? std::chrono::system_clock::now().time_since_epoch().count() : (uni10_uint64)*_seed; 
      uni10_mt19937 generator(seed);
      uni10_normal distribution(*mu, *var);

      uni10_uint64 elemNum = *is_diag ? std::min(*M, *N) : (*M)*(*N);

      for(uni10_uint64 i = 0; i < elemNum; i++)
        A->elem_ptr_[i] = distribution(generator);

    }

    void NormalRandomize(UniElemComplex* A, const uni10_bool* is_diag, const uni10_uint64* M, const uni10_uint64* N, 
        const uni10_double64* mu, const uni10_double64* var, const uni10_int64* _seed){

      uni10_uint64 seed = (*_seed < 0) ? std::chrono::system_clock::now().time_since_epoch().count() : (uni10_uint64)*_seed; 
      uni10_mt19937 generator(seed);
      uni10_normal distribution(*mu, *var);

      uni10_uint64 elemNum = *is_diag ? std::min(*M, *N) : (*M)*(*N);

      for(uni10_uint64 i = 0; i < elemNum; i++){
        A->elem_ptr_[i].real(distribution(generator));
        A->elem_ptr_[i].imag(distribution(generator));
      }

    }


  }

}
