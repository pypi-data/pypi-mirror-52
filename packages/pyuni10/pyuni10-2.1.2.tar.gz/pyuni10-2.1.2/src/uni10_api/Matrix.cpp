/****************************************************************************
 *  @file Matrix.h
 *  @license
 *    Universal Tensor Network Library
 *    Copyright (c) 2013-2014
 *    National Taiwan University
 *    National Tsing-Hua University

 *
 *    This file is part of Uni10, the Universal Tensor Network Library.
 *
 *    Uni10 is free software: you can redistribute it and/or modify
 *    it under the terms of the GNU Lesser General Public License as published by
 *    the Free Software Foundation, either version 3 of the License, or
 *    (at your option) any later version.
 *
 *    Uni10 is distributed in the hope that it will be useful,
 *    but WITHOUT ANY WARRANTY; without even the implied warranty of
 *    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *    GNU Lesser General Public License for more details.
 *
 *    You should have received a copy of the GNU Lesser General Public License
 *    along with Uni10.  If not, see <http://www.gnu.org/licenses/>.
 *  @endlicense
 *  @brief Header file for Matrix class
 *  @author Yun-Da Hsieh
 *  @date 2014-05-06
 *  @since 0.1.0
 *
 *****************************************************************************/
#include <math.h>

#include "uni10_error.h"
#include "uni10_api/Matrix.h"

namespace uni10{


  template <typename UniType>
    Matrix<UniType>::Matrix(): Block<UniType>(){};

  template <typename UniType>
    Matrix<UniType>::Matrix(uni10_uint64 row, uni10_uint64 col, uni10_bool diag): Block<UniType>(row, col, diag){
      Init_();
    };

  template <typename UniType>
    Matrix<UniType>::Matrix(uni10_uint64 row, uni10_uint64 col, UniType* srcptr, uni10_bool diag): Block<UniType>(row, col, diag){
      Init_(srcptr);
    };

  // Copy constructor
  template <typename UniType>
    Matrix<UniType>::Matrix(Matrix const& kmat): Block<UniType>(kmat.row_, kmat.col_, kmat.diag_){
      this->Init_(kmat.elem_);
    };

  template <typename UniType>
    Matrix<UniType>::Matrix(Block<UniType> const& kblk): Block<UniType>(kblk.row_, kblk.col_, kblk.diag_){
      this->Init_( kblk.elem_);
    };

  template <typename UniType>
    Matrix<UniType>::Matrix(const std::string& kfilename){

      FILE* fp = fopen(kfilename.c_str(), "r");
      uni10_error_msg(!fread(&this->row_, sizeof(this->row_), 1, fp), "%s", "Loading row_ is failure. (Matrix<T>)");
      uni10_error_msg(!fread(&this->col_, sizeof(this->col_), 1, fp), "%s", "Loading col_ is failure. (Matrix<T>)");
      uni10_error_msg(!fread(&this->diag_, sizeof(this->diag_), 1, fp), "%s", "Loading diag_ is failure. (Matrix<T>)");
      this->elem_.Load(fp);
      fclose(fp);

    };

  template <typename UniType>
    Matrix<UniType>::~Matrix(){};

  template<typename UniType>
    Matrix<UniType>& Matrix<UniType>::operator=(const Matrix<UniType>& kmat){
      this->row_   = kmat.row_;
      this->col_   = kmat.col_;
      this->diag_  = kmat.diag_;
      this->Init_(kmat.elem_);
      return *this;
    }

  template<typename UniType>
    Matrix<UniType>& Matrix<UniType>::operator=(const Block<UniType>& kblk){
      this->row_  = kblk.row_;
      this->col_  = kblk.col_;
      this->diag_ = kblk.diag_;
      this->Init_(kblk.elem_);
      return *this;
    }

  template<typename UniType>
    Matrix<UniType>& Matrix<UniType>::operator+=(const Matrix<UniType>& kmat){
      linalg_unielem_internal::MatrixAdd(&this->elem_, &this->diag_, &kmat.elem_, &kmat.diag_, &kmat.row_, &kmat.col_ );
      this->diag_ = (this->diag_ && kmat.diag_);
      return *this;
    }

