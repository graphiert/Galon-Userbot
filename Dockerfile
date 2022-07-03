FROM ubuntu:22.04
RUN apt-get update -y && apt-get upgrade -y
RUN apt-get install python3 python3-pip nodejs -y
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . /app/
WORKDIR /app/
CMD ["python3", "-m", "Galon"]
