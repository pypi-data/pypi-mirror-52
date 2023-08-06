#
#  @file CMakeLists.txt
#  @license
#    Copyright (c) 2013-2017
#    National Taiwan University
#    National Tsing-Hua University
#
#    This file is part of Uni10, the Universal Tensor Network Library.
#
#    Uni10 is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Uni10 is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with Uni10.  If not, see <http://www.gnu.org/licenses/>.
#  @endlicense
#  @brief Main specification file for CMake
#  @author Ying-Jer Kao
#  @date 2014-05-06
#  @since 0.1.0
#
cmake_minimum_required(VERSION 2.8.0 FATAL_ERROR)


######################################################################
### ADD SOURCE FILES
######################################################################

set(uni10_api_sources 
  Block.cpp
  Bond.cpp
  Matrix_Auxiliary.cpp
  Matrix.cpp
  Qnum.cpp
  UniTensor_Auxiliary.cpp
  UniTensor.cpp
  uni10_linalg_inplace/uni10_linalg_inplace_dot.cpp
  #uni10_linalg_inplace/uni10_hirnk_linalg_inplace_contractargs.cpp
  tensor_tools/tensor_tools.cpp
  Network.cpp 
  network_tools/network_tools.cpp
  network_tools/node.cpp
  network_tools/layer.cpp
  network_tools/netorder.cpp
  network_tools/pseudotensor.cpp
  )
add_library(uni10-api OBJECT ${uni10_api_sources})
  
