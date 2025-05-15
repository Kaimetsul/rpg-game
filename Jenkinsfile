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
                bat '"C:\\Program Files\\Python39\\python.exe" -m pip install pytest'
                bat '"C:\\Program Files\\Python39\\python.exe" -m pytest tests/'
            }
        }
        
        stage('Deploy') {
            steps {
                bat 'docker run -d -p 8000:8000 rpg-game'
            }
        }
    }
}