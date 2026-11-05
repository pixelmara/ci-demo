# Образ Jenkins с Docker CLI и Python — для кейсов 4, 5, 9, 10
FROM jenkins/jenkins:lts
USER root
RUN apt-get update \
 && apt-get install -y --no-install-recommends docker.io python3 python3-venv python3-pip \
 && rm -rf /var/lib/apt/lists/*
# Для учебного стенда оставляем root, чтобы был доступ к docker.sock
USER root
