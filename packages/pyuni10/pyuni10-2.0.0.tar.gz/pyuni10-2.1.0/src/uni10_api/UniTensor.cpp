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

#include "uni10_error.h"
#include "uni10_api/linalg.h"
#include "uni10_api/tensor_tools/tensor_tools.h"
#include "uni10_api/uni10_hirnk_linalg_inplace/uni10_hirnk_linalg_inplace_permute.h"
#include "uni10_api/uni10_hirnk_linalg_inplace/uni10_hirnk_linalg_inplace_pseudoPermute.h"
#ifdef UNI_HDF5
  #include "uni10_hdf5/uni10_hdf5.hpp"
#endif

namespace uni10{

  template <typename uni10_type>
    UniTensor<uni10_type>::UniTensor(): style(no_sym){

      this->init_para();
      this->meta_link();
      *status = 0;
      this->init();
      (*this->U_elem)[0] = 0;

    };

  template <typename uni10_type>
    UniTensor<uni10_type>::UniTensor(uni10_type val, const contain_type s){

      this->style = s;
      this->init_para();
      this->meta_link();
      *status = 0;
      this->init();

      (*this->U_elem)[0] = val;
    }

  template <typename uni10_type>
    UniTensor<uni10_type>::UniTensor(const std::vector<Bond>& _bonds, const std::string& _name){

      this->style = check_bonds(_bonds);
      this->init_para();
      this->meta_link();
      *name  = _name;
      *bonds = _bonds;
      *status= 0;
      this->init();

    }

  template <typename uni10_type>
    UniTensor<uni10_type>::UniTensor(const std::vector<Bond>& _bonds, int* _labels, const std::string& _name){

      this->style = check_bonds(_bonds);
      this->init_para();
      this->meta_link();
      *name  = _name;
      *bonds = _bonds;
      *status= 0;
      this->init();
      this->SetLabel(_labels);

    }

  template <typename uni10_type>
    UniTensor<uni10_type>::UniTensor(const std::vector<Bond>& _bonds, std::vector<int>& _labels, const std::string& _name){

      this->style = check_bonds(_bonds);
      this->init_para();
      this->meta_link();
      *name  = _name;
      *bonds = _bonds;
      *status= 0;
      this->init();
      this->SetLabel(_labels);

    }

  template <typename uni10_type>
    UniTensor<uni10_type>::UniTensor(const UniTensor& UniT): style(UniT.style){

      if(UniT.paras !=NULL){
        this->init_para();
        this->meta_link();
        this->copy_para(UniT.paras);
        this->initBlocks();
      }else{
        this->init_paras_null();
      }

      ELEMNUM += *this->U_elemNum;
      COUNTER++;
      if(ELEMNUM > MAXELEMNUM)
        MAXELEMNUM = ELEMNUM;
      if(*this->U_elemNum > MAXELEMTEN)
        MAXELEMTEN = *this->U_elemNum;

    }

  template <typename uni10_type>
    UniTensor<uni10_type>::UniTensor(const std::string& fname){

      this->style = no_sym;
      this->init_para();
      this->Load(fname);

    }

  template <typename uni10_type>
    UniTensor<uni10_type>::UniTensor(const Block<uni10_type>& blk){

      Bond bdi(BD_IN, blk.row_);
      Bond bdo(BD_OUT, blk.col_);
      this->style = no_sym;
      this->init_para();
      this->meta_link();
      bonds->push_back(bdi);
      bonds->push_back(bdo);
      this->init();
      this->PutBlock(blk);

    }

  template <typename uni10_type>
    UniTensor<uni10_type>::~UniTensor(){
      ELEMNUM -= *this->U_elemNum;
      COUNTER--;
      this->free_para();
    }


  template<typename uni10_type>
    UniTensor<uni10_type>& UniTensor<uni10_type>::operator=(UniTensor<uni10_type> const& UniT){

      if(this->paras != NULL)
        this->free_para();

      if(UniT.paras != NULL){
        this->style = UniT.style;
        this->init_para();
        this->meta_link();
        this->copy_para(UniT.paras);
        this->initBlocks();
      }else
        this->init_paras_null();

      return *this;
    }

  template<typename uni10_type>
    UniTensor<uni10_type>& UniTensor<uni10_type>::operator+=( const UniTensor<uni10_type>& Tb ){
      linalg_unielem_internal::VectorAdd(this->U_elem, Tb.U_elem, &Tb.U_elem->elem_num_ );
      return *this;
    };

  template<typename uni10_type>
    UniTensor<uni10_type>& UniTensor<uni10_type>::operator-=( const UniTensor<uni10_type>& Tb ){
      linalg_unielem_internal::VectorSub(this->U_elem, Tb.U_elem, &Tb.U_elem->elem_num_ );
      return *this;
    };

  template<typename uni10_type>
    UniTensor<uni10_type>& UniTensor<uni10_type>::operator*= (uni10_double64 a){
      linalg_unielem_internal::VectorScal(&a, this->U_elem, &this->U_elem->elem_num_);
      return *this;
    };

#ifdef UNI_HDF5
  template <typename uni10_type>
    void UniTensor<uni10_type>::H5Save(const std::string& fname, const std::string& gname, const bool& Override) const{
      if ( Override ){
        HDF5IO* file = new HDF5IO(fname, Override);
        file->SaveTensor(gname, *this);
        delete file;
      }else{
        HDF5IO* file = new HDF5IO(fname);
        file->SaveTensor(gname, *this);
        delete file;
      }
    };

  template <typename uni10_type>
    void UniTensor<uni10_type>::H5Load(const std::string& fname, const std::string& gname){
      HDF5IO* file = new HDF5IO(fname);
      file->LoadTensor(gname, *this);
      delete file;
    };
#endif

