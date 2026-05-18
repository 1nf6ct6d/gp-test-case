
-- Создание таблицы api_posts

CREATE TABLE IF NOT EXISTS stg.api_posts(
    post_id INTEGER PRIMARY KEY,
    user_id INTEGER,
    title TEXT,
    body TEXT,
    load_dttm TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    source VARCHAR(100) DEFAULT 'jsonplaceholder'
);