#include <stdio.h>
#include "nvshmem.h"
#include "nvshmemx.h"

extern "C" int add(int a, int b) {
    return a + b;
}

nvshmemx_init_attr_t attr = NVSHMEMX_INIT_ATTR_INITIALIZER;
nvshmemx_uniqueid_t id = NVSHMEMX_UNIQUEID_INITIALIZER;

// 该接口只能 rank 0 进行调用, 用于初始化通信 id 的信息
extern "C" void init_nvshmemx_communication_ids(char * init_param, int * length) {
    nvshmemx_get_uniqueid(&id);
    char * data = (char *)&id;
    for(int i = 0; i < sizeof(nvshmemx_uniqueid_t); i++) {
        init_param[i] = data[i];
    }
    *length = sizeof(nvshmemx_uniqueid_t);
}

extern "C" void init_nvshmemx_env(int rank, int global_world_size, char * init_param, int * length) {
    char * data = (char *)&id;
    for(int i = 0; i < sizeof(nvshmemx_uniqueid_t); i++) {
        data[i] = init_param[i];
    }

    nvshmemx_set_attr_uniqueid_args(rank, global_world_size, &id, &attr);
    nvshmemx_init_attr(NVSHMEMX_INIT_WITH_UNIQUEID, &attr);
    return;
}

