FROM python:3.11-slim-bullseye

ENV PYTHONUNBUFFERED=1

COPY api /app/api
COPY core /app/core

WORKDIR /app

RUN pip install --no-cache-dir --upgrade -r ./api/requirements.txt -r ./core/requirements.txt

EXPOSE 8000

CMD ["bash", "api/run.sh"]
