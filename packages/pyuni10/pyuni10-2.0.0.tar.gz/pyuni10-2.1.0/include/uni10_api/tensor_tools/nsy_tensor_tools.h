#ifndef __UNI10_NSY_TENSOR_TOOLS_H__
#define __UNI10_NSY_TENSOR_TOOLS_H__

#include <stdio.h>

#include "uni10_api/rng.h"
#include "uni10_api/UniTensor.h"
#include "uni10_elem_hirnk_linalg.h"

namespace uni10{
  
  namespace tensor_tools{

    //Function prototype.
    template<typename UniType>
      U_para<UniType>* init_para_nsy(U_para<UniType>* para);

    template<typename UniType>
      void copy_para_nsy(U_para<UniType>* para, const U_para<UniType>* src_para);

    template<typename UniType>
      void free_para_nsy(U_para<UniType>* para);

    template<typename UniType>
      void init_nsy(U_para<UniType>* para);

    template<typename UniType>
      uni10_uint64 grouping_nsy(U_para<UniType>* para);

    template <typename UniType>
      void initBlocks_nsy(U_para<UniType>* para);

    template <typename UniType>
      void setRawElem_nsy(U_para<UniType>* para, const UniType* rawElem);

    template <typename UniType>
      void putBlock_nsy(U_para<UniType>* para,const Qnum& qnum, const Block<UniType>& mat);

    template <typename UniType>
      void set_zero_nsy(U_para<UniType>* para);

    template <typename UniType>
      void randomize_nsy(U_para<UniType>* para);

    template <typename UniType>
      void transpose_nsy(U_para<UniType>* para, const U_para<UniType>* src_para);

    template <typename UniType>
      void dagger_nsy(U_para<UniType>* para, const U_para<UniType>* src_para);

    template <typename UniType>
      void conj_nsy(U_para<UniType>* para, const U_para<UniType>* src_para);

    template <typename UniType>
      void permute_nsy(const U_para<UniType>* t1_para, const std::vector<uni10_int>& t1_rspbdidx,
        U_para<UniType>* t2_para, uni10_bool inorder);

    template <typename To, typename T, typename U>
      void contract_nsy(  const U_para<T>* t1_para, const U_para<U>* t2_para, UniTensor<To>& t3 );

    template <typename UniType>
      void traceByRow_nsy(U_para<UniType>* Tout_para, const U_para<UniType>* Tin_para, uni10_int la, uni10_int lb );

    template <typename UniType>
      void addGate_nsy(U_para<UniType>* t1_para, const std::vector<_Swap>& swaps);

    template <typename UniType>
      UniType tensorAt_nsy(U_para<UniType>* T_para, const uni10_uint64* idxs);

    //Functions.
    template<typename UniType>
       U_para<UniType>* init_para_nsy(U_para<UniType>* para){

        U_para<UniType>* ptr;
        ptr      = new struct U_para<UniType>[1];
        ptr->nsy = new struct no_sym_para<UniType>[1];
        ptr->check_status = 1;
        para = ptr;

        return para;
        
      }

    template<typename UniType>
      void copy_para_nsy(U_para<UniType>* para, const U_para<UniType>* src_para){

        if(src_para != NULL)
          *para->nsy = *src_para->nsy;

      }

    template<typename UniType>
       void free_para_nsy(U_para<UniType>* para){
        
         if(para!=NULL){
           delete [] para->nsy;
           delete [] para;
         }
        
      }

    template<typename UniType>
      void init_nsy(U_para<UniType>* para){

        if(para->nsy->bonds.size()){
          para->nsy->U_elemNum = grouping_nsy(para);
          if(!(para->nsy->blocks.size() > 0)){ //No block in Tensor, Error!
            uni10_error_msg(true, "%s", "There is no symmetry block with the given bonds:\n");
            for(uni10_int b = 0; b < (uni10_int)para->nsy->bonds.size(); b++)
              std::cout<<"    "<<para->nsy->bonds[b];
          }

          para->nsy->labels.assign(para->nsy->bonds.size(), 0);
          for(uni10_int b = 0; b < (uni10_int)para->nsy->bonds.size(); b++)
            para->nsy->labels[b] = b;

        }
        else{
          Qnum q0(0);
          para->nsy->blocks[q0] = Block<UniType>(1, 1);
          para->nsy->RBondNum = 0;
          para->nsy->RQdim = 0;
          para->nsy->CQdim = 0;
          para->nsy->U_elemNum = 1;

        }

        para->nsy->U_elem.Init(1, para->nsy->U_elemNum, false);
        initBlocks_nsy(para);

      }

