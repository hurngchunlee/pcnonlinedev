FROM jupyter/scipy-notebook

RUN mkdir -p /home/jovyan/models
RUN mkdir -p /home/jovyan/models/lifespan_57K_82sites

COPY apply_normative_models.py /home/jovyan/
COPY models/* /home/jovyan/models/lifespan_57K_82sites/
COPY docs/* /home/jovyan/docs/
COPY app_df.py /home/jovyan/

RUN pip install pcntoolkit==0.20
RUN pip install dash
RUN pip install flask
RUN pip install plotly
RUN pip install gunicorn
