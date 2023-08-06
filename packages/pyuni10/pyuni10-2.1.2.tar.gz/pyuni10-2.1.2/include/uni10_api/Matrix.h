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
#ifndef __UNI10_MATRIX_H__
#define __UNI10_MATRIX_H__

#include "uni10_api/Block.h"

namespace uni10{

  /// @class Matrix
  /// @brief The Matrix class defines a common matrix
  ///
  /// Matrix is an auxilliary class used to extract block information on UniTensor and perform linear algebra
  /// operations. A symmetric tensor contains Block's with corresponding Qnum's. Each block is a Matrix with
  /// tensor elements. 
  ///
  /// The Matrix follows the C convention that the memory storage is row-major and indices start from 0.
  ///
  /// All the basic opertors of Block also work on Matrix.
  ///
  /// @see \ref Block, UniTensor
  
  // Element-wise multiplication.
  template<typename T>
    Matrix<T> operator*(uni10_double64 a, const Block<T>& kblk); 

  template<typename T>
    Matrix<uni10_complex128> operator*(uni10_complex128 a, const Block<T>* kblk);

  template<typename T>
    Matrix<T> operator*( const Block<T>& kblk, uni10_double64 a); 

  template<typename T>
    Matrix<uni10_complex128> operator*( const Block<T>& kblk, uni10_complex128 a); 

  // Element-wise addition.
  template<typename T>
    Matrix<T> operator+(const Block<uni10_double64>& kblk1, const Block<T>& kblk2);

  template<typename T>
    Matrix<uni10_complex128> operator+(const Block<uni10_complex128>& kblk1, const Block<T>& kblk2);

  // Element-wise subtract.
  template<typename T>
    Matrix<T> operator-(const Block<uni10_double64>& kblk1, const Block<T>& kblk2); 

  template<typename T>
    Matrix<uni10_complex128> operator-(const Block<uni10_complex128>& kblk1, const Block<T>& kblk2); 

  // Element-wise multipliation.
  template<typename T>
    Matrix<T> operator*( const Block<uni10_double64>& kblk1, const Block<T>& kblk2); 

  template<typename T>
    Matrix<uni10_complex128> operator*( const Block<uni10_complex128>& kblk1, const Block<T>& kblk2); 

  Matrix<uni10_complex128>& operator+=(Matrix<uni10_complex128>& mat, const Matrix<uni10_double64>& kmat);

  Matrix<uni10_complex128>& operator-=(Matrix<uni10_complex128>& mat, const Matrix<uni10_double64>& kmat);

  Matrix<uni10_complex128>& operator*=(Matrix<uni10_complex128>& mat, uni10_complex128 a);

  Matrix<uni10_complex128>& operator*=(Matrix<uni10_complex128>& mat, const Matrix<uni10_double64>& kmat);

  template <typename UniType>
    class Matrix:public Block<UniType> {

      private:

        void Init_(const UniType* ksrcptr = NULL);

        void Init_(const UELEM(UniElem, _package, _type)<UniType>& ksrcelem);     // pointer to a real matrix

        template<typename U>
          void Init_(const UELEM(UniElem, _package, _type)<U>& ksrcelem );

      public:
        /// @brief Default constructor.
        explicit Matrix();

        /// @brief Create a Matrix
        ///
        /// Allocate memory of size <tt> row*col </tt> (or <tt>min(row_, col_)</tt> if \c diag_ is \c true) for
        /// matrix elements and set the elements to zero.
        /// @param row Number of Rows
        /// @param col Number of Columns
        /// @param diag Set \c true for diagonal matrix, defaults to \c false
        explicit Matrix(uni10_uint64 row, uni10_uint64 col, bool diag=false);

        explicit Matrix(uni10_uint64 row, uni10_uint64 col, UniType* _src, bool diag=false);

        /// @brief Construct a Matrix, and assign a stored Matrix to it.
        ///
        /// @param kfilename Path where the Matrix stored.
        explicit Matrix(const std::string& kfilename);

        Matrix<UniType>(Block<UniType> const& kblk);

        template<typename U>
          Matrix<UniType>(Block<U> const& kblk);
        
        Matrix(Matrix const& kmat);

        /// @brief Copy constructor.
        ///
        /// @param kamt Matrix to be copied.
        template<typename U>
          Matrix<UniType>(Matrix<U> const& kmat);

        ~Matrix();

        /// @brief ask yun-hsuan.
        void Assign(uni10_uint64 row, uni10_uint64 col, uni10_bool diag = false);

