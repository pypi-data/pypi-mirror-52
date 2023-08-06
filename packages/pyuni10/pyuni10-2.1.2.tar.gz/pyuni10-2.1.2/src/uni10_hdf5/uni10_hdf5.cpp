#include <exception>
#include <sstream>
#include <cstdlib>
#include "uni10_hdf5/uni10_hdf5.hpp"

namespace uni10{
  /* For the HDF5IO class */
  const H5::CompType HDF5IO::InitComplexDataType(){
    H5::CompType Type(sizeof(std::complex<double>));
    // NOTE: New HDF5 with native complex datatypes ??
    Type.insertMember("real", 0, H5::PredType::NATIVE_DOUBLE);
    Type.insertMember("imag", sizeof(double), H5::PredType::NATIVE_DOUBLE);
    try {
      Type.commit(*this, "uni10Types/complex");
    } catch(H5::DataTypeIException){};
    return Type;
  }

  const H5::EnumType HDF5IO::InitParityEnumType(){
    H5::EnumType Type( sizeof(int) );
    uni10::parityType pt = uni10::PRT_EVEN;
    Type.insert("PRT_EVEN", &pt);
    pt = uni10::PRT_ODD;
    Type.insert("PRT_ODD", &pt);
    try {
      Type.commit(*this, "uni10Types/parityType");
    } catch(H5::DataTypeIException){};
    return Type;
  }

  const H5::EnumType HDF5IO::InitParityFEnumType(){
    H5::EnumType Type( sizeof(int) );
    uni10::parityFType pt = uni10::PRTF_EVEN;
    Type.insert("PRTF_EVEN", &pt);
    pt = uni10::PRTF_ODD;
    Type.insert("PRTF_ODD", &pt);
    try {
      Type.commit(*this, "uni10Types/parityFType");
    } catch(H5::DataTypeIException){};
    return Type;
  }

  const H5::CompType HDF5IO::InitQnumCompType(){
    H5::CompType Type( sizeof(uni10_qnum_hdf5) );
    H5::EnumType ParityEnumType = InitParityEnumType();
    H5::EnumType ParityFEnumType = InitParityFEnumType();
    Type.insertMember("U1", HOFFSET(uni10_qnum_hdf5, m_U1), H5::PredType::NATIVE_INT);
    Type.insertMember("parity", HOFFSET(uni10_qnum_hdf5, m_prt), ParityEnumType);
    Type.insertMember("parityF", HOFFSET(uni10_qnum_hdf5, m_prtF), ParityFEnumType);
    try {
      Type.commit(*this, "uni10Types/qnum");
    } catch(H5::DataTypeIException){};
    return Type;
  }

  const H5::EnumType HDF5IO::InitBondEnumType(){
    H5::EnumType Type( sizeof(int) );
    uni10::bondType bond = uni10::BD_IN;
    Type.insert("In", &bond);
    bond = uni10::BD_OUT;
    Type.insert("Out", &bond);
    try {
      Type.commit(*this, "uni10Types/bondType");
    } catch(H5::DataTypeIException){};
    return Type;
  }

  bool HDF5IO::FileExists(const std::string& FileName){
    try {
      H5::Exception::dontPrint();
      return isHdf5(FileName.c_str());
    } catch(H5::FileIException){
      return false;
    }
  }

  HDF5IO::HDF5IO (const std::string& fn) :
  H5File(fn.c_str(), FileExists(fn) ? H5F_ACC_RDWR : H5F_ACC_TRUNC),
  FileName(fn),
  Uni10TypeGroup(GetGroup("uni10Types")),
  ComplexDataType(InitComplexDataType()),
  QnumCompType(InitQnumCompType()),
  BondEnumType(InitBondEnumType()){}

  HDF5IO::HDF5IO (const std::string& fn, const bool force):
  H5File(fn.c_str(), H5F_ACC_TRUNC),
  FileName(fn),
  Uni10TypeGroup(GetGroup("uni10Types")),
  ComplexDataType(InitComplexDataType()),
  QnumCompType(InitQnumCompType()),
  BondEnumType(InitBondEnumType()){}

