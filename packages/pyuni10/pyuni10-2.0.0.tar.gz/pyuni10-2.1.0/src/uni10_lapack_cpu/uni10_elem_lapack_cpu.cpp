#include "uni10_type.h"
#include "uni10_error.h"
#include "uni10_lapack_cpu/uni10_elem_lapack_cpu.h"

namespace uni10{

  template<typename UniType>
    UniElemLapackCpu<UniType>::UniElemLapackCpu(): ongpu_(false), uni10_typeid_(UNI10_TYPE_ID(UniType)), elem_num_(0), elem_ptr_(NULL){};

  template<typename UniType>
    UniElemLapackCpu<UniType>::UniElemLapackCpu(uni10_uint64 row, uni10_uint64 col, uni10_bool diag, uni10_bool ongpu): 
      ongpu_(ongpu), uni10_typeid_(UNI10_TYPE_ID(UniType)), elem_ptr_(NULL){

      Init(row, col, diag, NULL);

    }

  template<typename UniType>
    UniElemLapackCpu<UniType>::UniElemLapackCpu(UniElemLapackCpu<UniType> const& ksrcelem): 
      ongpu_(ksrcelem.ongpu_), uni10_typeid_(ksrcelem.uni10_typeid_), elem_num_(ksrcelem.elem_num_), elem_ptr_(NULL){

      uni10_error_msg(ksrcelem.elem_ptr_ != NULL && ksrcelem.elem_num_==0, "%s", "The pointer of this element container point to another pointer and does not allocate. Hence we can't copy it.");
      Init(1, ksrcelem.elem_num_, false, ksrcelem);

    };

  template<typename UniType>
    UniElemLapackCpu<UniType>::~UniElemLapackCpu(){

      if(elem_ptr_ != NULL && elem_num_ != 0)
        tools_internal::UniElemFree(elem_ptr_, elem_num_ * sizeof(UniType));

      elem_ptr_  = NULL;
      elem_num_  = 0;

    };

  template<typename UniType>
    UniElemLapackCpu<UniType>& UniElemLapackCpu<UniType>::operator=(UniElemLapackCpu const& ksrcelem){

      uni10_typeid_ = ksrcelem.uni10_typeid_;
      ongpu_        = ksrcelem.ongpu_;

      this->Init(1, ksrcelem.elem_num_, false, ksrcelem.elem_ptr_);

      return *this;

    }

  template<typename UniType>
    void UniElemLapackCpu<UniType>::SetZeros(){

      uni10_error_msg( elem_ptr_ == NULL || elem_num_ == 0, "%s", "Please Initialize the uni10_elem with the constructor uni10(uni10_uint64, uni10_uint64, bool) befero setting the elements.");

      uni10_uint64 memsize = elem_num_ * sizeof(UniType);

      tools_internal::UniElemZeros( elem_ptr_, memsize );

    };

  template<typename UniType>
    void UniElemLapackCpu<UniType>::SetOnes(){

      uni10_error_msg( elem_ptr_ == NULL || elem_num_ == 0, "%s", "Please Initialize the uni10_elem with the constructor uni10(uni10_uint64, uni10_uint64, bool) before setting the elements.");

      tools_internal::Ones( elem_ptr_, elem_num_ );

    };

  template<typename UniType>
    void UniElemLapackCpu<UniType>::set_elem_ptr(const UniType* ksrcptr, bool src_ongpu){

      uni10_error_msg( ksrcptr  == NULL, "%s", "The source ptr is NULL.");
      uni10_error_msg( elem_ptr_ == NULL, "%s", "Please Initialize the uni10_elem with the constructor uni10(uni10_uint64, uni10_uint64, bool) befero setting the elements.");
      uni10_error_msg( src_ongpu, "%s", " The source pointer is on the device. Please install MAGMA or CUDAONLY gpu version instead.");

      tools_internal::UniElemCopy( elem_ptr_, ksrcptr, elem_num_ * sizeof(UniType) );

    };

  template<typename UniType>
    void UniElemLapackCpu<UniType>::Init(uni10_uint64 row, uni10_uint64 col, uni10_bool diag, UniElemLapackCpu const& ksrcelem){

      if(elem_ptr_ != NULL && elem_num_ != 0)
        tools_internal::UniElemFree(elem_ptr_, elem_num_*sizeof(UniType));

      elem_num_ =  diag ? std::min(row, col) : row * col ;

      uni10_uint64 memsize = elem_num_ * sizeof(UniType);

      if ( memsize ){

        elem_ptr_ = (UniType*)tools_internal::UniElemAlloc( memsize );
        tools_internal::UniElemCopy( elem_ptr_, ksrcelem.elem_ptr_, memsize );

      }

    };

