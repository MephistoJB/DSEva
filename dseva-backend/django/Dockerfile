FROM python:3.12.4-slim

WORKDIR /usr/src/dseva_backend

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y netcat-traditional && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip
COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /usr/src/dseva_backend/entrypoint.sh
RUN chmod +x /usr/src/dseva_backend/entrypoint.sh

COPY . .

ENTRYPOINT [ "/usr/src/dseva_backend/entrypoint.sh" ]