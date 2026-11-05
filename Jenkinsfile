pipeline {
agent any
environment {
IMAGE = 'pixelmara/ci-demo'
}
triggers {
pollSCM('H/2 * * * *')
}
stages {
stage('Build image') {
steps {
sh 'docker build -t $IMAGE:$BUILD_NUMBER -t $IMAGE:latest .'
}
}
stage('Push to Docker Hub') {
steps {
withCredentials([usernamePassword(credentialsId: 'dockerhub', usernameVariable: 'DH_USER', passwordVariable: 'DH_PASS')]) {
sh '''
echo "$DH_PASS" | docker login -u "$DH_USER" --password-stdin
docker push $IMAGE:$BUILD_NUMBER
docker push $IMAGE:latest
'''
}
}
}
}
}
