-- MySQL Database Schema for Reptile Template
-- This file defines the database structure for scraped data

-- Main scraped data table
CREATE TABLE IF NOT EXISTS scraped_data (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    url VARCHAR(2048) NOT NULL UNIQUE,
    title VARCHAR(512),
    content LONGTEXT,
    scraped_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    status ENUM('pending', 'success', 'failed') DEFAULT 'pending',
    error_message TEXT,
    response_time DECIMAL(10,3),
    size INT,
    metadata JSON,  -- JSON metadata
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_url (url(255)),
    INDEX idx_status (status),
    INDEX idx_scraped_at (scraped_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- URL queue table for async processing
CREATE TABLE IF NOT EXISTS url_queue (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    url VARCHAR(2048) NOT NULL,
    priority INT DEFAULT 0,
    status ENUM('pending', 'processing', 'completed', 'failed') DEFAULT 'pending',
    retry_count INT DEFAULT 0,
    max_retries INT DEFAULT 3,
    scheduled_at DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_status (status),
    INDEX idx_priority (priority DESC)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Configuration table
CREATE TABLE IF NOT EXISTS config (
    `key` VARCHAR(128) PRIMARY KEY,
    value TEXT,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Insert default configuration
INSERT IGNORE INTO config (`key`, value) VALUES 
    ('db_version', '1.0'),
    ('last_cleanup', NOW());

-- Statistics view for monitoring
CREATE OR REPLACE VIEW scraping_stats AS
SELECT 
    status,
    COUNT(*) as count,
    AVG(response_time) as avg_response_time,
    SUM(size) as total_size,
    DATE(scraped_at) as date
FROM scraped_data 
GROUP BY status, DATE(scraped_at);
