#include "uni10_type.h"
#include "uni10_error.h"
#include "uni10_cusolver_gpu/uni10_elem_cusolver_gpu.h"
#include "uni10_cusolver_gpu/tools_cusolver_gpu/cuda_kernel_funcs/uni10_kernel_gpu.h"

namespace uni10{

  template<typename UniType>
    UniElemCusolverGpu<UniType>::UniElemCusolverGpu(): uni10_typeid_(UNI10_TYPE_ID(UniType)), ongpu_(UNI10_ONGPU), elem_num_(0), elem_ptr_(NULL){};

  template<typename UniType>
    UniElemCusolverGpu<UniType>::UniElemCusolverGpu(uni10_uint64 row, uni10_uint64 col, uni10_bool diag, uni10_bool _ongpu): uni10_typeid_(UNI10_TYPE_ID(UniType)), ongpu_(_ongpu),elem_ptr_(NULL){

      Init(row, col, diag, NULL);

    }

  template<typename UniType>
    UniElemCusolverGpu<UniType>::UniElemCusolverGpu(UniElemCusolverGpu const& ksrcelem): 
      uni10_typeid_(ksrcelem.uni10_typeid_), ongpu_(ksrcelem.ongpu_), elem_num_(ksrcelem.elem_num_), elem_ptr_(NULL){

      uni10_error_msg(ksrcelem.elem_ptr_ != NULL && ksrcelem.elem_num_==0, "%s", "The pointer of this element container point to another pointer and does not allocate. Hence we can't copy it.");
      Init(1, elem_num_, false, ksrcelem.elem_ptr_);

    };

  template<typename UniType>
    UniElemCusolverGpu<UniType>::~UniElemCusolverGpu(){

      if(elem_ptr_ != NULL && elem_num_ != 0)
        tools_internal::UniElemFree(elem_ptr_, elem_num_ * sizeof(UniType), ongpu_);

      elem_ptr_ = NULL;
      elem_num_ = 0;

    };

  template<typename UniType>
    UniElemCusolverGpu<UniType>& UniElemCusolverGpu<UniType>::operator=(UniElemCusolverGpu const& ksrcelem){

      uni10_error_msg(ksrcelem.elem_ptr_ != NULL && ksrcelem.elem_num_==0, "%s", "The pointer of this element container point to another pointer and does not allocate. Hence we can't copy it.");
      uni10_typeid_ = ksrcelem.uni10_typeid_;
      ongpu_        = ksrcelem.ongpu_;
      this->Init(1, ksrcelem.elem_num_, false, ksrcelem.elem_ptr_);
      return *this;

    }

  template<typename UniType>
    void UniElemCusolverGpu<UniType>::Init(uni10_uint64 row, uni10_uint64 col, uni10_bool diag, const UniType* ksrcelem, uni10_bool srcongpu){

      if(elem_ptr_ != NULL && elem_num_ != 0)
        tools_internal::UniElemFree(elem_ptr_, elem_num_*sizeof(UniType), ongpu_);

      elem_num_ =  diag ? std::min(row, col) : row * col ;

      uni10_uint64 memsize = elem_num_ * sizeof(UniType);

      if ( memsize ){

        // The function tools_internal::UniElemAlloc is going to decide allocating memory on the device or the host.
        // So if RUNTIMETYPE is setted as hybird, the variable ongpu_ might be modified.
        elem_ptr_ = (UniType*)tools_internal::UniElemAlloc( memsize , ongpu_);

        if(ksrcelem != NULL){
          tools_internal::UniElemCopy( elem_ptr_, ksrcelem, memsize, ongpu_, srcongpu);
        }
        else{
          tools_internal::UniElemZeros( elem_ptr_, memsize , ongpu_);
        }

      }

    };