  H5::Group HDF5IO::GetGroup(const std::string &GroupName){
    H5::Group group;
    try{
      H5::Exception::dontPrint();
      group = H5::Group( this->openGroup( GroupName.c_str() ) );
    } catch( H5::FileIException not_found_error ){
      group = H5::Group( this->createGroup( GroupName.c_str() ) );
    } catch( const H5::Exception err ){
      std::cout << "In Group - " << GroupName << std::endl;
      throw std::runtime_error(" HDF5IO::GetGroup fail. ");
    }
    return group;
  }


  /* +------------------------------+
    | Load/Save C/C++ raw buffer   | Everything works from here!
    +------------------------------+  */
  template<typename T>
  void HDF5IO::SaveRawBuffer(const std::string& GroupName, const std::string& SetName, const size_t dim, const T* x){
    H5::DataType InputDataType = DetermineDataType( T(0) );
    try{
      H5::Exception::dontPrint();
      H5::DataSpace dataspace;// Default to H5S_SCALAR
      if ( dim != 1 ){
        hsize_t Dim[1] = {hsize_t(dim)};
        dataspace = H5::DataSpace(1,Dim);// Will change to H5S_SIMPLE
      }
      H5::Group FG = GetGroup( GroupName );
      try{
        H5::DataSet dset = FG.openDataSet(SetName.c_str());
        dset.write(x, InputDataType, dataspace);
      } catch ( const H5::GroupIException not_found_error ){
        H5::DataSet dset = FG.createDataSet(SetName.c_str(), InputDataType, dataspace);
        dset.write(x, InputDataType);
      } catch( const H5::FileIException error){
        // error.printError();
        std::cout << "In Group - " << GroupName << std::endl;
        throw std::runtime_error(" HDF5IO::SaveRawBuffer fail. ");
      } catch( const H5::DataSetIException error){
        // error.printError();
        std::cout << "In Group - " << GroupName << ", Set - " << SetName << std::endl;
        throw std::runtime_error(" HDF5IO::SaveRawBuffer fail. ");
      }
      FG.close();
    }catch ( const H5::Exception ) {
      std::cout << "In Group - " << GroupName << ", and SetName is " << SetName << std::endl;
      throw std::runtime_error(" HDF5IO::SaveRawBuffer<T> ");
    }
  }
  template void HDF5IO::SaveRawBuffer(const std::string& GroupName, const std::string& SetName, const size_t dim, const int* x);
  template void HDF5IO::SaveRawBuffer(const std::string& GroupName, const std::string& SetName, const size_t dim, const double* x);
  template void HDF5IO::SaveRawBuffer(const std::string& GroupName, const std::string& SetName, const size_t dim, const std::complex<double>* x);
  template<>
  void HDF5IO::SaveRawBuffer(const std::string& GroupName, const std::string& SetName, const size_t dim, const unsigned long* x){
    H5::DataType InputDataType = H5::PredType::NATIVE_ULLONG;
    try{
      H5::Exception::dontPrint();
      H5::DataSpace dataspace;// Default to H5S_SCALAR
      if ( dim != 1 ){
        hsize_t Dim[1] = {hsize_t(dim)};
        dataspace = H5::DataSpace(1,Dim);// Will change to H5S_SIMPLE
      }
      H5::Group FG = GetGroup( GroupName );
      try{
        H5::DataSet dset = FG.openDataSet(SetName.c_str());
        dset.write(x, InputDataType, dataspace);
      } catch ( const H5::GroupIException not_found_error ){
        H5::DataSet dset = FG.createDataSet(SetName.c_str(), InputDataType, dataspace);
        dset.write(x, InputDataType);
      } catch( const H5::FileIException error){
        // error.printError();
        std::cout << "In Group - " << GroupName << std::endl;
        throw std::runtime_error(" HDF5IO::SaveRawBuffer (ULONG) fail. ");
      } catch( const H5::DataSetIException error){
        // error.printError();
        std::cout << "In Group - " << GroupName << ", Set - " << SetName << std::endl;
        throw std::runtime_error(" HDF5IO::SaveRawBuffer (ULONG) fail. ");
      }
      FG.close();
    }catch ( const H5::Exception error){
      // error.printError();
      std::cout << "In Group - " << GroupName << ", and SetName is " << SetName << std::endl;
      throw std::runtime_error(" HDF5IO::SaveRawBuffer<ulong> ");
    }
  }

