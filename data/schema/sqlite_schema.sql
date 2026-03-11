-- SQLite Database Schema for Reptile Template
-- This file defines the database structure for scraped data

-- Main scraped data table
CREATE TABLE IF NOT EXISTS scraped_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    url TEXT NOT NULL UNIQUE,
    title TEXT,
    content TEXT,
    scraped_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    status TEXT DEFAULT 'pending',
    error_message TEXT,
    response_time REAL,
    size INTEGER,
    metadata TEXT,  -- JSON metadata
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for better performance
CREATE INDEX IF NOT EXISTS idx_scraped_data_url ON scraped_data(url);
CREATE INDEX IF NOT EXISTS idx_scraped_data_status ON scraped_data(status);
CREATE INDEX IF NOT EXISTS idx_scraped_data_scraped_at ON scraped_data(scraped_at);

-- URL queue table for async processing
CREATE TABLE IF NOT EXISTS url_queue (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    url TEXT NOT NULL,
    priority INTEGER DEFAULT 0,
    status TEXT DEFAULT 'pending',
    retry_count INTEGER DEFAULT 0,
    max_retries INTEGER DEFAULT 3,
    scheduled_at DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for queue
CREATE INDEX IF NOT EXISTS idx_url_queue_status ON url_queue(status);
CREATE INDEX IF NOT EXISTS idx_url_queue_priority ON url_queue(priority DESC);

-- Configuration table
CREATE TABLE IF NOT EXISTS config (
    key TEXT PRIMARY KEY,
    value TEXT,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Insert default configuration
INSERT OR IGNORE INTO config (key, value) VALUES 
    ('db_version', '1.0'),
    ('last_cleanup', CURRENT_TIMESTAMP);

-- Trigger to update updated_at timestamp
CREATE TRIGGER IF NOT EXISTS update_scraped_data_updated_at 
AFTER UPDATE ON scraped_data
BEGIN
    UPDATE scraped_data SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;