  template<typename UniType>
    void UniElemCusolverGpu<UniType>::Init(uni10_uint64 row, uni10_uint64 col, uni10_bool diag, UniElemCusolverGpu const& ksrcelem){

      //if(elem_ptr_ != NULL && elem_ptr_Nu == 0)
      if(elem_ptr_ != NULL && elem_num_ != 0)
        tools_internal::UniElemFree(elem_ptr_, elem_num_*sizeof(UniType), ongpu_);

      elem_num_ = diag ? std::min(row, col) : row*col;

      uni10_uint64 memsize = elem_num_ * sizeof(UniType);

      if ( memsize ){

        elem_ptr_ = (UniType*)tools_internal::UniElemAlloc( memsize, ongpu_ );
        tools_internal::UniElemCopy( elem_ptr_, ksrcelem.elem_ptr_, memsize, ongpu_, ksrcelem.ongpu_ );

      }

    };


  template<typename UniType>
    void UniElemCusolverGpu<UniType>::SetZeros(){

      uni10_error_msg( elem_ptr_ == NULL || elem_num_ == 0, "%s", "Please Initialize the uni10_elem with the constructor uni10(uni10_uint64, uni10_uint64, bool) befero setting the elements.");

      uni10_uint64 memsize = elem_num_ * sizeof(UniType);

      tools_internal::UniElemZeros( elem_ptr_, memsize , ongpu_);

    };

  template<typename UniType>
    void UniElemCusolverGpu<UniType>::set_elem_ptr(const UniType* ksrcptr, bool srcongpu){

      uni10_error_msg( srcongpu, "%s", " The source pointer is on the device. Please install MAGMA_GPU or CUSOLVER_GPU version instead.");
      uni10_error_msg( elem_ptr_ == NULL, "%s", "Please Initialize the uni10_elem with the constructor uni10(uni10_uint64, uni10_uint64, bool) befero setting the elements.");
      uni10_error_msg( ksrcptr  == NULL, "%s", "The source ptr is NULL.");

      tools_internal::UniElemCopy( elem_ptr_, ksrcptr, elem_num_ * sizeof(UniType), ongpu_, srcongpu);

    };

  template<typename UniType>
    void UniElemCusolverGpu<UniType>::Clear(){
      

      if(elem_ptr_ != NULL && elem_num_ != 0)
        tools_internal::UniElemFree(elem_ptr_, elem_num_ * sizeof(UniType), ongpu_);

      elem_num_ = 0;
      elem_ptr_ = NULL;

    }

  //
  // The default value of srcongpu is "false".
  //
  template<typename UniType>
    void UniElemCusolverGpu<UniType>::Copy(UniElemCusolverGpu const& ksrcelem){

      uni10_uint64 memsize = elem_num_ * sizeof(UniType);
      tools_internal::UniElemCopy( elem_ptr_, ksrcelem.elem_ptr_, memsize, ongpu_, ksrcelem.ongpu_);

    };

  template<typename UniType>
    void UniElemCusolverGpu<UniType>::Copy(uni10_uint64 begin_idx, const UniElemCusolverGpu<UniType>& ksrcelem, uni10_uint64 begin_src_idx, uni10_uint64 len){

      tools_internal::UniElemCopy( elem_ptr_ + begin_idx, ksrcelem.elem_ptr_ + begin_src_idx, len*sizeof(UniType), ongpu_, ksrcelem.ongpu_);

    }

  template<typename UniType>
    void UniElemCusolverGpu<UniType>::Copy(uni10_uint64 begin_idx, const UniElemCusolverGpu<UniType>& ksrcelem, uni10_uint64 len){

      this->Copy(begin_idx, ksrcelem, 0, len);

    }

  template<> template<>
    void UniElemCusolverGpu<uni10_double64>::Copy(UniElemCusolverGpu<uni10_complex128> const& ksrcelem){

      tools_internal::UniElemCast( elem_ptr_, ksrcelem.elem_ptr_, elem_num_, ongpu_, ksrcelem.ongpu_);

    };

  template<> template<>
    void UniElemCusolverGpu<uni10_complex128>::Copy(UniElemCusolverGpu<uni10_double64> const& ksrcelem){

      tools_internal::UniElemCast( elem_ptr_, ksrcelem.elem_ptr_, elem_num_, ongpu_, ksrcelem.ongpu_);

    };

