FROM cyberbotics/webots:R2023b-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update  && apt install -y git vim software-properties-common cmake wget build-essential libopenmpi-dev zlib1g-dev zip python3-pip && rm -rf /var/lib/apt/lists/*

RUN pip3 install --upgrade pip && pip3 install numpy control==0.9.4 protobuf zmq opencv-python

RUN groupadd -g 1000 user && \
    useradd -m -s /bin/bash -u 1000 -g 1000 -G sudo,root user
RUN echo 'user:user' | chpasswd
RUN echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

USER user
WORKDIR /home/user/webots_ws

CMD ["/bin/bash"]
