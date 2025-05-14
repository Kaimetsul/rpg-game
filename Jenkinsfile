pipeline {
    agent any
    
    stages {
        stage('Build') {
            steps {
                sh 'docker build -t rpg-game .'
            }
        }
        
        stage('Test') {
            steps {
                sh 'pytest tests/'
            }
        }
        
        stage('Deploy') {
            steps {
                sh 'docker run -d -p 8000:8000 rpg-game'
            }
        }
    }
}
