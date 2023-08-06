/****************************************************************************
 *  @file UniTensor.h
 *  @license
 *   Universal Tensor Network Library
 *   Copyright (c) 2013-2014
 *   National Taiwan University
 *   National Tsing-Hua University
 *
 *   This file is part of Uni10, the Universal Tensor Network Library.
 *
 *   Uni10 is free software: you can redistribute it and/or modify
 *   it under the terms of the GNU Lesser General Public License as published by
 *   the Free Software Foundation, either version 3 of the License, or
 *   (at your option) any later version.
 *
 *   Uni10 is distributed in the hope that it will be useful,
 *   but WITHOUT ANY WARRANTY; without even the implied warranty of
 *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *   GNU Lesser General Public License for more details.
 *
 *   You should have received a copy of the GNU Lesser General Public License
 *   along with Uni10.  If not, see <http://www.gnu.org/licenses/>.
 *  @endlicense
 *  @brief Header file for UniTensor class
 *  @author Yun-Da Hsieh
 *  @author Yun-Hsuan Chou
 *  @date 2014-05-06
 *  @since 0.1.0
 *
 *****************************************************************************/
#ifndef __UNI10_UNITENSOR_H__
#define __UNI10_UNITENSOR_H__

#include <string>

#include "uni10_api/Matrix.h"
#include "uni10_api/UniTensor_para.h"
#include "uni10_api/network_tools/network_tools.h"

/// @brief Uni10 - the Universal Tensor %Network Library
namespace uni10{

  enum contain_type{
    no_sym    = 0,
    bs_sym   = 1,
    fm_sym   = 2,
    spar_sym  = 3
  };

  struct nsy_paras;

  template<typename UniType>
    class UniTensor;


  template<typename UniType>
    std::ostream& operator<< (std::ostream& os, const UniTensor<UniType>& _b);

  template<typename UniType>
    UniTensor<UniType> operator*(const UniTensor<UniType>& Ta, uni10_double64 a);

  template<typename UniType>
    UniTensor<uni10_complex128> operator*(const UniTensor<UniType>& Ta, uni10_complex128 a);

  template<typename UniType>
    UniTensor<UniType> operator*(uni10_double64 a, const UniTensor<UniType>& Ta);

  template<typename UniType>
    UniTensor<uni10_complex128> operator*(uni10_complex128 a, const UniTensor<UniType>& Ta);

  // UniTensor element-wise addition.
  template<typename T>
    UniTensor<T> operator+(const UniTensor<uni10_double64>& t1, const UniTensor<T>& t2);

  template<typename T>
    UniTensor<uni10_complex128> operator+(const UniTensor<uni10_complex128>& t1, const UniTensor<T>& t2);

  // UniTensor element-wise subtract.
  template<typename T>
    UniTensor<T> operator-(const UniTensor<uni10_double64>& t1, const UniTensor<T>& t2);

  template<typename T>
    UniTensor<uni10_complex128> operator-(const UniTensor<uni10_complex128>& t1, const UniTensor<T>& t2);

  UniTensor<uni10_complex128> operator-(const UniTensor<uni10_double64>& t1, const UniTensor<uni10_complex128>& t2);

  UniTensor<uni10_complex128>& operator+=(UniTensor<uni10_complex128>& _m1, const UniTensor<uni10_double64>& _m2);

  UniTensor<uni10_complex128>& operator-=(UniTensor<uni10_complex128>& _m1, const UniTensor<uni10_double64>& _m2);

  UniTensor<uni10_complex128>& operator*=(UniTensor<uni10_complex128>& _m1, uni10_complex128 a);

  /// @class UniTensor
  /// @brief The UniTensor class defines the symmetric tensors
  ///
  /// A UniTensor consists of Bond's carrying quantum numbers Qnum's. The tensor elements are organized as
  /// quantum number blocks. The Qnum's on the Bonds defines the size of the Qnum blocks and the rank of
  /// UniTensor is defined by the number of Bond's.\par
  /// Each Bond carries a label. Labels are used to manipulate tensors, such as in permute, partialTrace and
  /// contraction. \par
  /// Operations on tensor elements is pefromed through  getBlock and putBlock functions to take out/put in
  /// block elements out as a Matrix.
  /// @see Qnum, Bond, Matrix< UniType >

  template <typename UniType>
    class UniTensor {

      private:

        contain_type style;
        struct U_para<UniType>* paras;

        void init_para();
        void meta_link();
        void copy_para(U_para<UniType>* src_para);
        void init();
        void check_status();
        void initBlocks();
        void free_para();
        void init_paras_null();
        contain_type check_bonds(const std::vector<Bond>& _bonds)const;

