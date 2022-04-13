# Building 1004.7s (20/20) FINISHED for centos and Python3.8
# Tomorrow:
# Create a docker compose with a volume and port. 
# See if compose works, then pull and test git repo app that can run the .csv download on gunicorn server.
FROM centos:7
RUN yum install gcc openssl-devel bzip2-devel libffi-devel zlib-devel -y
RUN curl https://www.python.org/ftp/python/3.8.9/Python-3.8.9.tgz --output /tmp/Python-3.8.9.tgz
WORKDIR /tmp
RUN tar xzf Python-3.8.9.tgz
WORKDIR /tmp/Python-3.8.9
RUN ./configure --enable-optimizations
RUN yum install make -y
RUN make altinstall
RUN yum install which -y
WORKDIR /tmp
RUN rm -r Python-3.8.9.tgz
RUN yum -y install epel-release
RUN curl https://bootstrap.pypa.io/get-pip.py --output get-pip.py
RUN python3.8 get-pip.py
RUN python3.8 -m pip install --upgrade pip
# Install dependencies here
# RUN echo "boto3==1.15.11" > requirements.txt
# RUN pip install -r requirements.txt
RUN yum update -y
RUN python3.8 -m pip install auto-sklearn
RUN python3.8 -m pip install pandas
#correct version?
RUN python3.8 -m pip install pcntoolkit==0.20 
RUN python3.8 -m pip install dash
RUN python3.8 -m pip install flask
RUN python3.8 -m pip install plotly
RUN python3.8 -m pip install gunicorn
# Torch is 750mb
#RUN ln -s /usr/bin/python3.8 /usr/bin/python
RUN mkdir -p /home/models
RUN mkdir -p /home/models/lifespan_57K_82sites
RUN mkdir -p /home/docs
# output will be the volume mount
RUN mkdir -p /home/output
COPY apply_normative_models.py /home/
COPY apply_normative_models_test.py /home/
COPY models/* /home/models/lifespan_57K_82sites/
COPY docs/* /home/docs/
#COPY app_df.py /home/
COPY app.py /home/