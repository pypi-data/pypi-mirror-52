#include<vector>
#include<algorithm>
#include<sstream>
#include<iterator>

#include "uni10_lapack_cpu/uni10_elem_linalg.h"
#include "uni10_lapack_cpu/uni10_elem_hirnk_linalg.h"

#if defined(UNI_TCL)

namespace uni10{

  namespace hirnk_linalg_unielem_internal{

    void TensorContract(const UniElemDouble* a, const long* size_a, const uni10_int* labela, const uni10_int ranka,
        const UniElemDouble* b, const long* size_b, const uni10_int* labelb, const uni10_int rankb,
        UniElemDouble* c,  const long* size_c, const uni10_int* labelc, const uni10_int rankc){

      std::stringstream labela_str, labelb_str, labelc_str;
      std::copy(labela, labela+ranka, std::ostream_iterator<int>(labela_str, ","));
      std::copy(labelb, labelb+rankb, std::ostream_iterator<int>(labelb_str, ","));
      std::copy(labelc, labelc+rankc, std::ostream_iterator<int>(labelc_str, ","));
      std::string la, lb, lc;
      la = labela_str.str();  lb = labelb_str.str(); lc = labelc_str.str(); 

      if(la.size() != 0)
        la.pop_back(); 
      if(lb.size() != 0)
        lb.pop_back(); 
      if(lc.size() != 0)
        lc.pop_back();

      const char* la_ptr = la.c_str();
      const char* lb_ptr = lb.c_str();
      const char* lc_ptr = lc.c_str();

      uni10_int row_major = 1;
      double alpha = 1.;
      double beta = 0.;

      double* elem_t1 = a->elem_ptr_;
      double* elem_t2 = b->elem_ptr_; 
      double* elem_t3 = c->elem_ptr_; 

      uni10_int crossbondnum = (ranka + rankb - rankc) / 2;

      if( crossbondnum == 0 ){

        uni10_uint64 m =  a->elem_num_;
        uni10_uint64 k =  1;
        uni10_uint64 n =  b->elem_num_;

        bool diag = false;

        linalg_unielem_internal::Dot(a, &diag, b, &diag, &m, &n, &k, c);

      }else if( rankc == 0 ){

        uni10_uint64 m =  1;
        uni10_uint64 k =  a->elem_num_;
        uni10_uint64 n =  1;
        bool diag = false;
        UniElemDouble tmpb(1, b->elem_num_, diag, false);

        std::vector<uni10_int> rsp_idxb(rankb);
        std::vector<uni10_int> size_bi(rankb);
        for(uni10_int a = 0; a < rankb; a++)
          size_bi[a] = size_b[a];

        for(uni10_int i = 0; i < ranka; i++)
          for(uni10_int j = 0; j < rankb; j++)
            if(labela[i] == labelb[j]){
              rsp_idxb[i] = j;
              break;
            }

        TensorTranspose(b, &rsp_idxb[0], rankb, &size_bi[0], &tmpb);
        linalg_unielem_internal::Dot(a, &diag, &tmpb, &diag, &m, &n, &k, c);

      }
      else
        dTensorMult(alpha, elem_t1, size_a, NULL, la_ptr,\
            elem_t2, size_b, NULL, lb_ptr,\
            beta, elem_t3, size_c, NULL, lc_ptr, row_major);

    }

    void TensorContract(const UniElemComplex* a, const long* size_a, const uni10_int* labela, const uni10_int ranka,
        const UniElemComplex* b, const long* size_b, const uni10_int* labelb, const uni10_int rankb,
        UniElemComplex* c,  const long* size_c, const uni10_int* labelc, const uni10_int rankc){

      std::stringstream labela_str, labelb_str, labelc_str;
      std::copy(labela, labela+ranka, std::ostream_iterator<int>(labela_str, ","));
      std::copy(labelb, labelb+rankb, std::ostream_iterator<int>(labelb_str, ","));
      std::copy(labelc, labelc+rankc, std::ostream_iterator<int>(labelc_str, ","));

      std::string la, lb, lc;
      la = labela_str.str();  lb = labelb_str.str(); lc = labelc_str.str(); 

      if(la.size() != 0)
        la.pop_back(); 
      if(lb.size() != 0)
        lb.pop_back(); 
      if(lc.size() != 0)
        lc.pop_back();

      const char* la_ptr = la.c_str();
      const char* lb_ptr = lb.c_str();
      const char* lc_ptr = lc.c_str();

      uni10_int row_major = 1;
      double _Complex alpha = 1.;
      double _Complex beta = 0.;

      double _Complex* elem_t1 = (double _Complex*)a->elem_ptr_;
      double _Complex* elem_t2 = (double _Complex*)b->elem_ptr_; 
      double _Complex* elem_t3 = (double _Complex*)c->elem_ptr_; 

      uni10_int crossbondnum = (ranka + rankb - rankc) / 2;

      if( crossbondnum == 0 ){

        uni10_uint64 m =  a->elem_num_;
        uni10_uint64 k =  1;
        uni10_uint64 n =  b->elem_num_;

        bool diag = false;

        linalg_unielem_internal::Dot(a, &diag, b, &diag, &m, &n, &k, c);

      }else if( rankc == 0 ){

        uni10_uint64 m =  1;
        uni10_uint64 k =  a->elem_num_;
        uni10_uint64 n =  1;
        bool diag = false;
        UniElemComplex tmpb(1, b->elem_num_, diag, false);

        std::vector<uni10_int> rsp_idxb(rankb);
        std::vector<uni10_int> size_bi(rankb);
        for(uni10_int a = 0; a < rankb; a++)
          size_bi[a] = size_b[a];

        for(uni10_int i = 0; i < ranka; i++)
          for(uni10_int j = 0; j < rankb; j++)
            if(labela[i] == labelb[j]){
              rsp_idxb[i] = j;
              break;
            }

        TensorTranspose(b, &rsp_idxb[0], rankb, &size_bi[0], &tmpb);
        linalg_unielem_internal::Dot(a, &diag, &tmpb, &diag, &m, &n, &k, c);

      }else
        zTensorMult(alpha, (const double _Complex*)elem_t1, size_a, NULL, la_ptr,\
            (const double _Complex*)elem_t2, size_b, NULL, lb_ptr,\
            beta, (double _Complex*)elem_t3, size_c, NULL, lc_ptr, row_major);

    }

    void TensorContract(const UniElemDouble* a, const long* size_a, const uni10_int* labela, const uni10_int ranka,
        const UniElemComplex* b, const long* size_b, const uni10_int* labelb, const uni10_int rankb,
        UniElemComplex* c,  const long* size_c, const uni10_int* labelc, const uni10_int rankc){

      UniElemComplex tmp(*a);
      TensorContract(&tmp, size_a, labela, ranka, b, size_b, labelb, rankb, c, size_c, labelc, rankc);

    }

    void TensorContract(const UniElemComplex* a, const long* size_a, const uni10_int* labela, const uni10_int ranka,
        const UniElemDouble* b, const long* size_b, const uni10_int* labelb, const uni10_int rankb,
        UniElemComplex* c,  const long* size_c, const uni10_int* labelc, const uni10_int rankc){

      UniElemComplex tmp(*b);
      TensorContract(a, size_a, labela, ranka, &tmp, size_b, labelb, rankb, c, size_c, labelc, rankc);


    }

  }

};

#endif
