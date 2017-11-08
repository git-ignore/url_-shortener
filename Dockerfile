FROM python:3
MAINTAINER Belov <BSemyona@gmail.com>

ENV PYTHONUNBUFFERED 1
RUN mkdir -p /opt/services/url_shortener/src
COPY requirements.txt /opt/services/url_shortener/src/
WORKDIR /opt/services/url_shortener/src
RUN pip install -r requirements.txt
COPY . /opt/services/url_shortener/src
EXPOSE 5090
CMD ["python", "app.py"]
