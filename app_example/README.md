# Repository for PCNtoolkit Normative Models via Docker Container

[View on Docker Hub](https://hub.docker.com/r/saruther/pcntoolkit-interface)

**Note:** The docker-compose YAML file was copied from this GitHub [repository](https://github.com/Donders-Institute/filer-gateway/blob/master/docker-compose.yml) and has not been edited at all (yet), meaning it is just a template/placeholder.

This is a python-based container that will install the necessary packages to run pre-trained cortical thickness and subcortical volume normative models and transfer these models to an unseen test set. The models are described in [Rutherford et al](https://elifesciences.org/articles/72904). The transfer test set is currently a multi-site dataset using public data from [OpenNeuro](https://openneuro.org/). This build currently does not support using your own transfer data set. This feature (uploading your own dataset) is actively being developed and a future release will allow users an option to input their own transfer data set. 

## Setup Steps: 
1. Clone this GitHub repository and `cd` into the cloned repository.

    ```git clone git@github.com:saigerutherford/PCNtoolkit-interface.git```

    ```cd PCNtoolkit-interface```

2. Pull the Docker image from DockerHub

    ```docker pull saruther/pcntoolkit-interface```

3. Run the container, and mount the GitHub repository using the Volume (-v) flag. Change the path to match the location of the cloned GitHub repository.

    ```docker run -v /path/to/PCNtoolkit-interface/repo:/home/jovyan/ pcntoolkit-interface python apply_normative_models.py```

## After the script has run:

There will be a file called `Z_predict.txt` that is located in each subdirectory in `/models/lifespan_57K_82sites/`. This file contains the Z-scores (deviation scores) for all subjects in the test set. There is one subdirectory and corresponding Z_predict.txt file for every model that was run. 
