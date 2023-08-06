#!/usr/bin/env bash
conda deactivate
cd /mlops
git pull
conda env update -f ./requirements.yml
conda activate mlops