        // General variables.
        std::string* name;
        std::vector<Bond>* bonds;
        std::vector<uni10_int>* labels;
        uni10_int*  RBondNum;       //Row bond number
        uni10_uint64* RQdim;
        uni10_uint64* CQdim;
        uni10_uint64* U_elemNum;
        std::map< Qnum, Block<UniType> >* blocks;
        UELEM(UniElem, _package, _type)<UniType>* U_elem;     // pointer to a real matrix
        uni10_int*  status;     //Check initialization, 1 initialized, 3 initialized with label, 5 initialized with elements

        static uni10_int COUNTER;
        static uni10_uint64 ELEMNUM;
        static uni10_uint64 MAXELEMNUM;
        static uni10_uint64 MAXELEMTEN;               //Max number of element of a tensor

        static const uni10_int HAVEBOND = 1;        /**< A flag for initialization */
        static const uni10_int HAVEELEM = 2;        /**< A flag for having element assigned */

      public:

        static uni10_int GET_HAVEBOND(){return HAVEBOND;};
        static uni10_int GET_HAVEELEM(){return HAVEELEM;};      /**< A flag for having element assigned */
        static uni10_int GET_COUNTER(){return COUNTER;}
        static uni10_uint64 GET_ELEMNUM(){return ELEMNUM;}
        static uni10_uint64 GET_MAXELEMNUM(){return MAXELEMNUM;};
        static uni10_uint64 GET_MAXELEMTEN(){return MAXELEMTEN;};

        ///
        /// @brief Default Constructor
        ///
        explicit UniTensor();
        /// @brief Create a rank-0 UniTensor with value \c val
        ///
        /// @param val Value of the scalar
        explicit UniTensor(UniType val, const contain_type s = no_sym);

        /// @brief Create a UniTensor from a list of Bond's
        /// @param _bonds List of bonds
        /// @param _name Name of the tensor, defaults to ""
        explicit UniTensor(const std::vector<Bond>& _bonds, const std::string& _name = "");

        /// @brief Create a UniTensor from a list of Bond's and assign labels
        /// @param _bonds List of bonds
        /// @param labels Labels for \c _bonds
        /// @param _name Name of the tensor, defaults to ""
        explicit UniTensor(const std::vector<Bond>& _bonds, int* labels, const std::string& _name = "");

        /// @brief Create a UniTensor from a list of Bond's and assign labels
        /// @param _bonds List of bonds
        /// @param labels Labels for \c _bonds
        /// @param _name Name of the tensor, defaults to ""
        explicit UniTensor(const std::vector<Bond>& _bonds, std::vector<int>& labels, const std::string& _name = "");

        //explicit UniTensor(const std::string& fname);

        /// @brief Create a UniTensor from a Block< UniType >
        explicit UniTensor(const Block<UniType>& UniT);

        /// @brief Copy constructor
        UniTensor(const UniTensor& UniT);

        template <typename U>
          UniTensor(const UniTensor<U>& UniT);

        /// @brief Construct tensor from a stored one.
        ///
        /// @param fname Path to the stored tensor
        UniTensor(const std::string& fname);

        /// @brief Destructor
        ///
        /// Destroys the UniTensor and freeing all allocated memory
        ~UniTensor();

        U_para<UniType>* get_paras_enforce(){
          return this->paras;
        };

        uni10_int get_status_enforce(){
            return this->status[0];
        };

        UELEM(UniElem, _package, _type)<UniType>* get_U_elem_enforce(){
            return this->U_elem;
        };

        contain_type get_style_enforce(){
            return this->style;
        };


        #ifdef UNI_HDF5
        /// @brief Save the tensor in HDF5 format.
        ///
        /// @param fname Path where the tensor will be stored
        /// @param gname Group name inside the HDF5 file for the tensor to be stored
        /// @param Override The file will be forced open and override
        void H5Save(const std::string& fname, const std::string& gname="/", const bool& Override=false) const;
        #endif
        /// @brief Save the tensor.
        ///
        /// @param fname Path where the tensor will be stored
        void Save(const std::string& fname) const;

        #ifdef UNI_HDF5
        /// @brief Load a tensor from HDF5 file and replace current object.
        ///
        /// @param fname Path where the tensor load
        void H5Load(const std::string& fname, const std::string& gname);
        #endif
        /// @brief Load a tensor and replace current object.
        ///
        /// @param fname Path where the tensor load
        void Load(const std::string& fname);
        void LoadOldVer(const std::string& fname, const contain_type& type, const std::string& version);

        /// @brief Set all tensor elements to \c 0.
        void Zeros();

        /// @brief Set elements of given block to \c 0.
        ///
        /// @param qnum Quntum number associated with the block being set to \c 0
        void Zeros(const Qnum& qnum);

        /// @brief Set all tensor elements to \c 1.
        void Ones();

        /// @brief Set elements of given block to \c 1.
        ///
        /// @param qnum Quntum number associated with the block being set to \c 1
        void Ones(const Qnum& qnum);