  template <typename uni10_type>
    void UniTensor<uni10_type>::Save(const std::string& fname) const{

      FILE* fp = fopen(fname.c_str(), "w");
      uni10_error_msg(!(fp != NULL), "Error in writing to file '%s'", fname.c_str());

      fwrite(&style, 1, sizeof(style), fp);
      uni10_uint64 namelen = name->size();
      fwrite(&namelen, 1, sizeof(namelen), fp);
      fwrite(&(*name)[0], namelen, sizeof((*name)[0]), fp);
      fwrite(&(*status), 1, sizeof(*status), fp);  //OUT: status(4 bytes)
      uni10_uint64 bondNum = bonds->size();
      fwrite(&bondNum, 1, sizeof(bondNum), fp);  //OUT: bondNum(4 bytes)
      uni10_uint64 qnum_sz = sizeof(Qnum);
      fwrite(&qnum_sz, 1, sizeof(qnum_sz), fp);  //OUT: sizeof(Qnum)
      for(uni10_uint64 b = 0; b < bondNum; b++){
        uni10_uint64 num_q = (*bonds)[b].Qnums.size();
        fwrite(&((*bonds)[b].m_type), 1, sizeof(bondType), fp); //OUT: Number of Qnums in the bond(4 bytes)
        fwrite(&num_q, 1, sizeof(num_q), fp);   //OUT: Number of Qnums in the bond(4 bytes)
        fwrite(&((*bonds)[b].Qnums[0]), num_q, qnum_sz, fp);
        fwrite(&((*bonds)[b].Qdegs[0]), num_q, sizeof((*bonds)[b].Qdegs[0]), fp);
      }
      uni10_uint64 num_l = labels->size();
      fwrite(&num_l, 1, sizeof(num_l), fp); //OUT: Number of Labels in the Tensor(4 bytes)
      fwrite(&((*labels)[0]), num_l, sizeof((*labels)[0]), fp);

      if(*status & HAVEELEM)
        U_elem->Save(fp);

      fclose(fp);

    }

  template <typename uni10_type>
    void UniTensor<uni10_type>::Load(const std::string& fname){

      FILE* fp = fopen(fname.c_str(), "r");
      uni10_error_msg(!(fp != NULL), "Error in opening file '%s'.", fname.c_str());
      uni10_error_msg(!fread(&style, 1, sizeof(style), fp), "%s", "Loading the style of UniTensor is failure. (UniTensor<T>)");
      //this->init_para();
      //this->meta_link();
      uni10_uint64 namelen;
      uni10_error_msg(!fread(&namelen, 1, sizeof(namelen), fp), "%s", "Loading the namelen of UniTensor is failure. (UniTensor<T>)");
      std::string bufname(" ", namelen);
      //name->assign(" ", namelen);
      //if(namelen != 0)
      //  uni10_error_msg(!fread(&(*name)[0], namelen, sizeof((*name)[0]), fp), "%s", "Loading the name of UniTensor is failure. (UniTensor<T>)");
      if(namelen != 0)
        uni10_error_msg(!fread(&bufname[0], namelen, sizeof(bufname[0]), fp), "%s", "Loading the name of UniTensor is failure. (UniTensor<T>)");
      uni10_int st;
      uni10_error_msg(!fread(&st, 1, sizeof(st), fp), "%s", "Loading the status of UniTensor is failure. (UniTensor<T>)");  //OUT: status(4 bytes)
      uni10_uint64 bondNum;
      uni10_error_msg(!fread(&bondNum, 1, sizeof(bondNum), fp), "%s", "Loading the bondNum of UniTensor is failure. (UniTensor<T>)");  //OUT: bondNum(4 bytes)
      uni10_uint64 qnum_sz;
      uni10_error_msg(!fread(&qnum_sz, 1, sizeof(qnum_sz), fp), "%s", "Loading the qnum_sz of UniTensor is failure. (UniTensor<T>)");  //OUT: sizeof(Qnum)
      uni10_error_msg(!(qnum_sz == sizeof(Qnum)), "Error in reading file '%s' in.", fname.c_str());

      std::vector<Bond> bufbonds;
      for(uni10_uint64 b = 0; b < bondNum; b++){
        uni10_uint64 num_q;
        bondType tp;
        uni10_error_msg(!fread(&tp, 1, sizeof(bondType), fp), "%s", "Loading the bondType of UniTensor is failure. (UniTensor<T>)"); //OUT: Number of Qnums in the bond(4 bytes)
        uni10_error_msg(!fread(&num_q, 1, sizeof(num_q), fp), "%s", "Loading the num_q of UniTensor is failure. (UniTensor<T>)");   //OUT: Number of Qnums in the bond(4 bytes)
        Qnum q0;
        std::vector<Qnum> qnums(num_q, q0);
        uni10_error_msg(!fread(&qnums[0], num_q, qnum_sz, fp), "%s", "Loading the qnums of UniTensor is failure. (UniTensor<T>)");
        std::vector<uni10_int> qdegs(num_q, 0);
        uni10_error_msg(!fread(&(qdegs[0]), num_q, sizeof(qdegs[0]), fp), "%s", "Loading the qdegs of UniTensor is failure. (UniTensor<T>)");
        std::vector<Qnum> tot_qnums;
        for(uni10_uint64 q = 0; q < num_q; q++)
          for(uni10_int d = 0; d < qdegs[q]; d++)
            tot_qnums.push_back(qnums[q]);

        Bond bd(tp, tot_qnums);
        bufbonds.push_back(bd);
      }

      this->Assign(bufbonds);
      this->SetName(bufname);

      uni10_uint64 num_l;
      uni10_error_msg(!fread(&num_l, 1, sizeof(num_l), fp), "%s", "Loading the num_l of UniTensor is failure. (UniTensor<T>)");  //OUT: Number of Labels in the Tensor(4 bytes)
      uni10_error_msg(!(num_l == bonds->size()), "Error in reading file '%s' in.", fname.c_str());
      //labels->assign(num_l, 0);
      std::vector<uni10_int> buflabels(num_l);
      if(num_l != 0)
        uni10_error_msg(!fread(&(buflabels[0]), num_l, sizeof(buflabels[0]), fp), "%s", "Loading the labels of UniTensor is failure. (UniTensor<T>)");
      this->SetLabel(buflabels);

      if(st & HAVEELEM){
        this->U_elem->Load(fp);
        (*this->status)|= HAVEELEM;
      }

      //ELEMNUM += *this->U_elemNum;
      //COUNTER++;
      //if(ELEMNUM > MAXELEMNUM)
      //  MAXELEMNUM = ELEMNUM;
      //if(*this->U_elemNum > MAXELEMTEN)
      //  MAXELEMTEN = *this->U_elemNum;

      fclose(fp);

    }

