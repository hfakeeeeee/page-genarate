FROM humana-dha-dhp-docker-artifacts.jfrog.io/continuumio/miniconda3:20250414.4

ARG ARTIFACT_USER
ARG ARTIFACT_PASSWORD

USER root

RUN useradd -m appuser

WORKDIR /app
COPY requirements.txt ./
COPY . ./
RUN chown -R appuser:appuser /app

ENV SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt
ENV PYTHONUNBUFFERED=1


RUN apt-get update && \
    apt-get install -y wget && apt install --only-upgrade libsoup2.4-1 -y && apt-get install -y unzip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade --no-cache-dir \
    --index-url=https://${ARTIFACT_USERNAME}:${ARTIFACT_PASSWORD}@humana.jfrog.io/artifactory/api/pypi/digital_health_and_analytics/simple \
    --extra-index-url=https://${ARTIFACT_USERNAME}:${ARTIFACT_PASSWORD}@humana.jfrog.io/humana/api/pypi/dha-pypi-virtual/simple \
    -r requirements.txt

COPY start_vite.sh start_vite.sh
COPY kill_process.sh kill_process.sh
RUN mkdir projects

RUN chmod +x start_vite.sh
RUN chmod +x kill_process.sh
RUN chmod +x ./projects

RUN echo "registry=https://humana.jfrog.io/artifactory/api/npm/dha-npm-virtual/" > /root/.npmrc \
    && echo "//humana.jfrog.io/artifactory/api/npm/dha-npm-virtual/:_auth=$(echo -n $ARTIFACT_USER:$ARTIFACT_PASSWORD | openssl base64 -A)" >> /root/.npmrc \
    && echo "//humana.jfrog.io/artifactory/api/npm/dha-npm-virtual/:username=$ARTIFACT_USER" >>/root/.npmrc \
    && echo "//humana.jfrog.io/artifactory/api/npm/dha-npm-virtual/:_password=$ARTIFACT_PASSWORD" >> /root/.npmrc \
    && echo "always-auth=true" >> /root/.npmrc

EXPOSE 8080

CMD ["sh", "-c", "python -m uvicorn app.main.main:app --host 0.0.0.0 --port 8080 --http h11"]
