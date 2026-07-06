pipeline {
    agent any
    environment {
      DOCKERHUB_CREDENTIALS = credentials('docker-dockerhub')
    }
    stages {
        stage('Build') {
            steps {
                sh 'echo "arun" | sudo -S docker build -t nginx:latest .'
            }
        }
        stage('Run') {
            steps {
                sh 'sudo docker run -d --name Web-server -p 8585:8383 nginx'
            }
        }
    }
}
