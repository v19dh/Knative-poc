FROM python:latest
COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt
COPY . /app
EXPOSE 9000
ENTRYPOINT [ "python" ]
CMD ["Batteryapp.py"]