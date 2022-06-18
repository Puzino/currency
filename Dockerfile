FROM python:3.10

WORKDIR /code/build

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

ENV PYTHONPATH /code/build/app

#CMD ["python", "app/manage.py", "runserver", "0.0.0.0:8000"]
CMD ["uwsgi", "--http-socket", "0.0.0.0:8000", "--module", "settings.wsgi", "--threads", "2", "--workers", "4"]