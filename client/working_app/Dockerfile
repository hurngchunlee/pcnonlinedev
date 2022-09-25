# Installs and copies
FROM python:3.8
RUN apt-get update
RUN apt-get install nano
RUN apt-get clean
RUN pip3 cache purge
COPY requirements.txt .
RUN pip3 install -r requirements.txt
RUN python3.8 -m pip install argparse
COPY app.py /home/
COPY execute_modelling.sh /home/
WORKDIR /home/

# Enable .ssh connection. Can all of this be removed for DCCN?
# Create a user that only can access the ssh keys copied in
RUN apt-get install -y openssh-client
RUN useradd -m user
RUN mkdir -p /home/user/.ssh/id_ed
# this can be removed in the deployed version (?)
COPY .ssh/* /home/user/.ssh/
RUN chown -R user:user /home/user/.ssh
#RUN echo "stuff in config" >> /home/user/.ssh/config
USER user
# to prevent error saying .ssh files are too open i.e. not private
RUN chmod 600 /home/user/.ssh/id_ed25519


# To execute Python commands on DCCN server with local bash script:
CMD [ "gunicorn", "--timeout=1000","--workers=5", "--threads=1", "-b 0.0.0.0:80", "app:server"]

