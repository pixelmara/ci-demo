# Образ Jenkins с Docker CLI и Python — для кейсов 4, 5, 9, 10
FROM jenkins/jenkins:lts
USER root
COPY --from=docker:cli /usr/local/bin/docker /usr/local/bin/docker
RUN apt-get update && apt-get install -y python3 python3-venv python3-pip
# Для учебного стенда оставляем root, чтобы был доступ к docker.sock
USER root
