FROM nvidia/cuda:11.7.1-cudnn8-runtime-ubuntu20.04
ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND noninteractive
ENV TZ "Europe/Moscow"

RUN apt update
RUN apt install -y \
    build-essential \
    curl \
    git \
    git-lfs \
    htop \
    libzbar0 \
    mc \
    openssh-server \
    python-is-python3 \
    python3 \
    python3-pip \
    libgl1 \
    nano \
    sudo \
    rsync \
    tmux \
    tzdata \
    wget
RUN apt clean
RUN rm -rf /var/lib/apt/lists/*

RUN mkdir /var/run/sshd

RUN pip install --upgrade setuptools pip
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install jupyter

RUN groupadd --gid 1000 user \
  && useradd --uid 1000 --gid user --shell /bin/bash --create-home user

RUN echo "user:12345678" | chpasswd

WORKDIR /home/user

ENTRYPOINT ["/usr/sbin/sshd", "-D"]
