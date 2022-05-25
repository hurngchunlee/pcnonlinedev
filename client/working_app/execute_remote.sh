#! /bin/bash
#ssh -oStrictHostKeyChecking=no piebar@mentat004.dccn.nl execute_remote.sh
#cat ./execute_remote.sh | ssh -oStrictHostKeyChecking=no piebar@mentat004.dccn.nl
# ssh command is executed in python script, key is copied into container
source remotepcnenv/bin/activate
# $1 = path to the right model
cd $1 
#/home/preclineu/piebar/remotepcnenv/models/
chmod u+x execute_model_remote.sh
#divided into two bash scripts so the final part can be qsubbed
cat "working directory: "$1
cat "model name: " $2
./execute_model_remote.sh $1 $2