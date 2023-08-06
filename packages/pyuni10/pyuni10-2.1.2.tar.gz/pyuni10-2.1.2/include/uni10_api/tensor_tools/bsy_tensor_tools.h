#ifndef __UNI10_BSY_TENSOR_TOOLS_H__
#define __UNI10_BSY_TENSOR_TOOLS_H__

#include <stdio.h>
#include <iostream>

#include <set>

#include "uni10_api/UniTensor.h"

namespace uni10{

  namespace tensor_tools{

    //Function prototype.
    template<typename UniType>
      U_para<UniType>* init_para_bsy(U_para<UniType>* para);

    template<typename UniType>
      void copy_para_bsy(U_para<UniType>* para, const U_para<UniType>* src_para);

    template<typename UniType>
      void free_para_bsy(U_para<UniType>* para);

    template<typename UniType>
      void init_bsy(U_para<UniType>* para);

    template<typename UniType>
      uni10_uint64 grouping_bsy(U_para<UniType>* _para);

    template <typename UniType>
      void initBlocks_bsy(U_para<UniType>* para);

    template <typename UniType>
      void setRawElem_bsy(U_para<UniType>* para, const UniType* rawElem);

    template <typename UniType>
      void putBlock_bsy(U_para<UniType>* para,const Qnum& qnum, const Block<UniType>& mat);

    template <typename UniType>
      void set_zero_bsy(U_para<UniType>* para);

    template <typename UniType>
      void randomize_bsy(U_para<UniType>* para);

    template <typename UniType>
      void transpose_bsy(U_para<UniType>* para, const U_para<UniType>* src_para);

    template <typename UniType>
      void dagger_bsy(U_para<UniType>* para, const U_para<UniType>* src_para);

    template <typename UniType>
      void conj_bsy(U_para<UniType>* para, const U_para<UniType>* src_para);

    template <typename UniType>
      void permute_bsy(const U_para<UniType>* t1_para, const std::vector<uni10_int>& rsp_idx,
          U_para<UniType>* t2_para, uni10_bool inorder);

    template <typename To, typename T, typename U>
      void contract_bsy( const U_para<T>* t1_para, const U_para<U>* t2_para, UniTensor<To>& t3 );

    template <typename UniType>
      void traceByRow_bsy(U_para<UniType>* Tout_para, const U_para<UniType>* Tin_para, uni10_int la, uni10_int lb );

    template <typename UniType>
      void addGate_bsy(U_para<UniType>* t1_para, const std::vector<_Swap>& swaps);

    template <typename UniType>
      UniType tensorAt_bsy(U_para<UniType>* T_para, const uni10_uint64* idxs);


    // Functions.
    template<typename UniType>
      U_para<UniType>* init_para_bsy(U_para<UniType>* para){

        U_para<UniType>* ptr;
        ptr      = new struct U_para<UniType>[1];
        ptr->bsy = new struct bs_sym_para<UniType>[1];
        ptr->check_status = 1;
        para = ptr;

        return para;

      }

    template<typename UniType>
      void copy_para_bsy(U_para<UniType>* para, const U_para<UniType>* src_para){

        uni10_error_msg(src_para->nsy != NULL, "%s", "Communication between nsy and bsy is developping!!");

        if(src_para!=NULL){
          *para->bsy = *src_para->bsy;
          typename std::map< Qnum, Block<UniType> >::const_iterator it2;
          typename std::map< const Block<UniType>* , Block<UniType>*> blkmap;
          typename std::map< Qnum, Block<UniType> >::iterator it = para->bsy->blocks.begin();
          for (; it != para->bsy->blocks.end(); it++ ){                       // blocks here is UniT.blocks
            it->second.elem_enforce().elem_ptr_ = &(para->bsy->U_elem.elem_ptr_[it->second.elem_enforce().elem_ptr_ - src_para->bsy->U_elem.elem_ptr_]);
            it2 = src_para->bsy->blocks.find(it->first);
            blkmap[&(it2->second)] = &(it->second);
          }

          if(src_para->bsy->status & UniTensor<UniType>::GET_HAVEBOND()){
            typename std::map<uni10_int, Block<UniType>*>::iterator it = para->bsy->RQidx2Blk.begin();
            for(; it != para->bsy->RQidx2Blk.end(); it++)
              it->second = blkmap[it->second];
          }

        }

      }

    template<typename UniType>
      void free_para_bsy(U_para<UniType>* para){

        if(para != NULL){
          delete [] para->bsy;
          delete [] para;
        }

      }

    template<typename UniType>
      void init_bsy(U_para<UniType>* para){

        if(para->bsy->bonds.size()){
          para->bsy->U_elemNum = grouping_bsy(para);
          if(!(para->bsy->blocks.size() > 0)){      //No block in Tensor, Error!
            uni10_error_msg(true, "%s", "There is no symmetry block with the given bonds:");
            for(uni10_int b = 0; b < (uni10_int)para->bsy->bonds.size(); b++)
              std::cout<<"   "<<para->bsy->bonds[b];
          }

          para->bsy->labels.assign(para->bsy->bonds.size(), 0);
          for(uni10_int b = 0; b < (uni10_int)para->bsy->bonds.size(); b++)
            para->bsy->labels[b] = b;

        }
        else{
          Qnum q0(0);
          para->bsy->blocks[q0] = Block<UniType>(1, 1);
          para->bsy->RBondNum = 0;
          para->bsy->RQdim = 0;
          para->bsy->CQdim = 0;
          para->bsy->U_elemNum = 1;
        }

        para->bsy->U_elem.Init(1, para->bsy->U_elemNum, false);
        initBlocks_bsy(para);

      }

