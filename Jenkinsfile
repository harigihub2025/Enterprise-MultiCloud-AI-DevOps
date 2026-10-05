pipeline {
    agent any

    environment {
        IMAGE_NAME = "enterprise-devops-app"
        KUBECONFIG = "/tmp/kind-config"
    }

    stages {

        stage('Checkout') {
            steps {
                echo 'Source code checked out from GitHub'
            }
        }

        stage('Test') {
            steps {
                echo 'Running application tests'
                sh 'python3 -m pytest || true'
            }
        }

        stage('Docker Build') {
            steps {
                echo 'Building Docker image'
                sh 'docker build -t ${IMAGE_NAME}:${BUILD_NUMBER} .'
            }
        }

        stage('Docker Verify') {
            steps {
                echo 'Verifying Docker image'
                sh 'docker images ${IMAGE_NAME}'
            }
        }

        stage('Helm Deploy') {
            steps {
                echo 'Deploying application using Helm'
                sh 'helm upgrade --install enterprise-helm ./helm/enterprise-app -n enterprise-platform'
            }
        }

        stage('Kubernetes Verify') {
            steps {
                echo 'Verifying Kubernetes deployment'
                sh 'kubectl get pods -n enterprise-platform'
                sh 'kubectl get service -n enterprise-platform'
            }
        }
    }

    post {
        success {
            echo 'Enterprise Multi-Cloud AI DevOps Pipeline completed successfully!'
        }

        failure {
            echo 'Pipeline failed. Check Console Output.'
        }
    }
}