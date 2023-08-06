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
### ADD SUB-DIRECTORIES
######################################################################

set(uni10_lapack_cpu_sources 
  uni10_elem_lapack_cpu.cpp
  linalg/uni10_elem_add.cpp
  linalg/uni10_elem_add_v.cpp
  linalg/uni10_elem_conj.cpp
  linalg/uni10_elem_dagger.cpp
  linalg/uni10_elem_det.cpp
  linalg/uni10_elem_dot.cpp
  linalg/uni10_elem_eig.cpp
  linalg/uni10_elem_eigh.cpp
  linalg/uni10_elem_exp_v.cpp
  linalg/uni10_elem_identity.cpp
  linalg/uni10_elem_inverse.cpp
  linalg/uni10_elem_ldq.cpp
  linalg/uni10_elem_lq.cpp
  linalg/uni10_elem_mul.cpp
  linalg/uni10_elem_mul_v.cpp
  linalg/uni10_elem_normalrandomize.cpp
  linalg/uni10_elem_norm.cpp
  linalg/uni10_elem_qdrcpivot.cpp
  linalg/uni10_elem_qdr.cpp
  linalg/uni10_elem_ql.cpp
  linalg/uni10_elem_qr.cpp
  linalg/uni10_elem_r2c.cpp
  linalg/uni10_elem_rq.cpp
  linalg/uni10_elem_scal_v.cpp
  linalg/uni10_elem_sdd.cpp
  linalg/uni10_elem_setdiag.cpp
  linalg/uni10_elem_sub.cpp
  linalg/uni10_elem_sub_v.cpp
  linalg/uni10_elem_sum_v.cpp
  linalg/uni10_elem_svd.cpp
  linalg/uni10_elem_sytrimateigdcp.cpp
  linalg/uni10_elem_trace.cpp
  linalg/uni10_elem_transpose.cpp
  linalg/uni10_elem_uniformrandomize.cpp
  hirnk_linalg/hptt_tcl/uni10_elem_tensortranspose.cpp
  hirnk_linalg/hptt_tcl/uni10_elem_tensorcontract.cpp
  hirnk_linalg/ttgt/uni10_elem_tensortranspose.cpp
  hirnk_linalg/ttgt/uni10_elem_tensorcontract.cpp
  tools_lapack_cpu/uni10_linalg_lapack_cpu_d.cpp
  tools_lapack_cpu/uni10_linalg_lapack_cpu_dz.cpp
  tools_lapack_cpu/uni10_linalg_lapack_cpu_z.cpp
  tools_lapack_cpu/uni10_tools_lapack_cpu.cpp
)


add_library(uni10-lapack_cpu OBJECT ${uni10_lapack_cpu_sources})
  