  // This is a temporary fix ONLY!!
  template <typename uni10_type>
    void UniTensor<uni10_type>::LoadOldVer(const std::string& fname, const contain_type& type, const std::string& version){

      FILE* fp = fopen(fname.c_str(), "r");
      uni10_error_msg(!(fp != NULL), "Error in opening file '%s'.", fname.c_str());
      int rf, cf;
      if ( version == "100"){
        fread(&rf, 1, sizeof(int), fp);//r_flag
        fread(&cf, 1, sizeof(int), fp);//c_flag
      }
      style = type;
      int namelen = 0;
      if ( version == "100") uni10_error_msg(!fread(&namelen, 1, sizeof(int), fp), "%s", "LoadOldVer: Loading the namelen of UniTensor is failure. (UniTensor<T>)");
      std::string bufname(" ", namelen);
      if(namelen != 0)
        uni10_error_msg(!fread(&bufname[0], namelen, sizeof(bufname[0]), fp), "%s", "LoadOldVer: Loading the name of UniTensor is failure. (UniTensor<T>)");
      int st;
      uni10_error_msg(!fread(&st, 1, sizeof(st), fp), "%s", "LoadOldVer: Loading the status of UniTensor is failure. (UniTensor<T>)");  //OUT: status(4 bytes)
      int bondNum;
      uni10_error_msg(!fread(&bondNum, 1, sizeof(bondNum), fp), "%s", "LoadOldVer: Loading the bondNum of UniTensor is failure. (UniTensor<T>)");  //OUT: bondNum(4 bytes)
      uni10_uint64 qnum_sz;
      uni10_error_msg(!fread(&qnum_sz, 1, sizeof(qnum_sz), fp), "%s", "LoadOldVer: Loading the qnum_sz of UniTensor is failure. (UniTensor<T>)");  //OUT: sizeof(Qnum)
      uni10_error_msg(!(qnum_sz == sizeof(Qnum)), "LoadOldVer: Error in reading file '%s' in.", fname.c_str());

      std::vector<Bond> bufbonds;
      for(uni10_uint64 b = 0; b < bondNum; b++){
        int num_q;
        bondType tp;
        uni10_error_msg(!fread(&tp, 1, sizeof(bondType), fp), "%s", "LoadOldVer: Loading the bondType of UniTensor is failure. (UniTensor<T>)"); //OUT: Number of Qnums in the bond(4 bytes)
        uni10_error_msg(!fread(&num_q, 1, sizeof(num_q), fp), "%s", "LoadOldVer: Loading the num_q of UniTensor is failure. (UniTensor<T>)");   //OUT: Number of Qnums in the bond(4 bytes)
        Qnum q0;
        std::vector<Qnum> qnums(num_q, q0);
        uni10_error_msg(!fread(&qnums[0], num_q, qnum_sz, fp), "%s", "LoadOldVer: Loading the qnums of UniTensor is failure. (UniTensor<T>)");
        std::vector<int> qdegs(num_q, 0);
        uni10_error_msg(!fread(&(qdegs[0]), num_q, sizeof(qdegs[0]), fp), "%s", "LoadOldVer: Loading the qdegs of UniTensor is failure. (UniTensor<T>)");
        std::vector<Qnum> tot_qnums;
        for(uni10_uint64 q = 0; q < num_q; q++)
          for(uni10_int d = 0; d < qdegs[q]; d++)
            tot_qnums.push_back(qnums[q]);

        Bond bd(tp, tot_qnums);
        bufbonds.push_back(bd);
      }

      this->Assign(bufbonds);
      this->SetName(bufname);

      int num_l;
      uni10_error_msg(!fread(&num_l, 1, sizeof(num_l), fp), "%s", "LoadOldVer: Loading the num_l of UniTensor is failure. (UniTensor<T>)");  //OUT: Number of Labels in the Tensor(4 bytes)
      uni10_error_msg(!(num_l == bonds->size()), "LoadOldVer: Error in reading file '%s' in.", fname.c_str());
      //labels->assign(num_l, 0);
      std::vector<int> buflabels(num_l);
      if(num_l != 0)
        uni10_error_msg(!fread(&(buflabels[0]), num_l, sizeof(buflabels[0]), fp), "%s", "LoadOldVer: Loading the labels of UniTensor is failure. (UniTensor<T>)");
      this->SetLabel(buflabels);
      if(st & HAVEELEM){
          size_t memsize = this->GET_ELEMNUM() * sizeof(uni10_type);
          uni10_type *tmp_elem = (uni10_type*)malloc(memsize);
          size_t num_el;
          fread(&num_el, 1, sizeof(U_elemNum), fp);	//OUT: Number of elements in the Tensor(4 bytes)
          fread(tmp_elem, num_el, sizeof(uni10_type), fp);
          this->SetElem(tmp_elem);
        (*this->status)|= HAVEELEM;
      }

      fclose(fp);

    }

  template <typename uni10_type>
    UniTensor<uni10_type>& UniTensor<uni10_type>::Assign(const std::vector<Bond>& _bonds ){

      if(this->paras != NULL)
        this->free_para();

      this->style = check_bonds(_bonds);
      this->init_para();
      this->meta_link();
      *bonds = _bonds;
      *status= 0;
      this->init();
      return *this;

    }

  template <typename uni10_type>
    void UniTensor<uni10_type>::PutBlock(const Block<uni10_type>& mat){
      Qnum q0(0);
      PutBlock(q0, mat);
    }

  template <typename uni10_type>
    void UniTensor<uni10_type>::PutBlock(const Qnum& qnum, const Block<uni10_type>& mat){

      tensor_tools::putBlock(paras, qnum, mat, style);
      *status |= HAVEELEM;

    }

  template <typename uni10_type>
    void UniTensor<uni10_type>::SetName(const std::string& _name){
      *name = _name;
    }

  template <typename uni10_type>
    void UniTensor<uni10_type>::SetLabel(const uni10_int newLabel, const uni10_uint64 idx){
      uni10_error_msg(labels->size() <= idx, "%s", "The bond index is out of the range of vector(labels).");
      (*labels)[idx] = newLabel;
    }

  template <typename uni10_type>
    void UniTensor<uni10_type>::SetLabel(const std::vector<uni10_int>& newLabels){
      uni10_error_msg(!(bonds->size() == newLabels.size()), "%s", "The size of input vector(labels) does not match for the number of bonds.");
      *labels = newLabels;
    }

  template <typename uni10_type>
    void UniTensor<uni10_type>::SetLabel(uni10_int* newLabels){
      std::vector<uni10_int> labels(newLabels, newLabels + bonds->size());
      SetLabel(labels);
    }

  template <typename uni10_type>
    bool UniTensor<uni10_type>::ContainLabels(const std::vector<uni10_int>& subLabels){
      bool contains = true;
      int i = 0;
      int len = subLabels.size();
      while (contains && i < len){
        contains *= (std::find((*labels).begin(), (*labels).end(), subLabels[i]) != (*labels).end());
        i += 1;
      }
      return contains;
    }

  template <typename uni10_type>
    bool UniTensor<uni10_type>::ContainLabels(const _Swap swap){
      std::vector<uni10_int> subLabels = {swap.b1, swap.b2};
      return this->ContainLabels(subLabels);
    }

  template <typename uni10_type>
    const Block<uni10_type>& UniTensor<uni10_type>::ConstGetBlock()const{
      Qnum q0(0);
      return ConstGetBlock(q0);
    }