  template<typename UniType>
    void UniElemLapackCpu<UniType>::Init(uni10_uint64 row, uni10_uint64 col, uni10_bool diag, const UniType* ksrcptr){

      if(elem_ptr_ != NULL && elem_num_ != 0)
        tools_internal::UniElemFree(elem_ptr_, elem_num_*sizeof(UniType));

      elem_num_ =  diag ? std::min(row, col) : row * col ;

      uni10_uint64 memsize = elem_num_ * sizeof(UniType);

      if ( memsize ){

        elem_ptr_ = (UniType*)tools_internal::UniElemAlloc( memsize );
        if(ksrcptr != NULL){
          tools_internal::UniElemCopy( elem_ptr_, ksrcptr, memsize );
        }
        else{
          tools_internal::UniElemZeros( elem_ptr_, memsize );
        }

      }

    };

  template<typename UniType>
    void UniElemLapackCpu<UniType>::Copy(UniElemLapackCpu const& ksrcelem){

      uni10_uint64 memsize = elem_num_ * sizeof(UniType);
      tools_internal::UniElemCopy( elem_ptr_, ksrcelem.elem_ptr_, memsize );

    };

  template<typename UniType>
    void UniElemLapackCpu<UniType>::Clear(){

      if(elem_ptr_ != NULL && elem_num_ != 0)
        tools_internal::UniElemFree(elem_ptr_, elem_num_ * sizeof(UniType));

      elem_num_ = 0;
      elem_ptr_ = NULL;

    }

  template<typename UniType>
    void UniElemLapackCpu<UniType>::Copy(uni10_uint64 begin_idx, const UniElemLapackCpu<UniType>& ksrcelem, uni10_uint64 begin_src_idx, uni10_uint64 len){

      tools_internal::UniElemCopy(elem_ptr_ + begin_idx, ksrcelem.elem_ptr_ + begin_src_idx, len*sizeof(UniType));

    }

  template<typename UniType>
    void UniElemLapackCpu<UniType>::Copy(uni10_uint64 begin_idx, const UniElemLapackCpu<UniType>& ksrcelem, uni10_uint64 len){

      this->Copy(begin_idx, ksrcelem, 0, len);

    }

  template<typename UniType>
    void UniElemLapackCpu<UniType>::CatElem(const UniElemLapackCpu<UniType>& ksrcelem){
        
      this->elem_ptr_ = (UniType*)realloc(this->elem_ptr_, (this->elem_num_ + ksrcelem.elem_num_)*sizeof(UniType));
      this->Copy(this->elem_num_, ksrcelem, ksrcelem.elem_num_);
      this->elem_num_ += ksrcelem.elem_num_;

    }

  // If Actual Usage == 0 -> The pointer is shared with another allocated object. 
  // if Actual Usage != 0 -> The number is eqaul to allcated element number.
  // If diag, the number is equal to max(row, col);
  // If !diag, the number is eqaul to row*col;
  
  template<typename UniType>
    void UniElemLapackCpu<UniType>::PrintElem(uni10_uint64 row, uni10_uint64 col, bool diag) const{

      std::cout << std::endl <<  row << " x " << col << " = " << row*col << " [ Actual Usage: " << elem_num_ << " ]";

      if(uni10_typeid_ == 1)  std::cout << ", REAL";
      else if(uni10_typeid_ == 2)   std::cout << ", COMPLEX";

      if(diag)
        std::cout << ", Diagonal";

      std::cout << std::endl << std::endl;

      if ( row == 1 ) {
        std::cout << "[ " ;
      }
      else {
        std::cout << "[ " ;
        std::cout << std::endl ;
      }

      if(elem_ptr_ == NULL){
        std::cout << "\nThe UniElemLapackCpu has not been allocated or linked. \n\n";
        std::cout << "];\n";
      }
      else if(diag){
        for( uni10_int i = 0; i < (uni10_int)row; ++i ) {
          for( uni10_int j = 0; j < (uni10_int)col; ++j ) {
            if ( i != j ) {
              if(uni10_typeid_ == 2){
                std::cout << "   0.              " ;
              }
              else{
                std::cout << "   0.    " ;
              }
            }
            else {
              tools_internal::PrintElem_I(elem_ptr_[ i ]);
            }
          }
          if ( row > 1 ) {
            std::cout << std::endl;
          }
          else{
            std::cout << " ";
          }
        }
        std::cout <<  "];\n" ;

      }
      else{
        for( uni10_int i = 0; i < (uni10_int)row; ++i ) {
          for( uni10_int j = 0; j < (uni10_int)col; ++j ) {
            if ( elem_ptr_[ i * col + j] == 0.) {
              if(uni10_typeid_ == 2){
                std::cout << "   0.              " ;
              }
              else{
                std::cout << "   0.    ";
              }
            }
            else {
              tools_internal::PrintElem_I(elem_ptr_[ i * col + j ]);
            }
          }
          if ( row > 1 ){
            std::cout << std::endl;
          }
          else {
            std::cout << " ";
          }
        }
        std::cout << "];\n";
        
      }

    }

