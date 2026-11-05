pipeline {
    agent any

    environment {
        DOCKERHUB_USER = 'pixelmara'
        IMAGE          = "${DOCKERHUB_USER}/ci-demo"
        DB_URL         = 'jdbc:postgresql://ci-postgres:5432/app'
    }

    // Jenkins у вас локальный, вебхук от GitHub до него не дойдёт,
    // поэтому раз в 2 минуты Jenkins сам проверяет новые коммиты
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
                    pytest --junitxml=reports/junit.xml --cov=app --cov-report=xml:coverage.xml
                '''
            }
        }

        // ---- Кейс 9: SonarQube ----
        stage('SonarQube analysis') {
            steps {
                script {
                    def scannerHome = tool 'sonar-scanner'
                    withSonarQubeEnv('sonarqube') {
                        sh """
                            ${scannerHome}/bin/sonar-scanner \
                              -Dsonar.projectKey=ci-demo \
                              -Dsonar.sources=. \
                              -Dsonar.exclusions=.venv/**,reports/**,db/** \
                              -Dsonar.tests=. \
                              -Dsonar.test.inclusions=test_*.py \
                              -Dsonar.python.version=3.12 \
                              -Dsonar.python.coverage.reportPaths=coverage.xml
                        """
                    }
                }
            }
        }

        stage('Quality Gate') {
            steps {
                timeout(time: 5, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }

        // ---- Кейс 4: сборка образа и отправка в Docker Hub ----
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

        // ---- Кейс 10: миграции БД (Flyway) перед каждым деплоем ----
        stage('DB migrations') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'app-db',
                                                  usernameVariable: 'DB_USER',
                                                  passwordVariable: 'DB_PASS')]) {
                    sh '''
                        docker run --rm --network ci --volumes-from jenkins \
                          flyway/flyway \
                          -url=$DB_URL -user=$DB_USER -password=$DB_PASS \
                          -locations=filesystem:$WORKSPACE/db/migration \
                          migrate
                    '''
                }
            }
        }

        // ---- Кейс 5: развёртывание ----
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