  template <typename uni10_type>
    const Block<uni10_type>& UniTensor<uni10_type>::ConstGetBlock(const Qnum& qnum)const{
      typename std::map<Qnum, Block<uni10_type> >::const_iterator it = blocks->find(qnum);
      if(it == blocks->end()){
        uni10_error_msg(true, "%s", "There is no block with the given quantum number ");
        std::cout << qnum;
      }
      return it->second;
    }

  template <typename uni10_type>
    std::vector<Qnum> UniTensor<uni10_type>::BlocksQnum()const{
      std::vector<Qnum> keys;
      typename std::map<Qnum, Block<uni10_type> >::const_iterator it = blocks->begin();
      for(; it != blocks->end(); it++)
        keys.push_back(it->first);
      return keys;
    }

  template <typename uni10_type>
    Qnum UniTensor<uni10_type>::BlockQnum(uni10_uint64 idx)const{

      uni10_error_msg(!(idx < blocks->size()), "Index exceeds the number of the blocks( %ld ).", blocks->size());
      typename std::map<Qnum, Block<uni10_type> >::const_iterator it = blocks->begin();
      for(; it != blocks->end(); it++){
        if(idx == 0)
          return it->first;
        idx--;
      }
      return Qnum();
    }

  template <typename uni10_type>
    std::map< Qnum, Matrix<uni10_type> > UniTensor<uni10_type>::GetBlocks()const{
      std::map<Qnum, Matrix<uni10_type> > mats;
      typename std::map<Qnum, Block<uni10_type> >::const_iterator it = blocks->begin();
      for(; it != blocks->end(); it++){
        Matrix<uni10_type> mat(it->second.row_, it->second.col_, it->second.elem_.elem_ptr_);
        mats.insert(std::pair<Qnum, Matrix<uni10_type> >(it->first, mat));
      }
      return mats;
    }

  template <typename uni10_type>
    Matrix<uni10_type> UniTensor<uni10_type>::GetBlock(uni10_bool diag_)const{
      Qnum q0(0);
      return GetBlock(q0, diag_);
    }

  template <typename uni10_type>
    Matrix<uni10_type> UniTensor<uni10_type>::GetBlock(const Qnum& qnum, uni10_bool diag_)const{
      typename std::map<Qnum, Block<uni10_type> >::const_iterator it = blocks->find(qnum);
      if(it == blocks->end()){
        uni10_error_msg(true, "%s", "There is no block with the given quantum number ");
        std::cout<<qnum;
      }
      if(diag_)
        return GetDiag(it->second);
      else{
        Matrix<uni10_type> mat(it->second.row_, it->second.col_, it->second.elem_.elem_ptr_, false);
        return mat;
      }
    }

  template <typename uni10_type>
    void UniTensor<uni10_type>::SetRawElem(const uni10_type* rawElem){

      tensor_tools::setRawElem(paras, rawElem, style);
      *status |= HAVEELEM;

    }

  template <typename uni10_type>
    void UniTensor<uni10_type>::SetRawElem(const std::vector<uni10_type>& rawElem){

      SetRawElem(&rawElem[0]);

    }

  template <typename uni10_type>
    void UniTensor<uni10_type>::SetRawElem(const Block<uni10_type>& blk){

      SetRawElem(blk.GetElem());

    }

  template <typename uni10_type>
    void UniTensor<uni10_type>::SetElem(const uni10_type* _src){
      //UELEM(uni10_elem, _package, _type)<uni10_type> _src(_elem, 1, *U_elemNum, false);
      U_elem->set_elem_ptr(_src, false);
      *status |= HAVEELEM;
    }

  template <typename uni10_type>
    void UniTensor<uni10_type>::SetElem(const std::vector<uni10_type>& _elem){
      uni10_error_msg(_elem.size() != *U_elemNum, "%s", "The number of input elements is defferent from the size of the UniTensor");
      SetElem(&_elem[0]);
    }

  template <typename uni10_type>
    UniTensor<uni10_type>& UniTensor<uni10_type>::CombineBond(const std::vector<uni10_int>& cmbLabels){

      uni10_error_msg((*status & HAVEBOND) == 0, "%s", "There is no bond in the tensor to be combined.");

      if(!(cmbLabels.size() > 1)){
        return *this;
      }

      std::vector<uni10_int> rsp_labels(labels->size(), 0);
      std::vector<uni10_int> reduced_labels(this->labels->size() - cmbLabels.size() + 1, 0);

      std::vector<uni10_int> marked(this->labels->size(), 0);
      std::vector<uni10_int> picked(cmbLabels.size(), 0);
      for(uni10_uint64 p = 0; p < cmbLabels.size(); p++){
        for(uni10_uint64 l = 0; l < this->labels->size(); l++){
          if(cmbLabels[p] == (*this->labels)[l]){
            picked[p] = l;
            marked[l] = 1;
            break;
          }
        }
      }

      uni10_int mark = 0;
      for(uni10_uint64 m = 0; m < marked.size(); m++)
        if(marked[m])
          mark++;

      uni10_error_msg(!(mark == cmbLabels.size()), "%s", "The input labels do not match for the labels of the tensor.");
      uni10_int enc = 0;
      uni10_int enc_r = 0;

      std::vector<Bond> newBonds;
      uni10_int RBnum = 0;
      for(uni10_uint64 l = 0; l < this->labels->size(); l++){
        if(marked[l] && l == (uni10_uint64)picked[0]){
          for(uni10_uint64 ll = 0; ll < cmbLabels.size(); ll++){
            rsp_labels[enc] = cmbLabels[ll];

            enc++;
          }
          std::vector<Bond> tmpBonds;
          for(uni10_uint64 p = 0; p < picked.size(); p++)
            tmpBonds.push_back((*this->bonds)[picked[p]]);
          if((*this->bonds)[picked[0]].type() == BD_IN)
            RBnum += picked.size();
          newBonds.push_back(combine(tmpBonds));
          reduced_labels[enc_r] = (*this->labels)[l];
          enc_r++;
        }
        else if(marked[l] == 0){
          rsp_labels[enc] = (*this->labels)[l];
          reduced_labels[enc_r] = (*this->labels)[l];
          if((*this->bonds)[l].type() == BD_IN)
            RBnum++;
          newBonds.push_back((*this->bonds)[l]);
          enc_r++;
          enc++;
        }
      }

      UniTensor<uni10_type> T_ori;
      Permute(T_ori, *this, rsp_labels, RBnum, INPLACE);

      uni10_int isInit = (*status & HAVEELEM);
      this->Assign(newBonds);
      this->SetLabel(reduced_labels);
      if(isInit){
        this->SetRawElem(T_ori.GetRawElem());
        //this->U_elem->Copy(0, *T_ori.U_elem, T_ori.U_elem->elem_num_);
        //*status |= HAVEELEM;
      }

      return *this;
    }