    template<typename UniType>
      uni10_uint64 grouping_bsy(U_para<UniType>* para){

        //std::cout << "- ININININ" << std::endl;

        para->bsy->blocks.clear();
        uni10_int row_bondNum = 0;
        uni10_int col_bondNum = 0;
        para->bsy->RQdim = 1;
        para->bsy->CQdim = 1;
        uni10_bool IN_BONDS_BEFORE_OUT_BONDS = true;

        for(uni10_uint64 i = 0; i < para->bsy->bonds.size(); i++){

          if(para->bsy->bonds[i].type() == BD_IN){
            uni10_error_msg(!(IN_BONDS_BEFORE_OUT_BONDS == true),
                "%s","Error in the input bond array: BD_OUT bonds must be placed after all BD_IN bonds.");

            para->bsy->RQdim *= para->bsy->bonds[i].const_getQnums().size();
            row_bondNum++;
          }
          else{
            para->bsy->CQdim *=  para->bsy->bonds[i].const_getQnums().size();
            col_bondNum++;
            IN_BONDS_BEFORE_OUT_BONDS = false;
          }
        }
        para->bsy->RBondNum = row_bondNum;

        std::map<Qnum,uni10_uint64> row_QnumMdim;
        std::vector<uni10_int> row_offs(row_bondNum, 0);
        std::map<Qnum,std::vector<uni10_int> > row_Qnum2Qidx;
        Qnum qnum;

        uni10_uint64 dim;
        uni10_int boff = 0;

        std::vector<uni10_uint64>tmpRQidx2Dim(para->bsy->RQdim, 1);
        std::vector<uni10_uint64>tmpCQidx2Dim(para->bsy->CQdim, 1);
        std::vector<uni10_uint64>tmpRQidx2Off(para->bsy->RQdim, 0);
        std::vector<uni10_uint64>tmpCQidx2Off(para->bsy->CQdim, 0);

        if(row_bondNum){
          while(1){
            qnum.assign();
            dim = 1;
            for(uni10_int b = 0; b < row_bondNum; b++){
              qnum = qnum * para->bsy->bonds[b].const_getQnums()[row_offs[b]];
              dim *= para->bsy->bonds[b].const_getQdegs()[row_offs[b]];
            }
            if(row_QnumMdim.find(qnum) != row_QnumMdim.end()){
              tmpRQidx2Off[boff] = row_QnumMdim[qnum];
              tmpRQidx2Dim[boff] = dim;
              row_QnumMdim[qnum] += dim;
            }
            else{
              tmpRQidx2Off[boff] = 0;
              tmpRQidx2Dim[boff] = dim;
              row_QnumMdim[qnum] = dim;
            }
            row_Qnum2Qidx[qnum].push_back(boff);
            boff++;
            uni10_int bidx;
            for(bidx = row_bondNum - 1; bidx >= 0; bidx--){
              row_offs[bidx]++;
              if(row_offs[bidx] < para->bsy->bonds[bidx].const_getQnums().size())
                break;
              else
                row_offs[bidx] = 0;
            }
            if(bidx < 0)  //run over all row_bond offsets
              break;
          }
        }
        else{
          qnum.assign();
          row_QnumMdim[qnum] = 1;
          row_Qnum2Qidx[qnum].push_back(0);
        }


        std::map<Qnum,uni10_uint64> col_QnumMdim;
        std::vector<uni10_int> col_offs(col_bondNum, 0);
        std::map<Qnum,std::vector<uni10_int> > col_Qnum2Qidx;
        boff = 0;
        if(col_bondNum){
          while(1){
            qnum.assign();
            dim = 1;
            for(uni10_int b = 0; b < col_bondNum; b++){
              qnum = qnum * para->bsy->bonds[b + row_bondNum].const_getQnums()[col_offs[b]];
              dim *= para->bsy->bonds[b + row_bondNum].const_getQdegs()[col_offs[b]];
            }
            if(row_QnumMdim.find(qnum) != row_QnumMdim.end()){
              if(col_QnumMdim.find(qnum) != col_QnumMdim.end()){
                tmpCQidx2Off[boff] = col_QnumMdim[qnum];
                tmpCQidx2Dim[boff] = dim;
                col_QnumMdim[qnum] += dim;
              }
              else{
                tmpCQidx2Off[boff] = 0;
                tmpCQidx2Dim[boff] = dim; col_QnumMdim[qnum] = dim; } col_Qnum2Qidx[qnum].push_back(boff); }
            boff++;
            uni10_int bidx;
            for(bidx = col_bondNum - 1; bidx >= 0; bidx--){
              col_offs[bidx]++;
              if(col_offs[bidx] < para->bsy->bonds[bidx + row_bondNum].const_getQnums().size())
                break;
              else
                col_offs[bidx] = 0;
            }
            if(bidx < 0)  //run over all row_bond offsets
              break;
          }
        }
        else{
          qnum.assign();
          if(row_QnumMdim.find(qnum) != row_QnumMdim.end()){
            col_QnumMdim[qnum] = 1;
            col_Qnum2Qidx[qnum].push_back(0);
          }
        }

        //std::cout << "row qnumdim : " << row_QnumMdim.size() << std::endl;
        //std::map<Qnum,uni10_uint64>::iterator ittmp;
        //for(ittmp = row_QnumMdim.begin(); ittmp != row_QnumMdim.end(); ittmp++)
        //  std::cout << ittmp->first << std::endl;
        //exit(0);

        std::map<Qnum,uni10_uint64>::iterator it;
        std::map<Qnum,uni10_uint64>::iterator it2;
        std::set<uni10_int> Qidx;
        uni10_int qidx;
        uni10_uint64 off = 0;
        for ( it2 = col_QnumMdim.begin() ; it2 != col_QnumMdim.end(); it2++ ){
          it = row_QnumMdim.find(it2->first);
          Block<UniType> blk(it->second, it2->second); // blk(Rnum, Cnum);
          off += blk.row() * blk.col();
          para->bsy->blocks[it->first] = blk;
          Block<UniType>* blkptr = &(para->bsy->blocks[it->first]);
          std::vector<uni10_int>& tmpRQidx = row_Qnum2Qidx[it->first];
          std::vector<uni10_int>& tmpCQidx = col_Qnum2Qidx[it->first];
          for(uni10_uint64 i = 0; i < tmpRQidx.size(); i++){
            para->bsy->RQidx2Blk[tmpRQidx[i]] = blkptr;
            for(uni10_uint64 j = 0; j < tmpCQidx.size(); j++){
              para->bsy->RQidx2Dim[tmpRQidx[i]] = tmpRQidx2Dim[tmpRQidx[i]];
              para->bsy->RQidx2Off[tmpRQidx[i]] = tmpRQidx2Off[tmpRQidx[i]];
              para->bsy->CQidx2Dim[tmpCQidx[j]] = tmpCQidx2Dim[tmpCQidx[j]];
              para->bsy->CQidx2Off[tmpCQidx[j]] = tmpCQidx2Off[tmpCQidx[j]];
              qidx = tmpRQidx[i] * para->bsy->CQdim + tmpCQidx[j];
              Qidx.insert(qidx);
            }
          }
        }
        uni10_uint64 elemEnc = 0;
        for(std::map<uni10_int, uni10_uint64>::iterator itr = para->bsy->RQidx2Dim.begin(); itr != para->bsy->RQidx2Dim.end(); itr++)
          for(std::map<uni10_int, uni10_uint64>::iterator itc = para->bsy->CQidx2Dim.begin(); itc != para->bsy->CQidx2Dim.end(); itc++){
            qidx = itr->first * para->bsy->CQdim + itc->first;
            if(Qidx.find(qidx) != Qidx.end()){
              para->bsy->QidxEnc[qidx] = elemEnc;
              elemEnc += para->bsy->RQidx2Dim[itr->first] * para->bsy->CQidx2Dim[itc->first];
            }
          }
        return off;

      }

