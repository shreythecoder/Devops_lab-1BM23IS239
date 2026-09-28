FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir prometheus-client

COPY delivery_metrics.py /app/

EXPOSE 8000

CMD ["python", "delivery_metrics.py"]
