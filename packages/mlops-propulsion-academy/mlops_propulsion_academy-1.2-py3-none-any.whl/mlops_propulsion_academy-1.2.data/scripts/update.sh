#!/usr/bin/env bash
ssh-keyscan gitlab.propulsion-home.ch >>/root/.ssh/known_hosts

FILE=/mlops
if [ -f "$FILE" ]
then
    cd /mlops
    git pull
else
    mkdir -p /mlops
    cd /mlops
    git clone git@gitlab.propulsion-home.ch:DOPE/mlops-cluster.git .
fi


# Build conda env
deactivate
cd /mlops/backend

FILE=/root/anaconda3/envs/mlops
if [ -f "$FILE" ]
then
    conda env update -f ./requirements.yml
else
    conda env create -f ./requirements.yml
fi


source activate mlops





