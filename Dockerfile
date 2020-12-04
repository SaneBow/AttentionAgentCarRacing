#Download base image ubuntu 16.04
FROM ubuntu:16.04
RUN apt-get update -o Acquire::CompressionTypes::Order::=gz
RUN apt-get upgrade -y
RUN apt-get update && apt-get install -y \
python3 python3-pip xvfb python3-opengl fontconfig python3-dev python3-tk python-opencv \
build-essential zlib1g-dev libsdl2-dev libjpeg-dev nasm tar libbz2-dev libgtk2.0-dev cmake git libfluidsynth-dev libgme-dev libopenal-dev timidity libwildmidi-dev unzip libboost-all-dev \
wget g++ make cmake libsdl2-dev git zlib1g-dev libbz2-dev libjpeg-dev libfluidsynth-dev libgme-dev libopenal-dev libmpg123-dev libsndfile1-dev libwildmidi-dev libgtk-3-dev timidity nasm tar chrpath alsa-utils

WORKDIR /opt/app
ADD . /opt/app
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
RUN pip3 install git+https://github.com/sanebow/competitive-rl.git
RUN echo 'pcm.!default { type plug slave.pcm "null" }' > /etc/asound.conf