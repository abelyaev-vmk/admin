Dockerfile usage: `docker build -f Dockerfile.SOME -t DOCKER/NAME[:TAG] .`

Docker run: `docker run -ti [/YOUR/PATH/TO/VOLUME:/DOCKER/PATH/TO/VOLUME] DOCKER/NAME:TAG`

### Full pipeline
* Install opencv, based on cuda8.0 with cudnn5.0 from official repository
  with python2.7 and python3.5 support (already installed in docker) \
  `docker build -f Dockerfile.opencv -t opencv:cuda8-cudnn5-py27-py35 .`
* Install caffe skeleton with all necessary dependencies to fast install any caffe versions \
  `docker build -f Dockerfile.caffe-skeleton -t caffe-skeleton .`
* Change Dockerfile.caffe in the way you want by following the instructions and install caffe like \
  `docker build -f Dockerfile.caffe -t bvlc/caffe .`

If you need more information about caffe installation and caffe's makefile editing, visit [BVLC/caffe](https://github.com/BVLC/caffe)

If you want to use GPU inside docker:
* Install nvidia drivers from apt-get, see [more](http://help.ubuntu.ru/wiki/%D0%B4%D1%80%D0%B0%D0%B9%D0%B2%D0%B5%D1%80_%D0%B2%D0%B8%D0%B4%D0%B5%D0%BE%D0%BA%D0%B0%D1%80%D1%82_nvidia) 
* Instal `nvidia-docker` to have access to GPU inside docker, see [more](https://github.com/NVIDIA/nvidia-docker)
