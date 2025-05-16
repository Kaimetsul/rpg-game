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
                bat 'docker build -t ${DOCKER_IMAGE} .'
            }
        }
        
        stage('Test') {
            steps {
                bat 'docker run --rm -e DISPLAY=:99 ${DOCKER_IMAGE} pytest tests/ --cov=src --cov-report=term-missing'
            }
        }
        
        stage('Code Quality') {
            steps {
                bat 'docker run --rm ${DOCKER_IMAGE} flake8 src/'
                bat 'docker run --rm ${DOCKER_IMAGE} pylint src/'
            }
        }
        
        stage('Deploy') {
            steps {
                echo 'Game is ready to run!'
            }
        }
    }
    
    post {
        always {
            cleanWs()
            echo 'Cleaning up workspace...'
        }
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Build or tests failed!'
        }
    }
}