import os
import ctypes
from nvshmem_kernel import init_nvshmemx_communication_ids, init_nvshmemx_uid, nvshmem_alloc_int32
import argparse


def main():
    # 创建解析器
    parser = argparse.ArgumentParser(description="Process some integers.")
    
    # 添加参数
    parser.add_argument('--rank', type=int, help='')
    parser.add_argument('--world_size', type=int, help='world_size')

    # 解析参数
    args = parser.parse_args()

    init_data = (ctypes.c_char * 1024)()
    
    if args.rank == 0:
        init_nvshmemx_communication_ids(init_data)
        # print(bytes(init_data))
        with open("./key.txt", mode="wb") as file:
            file.write(init_data[:])
        
        current_device_id = args.rank
        init_nvshmemx_uid(args.rank, args.world_size, current_device_id, init_data)
        print("init ok")
        nvshmem_alloc_int32(1, dim=1)
    else:
        with open("./key.txt", mode="rb") as file:
            init_id_datas = file.read()
        for i in range(len(init_id_datas)):
            init_data[i] = init_id_datas[i]
            
        current_device_id = args.rank
        init_nvshmemx_uid(args.rank, args.world_size, current_device_id, init_data)
        print('init ok')
        nvshmem_alloc_int32(1, dim=1)
        
if __name__ == "__main__":
    main()
    
# python test.py --rank 0 --world_size 2
# python test.py --rank 1 --world_size 2
