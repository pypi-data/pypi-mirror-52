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

set(uni10_cusolver_gpu_cpp_sources 
    uni10_elem_add.cpp
    uni10_elem_add_v.cpp
    uni10_elem_conj.cpp
    uni10_elem_cusolver_gpu.cpp
    uni10_elem_dagger.cpp
    uni10_elem_det.cpp
    uni10_elem_dot.cpp
    uni10_elem_eig.cpp
    uni10_elem_eigh.cpp
    uni10_elem_exp_v.cpp
    uni10_elem_identity.cpp
    uni10_elem_inverse.cpp
    uni10_elem_ldq.cpp
    uni10_elem_lq.cpp
    uni10_elem_mul.cpp
    uni10_elem_mul_v.cpp
    uni10_elem_normalrandomize.cpp
    uni10_elem_norm.cpp
    uni10_elem_qdrcpivot.cpp
    uni10_elem_qdr.cpp
    uni10_elem_ql.cpp
    uni10_elem_qr.cpp
    uni10_elem_rq.cpp
    uni10_elem_scal_v.cpp
    uni10_elem_sdd.cpp
    uni10_elem_setDiag.cpp
    uni10_elem_sub.cpp
    uni10_elem_sub_v.cpp
    uni10_elem_sum_v.cpp
    uni10_elem_svd.cpp
    uni10_elem_sytrimateigdcp.cpp
    uni10_elem_trace.cpp
    uni10_elem_trans.cpp
    uni10_elem_uniformrandomize.cpp
    tools_cusolver_gpu/uni10_linalg_cusolver_gpu_d.cpp
    tools_cusolver_gpu/uni10_linalg_cusolver_gpu_dz.cpp
    tools_cusolver_gpu/uni10_linalg_cusolver_gpu_z.cpp
    tools_cusolver_gpu/uni10_linalg_hybrid_d.cpp
    tools_cusolver_gpu/uni10_linalg_hybrid_dz.cpp
    tools_cusolver_gpu/uni10_linalg_hybrid_z.cpp
    tools_cusolver_gpu/uni10_linalg_lapack_cpu_d.cpp
    tools_cusolver_gpu/uni10_linalg_lapack_cpu_dz.cpp
    tools_cusolver_gpu/uni10_linalg_lapack_cpu_z.cpp
    tools_cusolver_gpu/uni10_tools_cusolver_gpu.cpp
)
add_library(uni10-cusolver_gpu OBJECT ${uni10_cusolver_gpu_cpp_sources})
  
