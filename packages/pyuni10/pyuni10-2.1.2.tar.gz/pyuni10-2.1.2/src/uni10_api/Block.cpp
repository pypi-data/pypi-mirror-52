/****************************************************************************
 *  @file Block.cpp
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
 *  @brief Implementation file of Block class
 *  @author Yun-Da Hsieh
 *  @date 2014-05-06
 *  @since 0.1.0
 *
 *****************************************************************************/
#include "uni10_api/Block.h"


namespace uni10{

  template<typename uni10_type>
    Block<uni10_type>::Block(): row_(0), col_(0), diag_(false){};

  template<typename uni10_type>
    Block<uni10_type>::Block(uni10_uint64 row, uni10_uint64 col, bool diag): row_(row), col_(col), diag_(diag){

    }

  template<typename uni10_type>
    Block<uni10_type>::Block(const Block& _b): row_(_b.row_), col_(_b.col_), diag_(_b.diag_){
      elem_.uni10_typeid_ = _b.elem_.uni10_typeid_;
      elem_.ongpu_        = _b.elem_.ongpu_;
      elem_.elem_num_     = _b.elem_.elem_num_;
      elem_.elem_ptr_     = _b.elem_.elem_ptr_;
    }

  template<typename uni10_type>
    Block<uni10_type>::~Block(){}

  template<typename uni10_type>
    uni10_uint64 Block<uni10_type>::row()const{return row_;}

  template<typename uni10_type>
    uni10_uint64 Block<uni10_type>::col()const{return col_;}

  template<typename uni10_type>
    bool Block<uni10_type>::diag()const{return diag_;}

  template<typename uni10_type>
    uni10_uint64 Block<uni10_type>::ElemNum()const{ return elem_.elem_num_; }

  template<typename uni10_type>
    int Block<uni10_type>::TypeId()const{ return elem_.uni10_typeid_;}

  template<typename uni10_type>
    uni10_type* Block<uni10_type>::GetElem()const{ return elem_.elem_ptr_; }

  template<typename uni10_type>
    bool Block<uni10_type>::IsEmpty()const{

      return this->elem_.Empty();

    }

  template<typename uni10_type>
    void Block<uni10_type>::Save(const std::string& fname)const{

      FILE* fp = fopen(fname.c_str(), "w");
      fwrite(&row_, sizeof(row_), 1, fp);
      fwrite(&col_, sizeof(col_), 1, fp);
      fwrite(&diag_, sizeof(diag_), 1, fp);

      elem_.Save(fp);

      fclose(fp);

    }

  template<typename uni10_type>
    uni10_type Block<uni10_type>::At(uni10_uint64 rowidx, uni10_uint64 colidx)const{
      if(diag_){
        if(rowidx == colidx)
          return elem_.elem_ptr_[colidx];
        else
          return 0.;
      }
      else
        return elem_.elem_ptr_[rowidx * col_ + colidx];
    }


#if defined(GPU)
  template<typename uni10_type>
    bool Block<uni10_type>::IsOngpu()const{return elem_.ongpu;}
#endif

  template class Block<uni10_double64>;
  template class Block<uni10_complex128>;

};
