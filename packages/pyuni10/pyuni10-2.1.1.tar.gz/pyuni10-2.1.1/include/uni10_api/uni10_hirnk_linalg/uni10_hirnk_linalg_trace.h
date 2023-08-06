#ifndef __UNI10_HIGH_RANK_LINALG_TRACE_H__
#define __UNI10_HIGH_RANK_LINALG_TRACE_H__

#include "uni10_api/uni10_hirnk_linalg_inplace/uni10_hirnk_linalg_inplace_permute.h"
#include "uni10_api/tensor_tools/tensor_tools.h"

namespace uni10{

  /// @ingroup hirnklin
  /// @brief Take trace of a tensor.
  /// 
  /// The product of incoming bond dimensions must equal to that of outgoing ones.
  /// @param[in] T Input tensor.
  /// @return The trace.
  template<typename UniType>
    UniType Trace(const UniTensor<UniType>& T);

  template<typename UniType>
    UniType Trace(const UniTensor<UniType>& T){

      uni10_error_msg(!((*T.status) & T.HAVEELEM), "%s", "Cannot Trace a tensor before setting its elements.");

      UniType trVal = 0.;
      if((*T.status) & T.HAVEBOND){
        typename std::map<Qnum, Block<UniType> >::const_iterator it = T.blocks->begin();
        for( ; it != T.blocks->end(); it++ ){
          uni10_error_msg(!(it->second.row() == it->second.col()), "%s", "Cannot Trace a non-square block.");
          trVal += Trace(it->second);
        }
        return trVal;
      }else
        return trVal;
    }  

};

#endif
