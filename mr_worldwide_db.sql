-- Create the database
CREATE DATABASE IF NOT EXISTS mr_worldwide;
USE mr_worldwide;

-- Artist table
CREATE TABLE IF NOT EXISTS artists (
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    genres TEXT,
    popularity INT,
    followers INT
);

-- Albums table
CREATE TABLE IF NOT EXISTS albums (
    id VARCHAR(50) PRIMARY KEY,
    artist_id VARCHAR(50),
    name VARCHAR(255),
    release_date DATE,
    total_tracks INT,
    image_url TEXT,
    FOREIGN KEY (artist_id) REFERENCES artists(id)
);

-- Tracks table
CREATE TABLE IF NOT EXISTS tracks (
    id VARCHAR(50) PRIMARY KEY,
    album_id VARCHAR(50),
    name VARCHAR(255),
    duration_ms INT,
    explicit BOOLEAN,
    track_number INT,
    preview_url TEXT,
    FOREIGN KEY (album_id) REFERENCES albums(id)
);