  template <typename uni10_type>
    UniTensor<uni10_type>& UniTensor<uni10_type>::CombineBond(uni10_int* combined_labels, uni10_int bondNum){

      std::vector<uni10_int> _combined_labels(combined_labels, combined_labels+bondNum);
      return this->CombineBond(_combined_labels);

    }

  template<typename uni10_type>
    uni10_type UniTensor<uni10_type>::At(const std::vector<uni10_uint64>& idxs)const{

      uni10_error_msg((*status & HAVEBOND) == 0, "%s", "The tensor is a scalar. Use UniTensor::operator() instead.");
      uni10_error_msg(!(idxs.size() == bonds->size()), "%s", "The size of input indices array does not match with the number of the bonds.");

      return tensor_tools::tensorAt(this->paras, &idxs[0], style);

    }


  template <typename uni10_type>
    void UniTensor<uni10_type>::AddGate(const std::vector<_Swap>& swaps){

      tensor_tools::addGate(this->paras, swaps, this->style);

    }

  template <typename uni10_type>
    std::vector<_Swap> UniTensor<uni10_type>::ExSwap(const UniTensor<uni10_double64>& Tb)const{

      std::vector<_Swap> swaps;

      if(*status & *Tb.status & HAVEBOND){
        uni10_int bondNumA = labels->size();
        uni10_int bondNumB = Tb.labels->size();
        std::vector<uni10_int> intersect;
        std::vector<uni10_int> left;
        for(uni10_int a = 0; a < bondNumA; a++){
          uni10_bool found = false;
          for(uni10_int b = 0; b < bondNumB; b++)
            if((*labels)[a] == (*Tb.labels)[b])
              found = true;
          if(found)
            intersect.push_back(a);
          else
            left.push_back(a);
        }
        _Swap sp;
        for(uni10_uint64 i = 0; i < intersect.size(); i++)
          for(uni10_uint64 j = 0; j < left.size(); j++){
            sp.b1 = intersect[i];
            sp.b2 = left[j];
            swaps.push_back(sp);
          }
      }
      return swaps;
    }

  template <typename uni10_type>
    std::vector<_Swap> UniTensor<uni10_type>::ExSwap(const UniTensor<uni10_complex128>& Tb)const{

      std::vector<_Swap> swaps;

      if(*status & *Tb.status & HAVEBOND){
        uni10_int bondNumA = labels->size();
        uni10_int bondNumB = Tb.labels->size();
        std::vector<uni10_int> intersect;
        std::vector<uni10_int> left;
        for(uni10_int a = 0; a < bondNumA; a++){
          uni10_bool found = false;
          for(uni10_int b = 0; b < bondNumB; b++)
            if((*labels)[a] == (*Tb.labels)[b])
              found = true;
          if(found)
            intersect.push_back(a);
          else
            left.push_back(a);
        }
        _Swap sp;
        for(uni10_uint64 i = 0; i < intersect.size(); i++)
          for(uni10_uint64 j = 0; j < left.size(); j++){
            sp.b1 = intersect[i];
            sp.b2 = left[j];
            swaps.push_back(sp);
          }
      }
      return swaps;
    }

  template <typename uni10_type>
    void UniTensor<uni10_type>::SetStyle(const contain_type s){
      this->style = s;
    }

  template <typename uni10_type>
    void UniTensor<uni10_type>::ApplySwapGate(uni10_int to_permute, const std::vector<uni10_int>& to_cross, bool permute_back){
      std::vector<int> lab_ori = this->label();
      int tbn = lab_ori.size();
      int ibn = this->InBondNum();
      int sgn = to_cross.size();  // swap gate number
      std::vector<int> lab_tmp;
      std::vector<int> lab_fin;

      std::vector<int> indi;  // indicate the bond is before/at/after crossed bonds
      bool before = true;
      for (int i = 0; i < tbn; ++i) {
        bool found = (lab_ori[i] == to_permute);
        int j = 0;
        while (!found && j < sgn) {
          found = (lab_ori[i] == to_cross[j]);
          j += 1;
        }
        if (found) {
          indi.push_back(1);
          if (before)
            before = false;
        }
        else
          indi.push_back((int)(!before)*2);
      }

      for (int n = 0; n < tbn; ++n) {
        if (indi[n] == 0) {
          lab_tmp.push_back(lab_ori[n]);
          lab_fin.push_back(lab_ori[n]);
        }
      }

      lab_fin.push_back(to_permute);
      for (int j = 0; j < sgn; ++j) {
        lab_tmp.push_back(to_cross[j]);
        lab_fin.push_back(to_cross[j]);
      }
      lab_tmp.push_back(to_permute);

      for (int n = 0; n < tbn; ++n) {
        if (indi[n] == 2) {
          lab_tmp.push_back(lab_ori[n]);
          lab_fin.push_back(lab_ori[n]);
        }
      }

      auto itc1 = std::find(lab_ori.begin(), lab_ori.end(), to_cross[0]);
      auto itc2 = std::find(lab_ori.begin(), lab_ori.end(), to_cross[to_cross.size()-1]);
      auto itp = std::find(lab_ori.begin(), lab_ori.end(), to_permute);
      auto ic1 = std::distance(lab_ori.begin(), itc1);
      auto ic2 = std::distance(lab_ori.begin(), itc2);
      auto ip = std::distance(lab_ori.begin(), itp);
      bool out2in_tmp = (this->bond()[ic2].type() == 1) && (this->bond()[ip].type() == -1);
      bool out2in_fin = (this->bond()[ic1].type() == 1) && (this->bond()[ip].type() == -1);
      PseudoPermute(*this, lab_tmp, ibn+(int)out2in_tmp, INPLACE);  // permute to_permute to neighbor of to_cross
      Permute(*this, lab_fin, ibn+(int)out2in_fin, INPLACE);  // apply swap gates
      if (permute_back)
        PseudoPermute(*this, lab_ori, ibn, INPLACE);
    }

  template <typename uni10_type>
    void UniTensor<uni10_type>::ApplySwapGate(uni10_int to_permute, uni10_int to_cross, bool permute_back){
      std::vector<uni10_int> to_cross_vec = {to_cross};
      this->ApplySwapGate(to_permute, to_cross_vec, permute_back);
    }

  template <typename uni10_type>
    void UniTensor<uni10_type>::ApplySwapGate(_Swap to_swap, bool permute_back){
      this->ApplySwapGate(to_swap.b1, to_swap.b2, permute_back);
    }