        /// @brief Set the whole block to identity matrix.
        void Identity();

        /// @brief Set given block to identity matrix.
        ///
        /// @param qnum Quntum number associated with the block being set to identity matrix
        void Identity(const Qnum& qnum);

        /// @brief Set the tensor by random element.
        ///
        /// Set the tensor element by random values with specific distribution.
        /// @param UorN Set to 'U' for uniform distribution; set to 'N' for normal distribution; default to 'U'
        /// @param dn_mu Lower bound for uniform distribution mean for normal distribution
        /// @param up_var Upper bound for uniform distribution variance for normal distribution
        void Randomize(char UorN='U', uni10_double64 dn_mu=-1, uni10_double64 up_var=1, uni10_int64 seed=uni10_clock);

        /// @brief Set given block by random element.
        ///
        /// Set the element of given block by random values by specific distribution.
        /// @param qnum Quntum number associated with the block being randomize
        /// @param UorN Set to 'U' for uniform distribution; set to 'N' for normal distribution; default to 'U'
        /// @param dn_mu Lower bound for uniform distribution; mean for normal distribution
        /// @param up_var Upper bound for uniform distribution; variance for normal distribution
        void Randomize(const Qnum& qnum, char UorN='U', uni10_double64 dn_mu=-1, uni10_double64 up_var=1, uni10_int64 seed=uni10_clock );

        /// @brief Set the whole block by a matrix with random orthogonal columns.
        ///
        /// The orthogonal columns will obtain by orthogonalize a random block with the element given by specific distribution.
        /// @param UorN Set to 'U' for uniform distribution; set to 'N' for normal distribution; default to 'U'
        /// @param dn_mu Lower bound for uniform distribution; mean for normal distribution
        /// @param up_var Upper bound for uniform distribution; variance for normal distribution
        void OrthoRand(char UorN='U', uni10_double64 dn_mu=-1, uni10_double64 up_var=1, uni10_int64 seed=uni10_clock);

        /// @brief Set a given block by a matrix with random orthogonal columns.
        ///
        /// The orthogonal columns will obtain by orthogonalize a random block with the element given by specific distribution.
        /// @param qnum Quntum number associated with the block being randomize
        /// @param UorN Set to 'U' for uniform distribution; set to 'N' for normal distribution; default to 'U'
        /// @param dn_mu Lower bound for uniform distribution; mean for normal distribution
        /// @param up_var Upper bound for uniform distribution; variance for normal distribution
        void OrthoRand(const Qnum& qnum, char UorN='U', uni10_double64 dn_mu=-1, uni10_double64 up_var=1, uni10_int64 seed=uni10_clock );

        /// @brief Assign elements to a block
        ///
        /// Assigns elements of the  matrix \c mat to the  block of quantum number \c qnum, replacing the origin
        /// elements. \par
        /// If \c mat is diagonal, all the off-diagonal elements are set to zero.
        /// @param mat The matrix elements to be assigned
        void PutBlock(const Block<UniType>& mat);

        /// @brief Assign elements to a block
        ///
        /// Assigns elements of the  matrix \c mat to the  Qnum(0) block, for non-symmetry tensors.
        ///
        /// If \c mat is diagonal,  all the off-diagonal elements are set to zero.
        /// @param qnum quantum number of the block
        /// @param mat The matrix elements to be assigned
        void PutBlock(const Qnum& qnum, const Block<UniType>& mat);

        /// @brief Access labels
        ///
        /// Returns the labels of the bonds in UniTensor< UniType >
        ///
        /// @return List of labels
        std::vector<int> label()const{return *labels;};

        /// @brief Access label
        ///
        /// Access the label of Bond \c idx
        /// @param idx Bond index
        /// @return Label of Bond \c idx
        uni10_int label(size_t idx)const{return (*labels)[idx];};

        /// @brief Access name
        ///
        /// Return the name of the UniTensor< UniType >.
        std::string GetName() const{return *name;};

        /// @brief Assign name
        ///
        /// Assigns name to the UniTensor< UniType >.
        /// @param name Name to be assigned
        void SetName(const std::string& _name);

        /// @brief Get all Blocks in UniTensor.
        ///
        /// @return Qnum and associated Block.
        const std::map<Qnum, Block<UniType> >& ConstGetBlocks()const{return *blocks;};

        /// @brief Access the number of bonds
        ///
        /// @return Number of bonds
        uni10_uint64 BondNum()const{return bonds->size();};

        /// @brief Access the number of incoming bonds
        ///
        /// @return Number of incoming bonds
        uni10_uint64 InBondNum()const{return *RBondNum;};

        /// @brief Access bonds
        ///
        /// Returns the bonds in UniTensor
        /// @return List of bonds
        std::vector<Bond> bond()const{return *bonds;};

