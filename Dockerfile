# pull official base image
FROM python:3.10-slim-buster

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install mysql dependencies
RUN apt-get update && apt-get install -y ffmpeg \
    && apt-get install -y libgl1-mesa-glx libglib2.0-0 \
    && apt-get install -y netcat gcc postgresql postgresql-contrib \
    && apt-get install -y dos2unix

# install dependencies
RUN pip install -U pip setuptools wheel
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir

# copy project
COPY . .

# Convert plain text files from Windows or Mac format to Unix
RUN apt-get install dos2unix
RUN dos2unix --newfile docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh

# Make entrypoint executable
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

# Entrypoint dependencies
RUN apt-get install netcat -y

# Create the folder if it doesn't exist, eliminar lineas
RUN mkdir -p /usr/src/app/media/
RUN mkdir -p /usr/src/app/staticfiles/
RUN mkdir -p /usr/src/app/static/

# Give permissions to the folder, eliminas lineas
RUN chmod -R 777 /usr/src/app/media/
RUN chmod -R 777 /usr/src/app/staticfiles/
RUN chmod -R 777 /usr/src/app/static/

# run entrypoint.sh
ENTRYPOINT ["bash", "/usr/local/bin/docker-entrypoint.sh"]
