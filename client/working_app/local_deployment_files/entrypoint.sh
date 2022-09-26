#!/bin/bash

## generate a new SSH key, the public key should be copied to the submission host of qsub
ssh-keygen -t rsa -N "" -C "PCNonline"

echo "copy the following content to ~/.ssh/authorized_keys"
cat ~/.ssh/id_rsa.pub