        /// @brief Load a stored Matrix.
        /// @param kfilname Path where the Matrix store.
        ///
        void Load(const std::string& kfilename);

        /// @brief Set elements of Matrix.
        ///
        /// @param ksrcptr Pointer to the input array.
        void SetElem(const UniType* ksrcptr, bool src_ongpu = false);

        /// @overload
        void SetElem(const std::vector<UniType>& ksrcvec, bool src_ongpu = false);

        /// @brief ask yun-hsuan.
        void SetDiag(const uni10_bool kdiag);

        /// @brief Set all elements to \c 0 .
        void Zeros();
        
        /// @brief Set all the diagonal elements to \c 1 and all the off-diagonal elements to \c 0 .
        void Identity();

        /// @brief ask yun-hsuan.
        void Randomize(char UorN='U', uni10_double64 dn_mu=-1, uni10_double64 up_var=1, uni10_int64 seed=uni10_clock);

        /// @brief ask yun-hsuan.
        void OrthoRand(char UorN='U', uni10_double64 dn_mu=-1, uni10_double64 up_var=1, uni10_int64 seed=uni10_clock);

        /// @brief Copy assignment operator.
        ///
        /// Assigns the content of \c mat to Matrix, replacing the original content by reallocating new memory
        /// fit for \c mat.
        /// @param kmat Second Matrix
        Matrix& operator=(const Matrix& kmat);

        template<typename U>
          Matrix& operator=(const Matrix<U>& kmat);

        Matrix& operator=(const Block<UniType>& kblk);

        template<typename U>
          Matrix& operator=(const Block<U>& kblk);

        UniType& operator[](uni10_uint64 idx){
          return this->elem_[idx];
        };

        UniType operator[](uni10_uint64 idx) const{
          return this->elem_[idx];
        };

        Matrix<UniType>& operator+=(const Matrix<UniType>& kmat);

        Matrix<UniType>& operator-=(const Matrix<UniType>& kmat);

        Matrix<UniType>& operator*=(const Matrix<UniType>& kmat);

        Matrix<UniType>& operator*=(uni10_double64 a);

        template<typename _T>
          friend Matrix<_T> operator* (uni10_double64 a, const Block<_T>& kblk);

        template<typename _T>
          friend Matrix<uni10_complex128> operator* (uni10_complex128 a, const Block<_T>& kblk);

        template<typename _T>
          friend Matrix<_T> operator* (const Block<_T>& kblk, uni10_double64 a);

        template<typename _T>
          friend Matrix<uni10_complex128> operator* (const Block<_T>& kblk, uni10_complex128 a);

        friend Matrix<uni10_complex128>& operator+=(Matrix<uni10_complex128>& mat, const Matrix<uni10_double64>& kmat);

        friend Matrix<uni10_complex128>& operator-=(Matrix<uni10_complex128>& mat, const Matrix<uni10_double64>& kmat);

        friend Matrix<uni10_complex128>& operator*=(Matrix<uni10_complex128>& mat, uni10_complex128 a);

        friend Matrix<uni10_complex128>& operator*=(Matrix<uni10_complex128>& mat, const Matrix<uni10_double64>& kmat);

        template<typename Res, typename Obj, typename... Args> 
          friend void DotArgs(Res& outmat, const Obj& kmat, const Args&... args);

        template<typename _UniType> 
          friend void Dots(Matrix<_UniType>& outmat, const std::vector< Matrix<_UniType>* >& kmatptrs, UNI10_INPLACE on);

        template<typename _UniType> 
          friend void Resize( Matrix<_UniType>& outmat , const Matrix<_UniType>& kmat, uni10_uint64 row, uni10_uint64 col, UNI10_INPLACE on);

        template<typename _UniType>
          friend void Inverse( Matrix<_UniType>& invmat, UNI10_INPLACE on );

        template<typename _UniType>
          friend void Transpose( Matrix<_UniType>& tmat, UNI10_INPLACE on );

        template<typename _UniType>
          friend void Dagger( Matrix<_UniType>& dmat, UNI10_INPLACE on );

        template<typename _UniType>
          friend void Conj( Matrix<_UniType>& cmat, UNI10_INPLACE on );

    };

  template<typename T>
    Matrix<T> operator* (uni10_double64 a, const Block<T>& kblk){

      Matrix<T> outmat(kblk);
      linalg_unielem_internal::VectorScal(&a, &outmat.elem_, &outmat.elem_.elem_num_);
      return outmat;

    }

