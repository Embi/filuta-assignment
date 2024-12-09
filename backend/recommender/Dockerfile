FROM python:3.11-alpine

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

COPY api /app/api
COPY utils /app/utils

WORKDIR /app

RUN pip install --no-cache-dir --upgrade -r ./api/requirements.txt

EXPOSE 8000

CMD ["sh", "api/run.sh"]
