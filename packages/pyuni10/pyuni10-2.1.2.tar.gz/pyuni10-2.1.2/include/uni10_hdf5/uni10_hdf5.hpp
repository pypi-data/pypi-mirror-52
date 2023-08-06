#ifndef __UNI10_HDF5IO_HPP__
#define __UNI10_HDF5IO_HPP__

#include <string>
#include <complex>
#include <vector>
#include <cassert>
#include <H5Cpp.h>
// #include "uni10.hpp"
#include "uni10_api/UniTensor.h"

namespace uni10{

  // uni10 types
  typedef struct uni10_qnum_hdf5 {
    int m_U1;
    uni10::parityType m_prt;
    uni10::parityFType m_prtF;
  } uni10_qnum_hdf5;


  class HDF5IO: public H5::H5File {
    private:
      std::string FileName;
      H5::Group Uni10TypeGroup;
      H5::CompType ComplexDataType;
      const H5::CompType InitComplexDataType(void);
      bool FileExists(const std::string &FileName);
      // uni10 types
      const H5::EnumType InitParityEnumType(void);
      const H5::EnumType InitParityFEnumType(void);
      H5::CompType QnumCompType;
      const H5::CompType InitQnumCompType(void);
      H5::EnumType BondEnumType;
      const H5::EnumType InitBondEnumType(void);

      // uni10 properties
      void SaveBondType(const std::string& GroupName, const std::string& SetName, const uni10::bondType& _bt);
      void SaveQnum(const std::string& GroupName, const std::string& SetName, const int &_U1, const uni10::parityType &_pt, const uni10::parityFType &_ptf);
      void LoadBondType(const std::string& GroupName, const std::string& SetName, uni10::bondType& _bt);
      void LoadQnum(const std::string& GroupName, const std::string& SetName, int &_U1, uni10::parityType &_pt, uni10::parityFType &_ptf);

      template<typename T>
      inline H5::DataType DetermineDataType(const T input){
        if ( sizeof(T) == 4){//int
          return H5::PredType::NATIVE_INT;
        }else if ( sizeof(T) == 8 ){//double
          return H5::PredType::NATIVE_DOUBLE;
        }else if ( sizeof(T) == 16 ){//complex<double>
          return ComplexDataType;
        }
      };

    public:
      HDF5IO (const std::string &FileName);
      HDF5IO (const std::string &FileName, const bool force);
      virtual ~HDF5IO (void){};
      inline H5::H5File GetFile(){return *this;};
      H5::Group GetGroup(const std::string &GroupName);

      template<typename T>
        void SaveRawBuffer(const std::string& GroupName, const std::string& SetName, const size_t dim, const T* x);
      template<typename T>
        void LoadRawBuffer(const std::string& GroupName, const std::string& SetName, size_t& dim, T*& x);

      template<typename T>
        inline void SaveNumber(const std::string& GroupName, const std::string& SetName, const T& x){
          size_t dim = 1;
          this->SaveRawBuffer(GroupName, SetName, dim, &x);
        };
      template<typename T>
        inline void LoadNumber(const std::string& GroupName, const std::string& SetName, T& x){
          T* val;
          size_t dim = 1;
          this->LoadRawBuffer(GroupName, SetName, dim, val);
          x = val[0];
        };

      template<typename T>
        inline void SaveStdVector(const std::string& GroupName, const std::string& SetName, const std::vector<T>& V){
          size_t dim = V.size();
          this->SaveRawBuffer(GroupName, SetName, dim, V.data());
        };
      template<typename T>
        inline void LoadStdVector(const std::string& GroupName, const std::string& SetName, std::vector<T>& V){
          T* val;
          size_t dim;
          this->LoadRawBuffer(GroupName, SetName, dim, val);
          V.clear();
          V.assign(val, val+dim);
        };

      template<typename T>
        void SaveTensor(const std::string& GroupName, const uni10::UniTensor<T> Ten);
      template<typename T>
        void LoadTensor(const std::string& GroupName, uni10::UniTensor<T>& Ten);
  };
};
#endif  /* end of include guard: __UNI10_HDF5IO_HPP__ */
