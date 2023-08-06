#ifndef __UNI10_NETORDER_H__
#define __UNI10_NETORDER_H__

#include <utility>

#include "uni10_api/UniTensor.h"
#include "uni10_api/network_tools/pseudotensor.h"

typedef std::vector< std::pair<const void*, int> >  ary1d_uptr;
typedef std::vector< std::vector<uni10_int> > ary2d_label;
typedef std::vector< std::string >            ary1d_name;
typedef std::vector< uni10_int >              ary1d_order;

typedef std::vector< uni10::PseudoTensor > ary1d_pten;
typedef std::vector< std::vector< uni10::PseudoTensor> > ary2d_pten;

namespace uni10{

  class NetOrder{

    public:

      NetOrder();

      ~NetOrder();

      NetOrder(const ary1d_uptr& tens_type, const ary2d_label& label_arr, const ary1d_name& _names);

      ary1d_order generate_order();

      friend class PseudoTensor;

    private:

      const ary1d_name* names;

      bool is_disjoint(const PseudoTensor& T1, const PseudoTensor& T2);

      bool is_overlap(const PseudoTensor& T1, const PseudoTensor& T2);

      PseudoTensor psesudocontract(const PseudoTensor& T1, const PseudoTensor& T2);

      float get_cost(const PseudoTensor& T1, const PseudoTensor& T2);

      ary2d_pten tensor_set;

      float xi_min;

      int numT;

      std::vector<int> netorder_idx;

  };

};
#endif
