# syntax=docker/dockerfile:1

FROM python:3.12.4-slim
RUN apt update -y

EXPOSE 5000

WORKDIR /databank

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN pip3 install dash_bootstrap_components
RUN pip3 install flask_cors
COPY . .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]