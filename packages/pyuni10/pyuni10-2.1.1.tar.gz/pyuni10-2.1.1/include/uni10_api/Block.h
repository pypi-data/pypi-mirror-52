/****************************************************************************
*  @file Block.h
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
*  @brief Header file for Block class
*  @author Yun-Da Hsieh
*  @author Yun-Hsuan Chou
*  @date 2014-05-06
*  @since 0.1.0
*
*****************************************************************************/
#ifndef __UNI10_BLOCK_H__
#define __UNI10_BLOCK_H__

#include <assert.h>

#include <iostream>
#include <iomanip>
#include <vector>

#include "uni10_type.h"
#include "uni10_elem.h"
#include "uni10_elem_linalg.h"

namespace uni10{

  enum UNI10_INPLACE{
    INPLACE = 1        //< Modified elements in the Matrix directly.
  };

  template<typename UniType>
    class UniTensor;

  template<typename UniType>
    class Matrix;

  /*! @brief Base class for Matrix. 
   * 
   *  A Block holds a reference to a Matrix. The Block constructor does not allocate memory. Memory allocation
   *  should be done through Matrix.
   *  @see \ref Matrix, UniTensor
   */
  template<typename UniType>
    class Block;

  template<typename UniType>
    std::ostream& operator<< (std::ostream& os, const Block<UniType>& kblk);

  template<typename T, typename U>
    uni10_bool operator==(const Block<T>& kblk1, const Block<U>& kblk2);

  template<typename T, typename U>
    uni10_bool operator!=(const Block<T>& kblk1, const Block<U>& kblk2);

  template<typename UniType>
    class Block{  

      protected:

        UELEM(UniElem, _package, _type)<UniType> elem_;

        uni10_uint64 row_;

        uni10_uint64 col_;

        uni10_bool diag_;

      public:

        uni10_uint64& row_enforce(){return row_;};

        uni10_uint64& col_enforce(){return col_;};

        uni10_bool& diag_enforce(){return diag_;};
        
        UELEM(UniElem, _package, _type)<UniType>& elem_enforce(){return elem_;};

        const UELEM(UniElem, _package, _type)<UniType>& const_elem_enforce()const{return elem_;};

        /// @brief Default constructor of Block.
        explicit Block();

        /// @brief Constructor of Block with block size specified.
        ///
        /// @param row Number of rows.
        /// @param col Number of columns.
        /// @param diag Set \c true for diagonal matrix, defaults to \c false.
        explicit Block(uni10_uint64 row, uni10_uint64 col, bool diag = false);

        /// @brief Copy constructor of Block.
        explicit Block(const Block& kblk);

        virtual ~Block();

        /// @brief Get number of row.
        /// @return Number of row.
        uni10_uint64 row()const;

        /// @brief Get number of column.
        /// @return Number of column.
        uni10_uint64 col()const;

        /// @brief Check if the Block is diagonal.
        /// @return \c ture if ths Block is diagonal, \c false if it is not.
        bool diag()const;

        /// @brief Save the content of the Block.
        /// 
        /// @param kFileName Path of the saved file.
        void Save(const std::string& kFileName)const;

        bool IsEmpty()const;

        /// @brief Get element number of the Block.
        /// @return Element number of the Block.
        uni10_uint64 ElemNum()const;

        uni10_int TypeId()const;      // --> uni10_elem().typeid()

        bool IsOngpu()const;            // --> uni10_elem().isOngpu()

        /// @brief Get the pointer to the first element of the Block.
        /// @return The pointer to the first element of the Block.
        UniType* GetElem()const;     // --> uni10_elem().getElem()

        /// @brief Get an element of Block at given position.
        /// 
        /// @param i Row index of the element.
        /// @param j Column index of the element.
        /// @return The element in i-th row and j-th column.
        UniType At(uni10_uint64 i, uni10_uint64 j)const;