  template<typename UniType>
    Matrix<UniType>& Matrix<UniType>::operator-=(const Matrix<UniType>& kmat){
      linalg_unielem_internal::MatrixSub(&this->elem_, &this->diag_, &kmat.elem_, &kmat.diag_, &kmat.row_, &kmat.col_ );
      this->diag_ = (this->diag_ && kmat.diag_);
      return *this;
    };

  template<typename UniType>
    Matrix<UniType>& Matrix<UniType>::operator*=(uni10_double64 a){ 
      linalg_unielem_internal::VectorScal(&a, &this->elem_, &this->elem_.elem_num_);
      return *this;
    }

  template<typename UniType>
    Matrix<UniType>& Matrix<UniType>::operator*=(const Matrix<UniType>& _m){            
      linalg_unielem_internal::MatrixMul(&this->elem_, &this->diag_, &_m.elem_, &_m.diag_, &_m.row_, &_m.col_ );
      this->diag_ = (this->diag_ || _m.diag_);
      return *this;
    }

  template <typename UniType>
    void Matrix<UniType>::Assign(uni10_uint64 row, uni10_uint64 col, uni10_bool diag){
      this->diag_ = diag;
      this->row_  = row;
      this->col_  = col;
      this->Init_();
    };

  template <typename UniType>
    void Matrix<UniType>::Load(const std::string& kfilename){

      FILE* fp = fopen(kfilename.c_str(), "r");
      uni10_error_msg(!fread(&this->row_ , sizeof(this->row_) , 1, fp), "%s", "Loading row_ is failure. (Matrix<T>)");
      uni10_error_msg(!fread(&this->col_ , sizeof(this->col_) , 1, fp), "%s", "Loading col_ is failure. (Matrix<T>)");
      uni10_error_msg(!fread(&this->diag_, sizeof(this->diag_), 1, fp), "%s", "Loading diag_ is failure. (Matrix<T>)");
      this->elem_.Load(fp);
      fclose(fp);

    };

  template <typename UniType>

    void Matrix<UniType>::SetElem(const UniType* ksrcptr, bool src_ongpu){

      uni10_error_msg( src_ongpu, "%s", " The source pointer is on the device. Please install the MAGMA or CUDAONLY gpu version instead.");

      if(this->elem_.uni10_typeid_ != UNI10_TYPE_ID(UniType)){

        uni10_error_msg( true, "%s", " Developping !!!");

      }

      this->elem_.set_elem_ptr(ksrcptr);

    };

  template <typename UniType>
    void Matrix<UniType>::SetElem(const std::vector<UniType>& ksrcvec, bool src_ongpu){

      uni10_error_msg( src_ongpu, "%s", " The source pointer is on the device. Please install the MAGMA or CUDAONLY gpu version instead.");

      uni10_error_msg(this->diag_ == false && this->row_*this->col_ != ksrcvec.size(),
          "Number of the input elements is: %ld, and it doesn't match to the size of matrix: %ld", ksrcvec.size(), this->row_*this->col_);

      uni10_error_msg(this->diag_ == true && fmin(this->row_, this->col_) != ksrcvec.size(), 
          "Number of the input elements is: %ld, and it doesn't match to the size of matrix: %.0f", ksrcvec.size(), fmin(this->row_,this->col_));

      SetElem(&ksrcvec[0], src_ongpu);

    };

  template <typename UniType>
    void Matrix<UniType>::Init_(const UniType* ksrcptr){

        this->elem_.Init(this->row_, this->col_, this->diag_, ksrcptr);

    };

  template <typename UniType>
    void Matrix<UniType>::Init_(const UELEM(UniElem, _package, _type)<UniType>& ksrcelem){

        this->elem_.Init(this->row_, this->col_, this->diag_, ksrcelem);

    };

