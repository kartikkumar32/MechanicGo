import mysql.connector
from mysql.connector import pooling
import os
from dotenv import load_dotenv

load_dotenv()

db_config = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
    "port": int(os.getenv("DB_PORT", 3306))
}

try:
    connection_pool = mysql.connector.pooling.MySQLConnectionPool(
        pool_name="mechanicgo_pool", pool_size=10, **db_config
    )
except mysql.connector.Error as err:
    print(f"Pool error (will retry on first request): {err}")
    connection_pool = None

def get_db():
    global connection_pool
    if connection_pool is None:
        connection_pool = mysql.connector.pooling.MySQLConnectionPool(
            pool_name="mechanicgo_pool2", pool_size=10, **db_config
        )
    return connection_pool.get_connection()

def init_db():
    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        port=int(os.getenv("DB_PORT", 3306))
    )

    cursor = conn.cursor()
    db_name = os.getenv("DB_NAME", "mechanicgo")
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
    cursor.execute(f"USE {db_name}")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(150) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            role ENUM('user', 'mechanic', 'admin') DEFAULT 'user',
            phone VARCHAR(20),
            profile_pic VARCHAR(255),
            is_active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            token VARCHAR(100) UNIQUE NOT NULL,
            role VARCHAR(20) NOT NULL,
            expires_at DATETIME NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS mechanics (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT UNIQUE NOT NULL,
            specialty VARCHAR(100) DEFAULT 'General',
            bio TEXT,
            experience_years INT DEFAULT 0,
            latitude DECIMAL(10,8),
            longitude DECIMAL(11,8),
            is_available BOOLEAN DEFAULT TRUE,
            rating DECIMAL(3,2) DEFAULT 0.00,
            total_jobs INT DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sos_requests (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            mechanic_id INT,
            latitude DECIMAL(10,8) NOT NULL,
            longitude DECIMAL(11,8) NOT NULL,
            issue_type VARCHAR(100) DEFAULT 'General',
            description TEXT,
            status ENUM('searching', 'dispatched', 'in_progress', 'completed', 'cancelled') DEFAULT 'searching',
            estimated_arrival INT,
            actual_arrival TIMESTAMP NULL,
            completed_at TIMESTAMP NULL,
            fare DECIMAL(10,2),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (mechanic_id) REFERENCES mechanics(id) ON DELETE SET NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ratings (
            id INT AUTO_INCREMENT PRIMARY KEY,
            request_id INT UNIQUE NOT NULL,
            mechanic_id INT NOT NULL,
            user_id INT NOT NULL,
            rating TINYINT NOT NULL CHECK (rating BETWEEN 1 AND 5),
            review TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (request_id) REFERENCES sos_requests(id) ON DELETE CASCADE,
            FOREIGN KEY (mechanic_id) REFERENCES mechanics(id) ON DELETE CASCADE,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notifications (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            title VARCHAR(200) NOT NULL,
            message TEXT NOT NULL,
            type ENUM('info', 'success', 'warning', 'error') DEFAULT 'info',
            is_read BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS payments (
            id INT AUTO_INCREMENT PRIMARY KEY,
            request_id INT NOT NULL,
            user_id INT NOT NULL,
            amount DECIMAL(10,2) NOT NULL,
            method ENUM('cash', 'card', 'upi') DEFAULT 'cash',
            status ENUM('pending', 'completed', 'refunded') DEFAULT 'pending',
            transaction_id VARCHAR(100),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (request_id) REFERENCES sos_requests(id) ON DELETE CASCADE,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    """)

    # Create default admin user if not exists
    cursor.execute("SELECT id FROM users WHERE email='admin@mechanicgo.com'")
    if not cursor.fetchone():
        import hashlib
        pw = hashlib.sha256("admin123".encode()).hexdigest()
        cursor.execute(
            "INSERT INTO users (name, email, password_hash, role) VALUES (%s,%s,%s,'admin')",
            ("Admin", "admin@mechanicgo.com", pw)
        )

    conn.commit()
    conn.close()
    print("✅ Database initialized successfully")