        /// @brief Access bond
        ///
        /// Returns the bond at the position \c idx
        /// @param idx Position of the bond being retrieved
        /// @return A bond
        Bond bond(uni10_uint64 idx)const{return (*bonds)[idx];};

        /// @brief Access the number of elements
        ///
        /// Returns the number of total elements of the blocks.
        /// @return  Number of elements
        uni10_uint64 ElemNum()const{return (*U_elemNum); };

        uni10_uint64 TypeId()const{return (U_elem->uni10_typeid_); };

        /// @brief Access the number of blocks
        ///
        /// Returns the number of blocks
        /// @return The number of blocks
        uni10_uint64 BlockNum()const{return blocks->size();};

        /// @brief Get the pointer to the array of tensor elements.
        UniType* GetElem()const{return U_elem->elem_ptr_; }

        Matrix<UniType> GetRawElem()const;

        /// @brief Get elements in a block
        ///
        /// Returns elements of Qnum(0) Block.
        /// @return The Qnum(0) Block
        const Block<UniType>& ConstGetBlock()const;

        /// @brief Get elements in a block
        ///
        /// Returns elements of \c qnum block.
        /// @return The \c qnum  Block
        const Block<UniType>& ConstGetBlock(const Qnum& qnum)const;

        /// @brief Assign label to a bond in UniTensor.
        ///
        /// Assigns the label to given bond of UniTensor, replacing the origin label on the bond.
        /// @param newLabel New label
        /// @param idx Position of the bond
        void SetLabel(const uni10_int newLabel, const uni10_uint64 idx);

        /// @brief Assign labels to bonds in UniTensor
        ///
        /// Assigns the labels \c newLabels to each bond of  UniTensor, replacing the origin labels on the bonds.
        /// @param newLabels Array of labels
        void SetLabel(const std::vector<uni10_int>& newLabels);

        /// @overload
        void SetLabel(uni10_int* newLabels);

        /// check if containing these labels
        bool ContainLabels(const std::vector<uni10_int>& subLabels);
        bool ContainLabels(const _Swap swap);

        /// @brief Access block quantum numbers
        ///
        /// Returns the quantum numbers for all blocks in UniTensor.
        /// The return array of quantum numbers is in the ascending order defined in Qnum.
        /// @return Array of Qnum's
        std::vector<Qnum> BlocksQnum()const;

        /// @brief Access block quantum number
        ///
        /// Returns the quantum number for block \c idx in UniTensor.
        /// Blocks are orderd in the ascending order of Qnum
        /// @param idx Block index
        /// @return Quantum number of block \c idx
        Qnum BlockQnum(uni10_uint64 idx)const;

        std::map< Qnum, Matrix<UniType> > GetBlocks()const;

        /// @brief Get the whole block of the tensor.
        Matrix<UniType> GetBlock(bool diag = false)const;

        /// @brief Get given block of the tensor.
        ///
        /// @param qnum Quantum number associated with the block
        Matrix<UniType> GetBlock(const Qnum& qnum, bool diag = false)const;

        /// @brief Assign raw elements
        ///
        /// Assigns raw elements in \c blk to UniTensor.
        ///
        /// This function will reorganize the raw elements into the block-diagonal form.
        /// @param blk  Block of raw elements
        void SetRawElem(const Block<UniType>& blk);

        /// @overload
        void SetRawElem(const UniType* rawElem);

        /// @overload
        void SetRawElem(const std::vector<UniType>& rawElem);

        /// @brief Assign elements to the whole Block.
        ///
        /// This function will assign element directly to the whole Block.
        /// @param _elem Pointer to the array of the elements.
        void SetElem(const UniType* _elem);

        /// @overload
        void SetElem(const std::vector<UniType>& _elem);

        /// @brief Assign a list of Bonds to UniTensor.
        ///
        /// The content of UnTensor will be remove.
        /// @param _bond List of Bonds
        UniTensor& Assign(const std::vector<Bond>& _bond);

        /// @brief Combine specific bonds to one bonds.
        ///
        /// Combine a list of bonds to one bond. The bonds to be combined will be permute to the order specified in the list.
        /// The result tensor will have one bond with first label in the list in replace of combined bonds.
        /// @param combined_labels Labels of bonds to be combined
        UniTensor& CombineBond(const std::vector<uni10_int>& combined_labels);

        /// @overload
        ///
        /// @param combined_labels Labels of bonds to be combined
        /// @param bonudNum Number of bonds to be combined
        UniTensor& CombineBond(uni10_int* combined_labels, uni10_int boundNum);

        /// @brief Get specific element of the tensor.
        ///
        /// @params idxs The position of the element.
        /// @return The value of given element
        UniType At(const std::vector<uni10_uint64>& idxs) const;

