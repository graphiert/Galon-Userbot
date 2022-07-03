FROM ubuntu:22.04
RUN apt-get update -y && apt-get upgrade -y 
RUN apt-get install python3 python3-pip -y
RUN pip install gitpython
COPY . /app/
WORKDIR /app/
CMD ["python3", "main.py"]
