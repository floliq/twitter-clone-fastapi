FROM python:3.13-slim

RUN apt-get update && rm -rf /var/lib/apt/lists/*

WORKDIR /twitter_clone

COPY . .

RUN pip install -r ./requirements.txt

CMD sh -c "alembic upgrade head && uvicorn main:app --host 0.0.0.0 --port 8000"
