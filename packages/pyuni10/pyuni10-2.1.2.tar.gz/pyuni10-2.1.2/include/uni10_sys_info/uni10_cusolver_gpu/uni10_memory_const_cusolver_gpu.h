#ifndef UNI10_GPU_MEM_H_INCLUDED
#define UNI10_GPU_MEM_H_INCLUDED

namespace uni10{

    //Please keep this struct can be see as a continuous memory address.
    struct MemoryConst{
        unsigned int blocksize_x;
        unsigned int blocksize_y;
        unsigned int blocksize_z;
        unsigned int gridsize_x ;
        unsigned int gridsize_y ;
        unsigned int gridsize_z ;
        unsigned int grid, block;
    };

    //interface
    void MemConstToGPU(const MemoryConst &HCnst);
    void MemConstFromGPU(MemoryConst &HCnst);

}

#endif // UNI10_GPU_MEM_H_INCLUDED
