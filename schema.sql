CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    is_admin BOOLEAN
);
CREATE TABLE platforms (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE,
    visible BOOLEAN
);
CREATE TABLE games (
    id SERIAL PRIMARY KEY,
    platform_id INTEGER REFERENCES platforms,
    name TEXT,
    visible BOOLEAN
);
CREATE TABLE collection_items (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    game_id INTEGER REFERENCES games,
    story_completed BOOLEAN,
    full_completion BOOLEAN,
    visible BOOLEAN
);
CREATE TABLE game_reviews (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    game_id INTEGER REFERENCES games,
    rating INTEGER,
    comments TEXT,
    review_added TIMESTAMP,
    visible BOOLEAN
);