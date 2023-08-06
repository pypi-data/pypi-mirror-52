/****************************************************************************
 *  @file Network.h
 *  @license
 *    Universal Tensor Network Library
 *    Copyright (c) 2013-2014
 *    National Taiwan University
 *    National Tsing-Hua University

 *
 *    This file is part of Uni10, the Universal Tensor Network Library.
 *
 *    Uni10 is free software: you can redistribute it and/or modify
 *    it under the terms of the GNU Lesser General Public License as published by
 *    the Free Software Foundation, either version 3 of the License, or
 *    (at your option) any later version.
 *
 *    Uni10 is distributed in the hope that it will be useful,
 *    but WITHOUT ANY WARRANTY; without even the implied warranty of
 *    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *    GNU Lesser General Public License for more details.
 *
 *    You should have received a copy of the GNU Lesser General Public License
 *    along with Uni10.  If not, see <http://www.gnu.org/licenses/>.
 *  @endlicense
 *  @brief Header file for Newtork class
 *  @author Yun-Da Hsieh
 *  @date 2014-05-06
 *  @since 0.1.0
 *
 *****************************************************************************/
#ifndef NETWORK_DEV_H
#define NETWORK_DEV_H

#include <utility>

#include "uni10_api/UniTensor.h"
#include "uni10_api/network_tools/layer.h"
#include "uni10_api/network_tools/netorder.h"

namespace uni10 {

  template<typename T>
    class UniTensor;

  class layer;

  class Node;

  class Network;

  std::ostream& operator<< (std::ostream& os, const Network& net);

  ///@class Network
  ///@brief The Network class defines the tensor networks
  ///
  /// A Network consists of connections which is specified by labels.
  /// To construct a network, prepare a file as the following example,
  ///
  ///     A: 1 2; 3 4
  ///     B: 3 4; 5 6
  ///     C: -1; 7 1
  ///     D: -2; 2 8
  ///     E: 7 5; -3
  ///     F: 6 8 -4
  ///     TOUT: -1 -2; -3 -4
  ///
  /// The first column specifies the labels of the tensors. The line starting with `TOUT` specifies the labels
  /// of the output tensor.
  /// Labels are separated by space or comma.  Incoming and outgoing labels are seperated by a semi-colon.
  ///
  /// @note The `TOUT:` line is required. If the result is a scalar, keep the line `TOUT:` without any labels.
  ///
  /// @see UniTensor
  class Network {

    public:

      /// @brief Construct Network
      ///
      /// Constructs a Network, initializing with the file \c fname. The file specifies the connections between
      /// tensors in the network.
      /// @param fname %Network filename
      Network(const std::string& fname);

      /// @brief Destructor
      ///
      /// Destroys Network and frees all the intermediate tensors.
      ~Network();

      void print_network()const;

      /// @brief Find the optimal contraction order of the Network.
      ///
      /// Should called after putting all tensors. This function will find the optimal contraction order but doesn't contract the tensors.
      void PreConstruct(bool force = true);

      /// @brief Assign tensor to Network.
      ///
      /// Assign UniTensor \c UniT to position \c idx in Network
      /// If \c force is set \c true, replace the tensor without reconstructing the pair-wise contraction sequence.
      /// @param idx Position of tensor in Network
      /// @param UniT A UniTensor
      /// @param force If set \true, replace without chaning the contraction sequence. Defaults to \c true.
      void PutTensor(int idx, const UniTensor<uni10_double64>& UniT, bool force = true);

      /// @overload
      void PutTensor(int idx, const UniTensor<uni10_complex128>& UniT, bool force = true);

      /// @brief Assign tensor to Network.
      ///
      /// Assign UniTensor \c UniT to position \c idx in Network
      /// If \c force is set \c true, replace the tensor without reconstructing the pair-wise contraction sequence.
      /// @param name Name of tensor in Network
      /// @param UniT A UniTensor
      /// @param force If set \true, replace without chaning the contraction sequence. Defaults to \c true.
      void PutTensor(const std::string& name, const UniTensor<uni10_double64>& UniT, bool force = true);

      /// @overload
      void PutTensor(const std::string& name, const UniTensor<uni10_complex128>& UniT, bool force = true);

      /// @brief Assign transpose of a tensor to Network.
      ///
      /// Assign the transpose of \c UniT to the position \c idx in Network.
      /// If \c force is set \c true, replace the tensor without reconstructing the pair-wise contraction sequence.
      /// @param idx Position of tensor in Network
      /// @param UniT A UniTensor
      /// @param force If set \true, replace without chaning the contraction sequence. Defaults to \c true.
      void PutTensorT(int idx, const UniTensor<uni10_double64>& UniT, bool force = true);

      /// @overload
      void PutTensorT(int idx, const UniTensor<uni10_complex128>& UniT, bool force = true);

      /// @brief Assign transpose of a tensor to Network.
      ///
      /// Assign the transpose of \c UniT to the position \c idx in Network.
      /// If \c force is set \c true, replace the tensor without reconstructing the pair-wise contraction sequence.
      /// @param name Name of tensor in Network
      /// @param UniT A UniTensor
      /// @param force If set \true, replace without chaning the contraction sequence. Defaults to \c true.
      void PutTensorT(const std::string& name, const UniTensor<uni10_double64>& UniT, bool force = true);

      /// @overload
      void PutTensorT(const std::string& name, const UniTensor<uni10_complex128>& UniT, bool force = true);

