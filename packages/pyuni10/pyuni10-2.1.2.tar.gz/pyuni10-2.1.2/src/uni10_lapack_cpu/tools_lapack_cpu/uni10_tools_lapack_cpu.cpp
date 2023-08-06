#include <iostream>
#include <iomanip>
#include <algorithm>

#include "uni10_env_info.h"
#include "uni10_lapack_cpu/tools_lapack_cpu/uni10_tools_lapack_cpu.h"

namespace uni10{

  namespace tools_internal{

    void* UniElemAlloc(uni10_uint64 memsize){

      void* ptr = NULL;
      ptr = malloc(memsize);

      env_variables.UsedMemory(memsize);
      uni10_error_msg(ptr==NULL, "%s","Fails in allocating memory.");

      return ptr;
    }

    void* UniElemCopy(void* des, const void* src, uni10_uint64 memsize){
      return memcpy(des, src, memsize);
    }

    void UniElemFree(void* ptr, uni10_uint64 memsize){

      free(ptr);
      env_variables.UsedMemory(-memsize);
      ptr = NULL;

    }

    void UniElemZeros(void* ptr, uni10_uint64 memsize){

      memset(ptr, 0, memsize);

    }

    // For double 
    //
    void Ones(uni10_double64* elem, uni10_uint64 elem_num){

      std::fill_n(elem, elem_num, 1);

    }

    void SetDiag(uni10_double64* elem, uni10_double64* diag_elem, uni10_uint64 m, uni10_uint64 n, uni10_uint64 diag_n){

      uni10_uint64 min = m < n ? m : n;

      min = min < diag_n ? min : diag_n;

      for(uni10_uint64 i = 0; i < min; i++)
        elem[i * n + i] = diag_elem[i];

    }

    void GetDiag(uni10_double64* elem, uni10_double64* diag_elem, uni10_uint64 m, uni10_uint64 n, uni10_uint64 diag_n){

      uni10_uint64 min = m < n ? m : n;

      min = min < diag_n ? min : diag_n;

      for(uni10_uint64 i = 0; i < min; i++)
        diag_elem[i] = elem[i * n + i];

    }

    void GetUpTri(uni10_double64* elem, uni10_double64* tri_elem, uni10_uint64 m, uni10_uint64 n){

      uni10_uint64 min = m < n ? m : n;

      for(uni10_uint64 i = 0; i < min; i++)
        UniElemCopy(tri_elem + i*min+i, elem + i*n + (n-min)+i, (min-i)*sizeof(uni10_double64));

    }

    void GetDnTri(uni10_double64* elem, uni10_double64* tri_elem, uni10_uint64 m, uni10_uint64 n){

      uni10_uint64 min = m < n ? m : n;

      for(uni10_uint64 i = 0; i < min; i++)
        UniElemCopy(tri_elem + i*min, elem + n*(m-min)+i*n, (i+1)*sizeof(uni10_double64));

    }

    void PrintElem_I(const uni10_double64& elem_i){
      /*
      std::cout << std::setfill (' ') << std::setw (8) << std::setprecision(4);
      std::cout << " " <<elem_i;
      */
      char buf[16];
      sprintf(buf, " %8.4f", elem_i);
      std::cout << buf;
    }

    uni10_double64 UNI10_REAL( uni10_double64 elem_i ){

      return elem_i;

    }

    void GetUpTri(uni10_complex128* elem, uni10_complex128* tri_elem, uni10_uint64 m, uni10_uint64 n){

      uni10_uint64 min = m < n ? m : n;

      for(uni10_uint64 i = 0; i < min; i++)
        UniElemCopy(tri_elem + i*min+i, elem + i*n+(n-min)+i, (min-i)*sizeof(uni10_complex128));

    }

    void GetDnTri(uni10_complex128* elem, uni10_complex128* tri_elem, uni10_uint64 m, uni10_uint64 n){

      uni10_uint64 min = m < n ? m : n;

      for(uni10_uint64 i = 0; i < min; i++)
        UniElemCopy(tri_elem + i*min, elem + n*(m-min)+i*n, (i+1)*sizeof(uni10_complex128));

    }

    uni10_double64 UNI10_IMAG( uni10_double64 elem_i ){

      return 0.;

    }

    // For complex 
    //

    void Ones(uni10_complex128* elem, uni10_uint64 elem_num){

      std::fill_n(elem, elem_num, 1);
      
    }

    void SetDiag(uni10_complex128* elem, uni10_complex128* diag_elem, uni10_uint64 m, uni10_uint64 n, uni10_uint64 diag_n){

      uni10_uint64 min = m < n ? m : n;

      min = min < diag_n ? min : diag_n;

      for(uni10_uint64 i = 0; i < min; i++)
        elem[i * n + i] = diag_elem[i];

    }
    void GetDiag(uni10_complex128* elem, uni10_complex128* diag_elem, uni10_uint64 m, uni10_uint64 n, uni10_uint64 diag_n){

      uni10_uint64 min = m < n ? m : n;

      min = min < diag_n ? min : diag_n;

      for(uni10_uint64 i = 0; i < min; i++)
        diag_elem[i] = elem[i * n + i];

    }

    void PrintElem_I(const uni10_complex128& elem_i){
      /*
      std::cout << std::setfill (' ') << std::setw (8) << std::setprecision(4);
      std::cout << " " << Z_REAL( elem_i ) << "+" << Z_IMAG( elem_i ) << "i";
      */
      char buf[32];
      sprintf(buf, " %8.4f+%8.4fi", elem_i.real(), elem_i.imag());
      std::cout << buf;
    }

    uni10_double64 UNI10_REAL( uni10_complex128 elem_i ){

      return elem_i.real();

    }

    uni10_double64 UNI10_IMAG( uni10_complex128 elem_i ){

      return elem_i.imag();

    }

    void ToReal(uni10_double64& M_i, uni10_double64 val){

      M_i = val;

    }

    void ToReal(uni10_complex128& M_i, uni10_double64 val){

      M_i.real(val);

    }

    void ToComplex(uni10_double64& M_i, uni10_double64 val){

      // Do nothing

    }

    void ToComplex(uni10_complex128& M_i, uni10_double64 val){

      M_i.imag(val);

    }

    // Convert
    void UniElemCast(uni10_complex128* des, const uni10_double64* src, uni10_uint64 N){

      for(uni10_uint64 i = 0; i < N; i++)
        des[i] = src[i];

    }

    void UniElemCast(uni10_double64* des, const uni10_complex128* src, uni10_uint64 N){

      for(uni10_uint64 i = 0; i < N; i++)
        des[i] = src[i].real();

    }

    void ShrinkWithoutFree(uni10_uint64 memsize){

      env_variables.UsedMemory(-memsize);

    }

  }

} /* namespace uni10 */
