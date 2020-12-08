#Python base image
FROM python:3.8.5

#Install Python requirements
COPY requirements.txt /tmp/
RUN pip3 install -r /tmp/requirements.txt

#Setting up working directory
COPY . /api
WORKDIR /api
ENV FLASK_APP=app.py

#Container port on which the server will be listening 
EXPOSE 5000

#Launch server app
ENTRYPOINT [ "python3", "api.py" ]