        /// @brief Copy assignment operator.
        ///
        /// @param kblk The Block being copied.
        Block& operator=(const Block& kblk){

          this->row_   = kblk.row_;
          this->col_   = kblk.col_;
          this->diag_  = kblk.diag_;

          this->elem_.uni10_typeid_ = kblk.elem_.uni10_typeid_;
          this->elem_.ongpu_        = kblk.elem_.ongpu_;
          this->elem_.elem_num_     = kblk.elem_.elem_num_;
          this->elem_.elem_ptr_     = kblk.elem_.elem_ptr_;
          return *this;
        };

        UniType operator[](uni10_uint64 idx) const{

          uni10_error_msg(idx > this->elem_.elem_num_, "%s", "The input index exceed the element number.");

          return this->elem_[idx];

        };

        /*********************  OPERATOR **************************/

        /// @brief Print out Block
        ///
        /// @detail Prints out the elements of Block
        ///
        /// For a 2 x 3 matrix \c M,
        /// \code
        /// 2 x 3 = 6
        ///
        /// -0.254 -0.858 -0.447
        ///
        /// 0.392  0.331 -0.859
        /// \endcode
        /// The number of elements is 2 x 3 = 6 and followed by a 2 by 3 matrix of elements.
        friend std::ostream& operator<< <>(std::ostream& os, const Block& kblk); // --> uni10_elem().print_elem()

        /// @brief Element-wise addition.
        ///
        /// @detail Perform element-wise addition of two Blocks. The Blocks should have same dimension.
        template<typename _T>
          friend Matrix<_T> operator+(const Block<uni10_double64>& kblk1, const Block<_T>& kblk2);

        template<typename _T>
          friend Matrix<uni10_complex128> operator+(const Block<uni10_complex128>& kblk1, const Block<_T>& kblk2);

        /// @brief Element-wise subtraction.
        ///
        /// @detail Perform element-wise substraction of two Blocks. The Blocks should have same dimension.
        template<typename _T>
          friend Matrix<_T> operator-(const Block<uni10_double64>& kblk1, const Block<_T>& kblk2);

        template<typename _T>
          friend Matrix<uni10_complex128> operator-(const Block<uni10_complex128>& kblk1, const Block<_T>& kblk2);

        /// @brief Element-wise multiplication.
        ///
        /// @detail Perform element-wise multiplication of two Blocks. The Blocks should have same dimension.
        template<typename _T>
          friend Matrix<_T> operator*(const Block<uni10_double64>& kblk1, const Block<_T>& kblk2);

        template<typename _T>
          friend Matrix<uni10_complex128> operator*(const Block<uni10_complex128>& kblk1, const Block<_T>& kblk2);

        template<typename _T, typename _U>
          friend uni10_bool operator== (const Block<_T>& kblk1, const Block<_U>& kblk2);

        template<typename _T, typename _U>
          friend uni10_bool operator!= (const Block<_T>& kblk1, const Block<_U>& kblk2);

        template<typename _UniType> 
          friend Matrix<_UniType> GetDiag( const Block<_UniType>& kblk );

        template<typename _To, typename _T, typename _U> 
          friend void Dot( Matrix<_To>& mat, const Block<_T>& kblk1, const Block<_U>& kblk2, UNI10_INPLACE on );

        template<typename _T> 
          friend void Dot( Matrix<uni10_complex128>& mat, const Block<_T>& kblk, UNI10_INPLACE on );

        friend void Dot( Matrix<uni10_double64>& mat, const Block<uni10_double64>& kblk, UNI10_INPLACE on );

        template<typename _UniType>
          friend void Conj( Matrix<_UniType>& matout, const Block<_UniType>& kblk, UNI10_INPLACE on );

        template<typename _UniType>
          friend void Dagger( Matrix<_UniType>& dmat, const Block<_UniType>& kmat, UNI10_INPLACE on );

        template<typename _UniType>
          friend void Transpose( Matrix<_UniType>& transmat, const Block<_UniType>& kblk, UNI10_INPLACE on );

        template<typename _UniType>
          friend void Svd( const Block<_UniType>& kblk, Matrix<_UniType>& u, Matrix<_UniType>& s, Matrix<_UniType>& vt, UNI10_INPLACE on );

        template<typename _UniType>
          friend void Sdd( const Block<_UniType>& kblk, Matrix<_UniType>& u, Matrix<_UniType>& s, Matrix<_UniType>& vt, UNI10_INPLACE on );