      /// @brief Assign complex conjugate of a tensor to Network.
      ///
      /// Assign complex conjugate of \c UniT to the position \c idx in Network.
      /// If \c force is set \c true, replace the tensor without reconstructing the pair-wise contraction sequence.
      /// @param idx Position of tensor in Network
      /// @param UniT A UniTensor
      /// @param force If set \true, replace without chaning the contraction sequence. Defaults to \c true.
      void PutTensorD(int idx, const UniTensor<uni10_double64>& UniT, bool force = true);

      /// @overload
      void PutTensorD(int idx, const UniTensor<uni10_complex128>& UniT, bool force = true);

      /// @brief Assign complex conjugate of a tensor to Network.
      ///
      /// Assign complex conjugate of \c UniT to the position \c idx in Network.
      /// If \c force is set \c true, replace the tensor without reconstructing the pair-wise contraction sequence.
      /// @param name Name of tensor in Network
      /// @param UniT A UniTensor
      /// @param force If set \true, replace without chaning the contraction sequence. Defaults to \c true.
      void PutTensorD(const std::string& name, const UniTensor<uni10_double64>& UniT, bool force = true);

      /// @overload
      void PutTensorD(const std::string& name, const UniTensor<uni10_complex128>& UniT, bool force = true);

      /// @brief Contract Network
      ///
      /// Performs contraction of tensors in Network with optimal order, returns a UniTensor named \c name.
      /// @param name Name of the result tensor
      /// @return A UniTensor
      void Launch(UniTensor<uni10_double64>& Tout, const std::string& Tname="");

      /// @overload
      void Launch(UniTensor<uni10_complex128>& Tout, const std::string& Tname="");

      std::string GetContractOrder() const;

      /// @brief Print the contraction order.
      ///
      /// Get the optimal contrction order obtain by PreConstruct or Launch.
      /// For example, the following Network
      ///
      ///     A: 1 2; 3 4
      ///     B: 3 4; 5 6
      ///     C: -1; 7 1
      ///     D: -2; 2 8
      ///     E: 7 5; -3
      ///     F: 6 8 -4
      ///     TOUT: -1 -2; -3 -4
      ///
      /// with all bonds have dimension 2 will yield the contraction order below:
      ///
      ///     L1N0
      ///     (16) __________
      ///       |           |
      ///       |           |
      ///     L0N1'         |
      ///     (16) ____     |
      ///       |     |     |
      ///       |     |     |
      ///     L0N2   L0N1  L0N0
      ///     (16)   (16)  (16)
      ///
      ///     L0N0       L0N1       L0N2
      ///     (16)____   (16)____   (16)____
      ///      |     |    |     |    |     |
      ///      |     |    |     |    |     |
      ///      E     C    F     D    B     A
      ///     (8)   (8)  (8)   (8)  (16)  (16)
      ///
      /// @note The optimal contraction order may vary for same Network file with different tensors put in it.
      /// @return A string indicates the optimal contraction order.
      friend std::ostream& operator<< (std::ostream& os, const Network& net);

      friend class layer;

      friend class Node;

      template<typename T>
        friend class UniTensor;

    private:

      // Name of the network file which can be written manually or generated from UNI10 GUI.
      std::string fname;

      //whether or not the network is ready for contraction, construct=> load=true, destruct=>load=false
      bool load, isChanged;

      // Tensor List.
      // For saving the pointers of UniTensors which are put in.
      // Under normal circumstance, these pointers have to keep in constant.
      std::vector< std::pair<const void*, int> > tensor_type;

      // whether or not the network has specific order.
      bool ordered;

      // Contraction order.
      std::vector<uni10_int> contract_order;

      // labels correspond to the tensor in the list.
      std::vector< std::vector<uni10_int> > label_arr;

      std::vector< uni10_int > iBondNums;

      // The name of each tenosr.
      std::vector<std::string> names;

      // To count the position index of each tensor in the network file.
      std::map<std::string, std::vector<uni10_int> > name2pos;

      // Swap gates.
      std::vector<_Swap> swap_gates;

      void FromFile_(const std::string& fname);

      // The structure of contraction B-tree.
      std::vector<layer*> contraction_layers;

      // pos2pos_int_tre[ten_idx_in_tensor_list][0] = layer idx, l.
      // pos2pos_int_tre[ten_idx_in_tensor_list][1] = node idx, n, in layer l.
      // pos2pos_int_tre[ten_idx_in_tensor_list][2] = idx, i, which is the idx of contraction order in node, n,.
      std::vector< std::vector<uni10_int> > pos2pos_in_tree;

      void PutTensorDriver_(int idx, const void* UniT, int typeID, bool force = true);

      // Initialize each layers in B-tree, which is a recursive function.
      void InitLayers_(uni10_int& idx_ly, std::vector<uni10_int>& _contrac_order, std::vector<uni10_int>& ori_ten_idx,
          std::vector<std::pair<const void*, int> >& _tens_type, std::vector<std::vector<uni10_int>* >& _label_arr, std::vector<std::string* >& _namas);

      // Construct contraction B-tree.
      void Construct_();

      // Destruct contraction B-tree.
      void Destruct_();

      void DestructTreeOnly_();

      //void InitSwapArrayInNodes_();

      //void DelSwapArrayInNodes_();

      //void AddSwap_();

  };

};  /* namespace uni10 */

#endif /* NETWORK<uni10_type>_H */