  template <typename uni10_type>
    void UniTensor<uni10_type>::PrintDiagram()const{

      if(this->paras == NULL){
        std::cout<<"This UniTensor has not been initialized."<< std::endl;
        return ;
      }

      if(!(*status & HAVEBOND)){
        if(U_elem->ongpu_)
          std::cout<<"\nScalar: " << U_elem->elem_ptr_[0]<<", onGPU";
        else
          std::cout<<"\nScalar: " << U_elem->elem_ptr_[0];
        std::cout<<"\n\n";
      }
      else{

        uni10_uint64 row = 0;
        uni10_uint64 col = 0;

        std::vector<Bond>_bonds = *bonds;
        for(uni10_uint64 i = 0; i < _bonds.size(); i++)
          if(_bonds[i].type() == BD_IN)
            row++;
          else
            col++;
        uni10_uint64 layer = std::max(row, col);
        uni10_uint64 nmlen = name->length() + 2;
        uni10_int star = 12 + (14 - nmlen) / 2;
        for(uni10_int s = 0; s < star; s++)
          std::cout << "*";
        if(name->length() > 0)
          std::cout << " " << *name << " ";
        for(uni10_int s = 0; s < star; s++)
          std::cout <<"*";
        std::cout<<std::endl;

        if(U_elem->uni10_typeid_ == 1)
          std::cout << "REAL" << std::endl;
        else if(U_elem->uni10_typeid_ == 2)
          std::cout << "COMPLEX" << std::endl;

        if(U_elem->ongpu_)
          std::cout<<"\n                 onGPU";
        std::cout << "\n             ____________\n";
        std::cout << "            |            |\n";
        uni10_uint64 llab = 0;
        uni10_uint64 rlab = 0;
        char buf[128];
        for(uni10_uint64 l = 0; l < layer; l++){
          if(l < row && l < col){
            llab = (*labels)[l];
            rlab = (*labels)[row + l];
            sprintf(buf, "    %5ld___|%-4d    %4d|___%-5ld\n", llab, _bonds[l].dim(), _bonds[row + l].dim(), rlab);
            std::cout<<buf;
          }
          else if(l < row){
            llab = (*labels)[l];
            sprintf(buf, "    %5ld___|%-4d    %4s|\n", llab, _bonds[l].dim(), "");
            std::cout<<buf;
          }
          else if(l < col){
            rlab = (*labels)[row + l];
            sprintf(buf, "    %5s   |%4s    %4d|___%-5ld\n", "", "", _bonds[row + l].dim(), rlab);
            std::cout << buf;
          }
          std::cout << "            |            |   \n";
        }
        std::cout << "            |____________|\n";

        std::cout << "\n================BONDS===============\n";
        for(uni10_uint64 b = 0; b < _bonds.size(); b++)
          std::cout << _bonds[b];

        std::cout << "\n\nTotal elemNum: "<<(*U_elemNum)<<std::endl;
        std::cout << "====================================\n";

      }
    }

  template<typename uni10_type>
    Matrix<uni10_type> UniTensor<uni10_type>::GetRawElem()const{

      if(*status & HAVEBOND && *status & HAVEELEM){
        uni10_int bondNum = bonds->size();
        uni10_uint64 rowNum = 1;
        uni10_uint64 colNum = 1;
        for(std::vector<Bond>::const_iterator it = bonds->begin(); it != bonds->end(); ++it){
          if(it->type() == BD_IN)
            rowNum *= it->dim();
          else
            colNum *= it->dim();
        }
        std::vector<uni10_uint64> idxs(bondNum, 0);
        uni10_int bend;
        std::vector<uni10_type> rawElem;
        while(1){
          rawElem.push_back(At(idxs));
          //std::cout << "testing: " << at(idxs) << std::endl;
          for(bend = bondNum - 1; bend >= 0; bend--){
            idxs[bend]++;
            if(idxs[bend] < (uni10_uint64)(*bonds)[bend].dim())
              break;
            else
              idxs[bend] = 0;
          }
          if(bend < 0)
            break;
        }
        return Matrix<uni10_type>(rowNum, colNum, &rawElem[0]);
      }
      else if(*status & HAVEELEM){
        return Matrix<uni10_type>(1, 1, this->U_elem->elem_ptr_);
      }

      return Matrix<uni10_type>();

    }

  template<typename uni10_type>
    std::string UniTensor<uni10_type>::PrintRawElem(bool print)const{

      std::ostringstream os;
      if(*status & HAVEBOND && *status & HAVEELEM){
        uni10_int bondNum = bonds->size();
        std::vector<Bond> ins;
        std::vector<Bond> outs;
        for(std::vector<Bond>::const_iterator it = bonds->begin(); it != bonds->end(); ++it){
          if(it->type() == BD_IN)
            ins.push_back(*it);
          else
            outs.push_back(*it);
        }
        if(ins.size() == 0 || outs.size() == 0)
          os<<GetRawElem();
        else{
          Bond rBond = combine(ins);
          Bond cBond = combine(outs);
          std::vector<Qnum> rowQ = rBond.Qlist();
          std::vector<Qnum> colQ = cBond.Qlist();
          uni10_uint64 colNum = cBond.dim();
          std::vector<uni10_uint64> idxs(bondNum, 0);

          os<< "     ";
          for(uni10_uint64 q = 0; q < colQ.size(); q++)
            os<< "   " << std::setw(2) << colQ[q].U1() << "," << colQ[q].prt();
          os<< std::endl << std::setw(5) << "" << std::setw(colQ.size() * 7 + 2) <<std::setfill('-')<<"";
          os<<std::setfill(' ');
          uni10_int cnt = 0;
          uni10_int r = 0;
          uni10_int bend;
          while(1){
            if(cnt % colNum == 0){
              os<<"\n    |\n" << std::setw(2) << rowQ[r].U1() << "," << rowQ[r].prt() << "|";
              r++;
            }
            os<< std::setw(7) << std::fixed << std::setprecision(3) << At(idxs);
            for(bend = bondNum - 1; bend >= 0; bend--){
              idxs[bend]++;
              if(idxs[bend] < (uni10_uint64)(*bonds)[bend].dim())
                break;
              else
                idxs[bend] = 0;
            }
            cnt++;
            if(bend < 0)
              break;
          }
          os <<"\n    |\n";
        }
      }
      if(*status & HAVEELEM){
        //os<<"\nScalar: " << c_elem[0]<<"\n\n";
      }
      else
        os<<"NO ELEMENT IN THE TENSOR!!!\n";

      if(print){
        std::cout<<os.str();
        return "";
      }

      return os.str();

    }

