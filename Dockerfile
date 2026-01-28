FROM python:3.13-slim

RUN apt-get update && apt-get install -y nginx && rm -rf /var/lib/apt/lists/*

WORKDIR /twitter_clone

COPY . .

RUN pip install -r ./requirements.txt

COPY nginx/production /etc/nginx/sites-available/default

EXPOSE 80

CMD ["sh", "-c", "alembic upgrade head && uvicorn main:app --host 0.0.0.0 --port 8000 & nginx -g 'daemon off;'"]
