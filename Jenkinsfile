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
