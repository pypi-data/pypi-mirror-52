/****************************************************************************
*  @file uni10_auxiliary.hpp
*  @license
*    Universal Tensor Network Library
*    Copyright (c) 2013-2016
*    Natioanl Taiwan University
*    National Tsing-Hua University
*  
*    This file is designed for setting environment variables and allocating uni10_elems in general.
*
*  @endlicense
*  @author Yun-Hsuan Chou
*  @date 2014-05-06
*  @since
*
*****************************************************************************/

#ifndef __UNI10_AUXILIARY_H__
#define __UNI10_AUXILIARY_H__

#include <stdio.h>

#include "uni10_type.h"
#include "uni10_env_info.h"

/// @defgroup config Uni10 Configuration
/// @brief Auxiliary environment management functions.
namespace uni10{

  /// @ingroup config
  /// @brief 
  /// Configurate the environment settings by default values or
  /// Collect the environmnet variable values form .uni10rc.
  ///
  /// In usual, the parameters argc and argv are trival.
  /// They are designed for MPI version. 
  /// More details of this two parameters, please to read MPI documentation.
  ///
  /// @param[in] argc  The number of arguments
  /// @param[in] argv  Argument vector
  ///
  void Uni10Create(int argc=0, char** argv=NULL);

  ///
  /// @ingroup config
  /// @brief To clear all objects which are declared by uni10::Uni10Create().
  /// 
  /// uni10::Uni10Destroy() would clear all objects which are declared 
  /// for saving environment information by uni10::Uni10Create().
  ///
  ///
  void Uni10Destroy();

  /// @ingroup config
  /// @brief Briefly print environmnent information.
  /// 
  /// For instance, in Uni10-v2.0 CPU version. 
  //
  /// @code
  /// #######  Uni10 environment information  #######
  /// # CPU   cores   :                      4 
  /// # Threads number:                      8 
  /// # Total memory  :                7903.52 MB
  /// # Free  memory  :                 223.00 MB
  /// # Swap  memory  :                4091.73 MB
  /// ###############################################
  /// @endcode
  ///
  void Uni10PrintEnvInfo();

  bool uni10_func(load_uni10_rc, _type)( );

}

#endif
