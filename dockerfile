# syntax=docker/dockerfile:1

#set base image
FROM python:3.8

#By default, listen on port 5000
EXPOSE 5000/tcp

#set working directory in container
WORKDIR /code

#copy dependencies to working directory
COPY requirements.txt requirements.txt

#install dependencies via pip   
RUN pip install -r requirements.txt

#copy content from local directory to working directory
COPY . .

#run app
CMD [ "python3", "jc.py" ]