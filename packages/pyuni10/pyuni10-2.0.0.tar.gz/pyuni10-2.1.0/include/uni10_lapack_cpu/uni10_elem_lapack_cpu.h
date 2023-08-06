#ifndef __UNI10_ELEM_LAPACK_CPU_H__
#define __UNI10_ELEM_LAPACK_CPU_H__

#include <iostream>
#include <vector>

#include "uni10_type.h"
#include "uni10_error.h"
#include "uni10_lapack_cpu/tools_lapack_cpu/uni10_tools_lapack_cpu.h"

namespace uni10{

  template<typename UniType>
    class UniElemLapackCpu{
      
      public:

        uni10_bool ongpu_;

        uni10_type_id uni10_typeid_;  

        uni10_uint64 elem_num_;

        UniType* elem_ptr_;

        explicit UniElemLapackCpu();

        explicit UniElemLapackCpu(uni10_uint64 row, uni10_uint64 col, uni10_bool diag = false, uni10_bool ongpu = false);

        UniElemLapackCpu( UniElemLapackCpu const& ksrcelem );

        template<typename U>
          UniElemLapackCpu< UniType >( UniElemLapackCpu<U> const& ksrcelem );

        UniElemLapackCpu& operator=( UniElemLapackCpu const& ksrcelem );

        template<typename U>
          UniElemLapackCpu<UniType>& operator=(UniElemLapackCpu<U> const& ksrcelem);

        ~UniElemLapackCpu();

        void Init( uni10_uint64 row, uni10_uint64 col, uni10_bool diag, UniElemLapackCpu const& ksrcelem );

        template<typename U>
          void Init( uni10_uint64 row, uni10_uint64 col, uni10_bool diag, UniElemLapackCpu<U> const& ksrcelem );

        void Init( uni10_uint64 row, uni10_uint64 col, uni10_bool diag, const UniType* ksrcptr=NULL );

        void set_elem_ptr(const UniType* ksrcptr, bool srcongpu = false);

        void SetZeros();

        void SetOnes();

        inline bool Empty() const{ return elem_ptr_ == NULL; }

        void Clear();

        void Copy( UniElemLapackCpu const& ksrcelem );

        template<typename U>
          void Copy(UniElemLapackCpu<U> const& ksrcelem);

        void Copy(uni10_uint64 begin_idx, const UniElemLapackCpu<UniType>& ksrcelem, uni10_uint64 begin_src_idx ,uni10_uint64 len);

        void Copy(uni10_uint64 begin_idx, const UniElemLapackCpu<UniType>& ksrcelem, uni10_uint64 len);

        void CatElem(const UniElemLapackCpu<UniType>& ksrcelem);

        void PrintElem(uni10_uint64 row, uni10_uint64 col, uni10_bool diag) const;

        void Save(FILE* fp) const;

        void Load(FILE* fp);

        void Reshape(const std::vector<int>& koriginbonddims, const std::vector<int>& knewbondidices, UniElemLapackCpu& out_elem, bool inorder);

        UniType& operator[](const uni10_uint64 kidx){

          uni10_error_msg( kidx > this->elem_num_, "%s", "The index is exceed the number of elements" );

          return this->elem_ptr_[kidx];

        }

        UniType operator[](const uni10_uint64 kidx) const{

          uni10_error_msg( kidx > this->elem_num_, "%s", "The index is exceed the number of elements" );

          return this->elem_ptr_[kidx];

        }

    };

}

#endif
