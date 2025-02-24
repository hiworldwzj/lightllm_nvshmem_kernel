import os
import ctypes
from nvshmem_kernel import init_nvshmemx_communication_ids, init_nvshmemx_env, nvshmem_alloc_int32, init_nvshmemx_mpi, nvshmemx_mpi_port_name
import argparse
import torch

def main():
    # 创建解析器
    parser = argparse.ArgumentParser(description="Process some integers.")
    
    # 添加参数
    parser.add_argument('--rank', type=int, help='')
    parser.add_argument('--world_size', type=int, help='world_size')

    # 解析参数
    args = parser.parse_args()

    port_name = (ctypes.c_char * 1024)()
    
    if args.rank == 0:
        torch.cuda.set_device(args.rank % 8) # for 8 card
        nvshmemx_mpi_port_name(port_name, 1024)
        # print(bytes(port_name))
        with open("./key.txt", mode="wb") as file:
            file.write(port_name[:])
        print("call init_nvshmemx_mpi")
        init_nvshmemx_mpi(args.rank, args.world_size, port_name, 1024)
        
        
        
        print("call nvshmem_alloc_int32")
        card_expert_token_num = nvshmem_alloc_int32(8, 256, dim = 2)
        print(card_expert_token_num)
        
    else:
        torch.cuda.set_device(args.rank % 8) # for 8 card
        with open("./key.txt", mode="rb") as file:
            init_id_datas = file.read()
        for i in range(len(init_id_datas)):
            port_name[i] = init_id_datas[i]
        print("call init_nvshmemx_mpi")
        init_nvshmemx_mpi(args.rank, args.world_size, port_name, 1024)
         
        print("call nvshmem_alloc_int32")
        card_expert_token_num = nvshmem_alloc_int32(8, 256, dim = 2)
        print(card_expert_token_num)
    
    import time
    time.sleep(1000)
        
if __name__ == "__main__":
    main()
    
# python test.py --rank 0 --world_size 2
# python test.py --rank 1 --world_size 2