  template<typename UniType>
    void UniElemCusolverGpu<UniType>::CatElem(const UniElemCusolverGpu<UniType>& ksrcelem){
        
      this->elem_ptr_ = (UniType*)realloc(this->elem_ptr_, (this->elem_num_ +ksrcelem.elem_num_)*sizeof(UniType));

      this->Copy(this->elem_num_, ksrcelem, ksrcelem.elem_num_);

      this->elem_num_ += ksrcelem.elem_num_;

    }

  template<typename UniType>
    void UniElemCusolverGpu<UniType>::PrintElem(uni10_uint64 row, uni10_uint64 col, bool diag) const{

      UniType* buffer = NULL;
      uni10_uint64 memsize = (diag) ? std::min(row, col) * sizeof(UniType) : row * col * sizeof(UniType);

      checkCudaErrors(cudaMallocHost(&buffer, memsize));

      tools_internal::UniElemCopy(buffer, elem_ptr_, memsize, false, ongpu_);

      fprintf(stdout, "\n%ld x %ld = %ld [ Real ElemNum: %ld ]", row, col, row*col, elem_num_);

      if(uni10_typeid_ == 1)  fprintf(stdout, ", REAL");
      else if(uni10_typeid_ == 2)   fprintf(stdout, ", COMPLEX" );

      if(diag)
        fprintf(stdout, ", Diagonal");

      if(ongpu_)
        fprintf(stdout, ", onGPU");
      else
        fprintf(stdout, ", onCPU");

      fprintf(stdout, "\n\n");

      if ( row == 1 ) {
        fprintf(stdout, "[ " );
      }
      else {
        fprintf(stdout, "[\n" );
      }

      if(elem_ptr_ == NULL){
        fprintf(stdout, "\nThe UniElemCusolverGpu has not been allocated or linked. \n\n" );
        fprintf(stdout, "];\n" );
      }
      else if(diag){
        for( int i = 0; i < (int)row; ++i ) {
          for( int j = 0; j < (int)col; ++j ) {
            if ( i != j) {
              if(uni10_typeid_ == 2)
                fprintf(stdout, "   0.              " );
              else
                fprintf(stdout, "   0.    " );
            }
            else {
              tools_internal::PrintElem_I(buffer[ i ]);
            }
          }
          if ( row > 1 ) 
            fprintf(stdout, "\n" );
          else 
            fprintf(stdout, " " );
        }
        fprintf(stdout, "];\n" );

      }
      else{
        for( int i = 0; i < (int)row; ++i ) {
          for( int j = 0; j < (int)col; ++j ) {
            if ( buffer[ i * col + j] == 0.) {
              if(uni10_typeid_ == 2)
                fprintf(stdout, "   0.              " );
              else
                fprintf(stdout, "   0.    " );
            }
            else {
              tools_internal::PrintElem_I(buffer[ i * col + j ]);
            }
          }
          if ( row > 1 ) 
            fprintf(stdout, "\n" );
          else 
            fprintf(stdout, " " );
        }
        fprintf(stdout, "];\n" );
      }

      checkCudaErrors(cudaFreeHost(buffer));

    }

  template<typename UniType>
    void UniElemCusolverGpu<UniType>::Save(FILE* fp) const{

      fwrite(&uni10_typeid_, sizeof(uni10_typeid_), 1, fp);
      fwrite(&ongpu_, sizeof(ongpu_), 1, fp);
      fwrite(&elem_num_, sizeof(elem_num_), 1, fp);
      fwrite(elem_ptr_, sizeof(UniType), elem_num_, fp);

    }

