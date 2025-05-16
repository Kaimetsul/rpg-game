pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = 'rpg-game'
        DOCKER_TAG = "${BUILD_NUMBER}"
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Build') {
            steps {
                sh 'docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} .'
            }
        }
        
        stage('Test') {
            steps {
                sh 'docker run --rm ${DOCKER_IMAGE}:${DOCKER_TAG} pytest tests/ --cov=src --cov-report=term-missing'
            }
        }
        
        stage('Code Quality') {
            steps {
                sh 'docker run --rm ${DOCKER_IMAGE}:${DOCKER_TAG} flake8 src/ tests/'
                sh 'docker run --rm ${DOCKER_IMAGE}:${DOCKER_TAG} pylint src/ tests/'
            }
        }
        
        stage('Deploy') {
            steps {
                echo 'Game is ready to run locally with: python src/main.py'
            }
        }
    }
    
    post {
        always {
            cleanWs()
            echo 'Pipeline completed successfully!'
        }
        success {
            echo 'Build and tests passed successfully!'
        }
        failure {
            echo 'Build or tests failed!'
        }
    }
}