  template<typename T>
  void HDF5IO::LoadRawBuffer(const std::string& GroupName, const std::string& SetName, size_t& dim, T*& x){
    H5::DataType OutputDataType = DetermineDataType( T(0) );
    try{
      H5::Group FG = GetGroup( GroupName );
      H5::DataSet DataSet = FG.openDataSet(SetName.c_str());
      try{
        H5::DataSpace DataSpace = DataSet.getSpace();
        hsize_t Dims[1];
        int NDims = DataSpace.getSimpleExtentDims(Dims);
        dim = ( NDims == 0 )? 1 : Dims[0];
        x = (T*)malloc( dim * sizeof(T) );
        DataSet.read(x, OutputDataType);
      } catch( const H5::DataSpaceIException error ){
        // error.printError();
        std::cout << "In Group - " << GroupName << ", Set - " << SetName << std::endl;
        throw std::runtime_error(" HDF5IO::LoadRawBuffer fail (DataSapce). ");
      } catch( const H5::DataSetIException error){
        // error.printError();
        std::cout << "In Group - " << GroupName << ", Set - " << SetName << std::endl;
        throw std::runtime_error(" HDF5IO::LoadRawBuffer fail (DataSet). ");
      } catch( const H5::FileIException error){
        // error.printError();
        std::cout << "In Group - " << GroupName << std::endl;
        throw std::runtime_error(" HDF5IO::LoadRawBuffer fail (File). ");
      }
      FG.close();
    }catch ( const H5::Exception error ) {
      // error.printError();
      std::cout << "In Group - " << GroupName << ", and SetName is " << SetName << std::endl;
      throw std::runtime_error(" HDF5IO::LoadRawBuffer<T>. ");
    }
  }
  template void HDF5IO::LoadRawBuffer(const std::string& GroupName, const std::string& SetName, size_t& dim, int*& x);
  template void HDF5IO::LoadRawBuffer(const std::string& GroupName, const std::string& SetName, size_t& dim, double*& x);
  template void HDF5IO::LoadRawBuffer(const std::string& GroupName, const std::string& SetName, size_t& dim, std::complex<double>*& x);
  template<>
  void HDF5IO::LoadRawBuffer(const std::string& GroupName, const std::string& SetName, size_t& dim, unsigned long*& x){
    H5::DataType OutputDataType = H5::PredType::NATIVE_ULONG;
    try{
      H5::Group FG = GetGroup( GroupName );
      H5::DataSet DataSet = FG.openDataSet(SetName.c_str());
      try{
        H5::DataSpace DataSpace = DataSet.getSpace();
        hsize_t Dims[1];
        int NDims = DataSpace.getSimpleExtentDims(Dims);
        dim = ( NDims == 0 )? 1 : Dims[0];
        x = (unsigned long*)malloc( dim * sizeof(unsigned long) );
        DataSet.read(x, OutputDataType);
      } catch( const H5::DataSpaceIException error ){
          // error.printError();
        std::cout << "In Group - " << GroupName << ", Set - " << SetName << std::endl;
        throw std::runtime_error(" HDF5IO::LoadRawBuffer fail (DataSapce). ");
      } catch( const H5::DataSetIException error){
        // error.printError();
        std::cout << "In Group - " << GroupName << ", Set - " << SetName << std::endl;
        throw std::runtime_error(" HDF5IO::LoadRawBuffer fail (DataSet). ");
      } catch( const H5::FileIException error){
        // error.printError();
        std::cout << "In Group - " << GroupName << std::endl;
        throw std::runtime_error(" HDF5IO::LoadRawBuffer fail (File). ");
      }
      FG.close();
    }catch ( const H5::Exception error){
      // error.printError();
      std::cout << "In Group - " << GroupName << ", and SetName is " << SetName << std::endl;
      throw std::runtime_error(" HDF5IO::LoadRawBuffer<ulong>. ");
    }
  }