        void AddGate(const std::vector<_Swap>& swaps);

        std::vector<_Swap> ExSwap(const UniTensor<uni10_double64>& Tb)const;

        std::vector<_Swap> ExSwap(const UniTensor<uni10_complex128>& Tb)const;

        /// bonds to_cross must be in consecutive order in label()
        void ApplySwapGate(uni10_int to_permute, const std::vector<uni10_int>& to_cross, bool permute_back = false);
        void ApplySwapGate(uni10_int to_permute, uni10_int to_cross, bool permute_back = false);
        void ApplySwapGate(_Swap to_swap, bool permute_back = false);

        /// @brief Print the diagrammatic representation of UniTensor< UniType >
        ///
        /// Prints out the diagrammatic representation of UniTensor \c uT as (for example):
        /// @code
        ///**************** Demo ****************
        ///     ____________
        ///    |            |
        ///0___|3          3|___2
        ///    |            |
        ///1___|3          3|___3
        ///    |            |
        ///    |____________|
        ///
        ///**************************************
        /// @endcode
        void PrintDiagram()const;

        std::string PrintRawElem(bool print=true)const;

        static std::string Profile(bool print = true);

        void SetStyle(const contain_type s);

        void Clear();

        UniTensor& operator=(UniTensor const& UniT);

        template<typename U>
          UniTensor& operator=(UniTensor<U> const& UniT);

        UniTensor<UniType>& operator+=( const UniTensor<UniType>& Tb );

        UniTensor<UniType>& operator-=( const UniTensor<UniType>& Tb );

        UniTensor& operator*= (uni10_double64 a);

        //friend UniTensor operator*(const UniTensor& Ta, const UniTensor& Tb);
        UniType operator[](uni10_uint64 idx)const{
          uni10_error_msg(!(idx < (*U_elemNum)), "Index exceeds the number of elements( %ld ).", *U_elemNum);
          return U_elem->elem_ptr_[idx];
        }

        /// @brief Print out UniTensor
        ///
        /// Prints out a UniTensor \c uT as(for example):
        /// @code
        ///**************** Demo ****************
        ///     ____________
        ///    |            |
        ///0___|3          3|___2
        ///    |            |
        ///1___|3          3|___3
        ///    |            |
        ///    |____________|
        ///
        ///================BONDS===============
        ///IN : (U1 = 1, P = 0, 0)|1, (U1 = 0, P = 0, 0)|1, (U1 = -1, P = 0, 0)|1, Dim = 3
        ///IN : (U1 = 1, P = 0, 0)|1, (U1 = 0, P = 0, 0)|1, (U1 = -1, P = 0, 0)|1, Dim = 3
        ///OUT: (U1 = 1, P = 0, 0)|1, (U1 = 0, P = 0, 0)|1, (U1 = -1, P = 0, 0)|1, Dim = 3
        ///OUT: (U1 = 1, P = 0, 0)|1, (U1 = 0, P = 0, 0)|1, (U1 = -1, P = 0, 0)|1, Dim = 3
        ///
        ///===============BLOCKS===============
        ///--- (U1 = -2, P = 0, 0): 1 x 1 = 1
        ///
        ///0.840
        ///
        ///--- (U1 = -1, P = 0, 0): 2 x 2 = 4
        ///
        ///0.394  0.783
        ///
        ///0.798  0.912
        ///
        ///--- (U1 = 0, P = 0, 0): 3 x 3 = 9
        ///
        ///0.198  0.335  0.768
        ///
        ///0.278  0.554  0.477
        ///
        ///0.629  0.365  0.513
        ///
        ///--- (U1 = 1, P = 0, 0): 2 x 2 = 4
        ///
        ///0.952  0.916
        ///
        ///0.636  0.717
        ///
        ///--- (U1 = 2, P = 0, 0): 1 x 1 = 1
        ///
        ///0.142
        ///
        ///Total elemNum: 19
        ///***************** END ****************
        /// @endcode
        ///  In the above example, \c uT has four bonds with default labels [0, 1, 2, 3]. The bonds 0 and 1 are
        /// incoming bonds, and  2, 3 are out-going bonds. Each bond has three states
        /// corresponding to three U1 quantum number [-1, 0, 1]. The block elements of the
        /// tensor are als shown. There are five blocks of various <tt>U1= [-2, -1, 0, 1, 2]</tt> and
        /// various sizes. The total element number is 19.
        friend std::ostream& operator<< <>(std::ostream& os, const UniTensor& _b);  // --> uni10_elem().print_elem()

        template<typename _UniType>
          friend UniTensor<_UniType> operator*(const UniTensor<_UniType>& Ta, uni10_double64 a);

        template<typename _UniType>
          friend UniTensor<uni10_complex128> operator*(const UniTensor<_UniType>& Ta, uni10_complex128 a);

