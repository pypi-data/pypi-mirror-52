#include <algorithm>

#include "uni10_lapack_cpu/uni10_elem_linalg.h"
#include "uni10_lapack_cpu/uni10_elem_hirnk_linalg.h"

namespace uni10{

#if !defined(UNI_TCL)

  namespace hirnk_linalg_unielem_internal{

    void TensorContract(const UniElemDouble* a, const long* size_a, const uni10_int* labela, const uni10_int ranka,
        const UniElemDouble* b, const long* size_b, const uni10_int* labelb, const uni10_int rankb,
        UniElemDouble* c,  const long* size_c, const uni10_int* labelc, const uni10_int rankc){

#if defined(UNI_DEBUG)
      printf(" @@@@@@@@  Naive Contraction @@@@@@@ \n");
#endif

      uni10_int crossnum = (ranka + rankb - rankc)/2;
      uni10_int belong2a = ranka - crossnum;
      uni10_int belong2b = rankb - crossnum;
      uni10_uint64 m=1, n=1, k=1;

      std::vector<uni10_int> crossidxa, rsp_idxa, rsp_idxb;

      for(uni10_int i = 0; i < ranka; i++ ){
        for(uni10_int j = 0; j < rankb; j++)
          if(labela[i] == labelb[j]){
            crossidxa.push_back(i);
            rsp_idxb.push_back(j);
            k *= size_a[i];
          }
      }

#if defined(UNI_DEBUG)
      printf("belong2a: %d\n", belong2a);
      printf("belong2b: %d\n", belong2b);

      printf("labela: ");
      for(uni10_int a = 0; a < ranka; a++)
        printf("%d,", labela[a]);
      printf("\n");

      printf("labelb: ");
      for(uni10_int b = 0; b < rankb; b++)
        printf("%d,", labelb[b]);
      printf("\n");

      printf("labelc: ");
      for(uni10_int c = 0; c < rankc; c++)
        printf("%d,", labelc[c]);
      printf("\n");
#endif

      for(uni10_int a = 0; a < belong2a; a++){
        uni10_int pos = std::find(labela, labela+ranka, labelc[a]) - labela;
        uni10_error_msg( pos >= ranka, \
            "Label (%d) belongs to tensor t1 is not finded in the t1 label list.", labelc[a]);
        rsp_idxa.push_back(pos);
        m *= size_a[pos];
      }

      for(uni10_int b = 0; b < belong2b; b++){
        uni10_int pos = std::find(labelb, labelb+rankb, labelc[belong2a+b]) - labelb;
        uni10_error_msg( pos >= rankb, \
            "Label (%d) belongs to tensor t2 is not finded in the t2 label list.", labelc[belong2a+b]);
        rsp_idxb.push_back(pos);
        n *= size_b[pos];
      }

      for(uni10_int c = 0; c < crossnum; c++)
        rsp_idxa.push_back(crossidxa[c]);

#if defined(UNI_DEBUG)
      printf("rsp_idxa: ");
      for(uni10_int a = 0; a < (int)rsp_idxa.size(); a++)
        printf("%d,", rsp_idxa[a]);
      printf("\n");

      printf("rsp_idxb: ");
      for(uni10_int b = 0; b < (int)rsp_idxb.size(); b++)
        printf("%d,", rsp_idxb[b]);
      printf("\n");
#endif

      bool diag = false;

      UniElemDouble pa(1, a->elem_num_, diag, false);
      UniElemDouble pb(1, b->elem_num_, diag, false);

      uni10_int* size_ai = (uni10_int*)malloc(ranka*sizeof(uni10_int));
      uni10_int* size_bi = (uni10_int*)malloc(rankb*sizeof(uni10_int));
      
      for(int i = 0; i < ranka; i++)
        size_ai[i] = size_a[i];

      for(int j = 0; j < rankb; j++)
        size_bi[j] = size_b[j];

      TensorTranspose(a, &rsp_idxa[0], ranka, size_ai, &pa);
      TensorTranspose(b, &rsp_idxb[0], rankb, size_bi, &pb);

      linalg_unielem_internal::Dot(&pa, &diag, &pb, &diag, &m, &n, &k, c);

      free(size_ai);
      free(size_bi);

    }

