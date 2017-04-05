Dockerfiles usage: `cat Dockerfile.DOCKERNAME | docker build -t YOUR_DOCKER/NAME:TAG -`

Docker run: `docker run -ti [/YOUR/PATH/TO/VOLUME:/DOCKER/PATH/TO/VOLUME] DOCKER/NAME:TAG`

Python compiler for dockerfile usage: 
```
python [-use-cudnn 0|1]         # default: 0
       [[-python2 0|1]|         # default: 1
       [-python3 0|1]]          # default: 0
       [-python-layers 0|1]     # default: 1
       [-caffe GIT_REPOSITORY]  # every caffe repository will store in /caffe, default:bvlc
       [-repository ADDITIONAL_REPOSITORY]
       [-from DOCKER_IMAGE]     # default: ubuntu:16.04
```
