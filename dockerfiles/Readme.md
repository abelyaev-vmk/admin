Dockerfiles usage: `cat Dockerfile.DOCKERNAME | docker build -t YOUR/NAME:TAG -`

Python compiller for dockerfile usage: 
```
python [-use-cudnn 0|1] 
             [[-python2 0|1]| 
             [-python3 0|1]] 
             [-python-layers 0|1]
             [-caffe GIT_REPOSITORY]  # every caffe repository will store in /caffe
             [-repository ADDITIONAL_REPOSITORY]
             [-from DOCKER_IMAGE]
```
