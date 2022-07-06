FROM python:3.8-slim-buster

WORKDIR /python-docker

# Copy `requirements.txt`, `app.py`, `vietTTS/`, ignoreing files indicated in .dockerignore
COPY . .

# Change back to root user to install dependencies
USER root

# download libsndfile1 app so audio files can be read and written out
RUN apt-get update -y && apt-get --yes install libsndfile1

RUN pip3 install -r requirements.txt

# Create audio folder that stores output audio; use chmod to set permission to 770 so that users of group root (gid=0) has write permission
RUN mkdir audio/ && chmod -R 770 audio/

# create user ctgroup and assign it to group root, disable password for the user (maybe consider setting password)
RUN adduser --disabled-password --gid 0 ctgroup && passwd -d ctgroup

# By best practices, don't run the code with root user
USER ctgroup

# automatic run sanic app, listening at port 5352 of container. This command will be override if new command is provided at docker run (or at docker-compose command instruction)
CMD ["sanic", "app:app", "-H", "0.0.0.0", "-p", "5352"]