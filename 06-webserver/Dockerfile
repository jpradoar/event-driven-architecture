FROM python:3.12-slim 

# Variables de entorno (seguridad y Python optimizado)
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_ENV=production

RUN addgroup --system app && adduser --system --ingroup app app && \
apt-get update && apt-get install -y --no-install-recommends ca-certificates curl && \
rm -rf /var/lib/apt/lists/* && \
pip install --no-cache-dir flask==3.0.2 requests==2.32.4 setuptools==78.1.1 waitress==3.0.2 

COPY app.py /app/
COPY templates/ /app/templates/

WORKDIR /app
USER app
EXPOSE 8080

CMD ["waitress-serve", "--host=0.0.0.0", "--port=8080", "app:app"]