        template<typename _UniType>
          friend UniTensor<_UniType> operator*(uni10_double64 a, const UniTensor<_UniType>& Ta);

        template<typename _UniType>
          friend UniTensor<uni10_complex128> operator*(uni10_complex128 a, const UniTensor<_UniType>& Ta);

        // UniTensor element-wise addition.
        template<typename _T>
          friend UniTensor<_T> operator+(const UniTensor<uni10_double64>& t1, const UniTensor<_T>& t2);

        template<typename _T>
          friend UniTensor<uni10_complex128> operator+(const UniTensor<uni10_complex128>& t1, const UniTensor<_T>& t2);

        // UniTensor element-wise subtract.
        template<typename _T>
          friend UniTensor<_T> operator-(const UniTensor<uni10_double64>& t1, const UniTensor<_T>& t2);

        template<typename _T>
          friend UniTensor<uni10_complex128> operator-(const UniTensor<uni10_complex128>& t1, const UniTensor<_T>& t2);

        friend UniTensor<uni10_complex128>& operator+=(UniTensor<uni10_complex128>& _m1, const UniTensor<uni10_double64>& _m2);

        friend UniTensor<uni10_complex128>& operator-=(UniTensor<uni10_complex128>& _m1, const UniTensor<uni10_double64>& _m2);

        friend UniTensor<uni10_complex128>& operator*=(UniTensor<uni10_complex128>& _m1, uni10_complex128 a);
        // The prototypes of high-rank linear algebras.
        template<typename _UniType>
          friend void Permute( UniTensor<_UniType>& Tout, const UniTensor<_UniType>& T, const std::vector<uni10_int>& newLabels, uni10_int inBondNum, UNI10_INPLACE on);

        template<typename _UniType>
          friend void Permute( UniTensor<_UniType>& T, const std::vector<uni10_int>& newLabels, uni10_int inBondNum, UNI10_INPLACE on);

        template<typename _UniType>
          friend void PseudoPermute( UniTensor<_UniType>& Tout, const UniTensor<_UniType>& T, const std::vector<uni10_int>& newLabels, uni10_int inBondNum, UNI10_INPLACE on);

        template<typename _UniType>
          friend void PseudoPermute( UniTensor<_UniType>& T, const std::vector<uni10_int>& newLabels, uni10_int inBondNum, UNI10_INPLACE on);

        template<typename _To, typename _T, typename _U>
          friend void Contract( UniTensor<_To>& t3, const UniTensor<_T>& t1, const UniTensor<_U>& t2, UNI10_INPLACE on);

        template<typename _To, typename _T, typename _U>
          friend void PseudoContract( UniTensor<_To>& t3, const UniTensor<_T>& t1, const UniTensor<_U>& t2, UNI10_INPLACE on);

        template<typename _UniType>
          friend void Transpose( UniTensor<_UniType>& Tout, const UniTensor<_UniType>& Tin, UNI10_INPLACE on );

        template<typename _UniType>
          friend void Dagger( UniTensor<_UniType>& Tout, const UniTensor<_UniType>& Tin, UNI10_INPLACE on );

        template<typename _UniType>
          friend void Conj( UniTensor<_UniType>& Tout, const UniTensor<_UniType>& Tin, UNI10_INPLACE on );

        template<typename _UniType>
          friend void PartialTrace(UniTensor<_UniType>& Tout, const UniTensor<_UniType>& Tin, uni10_int la, uni10_int lb, UNI10_INPLACE on);

        template<typename _UniType>
          friend UniTensor<_UniType> Permute( const UniTensor<_UniType>& T, const std::vector<uni10_int>& newLabels, uni10_int inBondNum);

        template<typename _UniType>
          friend UniTensor<_UniType> Permute( const UniTensor<_UniType>& T, uni10_int* newLabels, uni10_int inBondNum);

        template<typename _UniType>
          friend UniTensor<_UniType> Permute( const UniTensor<_UniType>& T, uni10_int rowBondNum);

        template<typename _UniType>
          friend UniTensor<_UniType> PseudoPermute( const UniTensor<_UniType>& T, const std::vector<uni10_int>& newLabels, uni10_int inBondNum);

        template<typename _UniType>
          friend UniTensor<_UniType> PseudoPermute( const UniTensor<_UniType>& T, uni10_int* newLabels, uni10_int inBondNum);

        template<typename _UniType>
          friend UniTensor<_UniType> PseudoPermute( const UniTensor<_UniType>& T, uni10_int rowBondNum);

        template<typename _UniType>
          friend UniTensor<_UniType> PartialTrace( const UniTensor<_UniType>& Tin, uni10_int la, uni10_int lb );

        template<typename _UniType>
          friend _UniType Trace( const UniTensor<_UniType>& Tin );

