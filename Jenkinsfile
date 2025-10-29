pipeline {
    agent any

    environment {
        ACR_LOGIN_SERVER = 'tododevopsacr.azurecr.io'
        ACR_USERNAME = credentials('acr-username')
        ACR_PASSWORD = credentials('acr-password')
        RESOURCE_GROUP = 'todo-devops-rg'
        AKS_CLUSTER_NAME = 'tododevopsaks'
        IMAGE_NAME = 'todo-app'
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/deepakurk22cs1081/Automated-ToDo-DevOps.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("${ACR_LOGIN_SERVER}/${IMAGE_NAME}:${env.BUILD_NUMBER}")
                }
            }
        }

        stage('Push to ACR') {
            steps {
                script {
                    docker.withRegistry("https://${ACR_LOGIN_SERVER}", 'acr-credentials') {
                        docker.image("${ACR_LOGIN_SERVER}/${IMAGE_NAME}:${env.BUILD_NUMBER}").push()
                        docker.image("${ACR_LOGIN_SERVER}/${IMAGE_NAME}:${env.BUILD_NUMBER}").push('latest')
                    }
                }
            }
        }

        stage('Deploy to AKS') {
            steps {
                script {
                    sh """
                        az aks get-credentials --resource-group ${RESOURCE_GROUP} --name ${AKS_CLUSTER_NAME} --overwrite-existing
                        kubectl apply -f kubernetes/
                        kubectl set image deployment/todo-app-deployment todo-app-container=${ACR_LOGIN_SERVER}/${IMAGE_NAME}:${env.BUILD_NUMBER}
                    """
                }
            }
        }
    }

    post {
        always {
            sh 'docker system prune -f'
        }
        success {
            echo 'Pipeline succeeded!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}