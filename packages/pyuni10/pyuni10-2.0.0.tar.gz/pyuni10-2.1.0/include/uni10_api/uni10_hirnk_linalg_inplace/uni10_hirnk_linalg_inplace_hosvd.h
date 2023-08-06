#ifndef __UNI10_HIGH_RANK_LINALG_INPLACE_HOSVD_H__
#define __UNI10_HIGH_RANK_LINALG_INPLACE_HOSVD_H__

#include "uni10_api/uni10_hirnk_linalg_inplace/uni10_hirnk_linalg_inplace_permute.h"
#include "uni10_api/tensor_tools/tensor_tools.h"

namespace uni10{

  /// @ingroup hirnklin_inplace
  /// @brief Driver function for High-order SVD
  ///
  /// Performs High order SVD of UniTensor.
  /// @param[in] group_labels Ordered labels of the bonds
  /// @param[in] groups Number of external bonds in each mode
  /// @param[in] groupSize Number of modes
  /// @param[out] Ls Singular values on each direction
  ///
  /// @code
  /// ***** Example ******
  ///     ____________                     ______                      ____
  ///    |            |               0___|  U1  |__-1 ___     __-2___|    |___1
  ///8___|            |___0               |______|       _|___|_      | U2 |___2
  ///    |            |                                 |       |     |____|
  ///9___|            |___1                        __11_|       |
  ///    |            |                            __3__|       |
  ///11__|            |___2                             |   S   |
  ///    |            |                    ______       |       |      ____
  ///6___|            |___3            8__|      |__-4__|       |__-3_|    |___4
  ///    |            |                9__|  U4  |      |_______|     | U3 |___5
  ///5___|            |___4               |______|                    |____|___6
  ///    |            |
  ///    |____________|
  ///
  /// @endcode
  /// We want to decompose the tensor into a tensor of four modes and two bonds unchanged.
  ///
  /// @code
  /// Mode 1 {0,-1}
  /// Mode 2 {1,2,-2}
  /// Mode 3 {4,5,6,-3}
  /// Mode 4 {8,9,-4}
  /// Fixed {3,11}
  /// @endcode
  /// The input parameters are
  /// @code
  /// group_labels = { 0, 1, 2, 4, 5, 6, 8, 9, 3, 11 }
  /// groups={1,2,3,2}
  /// groupSize=4
  /// @endcode
  /// Returns unitaries \c U1, \c U2, \c U3, \c U4, and core tensor \c S
  template<typename UniType>
    void Hosvd(UniTensor<UniType>& inten, uni10_int32* group_labels, uni10_int32* groups, uni10_uint64 groupsSize, 
        std::vector<UniTensor<UniType> >& Us, UniTensor<UniType>& S, std::vector<std::map<Qnum, Matrix<UniType> > >& Ls, UNI10_INPLACE on);

  template<typename UniType>
    void Hosvd(UniTensor<UniType>& inten, uni10_int32* group_labels, uni10_int32* groups, uni10_uint64 groupsSize, 
        std::vector<UniTensor<UniType> >& Us, UniTensor<UniType>& S, std::vector<Matrix<UniType> >& Ls, UNI10_INPLACE on);

  template<typename UniType>
    void Hosvd(UniTensor<UniType>& inten, std::vector<uni10_int32> group_labels, std::vector<uni10_int32> groups, 
        std::vector<UniTensor<UniType> >& Us, UniTensor<UniType>& S, std::vector<std::map<Qnum, Matrix<UniType> > >& Ls, UNI10_INPLACE on);

  template<typename UniType>
    void Hosvd(UniTensor<UniType>& inten, std::vector<uni10_int32> group_labels, std::vector<uni10_int32> groups, 
        std::vector<UniTensor<UniType> >& Us, UniTensor<UniType>& S, std::vector< Matrix<UniType> >& Ls, UNI10_INPLACE on);


