FROM python:3.8

RUN pip3 install pika
COPY ./ /root
CMD /root/business_consumer.py