    template<typename UniType>
      uni10_uint64 grouping_nsy(U_para<UniType>* para){

        para->nsy->blocks.clear();
        Qnum q0(0);
        uni10_int   row_bondNum = 0;
        uni10_int   col_bondNum = 0;
        para->nsy->RQdim = 1;
        para->nsy->CQdim = 1;
        uni10_bool IN_BONDS_BEFORE_OUT_BONDS = true;
        for(uni10_int i = 0; i < (uni10_int)para->nsy->bonds.size(); i++){
          uni10_error_msg( para->nsy->bonds[i].const_getQdegs().size() > 1 || para->nsy->bonds[i].const_getQnums().size() > 1
              , "%s", "This UniTensor has symmetry!!");
          if(para->nsy->bonds[i].type() == BD_IN){
            uni10_error_msg(!(IN_BONDS_BEFORE_OUT_BONDS == true), 
                "%s","Error in the input bond array: BD_OUT bonds must be placed after all BD_IN bonds.");
            para->nsy->RQdim *= para->nsy->bonds[i].const_getQdegs()[0];
            row_bondNum++;
          }
          else{
            para->nsy->CQdim *= para->nsy->bonds[i].const_getQdegs()[0];
            col_bondNum++;
            IN_BONDS_BEFORE_OUT_BONDS = false;
          }
        }
        para->nsy->RBondNum = row_bondNum;
        para->nsy->blocks[q0] = Block<UniType>(para->nsy->RQdim, para->nsy->CQdim);

        return para->nsy->RQdim*para->nsy->CQdim;

      }

    template <typename UniType>
      void initBlocks_nsy(U_para<UniType>* para){
        uni10_uint64 offset = 0;
        typename std::map< Qnum, Block<UniType> >::iterator it = para->nsy->blocks.begin();
        for(; it != para->nsy->blocks.end(); it++ ){
          it->second.elem_enforce().elem_ptr_ = &(para->nsy->U_elem.elem_ptr_[offset]);
          offset += it->second.row_enforce() * it->second.col_enforce();
        }
      }

    template <typename UniType>
      void setRawElem_nsy(U_para<UniType>* para, const UniType* rawElem){
      
        para->nsy->U_elem.set_elem_ptr(rawElem);

      }

    template <typename UniType>
      void putBlock_nsy(U_para<UniType>* para,const Qnum& qnum, const Block<UniType>& mat){

        typename std::map<Qnum, Block<UniType> >::iterator it;

        if(!((it = para->nsy->blocks.find(qnum)) != para->nsy->blocks.end())){
          uni10_error_msg(true, "%s", "There is no block with the given quantum number ");
          std::cout<<qnum;
        }

        uni10_error_msg(!(mat.row() == it->second.row_enforce() && mat.col() == it->second.col_enforce()), "%s", 
            "The dimension of input matrix does not match for the dimension of the block with quantum number \n  Hint: Use Matrix::resize(int, int)");

        if(mat.GetElem() != it->second.GetElem()){
          if(mat.diag()){
            linalg_unielem_internal::SetDiag(&it->second.elem_enforce(), &mat.const_elem_enforce(), &it->second.row_enforce(), &it->second.col_enforce());
          }
          else
            it->second.elem_enforce().Copy(0, mat.const_elem_enforce(), it->second.row_enforce() * it->second.col_enforce() );

        }

      }

    template <typename UniType>
      void set_zero_nsy(U_para<UniType>* para){

        para->nsy->U_elem.SetZeros();

      }

    template <typename UniType>
      void randomize_nsy(U_para<UniType>* para){

        uni10_error_msg(true, "%s", "Developping!!!\n");

      }

