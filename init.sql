-- Создание пользователя и предоставление прав
CREATE USER IF NOT EXISTS 'forum_user'@'%' IDENTIFIED BY 'forum_password';
GRANT ALL PRIVILEGES ON forum_logs.* TO 'forum_user'@'%';
FLUSH PRIVILEGES;

-- Создание таблиц
USE forum_logs;

CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE,
    email VARCHAR(100) UNIQUE,
    password_hash VARCHAR(255),
    registration_date DATETIME,
    last_login DATETIME,
    is_active BOOLEAN DEFAULT TRUE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS topics (
    topic_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    created_by INT,
    creation_date DATETIME NOT NULL,
    is_deleted BOOLEAN DEFAULT FALSE,
    delete_date DATETIME,
    FOREIGN KEY (created_by) REFERENCES users(user_id) ON DELETE SET NULL
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS messages (
    message_id INT AUTO_INCREMENT PRIMARY KEY,
    topic_id INT NOT NULL,
    author_id INT,
    content TEXT NOT NULL,
    creation_date DATETIME NOT NULL,
    is_anonymous BOOLEAN DEFAULT FALSE,
    author_name VARCHAR(50),
    FOREIGN KEY (topic_id) REFERENCES topics(topic_id) ON DELETE CASCADE,
    FOREIGN KEY (author_id) REFERENCES users(user_id) ON DELETE SET NULL
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS user_logs (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    action_type VARCHAR(50) NOT NULL,
    action_description TEXT,
    entity_id INT,
    server_response VARCHAR(255) NOT NULL,
    action_timestamp DATETIME NOT NULL,
    ip_address VARCHAR(45),
    user_agent TEXT,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE SET NULL
) ENGINE=InnoDB;