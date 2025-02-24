# install 

pip install -e .

# test

python test.py --rank 0 --world_size 2
python test.py --rank 1 --world_size 2