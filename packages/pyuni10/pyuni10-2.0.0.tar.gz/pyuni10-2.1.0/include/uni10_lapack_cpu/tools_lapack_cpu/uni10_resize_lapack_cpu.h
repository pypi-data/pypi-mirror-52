#ifndef __UNI10_RESIZE_LAPACK_CPU_H__
#define __UNI10_RESIZE_LAPACK_CPU_H__

#include "uni10_type.h"
#include "uni10_lapack_cpu/uni10_elem_lapack_cpu.h"

namespace uni10{

  template <typename _uni10_type>
    void resize(UniElemLapackCpu<_uni10_type>& Eout, uni10_uint64 _row, uni10_uint64 _col, 
        const UniElemLapackCpu<_uni10_type>& Ein, const uni10_uint64 _Rnum, const uni10_uint64 _Cnum, uni10_const_bool& _fixHead);

  template <typename _uni10_type>
    void resize(UniElemLapackCpu<_uni10_type>& Eout, uni10_uint64 _row, uni10_uint64 _col, 
        const UniElemLapackCpu<_uni10_type>& Ein, const uni10_uint64 _Rnum, const uni10_uint64 _Cnum, uni10_const_bool& _fixHead){

      uni10_bool isdiag = _Rnum * _Cnum != Ein.elem_num_;

      uni10_uint64 _elemNum = Eout.elem_num_;

      if(_fixHead){

        if(isdiag){


          if(_elemNum > Ein.elem_num_){

            tools_internal::UniElemCopy(Eout.elem_ptr_, Ein.elem_ptr_, Ein.elem_num_ * sizeof(_uni10_type));

          }
          else
            tools_internal::UniElemCopy(Eout.elem_ptr_, Ein.elem_ptr_, Eout.elem_num_ * sizeof(_uni10_type));
            //shrinkWithoutFree( (Ein.elem_num_ - _elemNum) * sizeof(_uni10_type) );

        }
        else{

          if(_col == _Cnum){

            if(_row > _Rnum){

              tools_internal::UniElemCopy(Eout.elem_ptr_, Ein.elem_ptr_, Ein.elem_num_ * sizeof(_uni10_type) );

            }
            else
              tools_internal::UniElemCopy(Eout.elem_ptr_, Ein.elem_ptr_, Eout.elem_num_ * sizeof(_uni10_type) );
              //shrinkWithoutFree( (Ein.elem_num_ - _elemNum) * sizeof(_uni10_type) );

          }
          else{

            uni10_uint64 data_row = _row < _Rnum ? _row : _Rnum;
            uni10_uint64 data_col = _col < _Cnum ? _col : _Cnum;

            for(uni10_int r = 0; r < (uni10_int)data_row; r++)
              tools_internal::UniElemCopy( &(Eout.elem_ptr_[r * _col]), &(Ein.elem_ptr_[r * _Cnum]), data_col * sizeof(_uni10_type) );

          }

        }

      }else{

        uni10_error_msg(true, "%s", "Resize fixTail is developping !!!");

      }


    }

} // End of namespace.

#endif
