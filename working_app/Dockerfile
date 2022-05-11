FROM python:3.8
RUN apt-get update
RUN apt-get install nano

COPY requirements.txt .
RUN pip3 install -r requirements.txt
RUN mkdir -p /home/models
RUN mkdir -p /home/models/lifespan_57K_82sites
RUN mkdir -p /home/docs
# output will be the volume mount
RUN mkdir -p /home/output
COPY apply_normative_models_app.py /home/
COPY models/* /home/models/lifespan_57K_82sites/
COPY docs/* /home/docs/
COPY apply_normative_models_app.py /home/
COPY apply_normative_models.py /home/
RUN python3.8 -m pip install pcntoolkit==0.20
RUN python3.8 -m pip install argparse
COPY app.py /home/
WORKDIR /home/
CMD [ "gunicorn", "--timeout=500","--workers=5", "--threads=1", "-b 0.0.0.0:80", "app:server"]