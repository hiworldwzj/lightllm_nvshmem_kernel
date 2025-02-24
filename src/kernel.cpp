#include <stdio.h>
#include "nvshmem.h"
#include "nvshmemx.h"
#include <cassert>

extern "C" int add(int a, int b) {
    return a + b;
}

nvshmemx_init_attr_t attr = NVSHMEMX_INIT_ATTR_INITIALIZER;
nvshmemx_uniqueid_t id = NVSHMEMX_UNIQUEID_INITIALIZER;

// 该接口只能 rank 0 进行调用, 用于初始化通信 id 的信息
extern "C" void init_nvshmemx_communication_ids(char * init_param) {
    nvshmemx_get_uniqueid(&id);
    char * data = (char *)&id;
    for(int i = 0; i < sizeof(nvshmemx_uniqueid_t); i++) {
        init_param[i] = data[i];
    }
}

extern "C" void init_nvshmemx_env(int rank, int global_world_size, char * init_param) {
    char * data = (char *)&id;
    for(int i = 0; i < sizeof(nvshmemx_uniqueid_t); i++) {
        data[i] = init_param[i];
    }

    nvshmemx_set_attr_uniqueid_args(rank, global_world_size, &id, &attr);
    nvshmemx_init_attr(NVSHMEMX_INIT_WITH_UNIQUEID, &attr);
    
    return;
}

extern "C" int* nvshmem_alloc_int32(int a, int b, int c, int d, int dim) {
    assert(dim <= 4);
    
    // 将维度参数存储在数组中
    int dims[] = {a, b, c, d};
    long long size = 1;

    // 计算总大小
    for (int i = 0; i < dim; ++i) {
        size *= dims[i];
    }

    int* destination = (int*)nvshmem_malloc(sizeof(int) * size);
    return destination;
}

extern "C" short* nvshmem_alloc_int16(int a, int b, int c, int d, int dim) {
    assert(dim <= 4);
    
    // 将维度参数存储在数组中
    int dims[] = {a, b, c, d};
    long long size = 1;

    // 计算总大小
    for (int i = 0; i < dim; ++i) {
        size *= dims[i];
    }

    short* destination = (short*)nvshmem_malloc(sizeof(short) * size);
    return destination;
}

extern "C" char* nvshmem_alloc_int8(int a, int b, int c, int d, int dim) {
    assert(dim <= 4);
    
    // 将维度参数存储在数组中
    int dims[] = {a, b, c, d};
    long long size = 1;

    // 计算总大小
    for (int i = 0; i < dim; ++i) {
        size *= dims[i];
    }

    char* destination = (char*)nvshmem_malloc(sizeof(char) * size);
    return destination;
}


// extern "C" void broad_card_expert_token(int rank, int global_world_size, int expert_num_per_card, int * data) {

// }

