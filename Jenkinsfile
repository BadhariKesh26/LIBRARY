pipeline {
    agent any
    environment {
        DOCKER_USER = "YOUR_DOCKERHUB_USERNAME" // Replace with your DockerHub ID
    }
    stages {
        stage('1. Pull From GitHub') {
            steps {
                git 'https://github.com'
            }
        }
        stage('2. Docker Build') {
            steps {
                sh "docker build -t ${DOCKER_USER}/library-system:latest ."
            }
        }
        stage('3. Docker Push') {
            steps {
                // Ensure you have configured 'dockerhub-creds' inside Jenkins Credentials Manager
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', passwordVariable: 'PASS', usernameVariable: 'USER')]) {
                    sh "echo ${PASS} | docker login -u ${USER} --password-stdin"
                    sh "docker push ${DOCKER_USER}/library-system:latest"
                }
            }
        }
        stage('4. Kubernetes Deploy') {
            steps {
                sh "sed -i 's|DOCKERHUB_USERNAME|${DOCKER_USER}|g' k8s/deployment.yaml"
                sh "kubectl apply -f k8s/deployment.yaml"
            }
        }
    }
}
