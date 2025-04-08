pipeline {
    agent any
    
    environment {
        DB_HOST = 'localhost'
        DB_NAME = 'forum_logs'
        DB_USER = 'forum_user'
        DB_PASS = 'forum_password'
        OUTPUT_FILE = 'forum_metrics.csv'
    }
    
    stages {
        stage('Checkout') {
            steps {
                git branch: 'lab5-08.04',
                url: 'https://github.com/Totoshka89/BigData'
            }
        }
        
        stage('Extract') {
            steps {
                script {
                    // Выполняем SQL-запрос для извлечения данных
                    def sql_query = """
                        SELECT 
                            DATE(action_timestamp) as day,
                            COUNT(DISTINCT CASE WHEN action_type = 'registration' THEN user_id END) as new_accounts,
                            COUNT(CASE WHEN action_type = 'post_message' THEN 1 END) as total_messages,
                            COUNT(CASE WHEN action_type = 'post_message' AND user_id IS NULL THEN 1 END) as anonymous_messages,
                            COUNT(DISTINCT CASE WHEN action_type = 'create_topic' AND server_response = 'success' THEN entity_id END) as new_topics
                        FROM user_logs
                        WHERE DATE(action_timestamp) = DATE_SUB(CURDATE(), INTERVAL 1 DAY)
                        GROUP BY DATE(action_timestamp)
                    """
                    
                    // Сохраняем запрос в файл
                    writeFile file: 'extract.sql', text: sql_query
                }
            }
        }
        
        stage('Transform') {
            steps {
                script {
                    // Используем Python скрипт для трансформации
                    sh """
                        python3 transform.py \
                            --db-host ${DB_HOST} \
                            --db-name ${DB_NAME} \
                            --db-user ${DB_USER} \
                            --db-pass ${DB_PASS} \
                            --input-file extract.sql \
                            --output-file ${OUTPUT_FILE}
                    """
                }
            }
        }
        
        stage('Load') {
            steps {
                script {
                    // Архивируем результаты
                    sh "zip -r forum_metrics.zip ${OUTPUT_FILE}"
                    
                    // aws s3 cp forum_metrics.zip s3://your-bucket/
                    
                    archiveArtifacts artifacts: 'forum_metrics.zip', fingerprint: true
                }
            }
        }
    }
    
    post {
        always {
            cleanWs() // Очистка рабочей директории
        }
    }
}