FROM python:3.9-slim

ENV PYTHONUNBUFFERED=1 \
  PYTHONDONTWRITEBYTECODE=1 \
  PORT=5000

WORKDIR /app

RUN apt-get update && \
  apt-get install -y --no-install-recommends gcc && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

USER nobody

EXPOSE $PORT

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--threads", "8", "--access-logfile", "-", "--error-logfile", "-", "--log-level", "error", "production:app"]