  /* +----------------------------+
    | Load/Save uni10 properties |
    +----------------------------+ */
  void HDF5IO::SaveBondType(const std::string& GroupName, const std::string& SetName, const uni10::bondType& _bt){
    H5::Group FG = GetGroup( GroupName );
    try{
      H5::Exception::dontPrint();
      H5::DataSet dset = FG.openDataSet(SetName.c_str());
      dset.write(&_bt, BondEnumType);
    }catch( H5::GroupIException not_found_error ) {
      H5::DataSet dset = FG.createDataSet(SetName.c_str(), BondEnumType, H5::DataSpace());
      dset.write(&_bt, BondEnumType);
    }catch( const H5::Exception ) {
      std::cout << "In Group - " << GroupName << ", and SetName is " << SetName << std::endl;
      throw std::runtime_error(" HDF5IO::SaveBondType ");
    }
  }

  void HDF5IO::SaveQnum(const std::string& GroupName, const std::string& SetName, const int &_U1, const uni10::parityType &_pt, const uni10::parityFType &_ptf) {
    uni10_qnum_hdf5 _input;
    _input.m_U1 = _U1;
    _input.m_prt = _pt;
    _input.m_prtF = _ptf;
    H5::Group FG = GetGroup( GroupName );
    try{
      H5::Exception::dontPrint();
      H5::DataSet dset = FG.openDataSet(SetName.c_str());
      dset.write(&_input, QnumCompType);
    }catch( H5::GroupIException not_found_error ) {
      H5::DataSet dset = FG.createDataSet(SetName.c_str(), QnumCompType, H5::DataSpace());
      dset.write(&_input, QnumCompType);
    }catch( const H5::Exception ) {
      std::cout << "In Group - " << GroupName << ", and SetName is " << SetName << std::endl;
      throw std::runtime_error(" HDF5IO::SaveQnum ");
    }
  }

  void HDF5IO::LoadBondType(const std::string& GroupName, const std::string& SetName, uni10::bondType& _bt){
    try{
      H5::Group FG = GetGroup( GroupName );
      H5::DataSet DataSet = FG.openDataSet( SetName.c_str() );
      DataSet.read(&_bt, BondEnumType);
      FG.close();
    }catch( const H5::Exception ) {
      std::cout << "In Group - " << GroupName << ", and SetName is " << SetName << std::endl;
      throw std::runtime_error(" HDF5IO::LoadBondType ");
    }
  }

  void HDF5IO::LoadQnum(const std::string& GroupName, const std::string& SetName, int &_U1, uni10::parityType &_pt, uni10::parityFType &_ptf){
    try{
      H5::Group FG = GetGroup( GroupName );
      H5::DataSet DataSet = FG.openDataSet( SetName.c_str() );
      uni10_qnum_hdf5 _output;
      DataSet.read(&_output, QnumCompType);
      _U1 = _output.m_U1;
      _pt = _output.m_prt;
      _ptf = _output.m_prtF;
      FG.close();
    }catch( const H5::Exception ) {
      std::cout << "In Group - " << GroupName << ", and SetName is " << SetName << std::endl;
      throw std::runtime_error(" HDF5IO::LoadQnum ");
    }
  }

