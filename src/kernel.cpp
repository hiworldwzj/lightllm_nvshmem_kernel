#include <stdio.h>
#include "nvshmem.h"
#include "nvshmemx.h"
#include <mpi.h>
#include <cassert>

extern "C" int add(int a, int b) {
    return a + b;
}

nvshmemx_init_attr_t attr = NVSHMEMX_INIT_ATTR_INITIALIZER;
nvshmemx_uniqueid_t id = NVSHMEMX_UNIQUEID_INITIALIZER;
MPI_Comm local_self = MPI_COMM_WORLD;

// 该接口只能 rank 0 进行调用, 用于初始化通信 id 的信息
extern "C" void init_nvshmemx_communication_ids(char * init_param) {
    id = NVSHMEMX_UNIQUEID_INITIALIZER;
    nvshmemx_get_uniqueid(&id);
    char * data = (char *)&id;
    for(int i = 0; i < sizeof(nvshmemx_uniqueid_t); i++) {
        init_param[i] = data[i];
    }
}

extern "C" void nvshmemx_mpi_port_name(char * port_name, int port_length) {
    MPI_Init(NULL, NULL);
    assert(MPI_MAX_PORT_NAME <= port_length);
    MPI_Open_port(MPI_INFO_NULL, port_name);
    printf("init_nvshmemx_mpi Port: %s\n", port_name);
}

extern "C" void init_nvshmemx_mpi(int rank, int global_world_size, char * port_name, int port_length) {
    assert(MPI_MAX_PORT_NAME <= port_length);
    local_self = MPI_COMM_WORLD;

    if(rank == 0) {

        MPI_Comm client_comm;
        MPI_Comm new_client_comm;
        for (int i = 0; i < global_world_size - 1 - rank; i++) {
            MPI_Comm_accept(port_name, MPI_INFO_NULL, 0, local_self, &client_comm);
            printf("Accepted connection from client %d\n", rank + i + 1);
            MPI_Intercomm_merge(client_comm, 0, &new_client_comm);
            int new_rank;
            MPI_Comm_rank(new_client_comm, &new_rank);
            printf("init_nvshmemx_mpi new_rank %d\n", new_rank);
            local_self = new_client_comm;
        }

    } else {

        MPI_Init(NULL, NULL);
        MPI_Comm server_comm;
        MPI_Comm_connect(port_name, MPI_INFO_NULL, 0, local_self, &server_comm);
        int new_rank;
        MPI_Comm new_server_comm;
        MPI_Intercomm_merge(server_comm, 1, &new_server_comm);
        MPI_Comm_rank(new_server_comm, &new_rank);
        printf("init_nvshmemx_mpi new_rank %d\n", new_rank);
        local_self = new_server_comm;
        MPI_Comm client_comm;
        MPI_Comm new_client_comm;

        for (int i = 0; i <  global_world_size - 1 - rank; i++) {
            MPI_Comm_accept(port_name, MPI_INFO_NULL, 0, local_self, &client_comm);
            printf("Accepted connection from client %d\n", rank + i + 1);
            MPI_Intercomm_merge(client_comm, 0, &new_client_comm);
            MPI_Comm_rank(new_client_comm, &new_rank);
            printf("init_nvshmemx_mpi new_rank %d", new_rank);
            local_self = new_client_comm;
        }
        printf("connect ok\n");
    }
 
    attr.mpi_comm = &local_self;
    nvshmemx_init_attr(NVSHMEMX_INIT_WITH_MPI_COMM, &attr);
    printf("wzj ok\n");
    
    return;
}



extern "C" void init_nvshmemx_uid(int rank, int global_world_size, int current_device_id, char * init_param) {
    char * data = (char *)&id;
    for(int i = 0; i < sizeof(nvshmemx_uniqueid_t); i++) {
        data[i] = init_param[i];
    }
    attr = NVSHMEMX_INIT_ATTR_INITIALIZER;
    nvshmemx_set_attr_uniqueid_args(rank, global_world_size, &id, &attr);
    nvshmemx_init_attr(NVSHMEMX_INIT_WITH_UNIQUEID, &attr);
    printf("nvshmemx set current device %d \n", current_device_id);
    // torch.cuda.set_device 不能在这里使其生效，所以需要单独再设置一次。切记切记
    cudaSetDevice(current_device_id);
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

