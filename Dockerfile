FROM ubuntu:18.04

RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt update
RUN apt install python3.8
RUN apt install python3-pip
RUN python3.8 -m pip install auto-sklearn
RUN python3.8 -m pip install pandas 
RUN python3.8 -m pip install pcntoolkit==0.20
RUN python3.8 -m pip install dash
RUN python3.8 -m pip install flask
RUN python3.8 -m pip install plotly
RUN python3.8 -m pip install gunicorn
RUN ln -s /usr/bin/python3.8 /usr/bin/python

RUN mkdir -p /home/jovyan/models
RUN mkdir -p /home/jovyan/models/lifespan_57K_82sites

COPY apply_normative_models.py /home/jovyan/
COPY models/* /home/jovyan/models/lifespan_57K_82sites/
COPY docs/* /home/jovyan/docs/
COPY app_df.py /home/jovyan/

VOLUME ["/home/jovyan/models/lifespan_57K_82sites"]
CMD [ "python", "./apply_normative_models.py" ]