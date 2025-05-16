pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = 'rpg-game'
        DOCKER_TAG = "${BUILD_NUMBER}"
        // Quality thresholds
        QUALITY_THRESHOLD = '80'
        COVERAGE_THRESHOLD = '30'
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Build') {
            steps {
                bat 'docker build -t %DOCKER_IMAGE% .'
            }
        }
        
        stage('Test') {
            steps {
                bat 'docker run --rm -e DISPLAY=:99 %DOCKER_IMAGE% pytest tests/ --cov=src --cov-report=term-missing'
            }
        }
        
        stage('Code Quality') {
            steps {
                script {
                    try {
                        // Run code quality checks
                        bat 'docker run --rm %DOCKER_IMAGE% flake8 src/'
                        bat 'docker run --rm %DOCKER_IMAGE% pylint src/'
                        
                        // If we get here, quality checks passed
                        echo 'Code quality checks passed successfully!'
                    } catch (Exception e) {
                        // Log the quality issues but don't fail the build
                        echo 'Code quality checks found issues:'
                        echo e.message
                        
                        // Mark as unstable but continue
                        currentBuild.result = 'UNSTABLE'
                        echo 'Marking build as UNSTABLE due to code quality issues'
                        echo 'This indicates the code works but could be improved'
                    }
                }
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
        unstable {
            echo 'Pipeline completed with code quality issues.'
            echo 'The game is functional but could benefit from code style improvements.'
            echo 'Consider fixing:'
            echo '- Line length issues (E501)'
            echo '- Missing blank lines between functions (E302)'
            echo '- Trailing whitespace (W291)'
            echo '- Missing newlines at end of files (W292)'
        }
    }
}