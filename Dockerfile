FROM python:2.7
ADD . /code
WORKDIR /code
ENV DC_CONFIG_FILE config/live.py
RUN pip install -r requirements.txt
