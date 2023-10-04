FROM rabbitmq:3-management AS rabbitmq

FROM python AS python


COPY . /application
WORKDIR /application

RUN apt-get update && apt-get install -y wget curl
RUN pip3 install -r /application/requirements.txt
RUN pip install pandas
