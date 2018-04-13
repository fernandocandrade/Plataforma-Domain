FROM pmoneda/domain_base:latest

WORKDIR /app
COPY . .
ENV POSTGRES_HOST postgres
ENV POSTGRES_USER postgres
EXPOSE 9110
ENTRYPOINT if [ "$DOMAIN_API" -eq "1" ]; then python main.py && gunicorn -b 0.0.0.0:9110 --timeout 300 app.wsgi:app;else python run.py; fi