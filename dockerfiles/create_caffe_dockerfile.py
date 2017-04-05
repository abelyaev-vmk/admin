import argparse
from os.path import abspath, join, dirname


def parse():
    parser = argparse.ArgumentParser(description='Makefile.config compiller for caffe')
    parser.add_argument('-use-cudnn', action='store', dest='use_cudnn', default=0)
    parser.add_argument('-python2', action='store', dest='python2', default=1)
    parser.add_argument('-python3', action='store', dest='python3', default=0)
    parser.add_argument('-python-layers', action='store', dest='python_layers', default=1)
    parser.add_argument('-caffe', action='store', dest='caffe', type=str,
                        default='https://github.com/BVLC/caffe')
    parser.add_argument('-repository', action='store', dest='repository', type=str, default='')
    parser.add_argument('-from', action='store', dest='FROM', type=str,
                        # default='opencv:cuda8-cudnn5-py27-py34')
                        default='ubuntu:16.04')
    parser.add_argument('-volume', action='store', dest='volume', default='shared')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse()

    makefile_config = """ 
## Refer to http://caffe.berkeleyvision.org/installation.html
# Contributions simplifying and improving our build system are welcome!

# cuDNN acceleration switch (uncomment to build with cuDNN).
{0} USE_CUDNN := 1

# CPU-only switch (uncomment to build without GPU support).
# CPU_ONLY := 1

# uncomment to disable IO dependencies and corresponding data layers
# USE_OPENCV := 0
# USE_LEVELDB := 0
# USE_LMDB := 0

# uncomment to allow MDB_NOLOCK when reading LMDB files (only if necessary)
#	You should not set this flag if you will be reading LMDBs with any
#	possibility of simultaneous read and write
# ALLOW_LMDB_NOLOCK := 1

# Uncomment if you're using OpenCV 3
OPENCV_VERSION := 3

# To customize your choice of compiler, uncomment and set the following.
# N.B. the default for Linux is g++ and the default for OSX is clang++
# CUSTOM_CXX := g++

# CUDA directory contains bin/ and lib/ directories that we need.
CUDA_DIR := /usr/local/cuda
# On Ubuntu 14.04, if cuda tools are installed via
# "sudo apt-get install nvidia-cuda-toolkit" then use this instead:
# CUDA_DIR := /usr

# CUDA architecture setting: going with all of them.
# For CUDA < 6.0, comment the *_50 through *_61 lines for compatibility.
# For CUDA < 8.0, comment the *_60 and *_61 lines for compatibility.
CUDA_ARCH := -gencode arch=compute_30,code=sm_30 \
		-gencode arch=compute_35,code=sm_35 \
		-gencode arch=compute_50,code=sm_50 \
		-gencode arch=compute_52,code=sm_52 \
		-gencode arch=compute_60,code=sm_60 \
		-gencode arch=compute_61,code=sm_61 \
		-gencode arch=compute_61,code=compute_61

# BLAS choice:
# atlas for ATLAS (default)
# mkl for MKL
# open for OpenBlas
BLAS := atlas
# Custom (MKL/ATLAS/OpenBLAS) include and lib directories.
# Leave commented to accept the defaults for your choice of BLAS
# (which should work)!
# BLAS_INCLUDE := /path/to/your/blas
# BLAS_LIB := /path/to/your/blas

# Homebrew puts openblas in a directory that is not on the standard search path
# BLAS_INCLUDE := $(shell brew --prefix openblas)/include
# BLAS_LIB := $(shell brew --prefix openblas)/lib

# This is required only if you will compile the matlab interface.
# MATLAB directory should contain the mex binary in /bin.
# MATLAB_DIR := /usr/local
# MATLAB_DIR := /Applications/MATLAB_R2012b.app

# NOTE: this is required only if you will compile the python interface.
# We need to be able to find Python.h and numpy/arrayobject.h.
{1} PYTHON_INCLUDE := /usr/include/python2.7 \
{1} 		/usr/lib/python2.7/dist-packages/numpy/core/include
# Anaconda Python distribution is quite popular. Include path:
# Verify anaconda location, sometimes it's in root.
# ANACONDA_HOME := $(HOME)/anaconda
# PYTHON_INCLUDE := $(ANACONDA_HOME)/include \
		# $(ANACONDA_HOME)/include/python2.7 \
		# $(ANACONDA_HOME)/lib/python2.7/site-packages/numpy/core/include

# Uncomment to use Python 3 (default is Python 2)
{2} PYTHON_LIBRARIES := boost_python-py35 python3
{2} PYTHON_INCLUDE := /usr/include/python3.5m \
                /usr/lib/python3.5/dist-packages/numpy/core/include

# We need to be able to find libpythonX.X.so or .dylib.
PYTHON_LIB := /usr/lib /usr/lib/python3.5 /usr/lib/python3
# PYTHON_LIB := $(ANACONDA_HOME)/lib

# Homebrew installs numpy in a non standard path (keg only)
# PYTHON_INCLUDE += $(dir $(shell python -c 'import numpy.core; print(numpy.core.__file__)'))/include
# PYTHON_LIB += $(shell brew --prefix numpy)/lib

# Uncomment to support layers written in Python (will link against Python libs)
{3} WITH_PYTHON_LAYER := 1

# Whatever else you find you need goes here.
INCLUDE_DIRS := $(PYTHON_INCLUDE) /usr/local/include /usr/local/cuda/include
LIBRARY_DIRS := $(PYTHON_LIB) /usr/local/lib /usr/lib /usr/lib/x86_64-linux-gnu/hdf5/serial 

# If Homebrew is installed at a non standard location (for example your home directory) and you use it for general dependencies
# INCLUDE_DIRS += $(shell brew --prefix)/include
# LIBRARY_DIRS += $(shell brew --prefix)/lib

# NCCL acceleration switch (uncomment to build with NCCL)
# https://github.com/NVIDIA/nccl (last tested version: v1.2.3-1+cuda8.0)
# USE_NCCL := 1

# Uncomment to use `pkg-config` to specify OpenCV library paths.
# (Usually not necessary -- OpenCV libraries are normally installed in one of the above $LIBRARY_DIRS.)
# USE_PKG_CONFIG := 1

# N.B. both build and distribute dirs are cleared on `make clean`
BUILD_DIR := build
DISTRIBUTE_DIR := distribute

# Uncomment for debugging. Does not work on OSX due to https://github.com/BVLC/caffe/issues/171
# DEBUG := 1

# The ID of the GPU that 'make runtest' will use to run unit tests.
TEST_GPUID := 0

# enable pretty build (comment to see full commands)
Q ?= @
        """.format(
            '' if args.use_cudnn else '#',
            '' if args.python2 else '#',
            '' if args.python3 else '#',
            '' if args.python_layers else '#'
        )
    caffe_name = args.caffe.split('/')[-1].split('.')[0]
    with open('Makefile.config.%s' % caffe_name, 'w') as f:
        f.write(makefile_config)
    dockerfile = """# Generated by create_caffe_dockerfile.py
FROM {0.FROM}
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        cmake \
        git \
        wget \
        libatlas-base-dev \
        libboost-all-dev \
        libgflags-dev \
        libgoogle-glog-dev \
        libhdf5-serial-dev \
        libleveldb-dev \
        liblmdb-dev \
        libopencv-dev \
        libprotobuf-dev \
        libsnappy-dev \
        protobuf-compiler \
        python-dev \
        python-numpy \
        python-pip \
        python-setuptools \
        python-scipy && \
    rm -rf /var/lib/apt/lists/*
RUN git clone --recursive {0.caffe}
{1}
RUN cd /caffe/python && for req in $(cat requirements.txt) pydot; do python{2} -m pip install $req; done && \
     python{2} -m pip install easydict xgboost
COPY Makefile.config.{3} /caffe/Makefile.config
RUN cd /caffe && \
     make all -j9 \
     make pycaffe
RUN mkdir /{0.volume}
VOLUME /{0.volume}

ENV CAFFE_ROOT=/caffe
ENV PYCAFFE_ROOT $CAFFE_ROOT/python
ENV PYTHONPATH $PYCAFFE_ROOT:$PYTHONPATH
ENV PATH $CAFFE_ROOT/build/tools:$PYCAFFE_ROOT:$PATH
RUN echo "$CAFFE_ROOT/build/lib" >> /etc/ld.so.conf.d/caffe.conf && ldconfig

{4}
    """.format(
        args,
        'RUN mv %s /caffe' % caffe_name if caffe_name != 'caffe' else '',
        2 if args.python2 else 3,
        caffe_name,
        '' if len(args.repository) < 2 else 'RUN cd / && git clone --recursive %s' % args.repository
    )

    with open(join(abspath(dirname(abspath(__file__))), 'Dockerfile.%s' % caffe_name), 'w') as f:
        f.write(dockerfile)
