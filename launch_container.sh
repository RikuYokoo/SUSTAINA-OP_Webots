#!/bin/bash

docker_image="collect_image_env"

id=${1:-"1"}

xhost +
docker run --gpus=all -it --rm -v /tmp/.X11-unix:/tmp/.X11-unix:rw --privileged \
		   -e DISPLAY \
                   -v $(pwd):/home/user/webots_ws/ \
		   --name webots_$id \
		   --env="QT_X11_NO_MITSHM=1" \
		   $docker_image \
                   webots --batch webots/world/collect_image.wbt
