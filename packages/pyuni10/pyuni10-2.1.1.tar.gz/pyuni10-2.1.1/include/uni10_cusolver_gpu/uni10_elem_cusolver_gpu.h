#ifndef __UNI10_ELEM_CUSOLVER_GPU_H__
#define __UNI10_ELEM_CUSOLVER_GPU_H__

#include <iostream>
#include <vector>

#include "uni10_type.h"
#include "uni10_error.h"
#include "uni10_cusolver_gpu/tools_cusolver_gpu/uni10_tools_cusolver_gpu.h"

namespace uni10{

  template<typename UniType>
    class UniElemCusolverGpu{

      public:

        uni10_bool ongpu_;

        uni10_type_id uni10_typeid_;  

        uni10_uint64 elem_num_;

        UniType* elem_ptr_;

        // Done
        explicit UniElemCusolverGpu();

        // Done
        explicit UniElemCusolverGpu(uni10_uint64 row, uni10_uint64 col, uni10_bool diag = false, uni10_bool _ongpu = UNI10_ONGPU);

        // Done
        UniElemCusolverGpu(UniElemCusolverGpu const& ksrcelem);

        // Done
        template<typename U>
          UniElemCusolverGpu<UniType>(UniElemCusolverGpu<U> const& ksrcelem);

        UniElemCusolverGpu& operator=(UniElemCusolverGpu const& ksrcelem);

        template<typename U>
          UniElemCusolverGpu<UniType>& operator=(UniElemCusolverGpu<U> const& ksrcelem);

        ~UniElemCusolverGpu();

        void Init(uni10_uint64 row, uni10_uint64 col, uni10_bool diag, UniElemCusolverGpu const& ksrcelem);

        template<typename U>
          void Init(uni10_uint64 row, uni10_uint64 col, uni10_bool diag, UniElemCusolverGpu<U> const& ksrcelem);

        void Init(uni10_uint64 row, uni10_uint64 col, uni10_bool diag, const UniType* src=NULL, uni10_bool srcongpu=false);

        void set_elem_ptr(const UniType* ksrcptr, bool srcongpu = false);

        void SetZeros();

        inline bool Empty() const{ return elem_ptr_ == NULL; }

        void Clear();

        // Done
        void Copy(UniElemCusolverGpu const& ksrcelem);

        template<typename U>
          void Copy(UniElemCusolverGpu<U> const& ksrcelem);

        void Copy(uni10_uint64 begin_idx, const UniElemCusolverGpu<UniType>& ksrcelem, uni10_uint64 begin_src_idx ,uni10_uint64 len);

        void Copy(uni10_uint64 begin_idx, const UniElemCusolverGpu<UniType>& ksrcelem, uni10_uint64 len);

        void CatElem(const UniElemCusolverGpu<UniType>& ksrcelem);

        // Done
        void PrintElem(uni10_uint64 row, uni10_uint64 col, uni10_bool diag) const;

        // Done
        void Save(FILE* fp) const;

        // Done
        void Load(FILE* fp);

        void Reshape(const std::vector<int>& koriginbonddims, const std::vector<int>& knewbondidices, UniElemCusolverGpu& out_elem, bool inorder);

        UniType& operator[](const uni10_uint64 kidx){

          uni10_error_msg(kidx>this->elem_num_, "%s", "The index is exceed the number of elements");

          return this->elem_ptr_[kidx];

        }

        UniType operator[](const uni10_uint64 kidx) const{

          uni10_error_msg( kidx > this->elem_num_, "%s", "The index is exceed the number of elements" );

          return this->elem_ptr_[kidx];

        }

    };

}

#endif