    template <typename UniType>
      void initBlocks_bsy(U_para<UniType>* para){

        uni10_uint64 offset = 0;
        typename std::map< Qnum, Block<UniType> >::iterator it = para->bsy->blocks.begin();
        for(; it != para->bsy->blocks.end(); it++ ){
          it->second.elem_enforce().elem_ptr_ = &(para->bsy->U_elem.elem_ptr_[offset]);
          offset += it->second.row_enforce() * it->second.col_enforce();
        }

      }

    template <typename UniType>
      void putBlock_bsy(U_para<UniType>* para,const Qnum& qnum, const Block<UniType>& mat){

        typename std::map<Qnum, Block<UniType> >::iterator it;

        if(!((it = para->bsy->blocks.find(qnum)) != para->bsy->blocks.end())){
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

        para->bsy->status |= UniTensor<UniType>::GET_HAVEELEM();

      }

    template <typename UniType>
      void set_zero_bsy(U_para<UniType>* para){

        para->bsy->U_elem.SetZeros();

      }

    template <typename UniType>
      void randomize_bsy(U_para<UniType>* para){

        para = NULL;
        uni10_error_msg(true, "%s", "Developping");

      }

    template <typename UniType>
      void setRawElem_bsy(U_para<UniType>* para, const UniType* rawElem){

        uni10_error_msg((para->bsy->status & UniTensor<UniType>::GET_HAVEBOND()) == 0,
            "%s", "Setting elements to a tensor without bonds is not supported." );

        uni10_int bondNum = para->bsy->bonds.size();
        std::vector<uni10_int> Q_idxs(bondNum, 0);
        std::vector<uni10_int> Q_Bdims(bondNum, 0);
        std::vector<uni10_int> sB_idxs(bondNum, 0);
        std::vector<uni10_int> sB_sBdims(bondNum, 0);
        std::vector<uni10_int> rAcc(bondNum, 1);
        for(uni10_int b = 0; b < bondNum; b++)
          Q_Bdims[b] = para->bsy->bonds[b].const_getQnums().size();
        for(uni10_int b = bondNum - 1; b > 0; b--)
          rAcc[b - 1] = rAcc[b] * para->bsy->bonds[b].dim();
        uni10_int Q_off;
        uni10_int tmp;
        uni10_int RQoff, CQoff;
        uni10_uint64 sB_r, sB_c;        //sub-block of a Qidx
        uni10_uint64 sB_rDim, sB_cDim;  //sub-block of a Qidx
        uni10_uint64 B_cDim;
        uni10_uint64 E_off;
        uni10_int R_off;
        UniType* work = para->bsy->U_elem.elem_ptr_;

        for(std::map<uni10_int, uni10_uint64>::iterator it = para->bsy->QidxEnc.begin(); it != para->bsy->QidxEnc.end(); it++){
          Q_off = it->first;
          tmp = Q_off;
          for(uni10_int b = bondNum - 1; b >= 0; b--){
            Q_idxs[b] = tmp % Q_Bdims[b];
            tmp /= Q_Bdims[b];
          }
          R_off = 0;
          for(uni10_int b = 0; b < bondNum; b++){
            R_off += rAcc[b] * para->bsy->bonds[b].const_getOffsets()[Q_idxs[b]];
            sB_sBdims[b] = para->bsy->bonds[b].const_getQdegs()[Q_idxs[b]];
          }
          RQoff = Q_off / para->bsy->CQdim;
          CQoff = Q_off % para->bsy->CQdim;
          B_cDim = para->bsy->RQidx2Blk[RQoff]->col();

          E_off = (para->bsy->RQidx2Blk[RQoff]->elem_enforce().elem_ptr_ - para->bsy->U_elem.elem_ptr_) + (para->bsy->RQidx2Off[RQoff] * B_cDim) + para->bsy->CQidx2Off[CQoff];

          sB_rDim = para->bsy->RQidx2Dim[RQoff];
          sB_cDim = para->bsy->CQidx2Dim[CQoff];
          sB_idxs.assign(bondNum, 0);
          for(sB_r = 0; sB_r < sB_rDim; sB_r++)
            for(sB_c = 0; sB_c < sB_cDim; sB_c++){
              work[E_off + (sB_r * B_cDim) + sB_c] = rawElem[R_off];
              for(uni10_int bend = bondNum - 1; bend >= 0; bend--){
                sB_idxs[bend]++;
                if(sB_idxs[bend] < sB_sBdims[bend]){
                  R_off += rAcc[bend];
                  break;
                }
                else{
                  R_off -= rAcc[bend] * (sB_idxs[bend] - 1);
                  sB_idxs[bend] = 0;
                }
              }
            }
        }

        para->bsy->status |= UniTensor<UniType>::GET_HAVEELEM();

      }

    template <typename UniType>
      void transpose_bsy(U_para<UniType>* para, const U_para<UniType>* src_para){

        typename std::map<Qnum, Block<UniType> >::iterator it_in;
        typename std::map<Qnum, Block<UniType> >::iterator it_out;
        UELEM(UniElem, _package, _type)<UniType>* elem_in;
        UELEM(UniElem, _package, _type)<UniType>* elem_out;
        uni10_uint64 Rnum, Cnum;
        for ( it_in = src_para->bsy->blocks.begin() ; it_in != src_para->bsy->blocks.end(); it_in++ ){
          it_out = para->bsy->blocks.find((it_in->first));
          Rnum = it_in->second.row_enforce();
          Cnum = it_in->second.col_enforce();
          elem_in  = &(it_in->second.elem_enforce());
          elem_out = &(it_out->second.elem_enforce());
          linalg_unielem_internal::Transpose(elem_in, &Rnum, &Cnum, elem_out);
        }

      }


    template <typename UniType>
      void dagger_bsy(U_para<UniType>* para, const U_para<UniType>* src_para){

        typename std::map<Qnum, Block<UniType> >::iterator it_in;
        typename std::map<Qnum, Block<UniType> >::iterator it_out;
        UELEM(UniElem, _package, _type)<UniType>* elem_in;
        UELEM(UniElem, _package, _type)<UniType>* elem_out;
        uni10_uint64 Rnum, Cnum;
        for ( it_in = src_para->bsy->blocks.begin() ; it_in != src_para->bsy->blocks.end(); it_in++ ){
          it_out = para->bsy->blocks.find((it_in->first));
          Rnum = it_in->second.row_enforce();
          Cnum = it_in->second.col_enforce();
          elem_in  = &(it_in->second.elem_enforce());
          elem_out = &(it_out->second.elem_enforce());
          linalg_unielem_internal::Dagger(elem_in, &Rnum, &Cnum, elem_out);
        }

      }

    template <typename UniType>
      void conj_bsy(U_para<UniType>* para, const U_para<UniType>* src_para){

        linalg_unielem_internal::Conjugate(&src_para->bsy->U_elem, &src_para->bsy->U_elemNum, &para->bsy->U_elem);

      }

    // 1. The function is disigned for fiiting the latest API desinged for plunging higher-rank linear algbra packages, 
    // such as TCL, HPTT, TBLIS, etc...
    // 2. The orignal design is label dependent function but at the interface the function is changed to index dependent.
    // 3. rsp_idx records the mapping of original indices and new labels.
    // For example, if the gaol of permutation is [5,4,3]->[3,5,4], the rsp_idx = [2,0,1]
    // 4. Notice that besides permute_bsy() is index dependent function, all the functions in the scoope is label dependent, 
    // such as recSwap(), etc...

    template <typename UniType>
      void permute_bsy(const U_para<UniType>* t1_para, const std::vector<uni10_int>& rsp_idx,
          U_para<UniType>* t2_para, uni10_bool inorder){

        uni10_uint64 bondNum = t1_para->bsy->bonds.size();
        uni10_double64 sign = 1.0;
        //For Fermionic system
        std::vector<_Swap> swaps;

        //End Fermionic system
        std::vector<uni10_int> Qin_idxs(bondNum, 0);
        std::vector<uni10_int> Qot_idxs(bondNum, 0);
        uni10_int Qin_off, Qot_off;
        uni10_int tmp;
        uni10_int Qin_RQoff, Qin_CQoff;
        uni10_int Qot_CQoff, Qot_RQoff;
        uni10_uint64 sBin_r, sBin_c;	//sub-block of a Qidx
        uni10_uint64 sBin_rDim, sBin_cDim;	//sub-block of a Qidx
        uni10_uint64 sBot_cDim;	//sub-block of a Qidx
        uni10_uint64 sBot_r, sBot_c;
        uni10_uint64 Bin_cDim, Bot_cDim;
        UniType* Ein_ptr;
        UniType* Eot_ptr;
        std::vector<uni10_int> sBin_idxs(bondNum, 0);
        std::vector<uni10_int> sBin_sBdims(bondNum, 0);
        std::vector<uni10_int> Qot_acc(bondNum, 1);
        std::vector<uni10_int> sBot_acc(bondNum, 1);
        for(uni10_int b = bondNum	- 1; b > 0; b--)
          Qot_acc[b - 1] = Qot_acc[b] * t2_para->bsy->bonds[b].const_getQnums().size();

        for(std::map<uni10_int, uni10_uint64>::iterator it = t1_para->bsy->QidxEnc.begin(); it != t1_para->bsy->QidxEnc.end(); it++){
          Qin_off = it->first;
          tmp = Qin_off;
          uni10_int qdim;
          for(uni10_int b = bondNum - 1; b >= 0; b--){
            qdim = t1_para->bsy->bonds[b].const_getQnums().size();
            Qin_idxs[b] = tmp % qdim;
            sBin_sBdims[b] = t1_para->bsy->bonds[b].const_getQdegs()[Qin_idxs[b]];
            tmp /= qdim;
          }
          Qot_off = 0;
          for(uni10_uint64 b = 0; b < bondNum; b++){
            Qot_idxs[b] = Qin_idxs[rsp_idx[b]];
            Qot_off += Qot_idxs[b] * Qot_acc[b];
          }
          for(uni10_uint64 b = bondNum - 1; b > 0; b--)
            sBot_acc[rsp_idx[b-1]] = sBot_acc[rsp_idx[b]] * t1_para->bsy->bonds[rsp_idx[b]].const_getQdegs()[Qot_idxs[b]];

          Qin_RQoff = Qin_off / t1_para->bsy->CQdim;
          Qin_CQoff = Qin_off % t1_para->bsy->CQdim;
          Qot_RQoff = Qot_off / t2_para->bsy->CQdim;
          Qot_CQoff = Qot_off % t2_para->bsy->CQdim;
          Bin_cDim = t1_para->bsy->RQidx2Blk[Qin_RQoff]->col();
          Bot_cDim = t2_para->bsy->RQidx2Blk[Qot_RQoff]->col();
          Ein_ptr = t1_para->bsy->RQidx2Blk[Qin_RQoff]->GetElem() + (t1_para->bsy->RQidx2Off[Qin_RQoff] * Bin_cDim) + t1_para->bsy->CQidx2Off[Qin_CQoff];
          Eot_ptr = t2_para->bsy->RQidx2Blk[Qot_RQoff]->GetElem() + (t2_para->bsy->RQidx2Off[Qot_RQoff] * Bot_cDim) + t2_para->bsy->CQidx2Off[Qot_CQoff];
          sBin_rDim = t1_para->bsy->RQidx2Dim[Qin_RQoff];
          sBin_cDim = t1_para->bsy->CQidx2Dim[Qin_CQoff];
          sBot_cDim = t2_para->bsy->CQidx2Dim[Qot_CQoff];
          uni10_int cnt_ot = 0;
          sBin_idxs.assign(bondNum, 0);

          for(sBin_r = 0; sBin_r < sBin_rDim; sBin_r++)
            for(sBin_c = 0; sBin_c < sBin_cDim; sBin_c++){
              sBot_r = cnt_ot / sBot_cDim;
              sBot_c = cnt_ot % sBot_cDim;
              Eot_ptr[(sBot_r * Bot_cDim) + sBot_c] = sign * Ein_ptr[(sBin_r * Bin_cDim) + sBin_c];
              for(uni10_int bend = bondNum - 1; bend >= 0; bend--){
                sBin_idxs[bend]++;
                if(sBin_idxs[bend] < sBin_sBdims[bend]){
                  cnt_ot += sBot_acc[bend];
                  break;
                }
                else{
                  cnt_ot -= sBot_acc[bend] * (sBin_idxs[bend] - 1);
                  sBin_idxs[bend] = 0;
                }
              }
            }
        }

      }

    template <typename To, typename T, typename U>
      uni10_int contract_bsy( const U_para<T>* t1_para, const U_para<U>* t2_para, UniTensor<To>& t3 ){
        
        uni10_int t1_bondnum = t1_para->bsy->bonds.size();
        uni10_int t2_bondnum = t2_para->bsy->bonds.size();
        
        std::vector<uni10_int> t1_orilabels = (t1_para->bsy->labels);
        std::vector<uni10_int> t2_orilabels = (t2_para->bsy->labels);

        uni10_int t1_ori_ibdnum = (t1_para->bsy->RBondNum);
        uni10_int t2_ori_ibdnum = (t2_para->bsy->RBondNum);
        uni10_int t3_ibdnum = 0, t3_obdnum = 0;

        std::vector<uni10_int> t1_rspidx, t2_rspidx;
        std::vector<uni10_int> t1_rsplabel, t2_rsplabel;
        std::vector<Bond> t1_rspbonds, t2_rspbonds;

        std::vector<uni10_int> t1_interbdidx;

        std::vector<uni10_int> t2_mark(t2_bondnum, 0);
        std::vector<uni10_int> t3_newlabel;

        uni10_bool match;
        for(uni10_int a = 0; a < t1_bondnum; a++){
          match = false;
          for(uni10_int b = 0; b < t2_bondnum; b++)
            if(t1_orilabels[a] == t2_orilabels[b]){
              t2_mark[b] = 1;
              t1_interbdidx.push_back(a);
              t2_rspidx.push_back(b);
              t2_rsplabel.push_back(t2_orilabels[b]);
              uni10_error_msg(!( t1_para->bsy->bonds[a].dim() == t2_para->bsy->bonds[b].dim() ), "%s",
                  "Cannot Contract two bonds having different dimensions");
              match = true;
              break;
            }
          if(!match){
            t1_rspidx.push_back(a);
            t1_rsplabel.push_back(t1_orilabels[a]);
            t3_newlabel.push_back(t1_orilabels[a]);
            t3_ibdnum++;
          }
        }

        uni10_int crossbondnum = t1_interbdidx.size();

        for(uni10_int a = 0; a < (uni10_int)crossbondnum; a++){
          t1_rspidx.push_back(t1_interbdidx[a]);
          t1_rsplabel.push_back(t1_orilabels[t1_interbdidx[a]]);
        }

        for(uni10_int b = 0; b < t2_bondnum; b++)
          if(t2_mark[b] == 0){
            t2_rspidx.push_back(b);
            t2_rsplabel.push_back(t2_orilabels[b]);
            t3_newlabel.push_back(t2_orilabels[b]);
            t3_obdnum++;
          }

        bool t1_inorder=true, t2_inorder=true;

        for(uni10_int i = 0; i < (uni10_int)t1_rspidx.size(); i++)
          if(t1_rspidx[i] != i){
            t1_inorder=false;
            break;
          }

        for(uni10_int j = 0; j < (uni10_int)t2_rspidx.size(); j++)
          if(t2_rspidx[j] != j){
            t2_inorder=false;
            break;
          }

        bool t1_transpose = !(t1_inorder && t1_ori_ibdnum == t3_ibdnum);
        bool t2_transpose = !(t2_inorder && t2_ori_ibdnum == (uni10_int)crossbondnum);

        if(t1_transpose) {

          for(uni10_int a = 0; a < (uni10_int)t1_bondnum; a++){
            t1_rspbonds.push_back(t1_para->bsy->bonds[t1_rspidx[a]]);
          }
          for(uni10_int a = 0; a < (uni10_int)t1_bondnum; a++){
            if(a < t3_ibdnum)
              t1_rspbonds[a].change(BD_IN);
            else
              t1_rspbonds[a].change(BD_OUT);
          }

        }else{
          t1_rspbonds = t1_para->bsy->bonds;
        }

        if(t2_transpose) {

          for(uni10_int b = 0; b < (uni10_int)t2_bondnum; b++){
            t2_rspbonds.push_back(t2_para->bsy->bonds[t2_rspidx[b]]);
          }
          for(uni10_int b = 0; b < (uni10_int)t2_bondnum; b++){
            if(b < (uni10_int)crossbondnum)
              t2_rspbonds[b].change(BD_IN);
            else
              t2_rspbonds[b].change(BD_OUT);
          }

        }else{
          t2_rspbonds = t2_para->bsy->bonds;
        }

        UniTensor<T> pt1(t1_rspbonds, t1_rsplabel);
        UniTensor<U> pt2(t2_rspbonds, t2_rsplabel);

        U_para<T>* pt1_para = pt1.get_paras_enforce();
        U_para<U>* pt2_para = pt2.get_paras_enforce();

        permute_bsy(t1_para, t1_rspidx, pt1_para, t1_inorder);
        permute_bsy(t2_para, t2_rspidx, pt2_para, t2_inorder);

        std::vector<Bond> t3_bonds;

        for(uni10_int i = 0; i < t3_ibdnum; i++)
          t3_bonds.push_back(t1_rspbonds[i]);

        for(uni10_int i = crossbondnum; i < t2_bondnum; i++){
          t3_bonds.push_back(t2_rspbonds[i]);
        }

        if(t3_bonds.size() != 0){
          t3.Assign(t3_bonds);
          if(t3_newlabel.size())
            t3.SetLabel(t3_newlabel);
          t3.Zeros();
        }
        else
          t3 = UniTensor<To>(0, bs_sym);

        U_para<To>* t3_para = t3.get_paras_enforce();

        Block<T> pt1_block;
        Block<U> pt2_block;
        Block<To> t3_block;

        typename std::map<Qnum, Block<T> >::iterator it;
        typename std::map<Qnum, Block<U> >::iterator it2;

        for(it = pt1_para->bsy->blocks.begin() ; it != pt1_para->bsy->blocks.end(); it++){

          if((it2 = pt2_para->bsy->blocks.find(it->first)) != pt2_para->bsy->blocks.end()){

            pt1_block = it->second;
            pt2_block = it2->second;
            t3_block = t3_para->bsy->blocks[it->first];
            uni10_error_msg(!(pt1_block.row() == t3_block.row() && pt2_block.col() == t3_block.col() && pt1_block.col() == pt2_block.row()),
                "%s", "The dimensions the bonds to be Contracted out are different.");

            linalg_unielem_internal::Dot(&pt1_block.elem_enforce(), &pt1_block.diag_enforce(), &pt2_block.elem_enforce(), &pt2_block.diag_enforce(),
                &pt1_block.row_enforce(), &pt2_block.col_enforce(), &pt1_block.col_enforce(), &t3_block.elem_enforce());
          }

        }

        return crossbondnum;

      }

    template <typename UniType>
      void addGate_bsy(U_para<UniType>* t1_para, const std::vector<_Swap>& swaps){

        uni10_error_msg((t1_para->bsy->status & UniTensor<UniType>::GET_HAVEBOND()) == 0, "%s",\
            "Adding swap gates to a tensor without bonds(scalar).");

        uni10_error_msg((t1_para->bsy->status & UniTensor<UniType>::GET_HAVEELEM()) == 0, "%s",\
            "Cannot add swap gates to a tensor before setting its elements.");

        uni10_int sign = 1;
        uni10_int bondNum = t1_para->bsy->bonds.size();
        std::vector<uni10_int> Q_idxs(bondNum, 0);
        std::vector<uni10_int> Q_Bdims(bondNum, 0);
        for(uni10_int b = 0; b < bondNum; b++)
          Q_Bdims[b] = t1_para->bsy->bonds[b].const_getQnums().size();
        uni10_int Q_off;
        uni10_int tmp;
        uni10_int RQoff, CQoff;
        uni10_uint64 sB_r, sB_c;  //sub-block of a Qidx
        uni10_uint64 sB_rDim, sB_cDim;  //sub-block of a Qidx
        uni10_uint64 B_cDim;
        UniType* Eptr;

        for(std::map<uni10_int, uni10_uint64>::iterator it = t1_para->bsy->QidxEnc.begin(); it != t1_para->bsy->QidxEnc.end(); it++){
          Q_off = it->first;
          tmp = Q_off;
          for(uni10_int b = bondNum - 1; b >= 0; b--){
            Q_idxs[b] = tmp % Q_Bdims[b];
            tmp /= Q_Bdims[b];
          }
          RQoff = Q_off / t1_para->bsy->CQdim;
          CQoff = Q_off % t1_para->bsy->CQdim;
          B_cDim = t1_para->bsy->RQidx2Blk[RQoff]->row_enforce();
          Eptr = t1_para->bsy->RQidx2Blk[RQoff]->elem_enforce().elem_ptr_ + (t1_para->bsy->RQidx2Off[RQoff] * B_cDim) + t1_para->bsy->CQidx2Off[CQoff];
          sB_rDim = t1_para->bsy->RQidx2Dim[RQoff];
          sB_cDim = t1_para->bsy->CQidx2Dim[CQoff];

          uni10_int sign01 = 0;
          for(uni10_int i = 0; i < (uni10_int)swaps.size(); i++)
            sign01 ^= (t1_para->bsy->bonds[swaps[i].b1].const_getQnums()[Q_idxs[swaps[i].b1]].prtF() \
                & t1_para->bsy->bonds[swaps[i].b2].const_getQnums()[Q_idxs[swaps[i].b2]].prtF());
          sign = sign01 ? -1 : 1;

          for(sB_r = 0; sB_r < sB_rDim; sB_r++)
            for(sB_c = 0; sB_c < sB_cDim; sB_c++)
              Eptr[(sB_r * B_cDim) + sB_c] *= sign;
        }

      }

    template <typename UniType>
      void traceByRow_bsy(U_para<UniType>* Tout_para, const U_para<UniType>* Tin_para, uni10_int ia, uni10_int ib ){

        uni10_int bondNum = Tin_para->bsy->bonds.size();
        std::vector<uni10_int> Q_acc(bondNum, 1);
        for(uni10_int b = bondNum - 1; b > 0; b--)
          Q_acc[b - 1] = Q_acc[b] * Tin_para->bsy->bonds[b].const_getQnums().size();

        uni10_int tQdim = Tin_para->bsy->bonds[ia].const_getQnums().size();
        uni10_error_msg(  !(tQdim == Tin_para->bsy->bonds[ib].const_getQnums().size()), "%s",  "The bonds of the given two labels does not match for trace.");

        Qnum q0(0, PRT_EVEN);
        for(uni10_int q = 0; q < tQdim; q++){
          uni10_error_msg(!((Tin_para->bsy->bonds[ia].const_getQnums()[q] * Tin_para->bsy->bonds[ib].const_getQnums()[q] == q0)
                && (Tin_para->bsy->bonds[ia].const_getQdegs()[q] == Tin_para->bsy->bonds[ib].const_getQdegs()[q]))
              , "%s", "The bonds of the given two labels does not match for trace.");
        }

        uni10_int tBnum = Tout_para->bsy->bonds.size();
        std::vector<uni10_int> Qt_Bdims(tBnum, 0);
        for(uni10_int b = 0; b < tBnum; b++)
          Qt_Bdims[b] = Tout_para->bsy->bonds[b].const_getQnums().size();

        uni10_int Qt_off;
        uni10_int Q_off;
        uni10_int Qt_RQoff, Qt_CQoff;
        uni10_int Q_RQoff, Q_CQoff;
        uni10_uint64 sBt_rDim, sBt_cDim;  //sub-block of a Qidx of Tt
        uni10_uint64 Bt_cDim;
        UniType* Et_ptr;

        std::vector<UniType*> E_offs(tQdim);
        std::vector<uni10_uint64> B_cDims(tQdim);
        uni10_int tQdim2 = tQdim * tQdim;
        uni10_int Qenc = Q_acc[ia] + Q_acc[ib];

        typename std::map<uni10_int, uni10_uint64>::iterator it = Tout_para->bsy->QidxEnc.begin();

        for(; it != Tout_para->bsy->QidxEnc.end(); it++){

          Qt_off = it->first;
          Qt_RQoff = Qt_off / Tout_para->bsy->CQdim;
          Qt_CQoff = Qt_off % Tout_para->bsy->CQdim;
          Bt_cDim = Tout_para->bsy->RQidx2Blk[Qt_RQoff]->col_enforce();
          Et_ptr = Tout_para->bsy->RQidx2Blk[Qt_RQoff]->elem_enforce().elem_ptr_ + (Tout_para->bsy->RQidx2Off[Qt_RQoff] * Bt_cDim) + Tout_para->bsy->CQidx2Off[Qt_CQoff];
          sBt_rDim = Tout_para->bsy->RQidx2Dim[Qt_RQoff];
          sBt_cDim = Tout_para->bsy->CQidx2Dim[Qt_CQoff];

          for(uni10_int q = 0; q < tQdim; q++){
            Q_off = Qt_off * tQdim2 + q * Qenc;
            Q_RQoff = Q_off / Tin_para->bsy->CQdim;
            Q_CQoff = Q_off % Tin_para->bsy->CQdim;
            B_cDims[q] = Tin_para->bsy->RQidx2Blk[Q_RQoff]->col_enforce();
            E_offs[q] = Tin_para->bsy->RQidx2Blk[Q_RQoff]->elem_enforce().elem_ptr_ + (Tin_para->bsy->RQidx2Off[Q_RQoff] * B_cDims[q]) + Tin_para->bsy->CQidx2Off[Q_CQoff];
          }
          uni10_int tQdeg, sB_c_off;
          UniType trVal;
          for(uni10_uint64 sB_r = 0; sB_r < sBt_rDim; sB_r++)
            for(uni10_uint64 sB_c = 0; sB_c < sBt_cDim; sB_c++){
              trVal = 0;
              for(uni10_int q = 0; q < tQdim; q++){
                tQdeg = Tin_para->bsy->bonds[ia].const_getQdegs()[q];
                sB_c_off = sB_c * (tQdeg * tQdeg);
                for(uni10_int t = 0; t < tQdeg; t++){
                  trVal += E_offs[q][(sB_r * B_cDims[q]) + sB_c_off + t * (tQdeg + 1)];
                }
              }
              Et_ptr[sB_r * Bt_cDim + sB_c] = trVal;
            }
        }

      }

    template <typename UniType>
      UniType tensorAt_bsy(U_para<UniType>* T_para, const uni10_uint64* idxs){

        uni10_int bondNum = T_para->bsy->bonds.size();
        std::vector<uni10_int> Qidxs(bondNum, 0);
        for(uni10_int b = 0; b < bondNum; b++){
          uni10_error_msg(!(idxs[b] < (uni10_uint64)T_para->bsy->bonds[b].dim()), "%s",
              "The input indices are out of range.");
          for(uni10_int q = T_para->bsy->bonds[b].const_getOffsets().size() - 1; q >= 0; q--){
            if(idxs[b] < (T_para->bsy->bonds)[b].const_getOffsets()[q])
              continue;
            Qidxs[b] = q;
            break;
          }
        }

        std::vector<uni10_int> Q_acc(bondNum, 1);
        for(uni10_int b = bondNum	- 1; b > 0; b--)
          Q_acc[b - 1] = Q_acc[b] * (T_para->bsy->bonds)[b].const_getQnums().size();
        uni10_int Qoff = 0;
        for(uni10_int b = 0; b < bondNum; b++)
          Qoff += Q_acc[b] * Qidxs[b];

        if(T_para->bsy->QidxEnc.find(Qoff) != T_para->bsy->QidxEnc.end()){
          uni10_int Q_RQoff = Qoff / T_para->bsy->CQdim;
          uni10_int Q_CQoff = Qoff % T_para->bsy->CQdim;
          Block<UniType>* blk = T_para->bsy->RQidx2Blk.find(Q_RQoff)->second;
          uni10_uint64 B_cDim = blk->col_enforce();
          uni10_uint64 sB_cDim = T_para->bsy->CQidx2Dim.find(Q_CQoff)->second;
          uni10_uint64 blkRoff = T_para->bsy->RQidx2Off.find(Q_RQoff)->second;
          uni10_uint64 blkCoff = T_para->bsy->CQidx2Off.find(Q_CQoff)->second;

          UniType* boff = &blk->elem_enforce()[0] + (blkRoff * B_cDim) + blkCoff;

          uni10_int cnt = 0;
          std::vector<uni10_int> D_acc(bondNum, 1);
          for(uni10_int b = bondNum	- 1; b > 0; b--)
            D_acc[b - 1] = D_acc[b] * T_para->bsy->bonds[b].const_getQdegs()[Qidxs[b]];
          for(uni10_int b = 0; b < bondNum; b++)
            cnt += (idxs[b] - T_para->bsy->bonds[b].const_getOffsets()[Qidxs[b]]) * D_acc[b];
          return boff[(cnt / sB_cDim) * B_cDim + cnt % sB_cDim];
        }
        else{
          return 0.0;
        }

      }

  };

};

#endif