    void TensorContract(const UniElemComplex* a, const long* size_a, const uni10_int* labela, const uni10_int ranka,
        const UniElemComplex* b, const long* size_b, const uni10_int* labelb, const uni10_int rankb,
        UniElemComplex* c,  const long* size_c, const uni10_int* labelc, const uni10_int rankc){

#if defined(UNI_DEBUG)
      printf(" @@@@@@@@  Naive Contraction @@@@@@@ \n");
#endif

      uni10_int crossnum = (ranka + rankb - rankc)/2;
      uni10_int belong2a = ranka - crossnum;
      uni10_int belong2b = rankb - crossnum;
      uni10_uint64 m=1, n=1, k=1;

      std::vector<uni10_int> crossidxa, rsp_idxa, rsp_idxb;

      for(uni10_int i = 0; i < ranka; i++ ){
        for(uni10_int j = 0; j < rankb; j++)
          if(labela[i] == labelb[j]){
            crossidxa.push_back(i);
            rsp_idxb.push_back(j);
            k *= size_a[i];
          }
      }

#if defined(UNI_DEBUG)
      printf("belong2a: %d\n", belong2a);
      printf("belong2b: %d\n", belong2b);

      printf("labela: ");
      for(uni10_int a = 0; a < ranka; a++)
        printf("%d,", labela[a]);
      printf("\n");

      printf("labelb: ");
      for(uni10_int b = 0; b < rankb; b++)
        printf("%d,", labelb[b]);
      printf("\n");

      printf("labelc: ");
      for(uni10_int c = 0; c < rankc; c++)
        printf("%d,", labelc[c]);
      printf("\n");
#endif

      for(uni10_int a = 0; a < belong2a; a++){
        uni10_int pos = std::find(labela, labela+ranka, labelc[a]) - labela;
        uni10_error_msg( pos >= ranka, \
            "Label (%d) belongs to tensor t1 is not finded in the t1 label list.", labelc[a]);
        rsp_idxa.push_back(pos);
        m *= size_a[pos];
      }

      for(uni10_int b = 0; b < belong2b; b++){
        uni10_int pos = std::find(labelb, labelb+rankb, labelc[belong2a+b]) - labelb;
        uni10_error_msg( pos >= rankb, \
            "Label (%d) belongs to tensor t2 is not finded in the t2 label list.", labelc[belong2a+b]);
        rsp_idxb.push_back(pos);
        n *= size_b[pos];
      }

      for(uni10_int c = 0; c < crossnum; c++)
        rsp_idxa.push_back(crossidxa[c]);

#if defined(UNI_DEBUG)
      printf("rsp_idxa: ");
      for(uni10_int a = 0; a < (int)rsp_idxa.size(); a++)
        printf("%d,", rsp_idxa[a]);
      printf("\n");

      printf("rsp_idxb: ");
      for(uni10_int b = 0; b < (int)rsp_idxb.size(); b++)
        printf("%d,", rsp_idxb[b]);
      printf("\n");
#endif

      bool diag = false;

      UniElemComplex pa(1, a->elem_num_, diag, false);
      UniElemComplex pb(1, b->elem_num_, diag, false);

      uni10_int* size_ai = (uni10_int*)malloc(ranka*sizeof(uni10_int));
      uni10_int* size_bi = (uni10_int*)malloc(rankb*sizeof(uni10_int));
      
      for(int i = 0; i < ranka; i++)
        size_ai[i] = size_a[i];

      for(int j = 0; j < rankb; j++)
        size_bi[j] = size_b[j];

      TensorTranspose(a, &rsp_idxa[0], ranka, size_ai, &pa);
      TensorTranspose(b, &rsp_idxb[0], rankb, size_bi, &pb);

      linalg_unielem_internal::Dot(&pa, &diag, &pb, &diag, &m, &n, &k, c);

      free(size_ai);
      free(size_bi);

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

#endif

};
