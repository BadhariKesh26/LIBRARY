pipeline {
    agent any
    
    environment {
        DOCKER_HUB_USER = "your_dockerhub_username"
        IMAGE_NAME      = "library-system"
        REGISTRY_TAG    = "${env.BUILD_NUMBER}"
    }
    
    stages {
        stage('1. Inception & Checkout') {
            steps {
                echo 'Pulling changes from GitHub...'
                checkout scm
            }
        }
        
        stage('2. Build Validation') {
            steps {
                echo 'Validating system compliance...'
                sh 'pip install -r requirements.txt'
            }
        }
        
        stage('3. Containerize App') {
            steps {
                echo 'Generating new immutable Docker build...'
                sh "docker build -t ${DOCKER_HUB_USER}/${IMAGE_NAME}:${REGISTRY_TAG} ."
            }
        }
        
        stage('4. Automated Feature Test') {
            steps {
                echo 'Spinning up container runtime for logic check...'
                sh "docker run -d -p 5000:5000 --name test_runtime ${DOCKER_HUB_USER}/${IMAGE_NAME}:${REGISTRY_TAG}"
                
                // Block executing dynamic verification requests against endpoints
                sh '''
                    sleep 3
                    curl -X POST http://localhost:5000/books -H "Content-Type: application/json" -d '{"id":"B001","title":"DevOps Core","author":"Agile Expert"}'
                    docker stop test_runtime
                    docker rm test_runtime
                '''
            }
        }
        
        stage('5. Artifact Preservation') {
            steps {
                echo 'Securing image artifact to registry...'
                withCredentials([usernamePassword(credentialsId: 'dockerhub-credentials', passwordVariable: 'PASS', usernameVariable: 'USER')]) {
                    sh "echo ${PASS} | docker login -u ${USER} --password-stdin"
                    sh "docker push ${DOCKER_HUB_USER}/${IMAGE_NAME}:${REGISTRY_TAG}"
                }
            }
        }
        
        stage('6. Orchestrated K8s Release') {
            steps {
                echo 'Applying manifest tracking mappings on cluster...'
                // Inject the distinct current build index tag dynamically inside yaml configs
                sh "sed -i 's|IMAGE_PLACEHOLDER|${DOCKER_HUB_USER}/${IMAGE_NAME}:${REGISTRY_TAG}|g' k8s/deployment.yaml"
                sh "kubectl apply -f k8s/"
            }
        }
        
        stage('7. Production Smoke Verification') {
            steps {
                echo 'Verifying application runtime stabilization status...'
                sh "kubectl rollout status deployment/library-deployment"
            }
        }
    }
}