  //
  // This function has a requerment.
  // If the length of elements in the file is equal to the elem_num_, we copy the values directly without allocation because the operation malloc() will change the address.
  // If the address of elem_ptr_ is changed, the UniTensor<T>::load() will crash.
  //
  template<typename UniType>
    void UniElemCusolverGpu<UniType>::Load(FILE* fp){

      uni10_type_id buftype;
      uni10_error_msg(!fread(&buftype, sizeof(uni10_typeid_), 1, fp), "%s", "Loading uni10_typeid_ is failure. (UNI10_CUSOLVER_GPU<T>)");

      uni10_error_msg(buftype != uni10_typeid_, "%s", "TYPE ERROR. Can't loading a Real or Complex container to a Complex or Real one respectively.");

      uni10_error_msg(!fread(&ongpu_, sizeof(ongpu_), 1, fp), "%s", "Loading ongpu_ is failure. (UNI10_CUSOLVER_GPU<T>)");
      uni10_uint64 bufelemNum;
      uni10_error_msg(!fread(&bufelemNum, sizeof(elem_num_), 1, fp), "%s", "Loading elem_num_ is failure. (UNI10_CUSOLVER_GPU<T>)");

      if(elem_ptr_ != NULL && elem_num_ != 0 && bufelemNum != elem_num_)
        tools_internal::UniElemFree(elem_ptr_, elem_num_*sizeof(UniType), ongpu_);

      uni10_uint64 memsize = bufelemNum * sizeof(UniType);

      if ( memsize ){

        if(bufelemNum != elem_num_)
          elem_ptr_ = (UniType*)tools_internal::UniElemAlloc( memsize, ongpu_);

        elem_num_ = bufelemNum;
        uni10_error_msg(!fread(elem_ptr_, sizeof(UniType), elem_num_, fp), "%s", "Loading elem_ptr_ is failure. (UNI10_CUSOLVER_GPU<T>)");

      }

    }

  template<typename UniType>
    void UniElemCusolverGpu<UniType>::Reshape(const std::vector<int>& ori_bdDims, const std::vector<int>& new_bdIdx, UniElemCusolverGpu<UniType>& out_elem, bool inorder){

      int bondNum = ori_bdDims.size();

      if(!inorder){

        if(RUNTIMETYPE == only_cpu){

          std::vector<int> newAcc(bondNum);
          newAcc[bondNum - 1] = 1;

          std::vector<int> transAcc(bondNum);
          transAcc[bondNum - 1] = 1;
          for(int b = bondNum - 1; b > 0; b--){
            newAcc[b - 1] = newAcc[b] * ori_bdDims[new_bdIdx[b]];
          }

          std::vector<int> newbondDims(bondNum);
          std::vector<int> idxs(bondNum);

          for(int b = 0; b < bondNum; b++){
            transAcc[new_bdIdx[b]] = newAcc[b];
            newbondDims[b] = ori_bdDims[new_bdIdx[b]];
            idxs[b] = 0;
          }

          int cnt_ot = 0;
          for(uni10_uint64 i = 0; i < elem_num_; i++){
            out_elem.elem_ptr_[cnt_ot] = this->elem_ptr_[i];
            for(int bend = bondNum - 1; bend >= 0; bend--){
              idxs[bend]++;
              if(idxs[bend] < ori_bdDims[bend]){
                cnt_ot += transAcc[bend];
                break;
              }
              else{
                cnt_ot -= transAcc[bend] * (idxs[bend] - 1);
                idxs[bend] = 0;
              }
            }
          }

        }

        else if(RUNTIMETYPE == only_gpu){

          size_t* perInfo = (size_t*) malloc (bondNum * 2 * sizeof(size_t));
          std::vector<size_t> newAcc(bondNum);
          newAcc[bondNum-1] = 1;
          perInfo[bondNum-1] = 1;
          for(int b = bondNum - 1; b > 0; b--){
            newAcc[b - 1] = newAcc[b] * ori_bdDims[new_bdIdx[b]];
            perInfo[b - 1] = perInfo[b] * ori_bdDims[b];
          }
          for(int b = 0; b < bondNum; b++)
            perInfo[bondNum + new_bdIdx[b]] = newAcc[b];

          linalg_driver_internal::Reshape_kernel(elem_ptr_, bondNum, elem_num_, perInfo, out_elem.elem_ptr_);

          free(perInfo);

        }

        else if(RUNTIMETYPE == hybrid){

          uni10_error_msg(true, "%s", "Developing");

        }


      }else{
        out_elem.Copy(0, *this, this->elem_num_);
      }

    }