  template<typename uni10_type>
    std::string UniTensor<uni10_type>::Profile(bool print){

      std::ostringstream os;
      os<<"\n===== Tensor profile =====\n";
      os<<"Existing Tensors: " << COUNTER << std::endl;
      os<<"Allocated Elements: " << ELEMNUM << std::endl;
      os<<"Max Allocated Elements: " << MAXELEMNUM << std::endl;
      os<<"Max Allocated Elements for a Tensor: " << MAXELEMTEN << std::endl;
      os<<"============================\n\n";
      if(print){
        std::cout<<os.str();
        return "";
      }
      return os.str();

    }

  template <typename uni10_type>
    void UniTensor<uni10_type>::init_para(){

      paras = tensor_tools::init_para(paras, style);

    }

  template <typename uni10_type>
    void UniTensor<uni10_type>::copy_para(U_para<uni10_type>* src_para){

      tensor_tools::copy_para(paras, src_para, style);

    }

  template <typename uni10_type>
    void UniTensor<uni10_type>::meta_link(){

      if(style == 0){

        this->name      = &paras->nsy->name;
        this->bonds     = &paras->nsy->bonds;
        this->labels    = &paras->nsy->labels;
        this->RBondNum  = &paras->nsy->RBondNum;
        this->RQdim     = &paras->nsy->RQdim;
        this->CQdim     = &paras->nsy->CQdim;
        this->U_elemNum = &paras->nsy->U_elemNum;
        this->blocks    = &paras->nsy->blocks;
        this->U_elem    = &paras->nsy->U_elem;
        this->status    = &paras->nsy->status;

      }
      else if(style == 1 || style == 2){

        this->name      = &paras->bsy->name;
        this->bonds     = &paras->bsy->bonds;
        this->labels    = &paras->bsy->labels;
        this->RBondNum  = &paras->bsy->RBondNum;
        this->RQdim     = &paras->bsy->RQdim;
        this->CQdim     = &paras->bsy->CQdim;
        this->U_elemNum = &paras->bsy->U_elemNum;
        this->blocks    = &paras->bsy->blocks;
        this->U_elem    = &paras->bsy->U_elem;
        this->status    = &paras->bsy->status;

      }
      else if(style == 3){
        //name = &paras->ssy->name;
        uni10_error_msg(true, "%s", "Developping!!!");
      }

    }

  template <typename uni10_type>
    void UniTensor<uni10_type>::init(){
      // You should init_para() first. Then you can use this function to initialize the UniTensor.
      tensor_tools::init(paras, style);
      this->check_status();

      ELEMNUM += *this->U_elemNum;
      COUNTER++;
      if(ELEMNUM > MAXELEMNUM)
        MAXELEMNUM = ELEMNUM;
      if(*this->U_elemNum > MAXELEMTEN)
        MAXELEMTEN = *this->U_elemNum;

    }

  template <typename uni10_type>
    void UniTensor<uni10_type>::check_status(){

      if(bonds->size())
          *status |= HAVEBOND;
      else
          *status |= HAVEELEM;

    }

  template <typename uni10_type>
    void UniTensor<uni10_type>::initBlocks(){
      
      tensor_tools::initBlocks(paras, style);

    }


  template <typename uni10_type>
    void UniTensor<uni10_type>::free_para(){
      // You should init_para() first. Then you can use this function to initialize the UniTensor.
      tensor_tools::free_para(paras, style);
    }

  template<typename uni10_type>
    void UniTensor<uni10_type>::init_paras_null(){

      this->paras = NULL;
      this->name = NULL;
      this->bonds = NULL;
      this->labels = NULL;
      this->RBondNum = NULL;
      this->RQdim = NULL;
      this->CQdim = NULL;
      this->U_elemNum = NULL;
      this->blocks = NULL;
      this->U_elem = NULL;
      this->status = NULL;

    };

  template <typename uni10_type>
    contain_type UniTensor<uni10_type>::check_bonds(const std::vector<Bond>& _bonds)const{

      contain_type s;
      uni10_bool withSymmetry = false;
      for(uni10_uint64 b = 0; b < _bonds.size(); b ++){
        if(_bonds[b].WithSymmetry()){
          std::vector<Qnum> qn = _bonds[b].const_getQnums();
          if(qn.size() == 1 && qn[0] == Qnum(0))
            continue;
          else {
            withSymmetry = true;
            break;
          }
        }
      }

      // Check parityF odd
      uni10_bool isPrtF = false;
      if(withSymmetry){
        for(uni10_uint64 b = 0; b < _bonds.size(); b ++){
          if(!isPrtF){
            for(uni10_uint64 q = 0; q < _bonds[b].const_getQnums().size(); q ++){
              if(_bonds[b].const_getQnums()[q].prtF() & PRTF_ODD){
                isPrtF = true;
                break;
              }
            }
          }
          if(isPrtF)
            break;
        }
        s = isPrtF ? fm_sym : bs_sym;
      }
      else
        s = no_sym;
      // spar_sym are developping
      return s;

    }

  template<typename uni10_type>
    void UniTensor<uni10_type>::Zeros(){

      this->U_elem->SetZeros();
      *status |= HAVEELEM;

    };

  template<typename uni10_type>
    void UniTensor<uni10_type>::Zeros(const Qnum& qnum){

      typename std::map<Qnum, Block<uni10_type> >::iterator it = this->blocks->find(qnum);

      uni10_error_msg(it == this->blocks->end(), "%s", "There is no block with the given quantum number.");

      Block<uni10_type>& block = it->second;
      block.elem_.SetZeros();
      *status |= HAVEELEM;

    };

template<typename uni10_type>
    void UniTensor<uni10_type>::Ones(){

      this->U_elem->SetOnes();
      *status |= HAVEELEM;

    };

  template<typename uni10_type>
    void UniTensor<uni10_type>::Ones(const Qnum& qnum){

      typename std::map<Qnum, Block<uni10_type> >::iterator it = this->blocks->find(qnum);

      uni10_error_msg(it == this->blocks->end(), "%s", "There is no block with the given quantum number.");

      Block<uni10_type>& block = it->second;
      block.elem_.SetOnes();
      *status |= HAVEELEM;

    };

  template<typename uni10_type>
    void UniTensor<uni10_type>::Identity(){

      typename std::map<Qnum, Block<uni10_type> >::iterator it = this->blocks->begin();
      for(; it != this->blocks->end(); it++)
        linalg_unielem_internal::Identity(&it->second.elem_, &it->second.diag_, &it->second.row_, &it->second.col_);
      *status |= HAVEELEM;

    };

