pipeline {
    agent any
    
    stages {
        stage('Build') {
            steps {
                bat 'docker build -t rpg-game .'
            }
        }
        
        stage('Test') {
            steps {
                // Run tests with a virtual display for Pygame
                bat 'docker run --rm -e DISPLAY=:99 rpg-game pytest tests/'
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
            echo 'Cleaning up workspace...'
            cleanWs()
            echo 'Pipeline completed successfully!'
        }
    }
}