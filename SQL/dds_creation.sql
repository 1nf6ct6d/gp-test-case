
-- Создание hub_user

CREATE TABLE IF NOT EXISTS dds.hub_user(
    user_hk VARCHAR(32) PRIMARY KEY,
    user_id INTEGER NOT NULL,
    load_dttm TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    source VARCHAR(100)
);

-- Создание hub_post

CREATE TABLE IF NOT EXISTS dds.hub_post(
    post_hk VARCHAR(32) PRIMARY KEY,
    post_id INTEGER NOT NULL,
    load_dttm TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    source VARCHAR(100)
);

-- Создание link_user_post

CREATE TABLE IF NOT EXISTS dds.link_user_post (
    user_post_hk VARCHAR(32) PRIMARY KEY,
    user_hk VARCHAR(32) NOT NULL,
    post_hk VARCHAR(32) NOT NULL,
    load_dttm TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    source VARCHAR(100),

    CONSTRAINT fk_link_user
        FOREIGN KEY (user_hk)
        REFERENCES dds.hub_user(user_hk),

    CONSTRAINT fk_link_post
        FOREIGN KEY (post_hk)
        REFERENCES dds.hub_post(post_hk)
);

-- Создание sat_post
CREATE TABLE IF NOT EXISTS dds.sat_post (
    post_hk VARCHAR(32) NOT NULL,
    title TEXT,
    body TEXT,
    hashdiff VARCHAR(32) NOT NULL,
    load_dttm TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    source VARCHAR(100),

    PRIMARY KEY (post_hk, load_dttm),

    CONSTRAINT fk_sat_post
        FOREIGN KEY (post_hk)
        REFERENCES dds.hub_post(post_hk)
);
