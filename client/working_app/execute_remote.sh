#! /bin/bash
# 1 = path to the project dir
# 2 = model name
# 3 = data type dir
# 4 = session id
# 5 = algorithm

# ssh connection is created in Dash app script, the ssh key is currently copied into container

# Activate our virtual environment.
source remotepcnenv/bin/activate
# Ensure working directory is our project.
cd /project_cephfs/3022051.01 
# optionally, qsub this batch script (will be sent to HPC). Useless until parallelized.
./execute_model_remote.sh $1 $2 $3 $4 $5