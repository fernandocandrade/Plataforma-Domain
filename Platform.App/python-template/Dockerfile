FROM pmoneda/python:latest

WORKDIR /app
COPY . .
ENV POSTGRES_HOST postgres
ENV POSTGRES_USER postgres

RUN pip install -r requirements.txt
RUN pip install gunicorn

EXPOSE 9110
ENTRYPOINT python main.py && gunicorn -b 0.0.0.0:9110 --timeout 300 app.wsgi:app
