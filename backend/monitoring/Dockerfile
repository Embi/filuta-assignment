FROM python:3.11-slim-bullseye

ENV PYTHONUNBUFFERED=1

COPY monitoring /app/monitoring

WORKDIR /app

RUN pip install --no-cache-dir --upgrade -r ./monitoring/requirements.txt

EXPOSE 8000

CMD ["bash", "monitoring/run.sh"]