        template<typename _UniType>
          friend void Hosvd(UniTensor<_UniType>& Tin, uni10_int* group_labels, uni10_int* groups, uni10_uint64 groupsSize,
              std::vector<UniTensor<_UniType> >& Us, UniTensor<_UniType>& S, std::vector<std::map<Qnum, Matrix<_UniType> > >& Ls, UNI10_INPLACE on);

        template<typename _UniType>
          friend void Hosvd(UniTensor<_UniType>& Tin, uni10_int* group_labels, uni10_int* groups, uni10_uint64 groupsSize,
              std::vector<UniTensor<_UniType> >& Us, UniTensor<_UniType>& S, std::vector<Matrix<_UniType> >& Ls, UNI10_INPLACE on);

        //bool similar(const UniTensor& Tb)const;
        //bool elemCmp(const UniTensor& UniT)const;

        template <typename _UniType>
          friend class UniTensor;

        friend class Network;


    };

  template <typename UniType>
    uni10_int UniTensor<UniType>::COUNTER = 0;

  template <typename UniType>
    uni10_uint64 UniTensor<UniType>::ELEMNUM = 0;

  template <typename UniType>
    uni10_uint64 UniTensor<UniType>::MAXELEMNUM = 0;

  template <typename UniType>
    uni10_uint64 UniTensor<UniType>::MAXELEMTEN = 0;

  template<typename UniType>
    std::ostream& operator<< (std::ostream& os, const UniTensor<UniType>& UniT){

      if(UniT.paras == NULL){
          std::cout<<"This UniTensor has not been initialized."<< std::endl;
          std::cout <<"Status: " << *UniT.status << std::endl;
          return os;
      }

      char buf[128];
      if(!(*(UniT.status) & UniT.HAVEBOND)){
        if(UniT.U_elem->ongpu_)
          std::cout<<"\nScalar: " << UniT.U_elem->elem_ptr_[0]<<", onGPU";
        else{
          sprintf(buf, "\nScalar: %0.10f", UniT.U_elem->elem_ptr_[0]);
          std::cout << buf;
          /*
          std::cout.precision(10);
          std::cout.setf(std::ios::fixed, std::ios::floatfield);
          std::cout<<"\nScalar: " << UniT.U_elem->elem_ptr_[0];
          */
        }
        std::cout<< "\n" << std::endl;
        return os;
      }

      uni10_uint64 row = 0;
      uni10_uint64 col = 0;

      std::vector<Bond>bonds = (*UniT.bonds);
      for(uni10_uint64 i = 0; i < bonds.size(); i++)
        if(bonds[i].type() == BD_IN)
          row++;
        else
          col++;
      uni10_uint64 layer = std::max(row, col);
      uni10_uint64 nmlen = UniT.name->length() + 2;
      uni10_int star = 12 + (14 - nmlen) / 2;
      std::cout << std::endl;
      for(uni10_int s = 0; s < star; s++)
        std::cout << "*";
      if(UniT.name->length() > 0)
        std::cout << " " << (*UniT.name) << " ";
      for(uni10_int s = 0; s < star; s++)
        std::cout <<"*";
      std::cout<<std::endl;

      if(UniT.U_elem->uni10_typeid_ == 1){
        std::cout <<"REAL(" << UniT.style << ")" << std::endl;
        //std::cout <<"Status: " << *UniT.status << "; Status Address: " << UniT.status << std::endl;
      }
      else if(UniT.U_elem->uni10_typeid_ == 2){
        std::cout <<"COMPLEX(" << UniT.style << ")" << std::endl;
        //std::cout <<"Status: " << *UniT.status << "; Status Address: " << UniT.status << std::endl;
      }

      if(UniT.U_elem->ongpu_)
        std::cout<<"\n                 onGPU";
      std::cout << "\n             ____________\n";
      std::cout << "            |            |\n";
      uni10_uint64 llab = 0;
      uni10_uint64 rlab = 0;
      //char buf[128];
      for(uni10_uint64 l = 0; l < layer; l++){
        if(l < row && l < col){
          llab = (*UniT.labels)[l];
          rlab = (*UniT.labels)[row + l];
          sprintf(buf, "    %5ld___|%-4d    %4d|___%-5ld\n", llab, bonds[l].dim(), bonds[row + l].dim(), rlab);
          std::cout<<buf;
        }
        else if(l < row){
          llab = (*UniT.labels)[l];
          sprintf(buf, "    %5ld___|%-4d    %4s|\n", llab, bonds[l].dim(), "");
          std::cout<<buf;
        }
        else if(l < col){
          rlab = (*UniT.labels)[row + l];
          sprintf(buf, "    %5s   |%4s    %4d|___%-5ld\n", "", "", bonds[row + l].dim(), rlab);
          std::cout << buf;
        }
        std::cout << "            |            |   \n";
      }
      std::cout << "            |____________|\n";

      std::cout << "\n================BONDS===============\n";
      for(uni10_uint64 b = 0; b < bonds.size(); b++)
        std::cout << bonds[b];

      std::cout<<"\n===============BLOCKS===============\n";
      typename std::map<Qnum, Block<UniType> >::const_iterator it = UniT.blocks->begin();
      for (; it != UniT.blocks->end(); it++ ){
        std::cout << "--- " << it->first << ": ";// << Rnum << " x " << Cnum << " = " << Rnum * Cnum << " ---\n\n";
        if((*(UniT.status) & UniT.HAVEELEM))
          std::cout<<it->second;
        else
          std::cout<<it->second.row() << " x "<<it->second.col()<<": "<<it->second.ElemNum()<<std::endl<<std::endl;
      }
      std::cout << "Total elemNum: "<<(*UniT.U_elemNum)<<std::endl;
      std::cout << "====================================" << std::endl;
      os << "\n";
      return os;
    }

