FROM humana-dha-dhp-docker-artifacts.jfrog.io/dhp-python-3.11:5032837

ARG ARTIFACT_USER
ARG ARTIFACT_PASSWORD

RUN useradd -m appuser

WORKDIR /app
COPY requirements.txt ./
COPY . ./
RUN chown -R appuser:appuser /app

ENV SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt
ENV PYTHONUNBUFFERED=1

RUN apt update && \
    apt upgrade -y && \
    apt install poppler-utils -y && \
    rm -rf /var/lib/apt/lists/* && \
    apt clean

RUN pip install --upgrade --no-cache-dir \
    --index-url=https://${ARTIFACT_USERNAME}:${ARTIFACT_PASSWORD}@humana.jfrog.io/artifactory/api/pypi/digital_health_and_analytics/simple \
    --extra-index-url=https://${ARTIFACT_USERNAME}:${ARTIFACT_PASSWORD}@humana.jfrog.io/humana/api/pypi/dha-pypi-virtual/simple \
    -r requirements.txt

USER appuser

EXPOSE 8080

CMD ["sh", "-c", "python -m uvicorn app.main.main:app --host 0.0.0.0 --port 8080"]
