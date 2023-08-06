#!/usr/bin/env bash

#Docker, docker-compose
sudo apt-get update

sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    software-properties-common \
    libssl-dev \
    git -y

sudo apt install python-pip -y

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

sudo add-apt-repository \
    "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
    $(lsb_release -cs) \
    stable"


sudo apt-get update -y

sudo apt-get install docker-ce -y

sudo gpasswd -a $USER docker

pip install docker-compose

curl -L https://packages.gitlab.com/install/repositories/runner/gitlab-runner/script.deb.sh | sudo bash

sudo apt-get install gitlab-runner

sudo gpasswd -a gitlab-runner docker

# Anaconda

cd /tmp

curl -O https://repo.anaconda.com/archive/Anaconda3-2019.07-Linux-x86_64.sh

bash Anaconda3-2019.07-Linux-x86_64.sh
bash

# Git
#cp ~/.ssh/authorized_keys /authorized_keys
#FILE=/root/.ssh/id_rsa.pub
#if [ -f "$FILE" ]
#then
#    echo "$FILE exists"
#else
#    ssh-keygen -t rsa -f /root/.ssh/id_rsa -q -P ""
#fi
#cp /authorized_keys ~/.ssh/
#cat /root/.ssh/id_rsa.pub
ssh-keyscan gitlab.propulsion-home.ch >>/root/.ssh/known_hosts
mkdir /mlops
cd /mlops
git clone git@gitlab.propulsion-home.ch:DOPE/mlops-cluster.git .

# Build conda env

cd /mlops/backend
conda env create -f ./requirements.yml
source activate mlops

