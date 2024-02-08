FROM python:3.10

ENV PYTHONUNBUFFERED=1

WORKDIR /code

COPY requirements.txt .

RUN apt update && apt install nginx -y \

COPY  ./nginx/default.conf /etc/nginxconf.d/default.conf
COPY . .

RUN pip install --upgrade pip \
    && apt-get update \
    && pip install -r requirements.txt

COPY . .

COPY run.sh .

RUN chmod +x run.sh

EXPOSE 80

CMD ["python", "manage.py", "runserver", "0.0.0.0:80"]
