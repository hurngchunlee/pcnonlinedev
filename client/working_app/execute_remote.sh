#! /bin/bash
# 1 = path to the project dir
# 2 = model name
# 3 = data type dir
# 4 = session id
# 5 = algorithm

# ssh connection is created in Dash app script, the ssh key is currently copied into container

# Activate our virtual environment.
#source remotepcnenv/bin/activate
# Activate pcntoolkit devel environment, preferred syntax above conda activate
module load "anaconda3/2021.05"
source activate remotepcn
# Ensure working directory is our project.
cd /project_cephfs/3022051.01 
# optionally, qsub this batch script (will be sent to HPC). But, useless until parallelized.
echo "$5"
python /project_cephfs/3022051.01/transfer_normative_models_online.py $1 $2 $3 $4 $5 $6