        template<typename _UniType>
          friend void Ldq( const Block<_UniType>& kblk, Matrix<_UniType>& l, Matrix<_UniType>& d, Matrix<_UniType>& q, UNI10_INPLACE on  );

        template<typename _UniType>
          friend void Lq( const Block<_UniType>& kblk, Matrix<_UniType>& l, Matrix<_UniType>& q, UNI10_INPLACE on  );

        template<typename _UniType>
          friend void QdrColPivot( const Block<_UniType>& kblk, Matrix<_UniType>& q, Matrix<_UniType>& d, Matrix<_UniType>& r, UNI10_INPLACE on );

        template<typename _UniType>
          friend void Qdr( const Block<_UniType>& kblk, Matrix<_UniType>& q, Matrix<_UniType>& d, Matrix<_UniType>& r, UNI10_INPLACE on );

        template<typename _UniType>
          friend void Qr( const Block<_UniType>& kblk, Matrix<_UniType>& q, Matrix<_UniType>& r, UNI10_INPLACE on );

        template<typename _UniType>
          friend void Ql( const Block<_UniType>& kblk, Matrix<_UniType>& q, Matrix<_UniType>& l, UNI10_INPLACE on  );

        template<typename _UniType>
          friend void Rq( const Block<_UniType>& kblk, Matrix<_UniType>& r, Matrix<_UniType>& q, UNI10_INPLACE on  );

        template<typename _UniType>
          friend void Eig( const Block<_UniType>& kblk, Matrix<uni10_complex128>& w, Matrix<uni10_complex128>& v, UNI10_INPLACE on );

        template<typename _UniType>
          friend void EigH( const Block<_UniType>& kblk, Matrix<uni10_double64>& w, Matrix<_UniType>& v, UNI10_INPLACE on );

        template<typename _UniType>
          friend Matrix<_UniType> ExpH( uni10_double64 a, const Block<_UniType>& kblk );

        template<typename _UniType>
          friend Matrix<uni10_complex128> ExpH( uni10_complex128 a, const Block<_UniType>& kblk );

        template<typename _UniType>
          friend _UniType Sum( const Block<_UniType>& kblk );

        template<typename _UniType>
          friend uni10_double64 Norm( const Block<_UniType>& kblk );

        template<typename _UniType>
          friend Matrix<_UniType> Inverse( const Block<_UniType>& kblk );

        template<typename _UniType>
          friend _UniType Trace( const Block<_UniType>& kblk );

        template<typename _UniType>
          friend _UniType Det( const Block<_UniType>& kblk );

        template<typename _UniType>
          friend class Matrix;

        template<typename _UniType>
          friend class UniTensor;

    };


  template<typename UniType>
    std::ostream& operator<< (std::ostream& os, const Block<UniType>& kblk){

      kblk.elem_.PrintElem(kblk.row_, kblk.col_, kblk.diag_);

      os << "";

      return os;
    }

  template<typename T, typename U>
    uni10_bool operator== (const Block<T>& kblk1, const Block<U>& kblk2){

      if( (kblk1.row_ != kblk2.row_) || (kblk1.col_ != kblk2.col_) || (kblk1.diag_ != kblk2.diag_) )
        return false;

      for(uni10_int i = 0; i < kblk1.elem_.elem_num_; i++)
        if(UNI10_REAL(kblk1.elem_.elem_ptr_[i] )- UNI10_REAL(kblk2.elem_.elem_ptr_[i] )> 10E-12)
          return false;

      if(kblk1.elem_.uni10_typeid_ == 2)
        for(uni10_int i = 0; i < kblk1.elem_.elem_num_; i++)
          if(UNI10_IMAG(kblk1.elem_.elem_ptr_[i]) - UNI10_IMAG(kblk2.elem_.elem_ptr_[i]) > 10E-12)
            return false;

      return true; 
    }

  template<typename T, typename U>
    uni10_bool operator!= (const Block<T>& kblk1, const Block<U>& kblk2){

      return !(kblk1 == kblk2); 

    }

};

#endif
