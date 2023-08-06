#ifndef __UNI10_FSY_TENSOR_TOOLS_H__
#define __UNI10_FSY_TENSOR_TOOLS_H__

#include <stdio.h>

#include <set>

#include "uni10_api/UniTensor.h"

namespace uni10{

	namespace tensor_tools{

		//Function prototype.
		template <typename UniType>
      void permute_fsy(const U_para<UniType>* t1_para, const std::vector<uni10_int>& rsp_idx,
          U_para<UniType>* t2_para, uni10_bool inorder);

    template <typename To, typename T, typename U>
      void contract_fsy( const U_para<T>* t1_para, const U_para<U>* t2_para, UniTensor<To>& t3 );

    //Functions.
    template <typename UniType>
      void permute_fsy(const U_para<UniType>* t1_para, const std::vector<uni10_int>& rsp_idx,
          U_para<UniType>* t2_para, uni10_bool inorder){

        uni10_uint64 bondNum = t1_para->bsy->bonds.size();
        uni10_double64 sign = 1.0;
        //For Fermionic system
        std::vector<_Swap> swaps;

        if(Qnum::isFermionic()){

          std::vector<uni10_int> inLabelF(bondNum);
          std::vector<uni10_int> outLabelF(bondNum);
          std::vector<uni10_int> ordF(bondNum);

          for(uni10_int b = 0; b < t1_para->bsy->RBondNum; b++){
            inLabelF[b] = t1_para->bsy->labels[b];
            ordF[b] = b;
          }

          for(uni10_int b = 0; b < t2_para->bsy->RBondNum; b++)
            outLabelF[b] = t1_para->bsy->labels[rsp_idx[b]];
           
          for(uni10_int b = bondNum - 1; b >= t1_para->bsy->RBondNum; b--){
            ordF[b] = bondNum - b + t1_para->bsy->RBondNum - 1;
            inLabelF[ordF[b]] = t1_para->bsy->labels[b];
          }

          for(uni10_int b = bondNum - 1; b >= t2_para->bsy->RBondNum; b--)
            outLabelF[bondNum - b + t2_para->bsy->RBondNum - 1] = t1_para->bsy->labels[rsp_idx[b]];

          std::vector<uni10_int> rspF_outin(bondNum);
          for(uni10_uint64 i = 0; i < bondNum; i++)
            for(uni10_uint64 j = 0; j < bondNum; j++)
              if(inLabelF[i] == outLabelF[j])
                rspF_outin[j] = i;
          swaps = recSwap(rspF_outin, ordF);
        }

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

          if(Qnum::isFermionic()){
            uni10_int sign01 = 0;
            for(uni10_uint64 i = 0; i < swaps.size(); i++)
              sign01 ^= (t1_para->bsy->bonds[swaps[i].b1].const_getQnums()[Qin_idxs[swaps[i].b1]].prtF() & t1_para->bsy->bonds[swaps[i].b2].const_getQnums()[Qin_idxs[swaps[i].b2]].prtF());
            sign = sign01 ? -1.0 : 1.0;
          }
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
      uni10_int contract_fsy( const U_para<T>* t1_para, const U_para<U>* t2_para, UniTensor<To>& t3 ){

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

        permute_fsy(t1_para, t1_rspidx, pt1_para, t1_inorder);
        permute_fsy(t2_para, t2_rspidx, pt2_para, t2_inorder);

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
	};

};

#endif
