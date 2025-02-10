FROM python:3.10

COPY . /app
WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

ENV POSTGRES_HOST=postgres
ENV POSTGRES_PORT=5432
ENV POSTGRES_DB=Db
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD="postgres"


CMD ["python", "marketplace/app.py"]