  template<typename T>
  void HDF5IO::SaveTensor(const std::string& GroupName, const uni10::UniTensor<T> Ten){
    // Create Group
    H5::Group FG = GetGroup( GroupName );
    // What to store?
    // Bonds and Qnums
    int BondNum = Ten.BondNum();
    std::string gname = GroupName;
    gname.append("/Bonds");
    SaveNumber(gname, "BondNum", BondNum);
    std::vector<int> labels = Ten.label();
    if ( labels.size() ){
      SaveStdVector(gname, "Labels", labels);
    }else{
      std::vector<int> tmp;
      for ( int i=0; i < BondNum; i++) tmp.push_back(i);
      SaveStdVector(gname, "Labels", tmp);
    }
    for(int b = 0; b < BondNum; b++){
      uni10::Bond bond = Ten.bond(b);
      gname = GroupName;
      gname.append("/Bonds/bond-");
      gname.append(std::to_string((unsigned long long)b));
      SaveBondType(gname, "BondType", bond.type());
      std::vector<uni10::Qnum> Qnums = bond.const_getQnums();
      int NumQnum = Qnums.size();
      SaveNumber(gname, "NumQnum", NumQnum);
      std::vector<int> Qdegs = bond.const_getQdegs();
      SaveStdVector(gname, "Qdegs", Qdegs);
      for (int q = 0; q < Qnums.size(); q++) {
          std::string setname = "Qnum-";
          setname.append(std::to_string((unsigned long long)q));
          SaveQnum(gname, setname, Qnums.at(q).U1(), Qnums.at(q).prt(), Qnums.at(q).prtF());
      }
    }
    gname = GroupName;
    gname.append("/Block");
    size_t ElemNum = Ten.ElemNum();
    SaveNumber(gname, "ElemNum", ElemNum);
    SaveRawBuffer(gname, "U_elem", ElemNum, Ten.GetElem());
  }
  template void HDF5IO::SaveTensor(const std::string& GroupName, const uni10::UniTensor<double> Ten);
  template void HDF5IO::SaveTensor(const std::string& GroupName, const uni10::UniTensor<std::complex<double> > Ten);

  template<typename T>
  void HDF5IO::LoadTensor(const std::string& GroupName, uni10::UniTensor<T>& Ten){
    std::string gname = GroupName;
    gname.append("/Bonds");
    std::vector<int> labels;
    LoadStdVector(gname, "Labels", labels);
    int BondNum;
    LoadNumber(gname, "BondNum", BondNum);
    std::vector<uni10::Bond> bonds;
    for ( size_t b = 0; b < BondNum; b++){
      gname = GroupName;
      gname.append("/Bonds/bond-");
      gname.append(std::to_string((unsigned long long)b));
      int NumQnum;
      LoadNumber(gname, "NumQnum", NumQnum);
      std::vector<int> Qdegs;
      LoadStdVector(gname, "Qdegs", Qdegs);
      std::vector<uni10::Qnum> Qnums;
      for ( size_t q = 0; q < NumQnum; q++){
        std::string setname = "Qnum-";
        setname.append(std::to_string((unsigned long long)q));
        int _U1;
        uni10::parityType _pt;
        uni10::parityFType _ptf;
        LoadQnum(gname, setname, _U1, _pt, _ptf);
        uni10::Qnum qnum(_ptf, _U1, _pt);
        for ( size_t d = 0; d < Qdegs.at(q); d++){
          Qnums.push_back(qnum);
        }
      }
      uni10::bondType _bt;
      LoadBondType(gname, "BondType", _bt);
      bonds.push_back(uni10::Bond(_bt, Qnums));
    }
    Ten.Assign(bonds);
    Ten.SetLabel(labels);
    gname = GroupName;
    gname.append("/Block");
    T* U_elem;
    size_t ElemNum;
    LoadNumber(gname, "ElemNum", ElemNum);
    LoadRawBuffer(gname, "U_elem", ElemNum, U_elem);
    Ten.SetElem(U_elem);
  }
  template void HDF5IO::LoadTensor(const std::string& GroupName, uni10::UniTensor<double>& Ten);
  template void HDF5IO::LoadTensor(const std::string& GroupName, uni10::UniTensor<std::complex<double> >& Ten);
}