  template<> template<>
    void UniElemCusolverGpu<uni10_complex128>::Init(uni10_uint64 row, uni10_uint64 col, uni10_bool diag, UniElemCusolverGpu<uni10_double64> const& ksrcelem){

      if(elem_ptr_ != NULL && elem_num_ != 0)
        tools_internal::UniElemFree(elem_ptr_, elem_num_*sizeof(uni10_complex128), ongpu_);

      elem_num_ = diag ? std::min(row, col) : row*col;

      uni10_uint64 memsize = elem_num_ * sizeof(uni10_complex128);

      if ( memsize ){

        elem_ptr_ = (uni10_complex128*)tools_internal::UniElemAlloc( memsize, ongpu_ );
        tools_internal::UniElemCast( elem_ptr_, ksrcelem.elem_ptr_, elem_num_, ongpu_, ksrcelem.ongpu_ );

      }

    };

  template<> template<>
    void UniElemCusolverGpu<uni10_double64>::Init(uni10_uint64 row, uni10_uint64 col, uni10_bool diag, UniElemCusolverGpu<uni10_complex128> const& ksrcelem){

      if(elem_ptr_ != NULL && elem_num_ != 0)
        tools_internal::UniElemFree(elem_ptr_, elem_num_*sizeof(uni10_double64), ongpu_);

      elem_num_ = diag ? std::min(row, col) : row*col;

      uni10_uint64 memsize = elem_num_ * sizeof(uni10_double64);

      if ( memsize ){

        elem_ptr_ = (uni10_double64*)tools_internal::UniElemAlloc( memsize, ongpu_ );
        tools_internal::UniElemCast( elem_ptr_, ksrcelem.elem_ptr_, elem_num_, ongpu_, ksrcelem.ongpu_);

      }

    };

  template<> template<>
    UniElemCusolverGpu<uni10_complex128>::UniElemCusolverGpu(UniElemCusolverGpu<uni10_double64> const& ksrcelem):
      uni10_typeid_(ksrcelem.uni10_typeid_), ongpu_(ksrcelem.ongpu_), elem_num_(ksrcelem.elem_num_), elem_ptr_(NULL){

      uni10_error_msg(ksrcelem.elem_ptr_ != NULL && ksrcelem.elem_num_==0, "%s", "The pointer of this element container point to another pointer and does not allocate. Hence we can't copy it.");
      Init(1, ksrcelem.elem_num_, false, ksrcelem);

    };

  template<> template<>
    UniElemCusolverGpu<uni10_double64>::UniElemCusolverGpu(UniElemCusolverGpu<uni10_complex128> const& ksrcelem):
      uni10_typeid_(ksrcelem.uni10_typeid_), ongpu_(ksrcelem.ongpu_), elem_num_(ksrcelem.elem_num_), elem_ptr_(NULL){

      uni10_error_msg(ksrcelem.elem_ptr_ != NULL && ksrcelem.elem_num_==0, "%s", "The pointer of this element container point to another pointer and does not allocate. Hence we can't copy it.");
      Init(1, ksrcelem.elem_num_, false, ksrcelem);

    };

  template<> template<>
    UniElemCusolverGpu<uni10_complex128>& UniElemCusolverGpu<uni10_complex128>::operator=(UniElemCusolverGpu<uni10_double64> const& ksrcelem){

      uni10_error_msg(ksrcelem.elem_ptr_ != NULL && ksrcelem.elem_num_==0, "%s", "The pointer of this element container point to another pointer and does not allocate. Hence we can't copy it.");
      uni10_typeid_ = ksrcelem.uni10_typeid_;
      ongpu_        = ksrcelem.ongpu_;
      Init(1, ksrcelem.elem_num_, false, ksrcelem);
      return *this;

    };

  template<> template<>
    UniElemCusolverGpu<uni10_double64>& UniElemCusolverGpu<uni10_double64>::operator=(UniElemCusolverGpu<uni10_complex128> const& ksrcelem){

      uni10_error_msg(ksrcelem.elem_ptr_ != NULL && ksrcelem.elem_num_==0, "%s", "The pointer of this element container point to another pointer and does not allocate. Hence we can't copy it.");
      uni10_typeid_ = ksrcelem.uni10_typeid_;
      ongpu_        = ksrcelem.ongpu_;
      Init(1, ksrcelem.elem_num_, false, ksrcelem);
      return *this;

    };


  template class UniElemCusolverGpu<uni10_double64>;
  template class UniElemCusolverGpu<uni10_complex128>;

} /* namespace uni10 */