    template <typename UniType>
      void transpose_nsy(U_para<UniType>* para, const U_para<UniType>* src_para){

        typename std::map<Qnum, Block<UniType> >::iterator it_in = src_para->nsy->blocks.begin();
        typename std::map<Qnum, Block<UniType> >::iterator it_out = para->nsy->blocks.begin();
        UELEM(UniElem, _package, _type)<UniType>*  elem_in;
        UELEM(UniElem, _package, _type)<UniType>*  elem_out;
        uni10_uint64 Rnum, Cnum;
        Rnum = it_in->second.row_enforce();
        Cnum = it_in->second.col_enforce();
        elem_in = &(it_in->second.elem_enforce());
        elem_out = &(it_out->second.elem_enforce());
        linalg_unielem_internal::Transpose(elem_in, &Rnum, &Cnum, elem_out);

      }

    template <typename UniType>
      void dagger_nsy(U_para<UniType>* para, const U_para<UniType>* src_para){

        typename std::map<Qnum, Block<UniType> >::iterator it_in = src_para->nsy->blocks.begin();
        typename std::map<Qnum, Block<UniType> >::iterator it_out = para->nsy->blocks.begin();
        UELEM(UniElem, _package, _type)<UniType>*  elem_in;
        UELEM(UniElem, _package, _type)<UniType>*  elem_out;
        uni10_uint64 Rnum, Cnum;
        Rnum = it_in->second.row_enforce();
        Cnum = it_in->second.col_enforce();
        elem_in = &(it_in->second.elem_enforce());
        elem_out = &(it_out->second.elem_enforce());
        linalg_unielem_internal::Dagger(elem_in, &Rnum, &Cnum, elem_out);

      }

    template <typename UniType>
      void conj_nsy(U_para<UniType>* para, const U_para<UniType>* src_para){

        linalg_unielem_internal::Conjugate(&src_para->nsy->U_elem, &src_para->nsy->U_elemNum, &para->nsy->U_elem);

      }

    template <typename UniType>
      void permute_nsy(const U_para<UniType>* t1_para, const std::vector<uni10_int>& t1_rspbdidx,
          U_para<UniType>* t2_para, uni10_bool inorder){

        uni10_int bondNum = t1_para->nsy->bonds.size();
        std::vector<uni10_int> ori_bdDims(bondNum);

        for(uni10_int b = 0; b < (uni10_int)bondNum; b++)
          ori_bdDims[b] = t1_para->nsy->bonds[b].const_getQdegs()[0];

        hirnk_linalg_unielem_internal::TensorTranspose(&t1_para->nsy->U_elem, &t1_rspbdidx[0], bondNum, &ori_bdDims[0], &t2_para->nsy->U_elem);
        
      }

    template <typename To, typename T, typename U>
      uni10_int contract_nsy(  const U_para<T>* t1_para, const U_para<U>* t2_para, UniTensor<To>& t3 ){


        uni10_int t1_bondnum = t1_para->nsy->bonds.size();
        uni10_int t2_bondnum = t2_para->nsy->bonds.size();

        // Get the stride of t1 and t2
        std::vector<long> size_t1(t1_bondnum);
        for(uni10_int i = 0; i < t1_bondnum; i++)
          size_t1[i] = t1_para->nsy->bonds[i].dim();

        std::vector<long> size_t2(t2_bondnum);
        for(uni10_int j = 0; j < t2_bondnum; j++)
          size_t2[j] = t2_para->nsy->bonds[j].dim();

        // Construct t3.
        std::vector<uni10_int> t2_mark(t2_bondnum, 0);
        std::vector<uni10_int> t3_labels;
        std::vector<Bond> t3_bonds;
        
        uni10_bool match;
        for(uni10_int a = 0; a < t1_bondnum; a++){
          match = false;
          for(uni10_int b = 0; b < t2_bondnum; b++){

            if(t1_para->nsy->labels[a] == t2_para->nsy->labels[b]){
              t2_mark[b] = 1;
              uni10_error_msg(!( size_t1[a] == size_t2[b] ), "%s", 
                  "Cannot Contract two bonds having different dimensions");
              match = true;
              break;
            }

          }
          if(!match){
            t3_labels.push_back(t1_para->nsy->labels[a]);
            t3_bonds.push_back(Bond(BD_IN, size_t1[a]));
          }
        }

        for(uni10_int b = 0; b < t2_bondnum; b++){
          if(t2_mark[b] == 0){
            t3_labels.push_back(t2_para->nsy->labels[b]);
            t3_bonds.push_back(Bond(BD_OUT, size_t2[b]));
          }
        }

        t3.Assign(t3_bonds);
        t3.SetLabel(t3_labels);
        t3.Zeros();

        uni10_int t3_bondnum = t3_bonds.size();
        U_para<To>* t3_para = t3.get_paras_enforce();

        std::vector<long> size_t3(t3_bondnum);
        for(uni10_int k = 0; k < t3_bondnum; k++)
          size_t3[k] = t3_para->nsy->bonds[k].dim();
        
        hirnk_linalg_unielem_internal::TensorContract(&t1_para->nsy->U_elem, &size_t1[0], &t1_para->nsy->labels[0], t1_bondnum,
            &t2_para->nsy->U_elem, &size_t2[0], &t2_para->nsy->labels[0], t2_bondnum,
            &t3_para->nsy->U_elem, &size_t3[0], &t3_para->nsy->labels[0], t3_bondnum);

        uni10_int crossbondnum = (t1_bondnum + t2_bondnum - t3_bondnum) / 2;

        return crossbondnum;

      }
  
  
    template <typename UniType>
      void addGate_nsy(U_para<UniType>* t1_para, const std::vector<_Swap>& swaps){

        return ;

      }

