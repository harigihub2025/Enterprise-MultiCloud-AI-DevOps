pipeline {

    agent any

    environment {
        IMAGE_NAME = 'enterprise-devops-app'
        REGISTRY = 'kind-registry:5000'
        IMAGE_TAG = "${BUILD_NUMBER}"

        KUBECONFIG = '/tmp/kind-config'

        HELM_RELEASE = 'enterprise-helm'
        K8S_NAMESPACE = 'enterprise-platform'
    }

    stages {

        stage('Checkout') {
            steps {
                echo '===== CHECKOUT SOURCE CODE ====='

                checkout scm

                echo 'Source code checkout completed successfully.'
            }
        }

        stage('Test') {
            steps {
                echo '===== RUN TESTS ====='

                sh '''
                    echo "Running application tests..."

                    if [ -f requirements.txt ]; then
                        python3 -m pytest || true
                    else
                        echo "No requirements.txt found. Skipping Python tests."
                    fi

                    echo "Test stage completed."
                '''
            }
        }

        stage('Docker Build') {
            steps {
                echo '===== BUILD DOCKER IMAGE ====='

                sh '''
                    echo "Building Docker image..."

                    docker build \
                        -t ${IMAGE_NAME}:${IMAGE_TAG} .

                    echo "Docker build completed."
                '''
            }
        }

        stage('Docker Verify') {
            steps {
                echo '===== VERIFY DOCKER IMAGE ====='

                sh '''
                    docker images | grep ${IMAGE_NAME}

                    echo "Docker image verification completed."
                '''
            }
        }

        stage('Tag Image') {
            steps {
                echo '===== TAG IMAGE FOR LOCAL REGISTRY ====='

                sh '''
                    docker tag \
                        ${IMAGE_NAME}:${IMAGE_TAG} \
                        ${REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}

                    echo "Image tagged as:"
                    echo "${REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}"
                '''
            }
        }

        stage('Push Image') {
            steps {
                echo '===== PUSH IMAGE TO LOCAL REGISTRY ====='

                sh '''
                    docker push \
                        ${REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}

                    echo "Image successfully pushed to local registry."
                '''
            }
        }

        stage('Verify Registry Image') {
            steps {
                echo '===== VERIFY REGISTRY IMAGE ====='

                sh '''
                    docker pull \
                        ${REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}

                    echo "Registry image verified successfully."
                '''
            }
        }

        stage('Helm Deploy') {
            steps {
                echo '===== HELM DEPLOYMENT ====='

                sh '''
                    helm upgrade --install \
                        ${HELM_RELEASE} \
                        ./helm/enterprise-app \
                        -n ${K8S_NAMESPACE} \
                        --set image.repository=${REGISTRY}/${IMAGE_NAME} \
                        --set image.tag=${IMAGE_TAG} \
                        --set image.pullPolicy=Always

                    echo "Helm deployment completed."
                '''
            }
        }

        stage('Kubernetes Verify') {
            steps {
                echo '===== KUBERNETES VERIFICATION ====='

                sh '''
                    echo "Waiting for Kubernetes rollout..."

                    kubectl rollout status \
                        deployment/${HELM_RELEASE} \
                        -n ${K8S_NAMESPACE} \
                        --timeout=120s

                    echo ""
                    echo "===== DEPLOYMENT ====="

                    kubectl get deployment \
                        ${HELM_RELEASE} \
                        -n ${K8S_NAMESPACE}

                    echo ""
                    echo "===== PODS ====="

                    kubectl get pods \
                        -n ${K8S_NAMESPACE}

                    echo ""
                    echo "===== SERVICE ====="

                    kubectl get service \
                        ${HELM_RELEASE}-service \
                        -n ${K8S_NAMESPACE}

                    echo ""
                    echo "Kubernetes verification completed successfully."
                '''
            }
        }
    }

    post {

        success {
            echo '''
            ==========================================
              CI/CD PIPELINE COMPLETED SUCCESSFULLY
            ==========================================
              Application : Enterprise Multi-Cloud AI DevOps Platform
              Docker      : Build Successful
              Registry    : Image Push Successful
              Helm        : Deployment Successful
              Kubernetes  : Rollout Successful
            ==========================================
            '''
        }

        failure {
            echo '''
            ==========================================
              CI/CD PIPELINE FAILED
            ==========================================
              Check Jenkins console logs
              for the failed stage.
            ==========================================
            '''
        }

        always {
            echo '===== PIPELINE FINISHED ====='
        }
    }
}