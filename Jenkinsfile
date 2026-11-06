pipeline {
    agent any

    environment {
        IMAGE = 'pixelmara/ci-demo'
    }

    triggers {
        pollSCM('H/2 * * * *')
    }

    stages {
        stage('Lint') {
            steps {
                sh '''
                    python3 -m venv .venv
                    . .venv/bin/activate
                    pip install -q -r requirements.txt -r requirements-dev.txt
                    flake8 .
                '''
            }
        }

        stage('Unit tests') {
            steps {
                sh '''
                    . .venv/bin/activate
                    mkdir -p reports
                    pytest --junitxml=reports/junit.xml
                '''
            }
        }

        stage('Build image') {
            steps {
                sh 'docker build -t $IMAGE:$BUILD_NUMBER -t $IMAGE:latest .'
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub',
                                                  usernameVariable: 'DH_USER',
                                                  passwordVariable: 'DH_PASS')]) {
                    sh '''
                        echo "$DH_PASS" | docker login -u "$DH_USER" --password-stdin
                        docker push $IMAGE:$BUILD_NUMBER
                        docker push $IMAGE:latest
                    '''
                }
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                    docker rm -f ci-demo-app || true
                    docker run -d --name ci-demo-app --network ci -p 8000:8000 $IMAGE:$BUILD_NUMBER
                    sleep 3
                    docker exec ci-demo-app python -c "import urllib.request; print(urllib.request.urlopen('http://localhost:8000/').read())"
                '''
            }
        }
    }

    post {
        always {
            junit allowEmptyResults: true, testResults: 'reports/*.xml'
        }
        success { echo 'Пайплайн выполнен успешно' }
        failure { echo 'Пайплайн упал' }
    }
}