  template <typename UniType>
    void Matrix<UniType>::SetDiag(const uni10_bool diag){

        this->diag_ = diag;

    };

  template <typename UniType>
    void Matrix<UniType>::Zeros(){

      this->elem_.SetZeros();

    };

  template <typename UniType>
    void Matrix<UniType>::Identity(){

      uni10_error_msg(this->ElemNum() == 0, "%s", "The matrix has not been initialized!!!");

      this->diag_ = true;
      if(!this->IsEmpty())
        this->elem_.Clear();
      this->elem_.Init(this->row_, this->col_, this->diag_);

      for(uni10_uint64 i = 0; i < this->elem_.elem_num_; i++)
        this->elem_.elem_ptr_[i] = 1.;

    };
  
  template<typename UniType> 
    void Matrix<UniType>::Randomize(char uniform_or_normal, uni10_double64 low_or_mu, uni10_double64 up_or_var, uni10_int64 seed){

      if(uniform_or_normal == 'U'){
        uni10_double64 dn = std::min(low_or_mu, up_or_var);
        uni10_double64 up = std::max(low_or_mu, up_or_var);
        linalg_unielem_internal::UniformRandomize(&this->elem_, &this->diag_, &this->row_, &this->col_, &dn, &up, &seed);
      }else if(uniform_or_normal == 'N'){
        linalg_unielem_internal::NormalRandomize(&this->elem_, &this->diag_, &this->row_, &this->col_, &low_or_mu, &up_or_var, &seed);
      }else
        uni10_error_msg(true, "%s", "Wrong flag. Hint: The fisrt parameter must be 'N' or 'U'");

    };

  template<typename UniType> 
    void Matrix<UniType>::OrthoRand(char uniform_or_normal, uni10_double64 low_or_mu, uni10_double64 up_or_var, uni10_int64 seed){

      if(uniform_or_normal == 'U'){
        uni10_double64 dn = std::min(low_or_mu, up_or_var);
        uni10_double64 up = std::max(low_or_mu, up_or_var);
        linalg_unielem_internal::UniformRandomize(&this->elem_, &this->diag_, &this->row_, &this->col_, &dn, &up, &seed);
      }
      else if(uniform_or_normal == 'N'){
        linalg_unielem_internal::NormalRandomize(&this->elem_, &this->diag_, &this->row_, &this->col_, &low_or_mu, &up_or_var, &seed);
        Matrix<UniType> tmp = *this;
      }
      else
        uni10_error_msg(true, "%s", "Wrong flag. Hint: The fisrt parameter must be 'N' or 'U'");

      uni10_uint64 min = std::min(this->row_, this->col_);
      UELEM(UniElem, _package, _type)<UniType>* u_elem  = NULL;
      UELEM(UniElem, _package, _type)<UniType>* vt_elem = NULL;
      UELEM(UniElem, _package, _type)<UniType> s(this->row_, this->col_, true);
      if(this->row_ < this->col_){
        vt_elem = new UELEM(UniElem, _package, _type)<UniType>(min, this->col_, this->diag_);
        linalg_unielem_internal::Svd(&this->elem_, &this->diag_, &this->row_, &this->col_, u_elem, &s, vt_elem);
        this->elem_.Copy(*vt_elem);
      }else{
        u_elem = new UELEM(UniElem, _package, _type)<UniType>(this->row_, min, this->diag_);
        linalg_unielem_internal::Svd(&this->elem_, &this->diag_, &this->row_, &this->col_, u_elem, &s, vt_elem);
        this->elem_.Copy(*u_elem);
      }

      if(u_elem != NULL)
        delete u_elem;
      else if(vt_elem != NULL)
        delete vt_elem;

    };

  Matrix<uni10_complex128>& operator*=(Matrix<uni10_complex128>& mat, uni10_complex128 a){ 
    linalg_unielem_internal::VectorScal(&a, &mat.elem_, &mat.elem_.elem_num_);
    return mat;
  }

  template class Matrix<uni10_double64>;
  template class Matrix<uni10_complex128>;

}  /* namespace uni10 */