  template<typename UniType>
    void UniElemLapackCpu<UniType>::Save(FILE* fp) const{

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
    void UniElemLapackCpu<UniType>::Load(FILE* fp){

      uni10_type_id buftype;
      uni10_error_msg(!fread(&buftype, sizeof(uni10_typeid_), 1, fp), "%s", "Loading uni10_typeid_ is failure. (UNI10_LAPACKE_CPU<T>)");

      uni10_error_msg(buftype != uni10_typeid_, "%s", "TYPE ERROR. Can't loading a Real or Complex container to a Complex or Real one respectively.");

      uni10_error_msg(!fread(&ongpu_, sizeof(ongpu_), 1, fp), "%s", "Loading ongpu_ is failure. (UNI10_LAPACKE_CPU<T>)");
      uni10_uint64 bufelemNum;
      uni10_error_msg(!fread(&bufelemNum, sizeof(elem_num_), 1, fp), "%s", "Loading elem_num_ is failure. (UNI10_LAPACKE_CPU<T>)");

      if(elem_ptr_ != NULL && elem_num_ != 0 && bufelemNum != elem_num_)
        tools_internal::UniElemFree(elem_ptr_, elem_num_*sizeof(UniType));

      uni10_uint64 memsize = bufelemNum * sizeof(UniType);

      if ( memsize ){

        if(bufelemNum != elem_num_)
          elem_ptr_ = (UniType*)tools_internal::UniElemAlloc( memsize );

        elem_num_ = bufelemNum;
        uni10_error_msg(!fread(elem_ptr_, sizeof(UniType), elem_num_, fp), "%s", "Loading elem_ptr_ is failure. (UNI10_LAPACKE_CPU<T>)");

      }

    }

  /*
  template<typename UniType>
    void UniElemLapackCpu<UniType>::Reshape(const std::vector<int>& kOriginBondDims, const std::vector<int>& kbondIdices, UniElemLapackCpu<UniType>& outelem, bool inorder){

      int bondNum = kOriginBondDims.size();

      if(!inorder){

        std::vector<int> newAcc(bondNum);
        newAcc[bondNum - 1] = 1;

        std::vector<int> transAcc(bondNum);
        transAcc[bondNum - 1] = 1;
        for(int b = bondNum - 1; b > 0; b--){
          newAcc[b - 1] = newAcc[b] * kOriginBondDims[kbondIdices[b]];
        }

        std::vector<int> newbondDims(bondNum);
        std::vector<int> idxs(bondNum);

        for(int b = 0; b < bondNum; b++){
          transAcc[kbondIdices[b]] = newAcc[b];
          newbondDims[b] = kOriginBondDims[kbondIdices[b]];
          idxs[b] = 0;
        }

        int cnt_ot = 0;
        for(uni10_uint64 i = 0; i < elem_num_; i++){
          outelem.elem_ptr_[cnt_ot] = this->elem_ptr_[i];
          for(int bend = bondNum - 1; bend >= 0; bend--){
            idxs[bend]++;
            if(idxs[bend] < kOriginBondDims[bend]){
              cnt_ot += transAcc[bend];
              break;
            }
            else{
              cnt_ot -= transAcc[bend] * (idxs[bend] - 1);
              idxs[bend] = 0;
            }
          }
        }
      }else{
        outelem.Copy(0, *this, this->elem_num_);
      }

    }
  */

  template<> template<>
    void UniElemLapackCpu<uni10_complex128>::Init(uni10_uint64 row, uni10_uint64 col, uni10_bool diag, UniElemLapackCpu<uni10_double64> const& ksrcelem){

      if(elem_ptr_ != NULL && elem_num_ != 0)
        tools_internal::UniElemFree(elem_ptr_, elem_num_*sizeof(uni10_complex128));

      elem_num_ =  diag ? std::min(row, col) : row * col ;

      uni10_uint64 memsize = elem_num_ * sizeof(uni10_complex128);

      if ( memsize ){

        elem_ptr_ = (uni10_complex128*)tools_internal::UniElemAlloc( memsize );
        tools_internal::UniElemCast( elem_ptr_, ksrcelem.elem_ptr_, elem_num_ );

      }

    };

  template<> template<>
    void UniElemLapackCpu<uni10_double64>::Init(uni10_uint64 row, uni10_uint64 col, uni10_bool diag, UniElemLapackCpu<uni10_complex128> const& ksrcelem){

      if(elem_ptr_ != NULL && elem_num_ != 0)
        tools_internal::UniElemFree(elem_ptr_, elem_num_*sizeof(uni10_double64));

      elem_num_ =  diag ? std::min(row, col) : row * col ;

      uni10_uint64 memsize = elem_num_ * sizeof(uni10_double64);

      if ( memsize ){

        elem_ptr_ = (uni10_double64*)tools_internal::UniElemAlloc( memsize );
        tools_internal::UniElemCast( elem_ptr_, ksrcelem.elem_ptr_, elem_num_);

      }

    };


  template<> template<>
    UniElemLapackCpu<uni10_complex128>::UniElemLapackCpu(UniElemLapackCpu<uni10_double64> const& ksrcelem):
      ongpu_(ksrcelem.ongpu_), uni10_typeid_(ksrcelem.uni10_typeid_), elem_num_(ksrcelem.elem_num_), elem_ptr_(NULL){

      uni10_error_msg(ksrcelem.elem_ptr_ != NULL && ksrcelem.elem_num_==0, "%s", "The pointer of this element container point to another pointer and does not allocate. Hence we can't copy it.");
      Init(1, ksrcelem.elem_num_, false, ksrcelem);

    };

  template<> template<>
    UniElemLapackCpu<uni10_double64>::UniElemLapackCpu(UniElemLapackCpu<uni10_complex128> const& ksrcelem):
       ongpu_(ksrcelem.ongpu_), uni10_typeid_(ksrcelem.uni10_typeid_), elem_num_(ksrcelem.elem_num_), elem_ptr_(NULL){

      uni10_error_msg(ksrcelem.elem_ptr_ != NULL && ksrcelem.elem_num_==0, "%s", "The pointer of this element container point to another pointer and does not allocate. Hence we can't copy it.");
      Init(1, ksrcelem.elem_num_, false,ksrcelem);

    };

  template<> template<>
    UniElemLapackCpu<uni10_complex128>& UniElemLapackCpu<uni10_complex128>::operator=(UniElemLapackCpu<uni10_double64> const& ksrcelem){

      uni10_error_msg(ksrcelem.elem_ptr_ != NULL && ksrcelem.elem_num_==0, "%s", "The pointer of this element container point to another pointer and does not allocate. Hence we can't copy it.");

      uni10_typeid_ = ksrcelem.uni10_typeid_;
      ongpu_        = ksrcelem.ongpu_;
      Init(1, ksrcelem.elem_num_, false, ksrcelem);
      return *this;

    };

  template<> template<>
    UniElemLapackCpu<uni10_double64>& UniElemLapackCpu<uni10_double64>::operator=(UniElemLapackCpu<uni10_complex128> const& ksrcelem){

      uni10_error_msg(ksrcelem.elem_ptr_ != NULL && ksrcelem.elem_num_==0, "%s", "The pointer of this element container point to another pointer and does not allocate. Hence we can't copy it.");

      uni10_typeid_ = ksrcelem.uni10_typeid_;
      ongpu_        = ksrcelem.ongpu_;
      Init(1, ksrcelem.elem_num_, false, ksrcelem);
      return *this;

    };

  template<> template<>
    void UniElemLapackCpu<uni10_double64>::Copy(UniElemLapackCpu<uni10_complex128> const& ksrcelem){

      tools_internal::UniElemCast( elem_ptr_, ksrcelem.elem_ptr_, elem_num_ );

    };

  template<> template<>
    void UniElemLapackCpu<uni10_complex128>::Copy(UniElemLapackCpu<uni10_double64> const& ksrcelem){

      tools_internal::UniElemCast( elem_ptr_, ksrcelem.elem_ptr_, elem_num_ );

    };


  template class UniElemLapackCpu<uni10_double64>;
  template class UniElemLapackCpu<uni10_complex128>;

} /* namespace uni10 */