  template<typename uni10_type>
    void UniTensor<uni10_type>::Identity(const Qnum& qnum){

      typename std::map<Qnum, Block<uni10_type> >::iterator it = this->blocks->find(qnum);
      uni10_error_msg(it == this->blocks->end(), "%s", "There is no block with the given quantum number.");
      Block<uni10_type>& block = it->second;
      linalg_unielem_internal::Identity(&block.elem_, &block.diag_, &block.row_, &block.col_);
      *status |= HAVEELEM;

    };

  template<typename uni10_type>
    void UniTensor<uni10_type>::Randomize(char UorN, uni10_double64 dn_mu, uni10_double64 up_var, uni10_int64 seed){

      typename std::map<Qnum, Block<uni10_type> >::iterator it = this->blocks->begin();
      if(UorN == 'U'){
        uni10_double64 dn = std::min(dn_mu, up_var);
        uni10_double64 up = std::max(dn_mu, up_var);
        for(; it != this->blocks->end(); it++)
          linalg_unielem_internal::UniformRandomize(&it->second.elem_, &it->second.diag_, &it->second.row_, &it->second.col_, &dn, &up, &seed);
      }else if(UorN == 'N'){
        for(; it != this->blocks->end(); it++)
          linalg_unielem_internal::NormalRandomize(&it->second.elem_, &it->second.diag_, &it->second.row_, &it->second.col_, &dn_mu, &up_var, &seed);
      }else
        uni10_error_msg(true, "%s", "Wrong flag. Hint: The fisrt parameter must be 'N' or 'U'");
      *status |= HAVEELEM;

    };

  template<typename uni10_type>
    void UniTensor<uni10_type>::Randomize(const Qnum& qnum, char UorN, uni10_double64 dn_mu, uni10_double64 up_var, uni10_int64 seed){

      typename std::map<Qnum, Block<uni10_type> >::iterator it = this->blocks->find(qnum);
      uni10_error_msg(it == this->blocks->end(), "%s", "There is no block with the given quantum number.");
      Block<uni10_type>& block = it->second;
      if(UorN == 'U'){
        uni10_double64 dn = std::min(dn_mu, up_var);
        uni10_double64 up = std::max(dn_mu, up_var);
        linalg_unielem_internal::UniformRandomize(&block.elem_, &block.diag_, &block.row_, &block.col_, &dn, &up, &seed);
      }
      else if(UorN == 'N')
        linalg_unielem_internal::NormalRandomize(&block.elem_, &block.diag_, &block.row_, &block.col_, &dn_mu, &up_var, &seed);
      else
        uni10_error_msg(true, "%s", "Wrong flag. Hint: The fisrt parameter must be 'N' or 'U'");
      *status |= HAVEELEM;

    };

  template<typename uni10_type>
    void UniTensor<uni10_type>::OrthoRand(char UorN, uni10_double64 dn_mu, uni10_double64 up_var, uni10_int64 seed){


      typename std::map<Qnum, Block<uni10_type> >::iterator it = this->blocks->begin();
      Matrix<uni10_type> U, S, vT;
      Matrix<uni10_type>* null_mat = NULL;
      if(UorN == 'U'){
        uni10_double64 dn = std::min(dn_mu, up_var);
        uni10_double64 up = std::max(dn_mu, up_var);
        for(; it != this->blocks->end(); it++){
          linalg_unielem_internal::UniformRandomize(&it->second.elem_, &it->second.diag_, &it->second.row_, &it->second.col_, &dn, &up, &seed);
          if(it->second.row_ < it->second.col_){
            Svd(it->second, *null_mat, S, vT, INPLACE);
            this->PutBlock(it->first, vT);
          }else{
            Svd(it->second, U, S, *null_mat, INPLACE);
            this->PutBlock(it->first, U);
          }
        }
      }else if(UorN == 'N'){
        for(; it != this->blocks->end(); it++){
          linalg_unielem_internal::NormalRandomize(&it->second.elem_, &it->second.diag_, &it->second.row_, &it->second.col_, &dn_mu, &up_var, &seed);
          if(it->second.row_ < it->second.col_){
            Svd(it->second, *null_mat, S, vT, INPLACE);
            this->PutBlock(it->first, vT);
          }else{
            Svd(it->second, U, S, *null_mat, INPLACE);
            this->PutBlock(it->first, U);
          }
        }
      }else
        uni10_error_msg(true, "%s", "Wrong flag. Hint: The fisrt parameter must be 'N' or 'U'");
      *status |= HAVEELEM;

    };

  template<typename uni10_type>
    void UniTensor<uni10_type>::OrthoRand(const Qnum& qnum, char UorN, uni10_double64 dn_mu, uni10_double64 up_var, uni10_int64 seed){

      typename std::map<Qnum, Block<uni10_type> >::iterator it = this->blocks->find(qnum);
      uni10_error_msg(it == this->blocks->end(), "%s", "There is no block with the given quantum number.");
      Matrix<uni10_type> U, S, vT;
      Matrix<uni10_type>* null_mat = NULL;
      Block<uni10_type>& block = it->second;
      if(UorN == 'U'){
        uni10_double64 dn = std::min(dn_mu, up_var);
        uni10_double64 up = std::max(dn_mu, up_var);
        linalg_unielem_internal::UniformRandomize(&block.elem_, &block.diag_, &block.row_, &block.col_, &dn, &up, &seed);
        if(it->second.row_ < it->second.col_){
          Svd(it->second, *null_mat, S, vT, INPLACE);
          this->PutBlock(it->first, vT);
        }else{
          Svd(it->second, U, S, *null_mat, INPLACE);
          this->PutBlock(it->first, U);
        }
      }
      else if(UorN == 'N'){
        linalg_unielem_internal::NormalRandomize(&block.elem_, &block.diag_, &block.row_, &block.col_, &dn_mu, &up_var, &seed);
        if(it->second.row_ < it->second.col_){
          Svd(it->second, *null_mat, S, vT, INPLACE);
          this->PutBlock(it->first, vT);
        }else{
          Svd(it->second, U, S, *null_mat, INPLACE);
          this->PutBlock(it->first, U);
        }
      }
      else
        uni10_error_msg(true, "%s", "Wrong flag. Hint: The fisrt parameter must be 'N' or 'U'");
      *status |= HAVEELEM;

    };

  template<typename uni10_type>
    void UniTensor<uni10_type>::Clear(){
      *this = UniTensor();
      (*status) &= ~HAVEELEM;
    }

  UniTensor<uni10_complex128>& operator*=(UniTensor<uni10_complex128>& t1, uni10_complex128 a){
    linalg_unielem_internal::VectorScal(&a, t1.U_elem, &t1.U_elem->elem_num_);
      return t1;
  }

  template class UniTensor<uni10_double64>;
  template class UniTensor<uni10_complex128>;
}