  template<typename T>
    Matrix<uni10_complex128> operator* (uni10_complex128 a, const Block<T>& kblk){

      Matrix<uni10_complex128> outmat(kblk);
      linalg_unielem_internal::VectorScal(&a, &outmat.elem_, &outmat.elem_.elem_num_);
      return outmat;

    }

  template<typename T>
    Matrix<T> operator* (const Block<T>& kblk, uni10_double64 a){
      return a * kblk;
    }

  template<typename T>
    Matrix<uni10_complex128> operator* (const Block<T>& kblk, uni10_complex128 a){
      return a * kblk;
    }

  template<typename T>
    Matrix<T> operator+ (const Block<uni10_double64>& kblk1, const Block<T>& kblk2){

      uni10_error_msg(kblk1.row_ != kblk2.row_ || kblk1.col_ != kblk2.col_, "%s", "Lack err msg!!!");

      Matrix<T> outmat(kblk1.row_, kblk1.col_, kblk1.diag_ && kblk2.diag_);
      linalg_unielem_internal::MatrixAdd(&kblk1.elem_, &kblk1.diag_, &kblk2.elem_, &kblk2.diag_, &kblk1.row_, &kblk1.col_, &outmat.elem_);

      return outmat;

    }
 
  template<typename T>
    Matrix<uni10_complex128> operator+ (const Block<uni10_complex128>& kblk1, const Block<T>& kblk2){

      uni10_error_msg(kblk1.row_ != kblk2.row_ || kblk1.col_ != kblk2.col_, "%s", "Lack err msg!!!");

      Matrix<uni10_complex128> outmat(kblk1.row_, kblk1.col_, kblk1.diag_ && kblk2.diag_);
      linalg_unielem_internal::MatrixAdd(&kblk1.elem_, &kblk1.diag_, &kblk2.elem_, &kblk2.diag_, &kblk1.row_, &kblk1.col_, &outmat.elem_);

      return outmat;

    }

  template<typename T>
    Matrix<T> operator- (const Block<uni10_double64>& kblk1, const Block<T>& kblk2){

      uni10_error_msg(kblk1.row_ != kblk2.row_ || kblk1.col_ != kblk2.col_, "%s", "Lack err msg!!!");

      Matrix<T> outmat(kblk1.row_, kblk1.col_, kblk1.diag_ && kblk2.diag_);
      linalg_unielem_internal::MatrixSub(&kblk1.elem_, &kblk1.diag_, &kblk2.elem_, &kblk2.diag_, &kblk1.row_, &kblk1.col_, &outmat.elem_);

      return outmat;
       
    }

  template<typename T>
    Matrix<uni10_complex128> operator- (const Block<uni10_complex128>& kblk1, const Block<T>& kblk2){

      uni10_error_msg(kblk1.row_ != kblk2.row_ || kblk1.col_ != kblk2.col_, "%s", "Lack err msg!!!");

      Matrix<uni10_complex128> outmat(kblk1.row_, kblk1.col_, kblk1.diag_ && kblk2.diag_);
      linalg_unielem_internal::MatrixSub(&kblk1.elem_, &kblk1.diag_, &kblk2.elem_, &kblk2.diag_, &kblk1.row_, &kblk1.col_, &outmat.elem_);

      return outmat;
       
    }

  template<typename T>
    Matrix<T> operator* (const Block<uni10_double64>& kblk1, const Block<T>& kblk2){

      uni10_error_msg(kblk1.row_ != kblk2.row_ || kblk1.col_ != kblk2.col_, "%s", "Lack err msg!!!");

      Matrix<T> outmat(kblk1.row_, kblk1.col_, kblk1.diag_ || kblk2.diag_);
      linalg_unielem_internal::MatrixMul(&kblk1.elem_, &kblk1.diag_, &kblk2.elem_, &kblk2.diag_, &kblk1.row_, &kblk1.col_, &outmat.elem_);

      return outmat;
       
    }

  template<typename T>
    Matrix<uni10_complex128> operator* (const Block<uni10_complex128>& kblk1, const Block<T>& kblk2){

      uni10_error_msg(kblk1.row_ != kblk2.row_ || kblk1.col_ != kblk2.col_, "%s", "Lack err msg!!!");

      Matrix<uni10_complex128> outmat(kblk1.row_, kblk1.col_, kblk1.diag_ || kblk2.diag_);
      linalg_unielem_internal::MatrixMul(&kblk1.elem_, &kblk1.diag_, &kblk2.elem_, &kblk2.diag_, &kblk1.row_, &kblk1.col_, &outmat.elem_);

      return outmat;
       
    }


};  /* namespace uni10 */

#endif /* MATRIX_H */
