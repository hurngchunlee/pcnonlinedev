FROM python:3.8
RUN apt-get update
RUN apt-get install nano

COPY requirements.txt .
RUN pip3 install -r requirements.txt
#RUN mkdir -p /home/models
#RUN mkdir -p /home/models/lifespan_57K_82sites
#RUN mkdir -p /home/docs
# output will be the future volume mount
#RUN mkdir -p /home/output
#COPY apply_normative_models_app.py /home/
#COPY models/* /home/models/lifespan_57K_82sites/
#COPY docs/* /home/docs/
#COPY apply_normative_models.py /home/
#RUN python3.8 -m pip install pcntoolkit==0.20
RUN python3.8 -m pip install argparse
COPY app.py /home/
COPY execute_remote.sh /home/
WORKDIR /home/

# Create a user that only can access the ssh keys copied in
RUN apt-get install -y openssh-client
RUN useradd -m user
RUN mkdir -p /home/user/.ssh/id_ed
COPY .ssh/* /home/user/.ssh/
RUN chown -R user:user /home/user/.ssh
#RUN echo "stuff in config" >> /home/user/.ssh/config
USER user
# to prevent error saying .ssh files are too open i.e. not private
RUN chmod 600 /home/user/.ssh/id_ed25519

#RUN chmod 755 /home/ to get full rights over a dir?
# To execute Python commands on DCCN server with local bash script:
# cat ./execute_remote.sh | ssh -oStrictHostKeyChecking=no piebar@mentat004.dccn.nl


#CMD ["/bin/bash"]
CMD [ "gunicorn", "--timeout=600","--workers=5", "--threads=1", "-b 0.0.0.0:80", "app:server"]
#CMD [ "ssh", (, -k "path/to/ssh_key"),"piebar@mentat003.dccn.nl"]
#CMD [ "qsub", "normative_parallel.py"]
#CMD [ "exit" ]
