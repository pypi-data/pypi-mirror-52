# Universal Tensor Network Library (Uni10)

  [Uni10](https://uni10.gitlab.io) is an open-source C++ library designed for the development of
tensor network algorithms. Programming tensor network algorithms is
tedious and  prone to errors.  The task of keeping track of tensor
indices while performing contraction of a complicated tensor network
can be daunting. It is desirable to have a platform that provides
 bookkeeping capability and optimization.

  This software distinguishes itself from  other available software
solutions by providing the following advantages:

  * Fully implemented in C++.

  * Aimed toward applications in tensor network algorithms.

  * Provides basic tensor operations with an easy-to-use interface.

  * Provides a `Network` class to process and store the  details of the
    graphical representations of the networks.

  * Provides a collection of Python wrappers which interact with the
    Uni10 C++ library to take advantage of the Python language
    for better code readability and faster prototyping, without
    sacrificing the speed.

  * Provides behind-the-scene optimization and acceleration.

## Current Release

### Latest release: v2.1.0

### What's new?

* Fixes issues #177, #178

* `pip install pyuni10` is now available.


## Copyright and Changes

  See GPL and LGPL for copyright conditions.

  See [Release Notes](ChangeLog.md) for release notes and changes.


## Installation

See the [Install Guide](http://uni10.gitlab.io/uni10.gitlab.io//InstallGuide.html).

### Download

The latest Uni10 source code can be downloaded from
<a href="https://gitlab.com/uni10/uni10" rel="nofollow" target="_blank">GitLab</a>.


### Requirements

  * <a href="http://cmake.org/" target="_blank">cmake</a> version > 2.8.12
  * C++ compiler with C++11 support

    * g++ >= 4.6.0
    * Intel C++ Compiler >= 15.0
    * Clang >= 9.0
    * Apple Clang >= 9.0
    
  * BLAS and LAPACK libraries and header files
  * <a href="http://www.stack.nl/~dimitri/doxygen/" target="_blank">Doxygen</a> (for documentation)


### Build

 To build Un10, follow the following steps:

  1. Create a build directory

  2. Use `Cmake` to generate makefile

  3. Build library and exmamples

  4. Install library and examples (May require root access)

For more detailed information see this [install guide](http://uni10.gitlab.io/uni10.gitlab.io//InstallGuide.html).

### Examples

Using system c++, blas and lapack

    > mkdir build
    > cd build
    > cmake </path/to/uni10/>
    > make
    > sudo make install

The installation path defaults to `/usr/local/uni10`.

To override the default path, use `CMAKE_INSTALL_PREFIX` :

    > cmake -DCMAKE_INSTALL_PREFIX=</installation_path> </path/to/uni10/>

To use MKL and Intel compiler:

    > cmake -DBUILD_WITH_MKL=on -DBUILD_WITH_INTEL_COMPILERS=on </path/to/uni10/>

If cmake failes to find blas and lapack, specify the libraries by

    > cmake -DBLAS_LIBRARIES=</path/to/blas> -DLAPACK_LIBRARIES=</path/to/lapack> </path/to/uni10/>

### Build Options

 Option                       | Description (Default value)
----------------------------- | -------------------------------------------
 BUILD_WITH_MKL               | Use Intel MKL for lapack and blas (off)
 BUILD_WITH_INTEL_COMPILERS   | Use Intel C++ compiler  (off)
 BUILD_EXAMPLES               | Build C++ examples (on)
 BUILD_DOC                    | Build Documentation (off)
 BUILD_CUDA_SUPPORT           | Build Library for CUDA GPUs (off)
 BUILD_HDF5_SUPPORT           | Build Library for HSF5 support (off)
 CMAKE_INSTALL_PREFIX         | Installation location (/usr/local/uni10)

## Citation

  If you find Uni10 useful and would like to acknowledge us, please cite the following paper,

```bibtex  
  @article{1742-6596-640-1-012040,
  author={Ying-Jer Kao and Yun-Da Hsieh and Pochung Chen},
  title={Uni10: an open-source library for tensor network algorithms},
  journal={Journal of Physics: Conference Series},
  volume={640},
  number={1},
  pages={012040},
  url={http://stacks.iop.org/1742-6596/640/i=1/a=012040},
  year={2015}
  }

```  
## Developers

### Contributors and maintainers

  * Ying-Jer Kao (National Taiwan University)

  * Pochung Chen (National Tsing-Hua University)

  * Yun-Hsuan Chou (National Taiwan University)

  * Kai-Hsin Wu (National Taiwan University)

  * Chih-Yuan Lee (National Taiwan University)

  * Chen-Yen Lai (Los Alamos National Laboratory)

  * Yen-Hsin Wu (National Tsing-Hua University)

  * Chung-Yu Lo (National Tsing-Hua University)

  * Yi-Hao Jhu (National Tsing-Hua University)

  * Ian McCulloch (University of Queensland)

  * [Adam Iaizzi](https://www.iaizzi.me) (National Taiwan University)

### Alumni

  * Yun-Da Hsieh (Code Base, GPU)

  * Tama Ma (CMake script)

  * Sukhbinder Singh (Matlab Wrapper)


## How to Contribute

  * Clone the project from [GitLab](https://gitlab.com/uni10/uni10) and use it.

  * Report bugs by creating issues at [Uni10 Repo](https://gitlab.com/uni10/uni10/issues/new?issue)

  * Fork us on [GitLab](https://gitlab.com/uni10/uni10).

  * Create Merge Requests.


## Known issues

  * CMake generated Xcode project fails to link.


## Links

  * [Uni10 Website](https://uni10.gitlab.io)

  * [Uni10 Repo](https://gitlab.com/uni10/uni10)

## Funding

  Uni10 is funded by Ministry of Science and Technology of Taiwan through Grants number: MOST-102-2112-M-002-003-MY3 and MOST-105-2112-M-002 -023 -MY3.  

[![Join the chat at https://gitter.im/uni10library/Lobby](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/uni10library/Lobby?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)


[![pipeline status](https://gitlab.com/uni10/uni10/badges/master/pipeline.svg)](https://gitlab.com/uni10/uni10/commits/master)
[![pipeline status](https://gitlab.com/uni10/uni10/badges/develop/pipeline.svg)](https://gitlab.com/uni10/uni10/commits/develop)

[![coverage report](https://gitlab.com/uni10/uni10/badges/master/coverage.svg)](https://gitlab.com/uni10/uni10/commits/master)
[![coverage report](https://gitlab.com/uni10/uni10/badges/develop/coverage.svg)](https://gitlab.com/uni10/uni10/commits/develop)