  template<typename UniType>
    void Hosvd(UniTensor<UniType>& inten, uni10_int32* group_labels, uni10_int32* groups, uni10_uint64 groupsSize, 
        std::vector<UniTensor<UniType> >& Us, UniTensor<UniType>& S, std::vector< std::map<Qnum, Matrix<UniType> > >& Ls, UNI10_INPLACE on){

      uni10_error_msg(on != 1, "%s", "Setting a wrong flag of uni10_Inplace." );
      uni10_error_msg(( (*inten.status) & inten.HAVEBOND) == 0,"%s","Cannot perform higher order SVD on a tensor without bonds(scalar).");
      uni10_error_msg(( (*inten.status) & inten.HAVEELEM) == 0,"%s", "Cannot perform higher order SVD on a tensor before setting its elements.");

      Us.clear();

      uni10_uint64 BondNum = inten.BondNum();
      // Save original inten tensor.

      uni10_uint64 groupElemNum=0;
      for(uni10_uint64 n = 0; n < groupsSize; n++)
        groupElemNum+=groups[n];

      if(&Ls != NULL)
        Ls.assign(groupsSize, std::map<Qnum, Matrix<UniType> >());

      UniTensor<UniType> bufS(inten);

      std::vector<uni10_int32> lrsp_labels(group_labels, group_labels+BondNum);
      std::vector<uni10_int32> rsp_labels = lrsp_labels;

      uni10_int32 min = *std::min_element(rsp_labels.begin(), rsp_labels.end());

      // For permutation
      UniTensor<UniType> bufT;

      for(uni10_uint64 m = 0; m < groupsSize; m++){
        uni10_int32 pos=0;
        for(uni10_uint64 l = 0; l < groupElemNum; l++){
          if(l >= groupElemNum-groups[m])
            rsp_labels[pos] = lrsp_labels[l-(groupElemNum-groups[m])];
          else
            rsp_labels[pos] = lrsp_labels[l+groups[m]];
          pos++;
        }

        std::vector<Bond> bonds;
        if(m % 2 == 0){
          Permute(bufT, inten, lrsp_labels, groups[m], INPLACE);
          bonds.assign(bufT.bonds->begin(), bufT.bonds->begin() + groups[m]);
        }
        else{
          Permute(inten, bufT, lrsp_labels, groups[m], INPLACE);
          bonds.assign(inten.bonds->begin(), inten.bonds->begin() + groups[m]);
        }

        bonds.push_back(combine(bonds).dummy_change(BD_OUT));
        Us.push_back(UniTensor<UniType>(bonds));

        typename std::map<Qnum, Block<UniType> >::iterator it    = (m % 2 == 0) ? bufT.blocks->begin() : inten.blocks->begin();
        typename std::map<Qnum, Block<UniType> >::iterator itEnd = (m % 2 == 0) ? bufT.blocks->end()   : inten.blocks->end();

        Matrix<UniType>* vT = NULL;
        Matrix<UniType> U, L;

        for(; it != itEnd; it++){
          Svd(it->second, U, L, *vT, INPLACE);
          Us[m].PutBlock(it->first, U);
          if(&Ls != NULL)
            Ls[m][it->first] = L;
        }

        for(uni10_int32 c = 0; c < groups[m]; c++)
          (*Us[m].labels)[c] = lrsp_labels[c];
        (*Us[m].labels)[groups[m]] = min -m - 1;

        UniTensor<UniType> tmp_u;
        Conj(tmp_u, Us[m], INPLACE);

        if(m % 2 == 0)
          Contract(S, bufS, tmp_u, INPLACE);
        else
          Contract(bufS, S, tmp_u, INPLACE);

        lrsp_labels = rsp_labels;
      } 

      if(groupsSize % 2 == 0)
        S = bufS;

    } 

  template<typename UniType>
    void Hosvd(UniTensor<UniType>& inten, uni10_int32* group_labels, uni10_int32* groups, uni10_uint64 groupsSize, 
        std::vector<UniTensor<UniType> >& Us, UniTensor<UniType>& S, std::vector<Matrix<UniType> >& Ls, UNI10_INPLACE on){

      uni10_bool withoutSymmetry = true;
      for(uni10_uint64 b = 0; b < inten.bonds->size(); b++){
        if((*inten.bonds)[b].const_getQnums().size() != 1){
          withoutSymmetry = false;
          break;
        }
      }

      uni10_error_msg(!withoutSymmetry, "%s", 
          "The tensor has symmetry quantum numbers. Cannot use non-symmetry version Hosvd(size_t, std::vector<uni10::Matrix>&)\n\
          Hint: Use UniTensor::Hosvd(uni10::rflag, std::vector<int>&, std::vector<int>& , std::vector<uni10::Matrix> >&)");

      std::vector<std::map<Qnum, Matrix<UniType> > >* symLs = NULL;

      if(&Ls != NULL)
        symLs = new std::vector<std::map<Qnum, Matrix<UniType> > >[1];

      Hosvd(inten ,group_labels, groups, groupsSize, Us, S, *symLs, on);

      if(&Ls != NULL){

        Ls.clear();
        Qnum q0(0);
        for(uni10_uint64 i = 0; i < symLs[0].size(); i++)
          Ls.push_back(symLs[0][i][q0]);

        delete [] symLs;

      }

    }

  template<typename UniType>
    void Hosvd(UniTensor<UniType>& inten, std::vector<uni10_int32> group_labels, std::vector<uni10_int32> groups, 
        std::vector<UniTensor<UniType> >& Us, UniTensor<UniType>& S, std::vector<std::map<Qnum, Matrix<UniType> > >& Ls, UNI10_INPLACE on){

      uni10_error_msg(group_labels.size() != inten.BondNum(), "%s", "The size of Group labels is not match to the number of tensor's bond.");
      Hosvd(inten, &group_labels[0], &groups[0], groups.size(), Us, S, Ls, on);

    }

  template<typename UniType>
    void Hosvd(UniTensor<UniType>& inten, std::vector<uni10_int32> group_labels, std::vector<uni10_int32> groups, 
        std::vector<UniTensor<UniType> >& Us, UniTensor<UniType>& S, std::vector< Matrix<UniType> >& Ls, UNI10_INPLACE on){

      Hosvd(inten, &group_labels[0], &groups[0], groups.size(), Us, S, Ls, on);

    }

};

#endif
