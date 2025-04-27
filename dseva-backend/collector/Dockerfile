FROM python:3.12.4-slim

ENV LISTEN_PORT=3001
EXPOSE 3001

ENV BACKEND=""
ENV DEBUG=0
ENV GITHUB_TOKEN=""

WORKDIR /usr/src/collector

RUN apt-get update && apt-get install -y nano curl iputils-ping dnsutils  && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip
COPY ./requirements.txt .

RUN pip install -r requirements.txt

#COPY ./entrypoint.sh .
#RUN sed -i 's/\r$//g' /usr/src/dseva_backend/entrypoint.sh
#RUN chmod +x /usr/src/dseva_backend/entrypoint.sh

COPY . .

RUN echo "The Backend is $BACKEND"
ENTRYPOINT [ "/usr/src/collector/entrypoint.sh" ]