    template <typename UniType>
      void traceByRow_nsy(U_para<UniType>* Tout_para, const U_para<UniType>* Tin_para, uni10_int ia, uni10_int ib ){

        uni10_int bondNum = Tin_para->nsy->bonds.size();
        std::vector<uni10_int> Q_acc(bondNum, 1);
        for(uni10_int b = bondNum - 1; b > 0; b--)
          Q_acc[b - 1] = Q_acc[b] * Tin_para->nsy->bonds[b].const_getQnums().size();

        uni10_int tQdim = Tin_para->nsy->bonds[ia].const_getQnums().size();
        uni10_uint64 sB_rDim  = Tin_para->nsy->bonds[ia].dim();
        uni10_uint64 sB_rDim2 = sB_rDim * sB_rDim;
        uni10_error_msg(  !(tQdim == Tin_para->nsy->bonds[ib].const_getQnums().size()), "%s",  "The bonds of the given two labels does not match for trace.");

        Qnum q0(0, PRT_EVEN);
        for(uni10_int q = 0; q < tQdim; q++){
          uni10_error_msg(!((Tin_para->nsy->bonds[ia].const_getQnums()[q] * Tin_para->nsy->bonds[ib].const_getQnums()[q] == q0) 
                && (Tin_para->nsy->bonds[ia].const_getQdegs()[q] == Tin_para->nsy->bonds[ib].const_getQdegs()[q]))
              , "%s", "The bonds of the given two labels does not match for trace.");
        }

        typename std::map<Qnum, Block<UniType> >::iterator itIn  = Tin_para->nsy->blocks.begin();
        typename std::map<Qnum, Block<UniType> >::iterator itOut = Tout_para->nsy->blocks.begin();
       
        uni10_uint64 realElemNum = itOut->second.row() * itOut->second.col();
        for(; itIn != Tin_para->nsy->blocks.end(); itIn++){
          for(uni10_uint64 i = 0; i < realElemNum; i++){
            itOut->second.elem_enforce().elem_ptr_[i] = 0;
            for(uni10_uint64 sB_r = 0; sB_r < sB_rDim; sB_r++)
              itOut->second.elem_enforce().elem_ptr_[i] += itIn->second.elem_enforce().elem_ptr_[i*sB_rDim2+sB_r*sB_rDim+sB_r];
          }
        }

      }

    template <typename UniType>
      UniType tensorAt_nsy(U_para<UniType>* T_para, const uni10_uint64* idxs){

        uni10_int bondNum = T_para->nsy->bonds.size();
        std::vector<uni10_int> Qidxs(bondNum, 0);

        uni10_uint64 bondDim = 1;
        uni10_uint64 idx = 0;
        for(uni10_int b = bondNum-1; b >= 0; b--){
          uni10_error_msg(!(idxs[b] < (uni10_uint64)T_para->nsy->bonds[b].dim()), "%s", 
              "The input indices are out of range.");
          idx += bondDim * idxs[b];
          bondDim *= T_para->nsy->bonds[b].dim();

        }

        return T_para->nsy->U_elem[idx];

      }

  };

};

#endif
