#!/usr/bin/env bash
ssh-keyscan gitlab.propulsion-home.ch >>/root/.ssh/known_hosts

FILE=/mlops
if [ -d "$FILE" ]
then
    cd /mlops
    git pull
else
    mkdir -p /mlops
    cd /mlops
    git clone git@gitlab.propulsion-home.ch:DOPE/mlops-cluster.git .
fi


# Build conda env
cd /mlops/backend

FILE=/root/anaconda3/envs/mlops
if [ -d "$FILE" ]
then
    conda env update -n=mlops -f=./requirements.yml
else
    conda env create -f ./requirements.yml
fi







