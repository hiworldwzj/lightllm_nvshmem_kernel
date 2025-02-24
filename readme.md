# install 

pip install -e .

# test
# 启动 pmix server
/usr/mpi/gcc/openmpi-4.1.5a1/bin/ompi-server --no-daemonize -r +

# 用环境变量暴露 pmix server
export OMPI_MCA_pmix_server_uri="653393920.0;tcp://10.121.4.14,172.17.0.1:52581"
python test.py --rank 0 --world_size 2

export OMPI_MCA_pmix_server_uri="653393920.0;tcp://10.121.4.14,172.17.0.1:52581"
python test.py --rank 1 --world_size 2