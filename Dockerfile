FROM rabbitmq:3-management AS rabbitmq

FROM python AS python

COPY ./requirements.txt /requirements.txt

WORKDIR /
RUN apt-get update && apt-get install -y wget curl
RUN pip3 install -r requirements.txt

COPY . /

ENTRYPOINT [ "python3" ]
CMD ["dataset/add_graph_dump.py"]
CMD [ "app/app.py" ]