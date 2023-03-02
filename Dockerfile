FROM ubuntu:22.04
RUN apt-get update -y && apt-get upgrade -y 
RUN apt-get install git python3 python3-pip -y
COPY . /app/
WORKDIR /app/
RUN pip3 install -r Galon/requirements.txt
CMD ["python3", "-m", "Galon"]
