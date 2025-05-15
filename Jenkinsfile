pipeline {
    agent any
    
    stages {
        stage('Build and Test') {
            steps {
                script {
                    bat 'docker build -t rpg-game:6 .'
                    bat 'docker run --rm rpg-game:6 pytest Game/test_ui.py'
                }
            }
        }
        
        stage('Deploy') {
            steps {
                script {
                    bat 'docker stop rpg-game-container'
                    echo 'No existing container to clean up'
                    bat 'docker run -d -p 8000:8000 --name rpg-game-container rpg-game:6'
                }
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