  template<typename UniType>
    UniTensor<UniType> operator*(const UniTensor<UniType>& Ta, uni10_double64 a){
      uni10_error_msg(!((*Ta.status) & Ta.HAVEELEM), "%s", "Cannot perform scalar multiplication on a tensor before setting its elements.");
      UniTensor<UniType> Tb(Ta);
      linalg_unielem_internal::VectorScal(&a, Tb.U_elem, &Tb.U_elem->elem_num_);
      return Tb;
    }

  template<typename UniType>
    UniTensor<uni10_complex128> operator*(const UniTensor<UniType>& Ta, uni10_complex128 a){
      uni10_error_msg(!((*Ta.status) & Ta.HAVEELEM), "%s", "Cannot perform scalar multiplication on a tensor before setting its elements.");
      UniTensor<uni10_complex128> Tb(Ta);
      linalg_unielem_internal::VectorScal(&a, Tb.U_elem, &Tb.U_elem->elem_num_);
      return Tb;
    }

  template<typename UniType>
    UniTensor<UniType> operator*(uni10_double64 a, const UniTensor<UniType>& Ta){return Ta*a;}

  template<typename UniType>
    UniTensor<uni10_complex128> operator*(uni10_complex128 a, const UniTensor<UniType>& Ta){return Ta*a;}

  template<typename T>
    UniTensor<T> operator+(const UniTensor<uni10_double64>& t1, const UniTensor<T>& t2){

      uni10_error_msg(t1.BondNum() != t2.BondNum(), "%s", "Cannot perform addition of two tensors having different bonds" );
      uni10_error_msg(!(*t1.bonds == *t2.bonds), "%s", "Cannot perform addition of two tensors having different bonds.");

      UniTensor<T> t3(t1);
      linalg_unielem_internal::VectorAdd(t3.U_elem, t2.U_elem, &t3.U_elem->elem_num_);
      return t3;

    };

  template<typename T>
    UniTensor<uni10_complex128> operator+(const UniTensor<uni10_complex128>& t1, const UniTensor<T>& t2){

      uni10_error_msg(t1.BondNum() != t2.BondNum(), "%s", "Cannot perform addition of two tensors having different bonds" );
      uni10_error_msg(!(*t1.bonds == *t2.bonds), "%s", "Cannot perform addition of two tensors having different bonds.");

      UniTensor<uni10_complex128> t3(t1);
      linalg_unielem_internal::VectorAdd(t3.U_elem, t2.U_elem, &t3.U_elem->elem_num_);
      return t3;

    };

  template<typename T>
    UniTensor<T> operator-(const UniTensor<uni10_double64>& t1, const UniTensor<T>& t2){

      uni10_error_msg(t1.BondNum() != t2.BondNum(), "%s", "Cannot perform addition of two tensors having different bonds" );
      uni10_error_msg(!(*t1.bonds == *t2.bonds), "%s", "Cannot perform addition of two tensors having different bonds.");

      UniTensor<T> t3(t1);
      linalg_unielem_internal::VectorSub(t3.U_elem, t2.U_elem, &t3.U_elem->elem_num_);
      return t3;

    };

  template<typename T>
    UniTensor<uni10_complex128> operator-(const UniTensor<uni10_complex128>& t1, const UniTensor<T>& t2){

      uni10_error_msg(t1.BondNum() != t2.BondNum(), "%s", "Cannot perform addition of two tensors having different bonds" );
      uni10_error_msg(!(*t1.bonds == *t2.bonds), "%s", "Cannot perform addition of two tensors having different bonds.");

      UniTensor<uni10_complex128> t3(t1);
      linalg_unielem_internal::VectorSub(t3.U_elem, t2.U_elem, &t3.U_elem->elem_num_);
      return t3;

    };

};

#endif
