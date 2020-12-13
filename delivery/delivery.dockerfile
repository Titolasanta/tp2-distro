FROM python:3.8
RUN pip3 install pika json_lines

COPY . /root
CMD /root/delivery.py