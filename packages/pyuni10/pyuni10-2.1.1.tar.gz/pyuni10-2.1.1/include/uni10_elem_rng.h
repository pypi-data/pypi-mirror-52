#ifndef __UNI10_ELEM_RNG_H__
#define __UNI10_ELEM_RNG_H__

#if defined(UNI_LAPACK) && defined(UNI_CPU)
#include "uni10_lapack_cpu/uni10_elem_rng.h"
#endif

#if defined(UNI_CUSOLVER) && defined(UNI_GPU)
#include "uni10_cusolver_gpu/uni10_elem_rng.h"
#endif

#if defined(UNI_SCALAPACK) && defined(UNI_MPI)
#include "uni10_scalapack_mpi/uni10_elem_rng.h"
#endif

#endif
