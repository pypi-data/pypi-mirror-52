#include "uni10_lapack_cpu/uni10_elem_hirnk_linalg.h"

#if !defined(UNI_TCL)

namespace uni10{

  namespace hirnk_linalg_unielem_internal{

    void TensorTranspose(const UniElemDouble* a, const uni10_int *knewbdidx, const uni10_int krank, const uni10_int* koribonddims, UniElemDouble* ta){

#if defined(UNI_DEBUG)
    printf(" @@@@@@@@  Naive Permutation @@@@@@@ \n");
#endif

      bool inorder = true;
      for(uni10_int i = 0; i < krank; i++)
        if(knewbdidx[i] != i){
          inorder = false;
          break;
        }

      if(!inorder){

        std::vector<uni10_uint64> newAcc(krank);
        newAcc[krank - 1] = 1;

        std::vector<uni10_uint64> transAcc(krank);
        transAcc[krank - 1] = 1;
        for(int b = krank - 1; b > 0; b--){
          newAcc[b - 1] = newAcc[b] * koribonddims[knewbdidx[b]];
        }

        std::vector<uni10_uint64> newbondDims(krank);
        std::vector<uni10_uint64> idxs(krank);

        for(int b = 0; b < krank; b++){
          transAcc[knewbdidx[b]] = newAcc[b];
          newbondDims[b] = koribonddims[knewbdidx[b]];
          idxs[b] = 0;
        }

        uni10_uint64 cnt_ot = 0;
        for(uni10_uint64 i = 0; i < a->elem_num_; i++){
          ta->elem_ptr_[cnt_ot] = a->elem_ptr_[i];
          for(int bend = krank - 1; bend >= 0; bend--){
            idxs[bend]++;
            if(idxs[bend] < koribonddims[bend]){
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
        ta->Copy(0, *a, a->elem_num_);
      }

    }


    void TensorTranspose(const UniElemComplex* a, const uni10_int *knewbdidx, const uni10_int krank, const uni10_int* koribonddims, UniElemComplex* ta){

#if defined(UNI_DEBUG)
    printf(" @@@@@@@@  Naive Permutation @@@@@@@ \n");
#endif

      bool inorder = true;
      for(uni10_int i = 0; i < krank; i++)
        if(knewbdidx[i] != i){
          inorder = false;
          break;
        }

      if(!inorder){

        std::vector<uni10_uint64> newAcc(krank);
        newAcc[krank - 1] = 1;

        std::vector<uni10_uint64> transAcc(krank);
        transAcc[krank - 1] = 1;
        for(int b = krank - 1; b > 0; b--){
          newAcc[b - 1] = newAcc[b] * koribonddims[knewbdidx[b]];
        }

        std::vector<uni10_uint64> newbondDims(krank);
        std::vector<uni10_uint64> idxs(krank);

        for(int b = 0; b < krank; b++){
          transAcc[knewbdidx[b]] = newAcc[b];
          newbondDims[b] = koribonddims[knewbdidx[b]];
          idxs[b] = 0;
        }

        uni10_uint64 cnt_ot = 0;
        for(uni10_uint64 i = 0; i < a->elem_num_; i++){
          ta->elem_ptr_[cnt_ot] = a->elem_ptr_[i];
          for(int bend = krank - 1; bend >= 0; bend--){
            idxs[bend]++;
            if(idxs[bend] < koribonddims[bend]){
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
        ta->Copy(0, *a, a->elem_num_);
      }

    }

  }

};

#endif
