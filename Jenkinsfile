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
                bat 'docker run --rm rpg-game pytest tests/'
            }
        }
        
        stage('Deploy') {
            steps {
                bat 'docker stop rpg-game-container || echo "No container to stop"'
                bat 'docker run -d -p 8000:8000 --name rpg-game-container rpg-game'
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