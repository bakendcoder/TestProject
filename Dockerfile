FROM python:3.6.12-slim-buster

RUN mkdir -p /usr/opt/directory_app
# COPY directory/ /usr/opt/directory_app
WORKDIR /usr/opt/directory_app

RUN pip3 install -r requirements.txt

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000", "--noreload"]

