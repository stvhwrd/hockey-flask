-- Fantasy Hockey Database Schema

-- Drop existing tables
DROP TABLE IF EXISTS fantasy_team_players;
DROP TABLE IF EXISTS fantasy_teams;
DROP TABLE IF EXISTS fantasy_leagues;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS player_stats;
DROP TABLE IF EXISTS players;
DROP TABLE IF EXISTS nhl_teams;

-- NHL Teams
CREATE TABLE nhl_teams (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    city TEXT NOT NULL,
    abbreviation TEXT NOT NULL UNIQUE,
    conference TEXT NOT NULL,
    division TEXT NOT NULL
);

-- Players
CREATE TABLE players (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    position TEXT NOT NULL,
    team_id INTEGER,
    jersey_number INTEGER,
    age INTEGER,
    height TEXT,
    weight INTEGER,
    FOREIGN KEY (team_id) REFERENCES nhl_teams (id)
);

-- Player Stats (season stats)
CREATE TABLE player_stats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id INTEGER NOT NULL,
    season TEXT NOT NULL,
    games_played INTEGER DEFAULT 0,
    goals INTEGER DEFAULT 0,
    assists INTEGER DEFAULT 0,
    points INTEGER DEFAULT 0,
    plus_minus INTEGER DEFAULT 0,
    penalty_minutes INTEGER DEFAULT 0,
    -- Goalie specific stats
    wins INTEGER DEFAULT 0,
    losses INTEGER DEFAULT 0,
    saves INTEGER DEFAULT 0,
    save_percentage REAL DEFAULT 0.0,
    goals_against_average REAL DEFAULT 0.0,
    shutouts INTEGER DEFAULT 0,
    FOREIGN KEY (player_id) REFERENCES players (id)
);

-- Fantasy Users
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Fantasy Leagues
CREATE TABLE fantasy_leagues (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    commissioner_id INTEGER NOT NULL,
    max_teams INTEGER DEFAULT 12,
    scoring_system TEXT DEFAULT 'standard',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    season TEXT NOT NULL,
    FOREIGN KEY (commissioner_id) REFERENCES users (id)
);

-- Fantasy Teams
CREATE TABLE fantasy_teams (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    owner_id INTEGER NOT NULL,
    league_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (owner_id) REFERENCES users (id),
    FOREIGN KEY (league_id) REFERENCES fantasy_leagues (id)
);

-- Fantasy Team Players (roster)
CREATE TABLE fantasy_team_players (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fantasy_team_id INTEGER NOT NULL,
    player_id INTEGER NOT NULL,
    position_type TEXT NOT NULL, -- 'starter', 'bench', 'ir'
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (fantasy_team_id) REFERENCES fantasy_teams (id),
    FOREIGN KEY (player_id) REFERENCES players (id),
    UNIQUE(fantasy_team_id, player_id)
);