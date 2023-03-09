FROM python:3.9
RUN apt update && apt upgrade -y
RUN apt install python3-pip -y
RUN apt install ffmpeg -y
RUN curl -fsSL https://deb.nodesource.com/setup_15.x |  bash -
RUN apt-get install -y nodejs
RUN npm i -g npm
RUN mkdir /app/
COPY . /app
WORKDIR /app
RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir --upgrade --requirement requirements.txt
CMD python3 main.py
