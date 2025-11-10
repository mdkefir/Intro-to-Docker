pipeline {
    // Указываем, что конвейер может выполняться на любом доступном агенте Jenkins
    agent any

    // Определяем переменные окружения, которые будут доступны на всех этапах
    environment {
        IMAGE_NAME = "mdkefir/intro-to-docker"
        DOCKERHUB_CREDENTIALS_ID = "dockerhub-credentials"
    }

    // Определяем этапы (стадии) конвейера
    stages {
        stage('1. Build Docker Image') {
            steps {
                // Собираем Docker образ. ${BUILD_NUMBER} - это встроенная переменная Jenkins (1, 2, 3...)
                // Это создает уникальный тег для каждой сборки: myuser/lab2-app:1, myuser/lab2-app:2 и т.д.
                echo "Building Docker image: ${env.IMAGE_NAME}:${BUILD_NUMBER}"
                script {
                    docker.build("${env.IMAGE_NAME}:${BUILD_NUMBER}", './app')
                }
            }
        }

        stage('2. Push Docker Image to Docker Hub') {
            steps {
                // Загружаем собранный образ в репозиторий Docker Hub
                echo "Pushing Docker image to Docker Hub..."
                script {
                    // Используем credentials, которые мы настроим в Jenkins
                    docker.withRegistry('https://registry.hub.docker.com', env.DOCKERHUB_CREDENTIALS_ID) {
                        // Пушим образ с номером сборки
                        docker.image("${env.IMAGE_NAME}:${BUILD_NUMBER}").push()
                        // Также пушим этот же образ с тегом 'latest', чтобы docker-compose мог его найти
                        docker.image("${env.IMAGE_NAME}:${BUILD_NUMBER}").push("latest")
                    }
                }
            }
        }

        stage('3. Deploy Application') {
            steps {
                // Разворачиваем приложение, используя docker-compose
                echo 'Deploying application...'
                // Сначала останавливаем и удаляем старые контейнеры, если они есть
                bat "docker-compose down"
                // Запускаем новые. 'docker-compose up' автоматически скачает ('pull')
                // образ с тегом 'latest' из Docker Hub, который мы только что запушили.
                bat "docker-compose up -d"
                echo 'Deployment complete! Application should be running on http://localhost:5000'
            }
        }
    }
}