pipeline {
    agent any

    environment {
        ACR_LOGIN_SERVER = 'tododevopsacr.azurecr.io'
        RESOURCE_GROUP = 'todo-devops-rg'
        AKS_CLUSTER_NAME = 'tododevopsaks'
        IMAGE_NAME = 'todo-app'
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/your-repo/Automated-ToDo-DevOps.git'
            }
        }

        stage('Azure Login') {
            steps {
                withCredentials([azureServicePrincipal(credentialsId: 'azure-credentials')]) {
                    sh 'az login --service-principal -u $AZURE_CLIENT_ID -p $AZURE_CLIENT_SECRET -t $AZURE_TENANT_ID'
                }
            }
        }

        stage('Build and Push Docker Image') {
            steps {
                script {
                    def imageTag = "${env.BUILD_NUMBER}"
                    sh "docker build -t ${ACR_LOGIN_SERVER}/${IMAGE_NAME}:${imageTag} ."
                    sh "docker tag ${ACR_LOGIN_SERVER}/${IMAGE_NAME}:${imageTag} ${ACR_LOGIN_SERVER}/${IMAGE_NAME}:latest"
                    withCredentials([usernamePassword(credentialsId: 'acr-credentials', usernameVariable: 'ACR_USER', passwordVariable: 'ACR_PASS')]) {
                        sh "docker login ${ACR_LOGIN_SERVER} -u $ACR_USER -p $ACR_PASS"
                        sh "docker push ${ACR_LOGIN_SERVER}/${IMAGE_NAME}:${imageTag}"
                        sh "docker push ${ACR_LOGIN_SERVER}/${IMAGE_NAME}:latest"
                    }
                }
            }
        }

        stage('Deploy to AKS') {
            steps {
                script {
                    def imageTag = "${env.BUILD_NUMBER}"
                    sh "az aks get-credentials --resource-group ${RESOURCE_GROUP} --name ${AKS_CLUSTER_NAME} --overwrite-existing"
                    sh "kubectl apply -f kubernetes/"
                    sh "kubectl set image deployment/todo-app-deployment todo-app-container=${ACR_LOGIN_SERVER}/${IMAGE_NAME}:${imageTag}"
                    sh "kubectl rollout status deployment/todo-app-deployment --timeout=300s"
                }
            }
        }
    }
}