FROM pmoneda/python:latest

WORKDIR /app
COPY . .
ENV POSTGRES_HOST postgres
ENV POSTGRES_USER postgres

RUN pip install -r requirements.txt
RUN pip install gunicorn

<<<<<<< Updated upstream:Platform.App/python-template/Dockerfile
EXPOSE 9110
ENTRYPOINT python main.py && gunicorn -b 0.0.0.0:9110 api.server:app
=======
ARG port={{port}}
ENV port=${port:-8000}
EXPOSE $port
ENTRYPOINT python main.py && gunicorn -b 0.0.0.0:$port api.server:app
>>>>>>> Stashed changes:Platform.App/python-template/Dockerfile.tmpl
