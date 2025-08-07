#!/usr/bin/env python3
"""
Script to populate the hockey database with test data.
"""

import sqlite3
import os
from datetime import datetime

def init_test_data():
    # Connect to the database
    db_path = 'instance/hockey.sqlite'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    print("Adding test data to database...")

    # Add NHL Teams
    teams_data = [
        # Eastern Conference - Atlantic Division
        ('Bruins', 'Boston', 'BOS', 'Eastern', 'Atlantic'),
        ('Sabres', 'Buffalo', 'BUF', 'Eastern', 'Atlantic'),
        ('Red Wings', 'Detroit', 'DET', 'Eastern', 'Atlantic'),
        ('Panthers', 'Florida', 'FLA', 'Eastern', 'Atlantic'),
        ('Canadiens', 'Montreal', 'MTL', 'Eastern', 'Atlantic'),
        ('Senators', 'Ottawa', 'OTT', 'Eastern', 'Atlantic'),
        ('Lightning', 'Tampa Bay', 'TBL', 'Eastern', 'Atlantic'),
        ('Maple Leafs', 'Toronto', 'TOR', 'Eastern', 'Atlantic'),

        # Eastern Conference - Metropolitan Division
        ('Hurricanes', 'Carolina', 'CAR', 'Eastern', 'Metropolitan'),
        ('Blue Jackets', 'Columbus', 'CBJ', 'Eastern', 'Metropolitan'),
        ('Devils', 'New Jersey', 'NJD', 'Eastern', 'Metropolitan'),
        ('Islanders', 'New York', 'NYI', 'Eastern', 'Metropolitan'),
        ('Rangers', 'New York', 'NYR', 'Eastern', 'Metropolitan'),
        ('Flyers', 'Philadelphia', 'PHI', 'Eastern', 'Metropolitan'),
        ('Penguins', 'Pittsburgh', 'PIT', 'Eastern', 'Metropolitan'),
        ('Capitals', 'Washington', 'WSH', 'Eastern', 'Metropolitan'),

        # Western Conference - Central Division
        ('Blackhawks', 'Chicago', 'CHI', 'Western', 'Central'),
        ('Avalanche', 'Colorado', 'COL', 'Western', 'Central'),
        ('Stars', 'Dallas', 'DAL', 'Western', 'Central'),
        ('Wild', 'Minnesota', 'MIN', 'Western', 'Central'),
        ('Predators', 'Nashville', 'NSH', 'Western', 'Central'),
        ('Blues', 'St. Louis', 'STL', 'Western', 'Central'),
        ('Jets', 'Winnipeg', 'WPG', 'Western', 'Central'),

        # Western Conference - Pacific Division
        ('Ducks', 'Anaheim', 'ANA', 'Western', 'Pacific'),
        ('Coyotes', 'Arizona', 'ARI', 'Western', 'Pacific'),
        ('Flames', 'Calgary', 'CGY', 'Western', 'Pacific'),
        ('Oilers', 'Edmonton', 'EDM', 'Western', 'Pacific'),
        ('Kings', 'Los Angeles', 'LAK', 'Western', 'Pacific'),
        ('Sharks', 'San Jose', 'SJS', 'Western', 'Pacific'),
        ('Kraken', 'Seattle', 'SEA', 'Western', 'Pacific'),
        ('Canucks', 'Vancouver', 'VAN', 'Western', 'Pacific'),
        ('Golden Knights', 'Vegas', 'VGK', 'Western', 'Pacific'),
    ]

    cursor.executemany(
        'INSERT INTO nhl_teams (name, city, abbreviation, conference, division) VALUES (?, ?, ?, ?, ?)',
        teams_data
    )

    # Add some star players
    players_data = [
        # Boston Bruins
        ('David Pastrnak', 'RW', 1, 88, 28, '6-0', 194),
        ('Patrice Bergeron', 'C', 1, 37, 38, '6-1', 195),
        ('Brad Marchand', 'LW', 1, 63, 35, '5-9', 181),
        ('Charlie McAvoy', 'D', 1, 73, 26, '6-0', 208),
        ('Jeremy Swayman', 'G', 1, 1, 25, '6-2', 192),

        # Toronto Maple Leafs
        ('Auston Matthews', 'C', 8, 34, 26, '6-3', 220),
        ('Mitch Marner', 'RW', 8, 16, 26, '6-0', 175),
        ('William Nylander', 'RW', 8, 88, 27, '6-0', 196),
        ('Morgan Rielly', 'D', 8, 44, 29, '6-0', 218),
        ('Joseph Woll', 'G', 8, 60, 25, '6-3', 203),

        # Tampa Bay Lightning
        ('Steven Stamkos', 'C', 7, 91, 34, '6-1', 188),
        ('Nikita Kucherov', 'RW', 7, 86, 30, '5-11', 178),
        ('Victor Hedman', 'D', 7, 77, 33, '6-6', 223),
        ('Andrei Vasilevskiy', 'G', 7, 88, 29, '6-3', 225),

        # Edmonton Oilers
        ('Connor McDavid', 'C', 26, 97, 27, '6-1', 193),
        ('Leon Draisaitl', 'C', 26, 29, 28, '6-2', 208),
        ('Ryan Nugent-Hopkins', 'C', 26, 93, 30, '6-0', 184),
        ('Evan Bouchard', 'D', 26, 2, 24, '6-2', 193),
        ('Stuart Skinner', 'G', 26, 74, 25, '6-4', 206),

        # Colorado Avalanche
        ('Nathan MacKinnon', 'C', 22, 29, 28, '6-0', 200),
        ('Mikko Rantanen', 'RW', 22, 96, 27, '6-4', 215),
        ('Cale Makar', 'D', 22, 8, 25, '5-11', 187),
        ('Alexandar Georgiev', 'G', 22, 40, 28, '6-1', 170),

        # Free agents / unsigned players
        ('Tyler Seguin', 'C', None, None, 32, '6-1', 200),
        ('Johnny Gaudreau', 'LW', None, None, 30, '5-9', 165),
    ]

    cursor.executemany(
        'INSERT INTO players (name, position, team_id, jersey_number, age, height, weight) VALUES (?, ?, ?, ?, ?, ?, ?)',
        players_data
    )

    # Add some player stats for 2023-24 season
    # Get player IDs first
    cursor.execute('SELECT id, name FROM players')
    player_ids = {name: id for id, name in cursor.fetchall()}

    stats_data = [
        # David Pastrnak
        (player_ids['David Pastrnak'], '2023-24', 82, 47, 63, 110, 8, 42, 0, 0, 0, 0.0, 0.0, 0),
        # Auston Matthews
        (player_ids['Auston Matthews'], '2023-24', 81, 69, 38, 107, 5, 55, 0, 0, 0, 0.0, 0.0, 0),
        # Connor McDavid
        (player_ids['Connor McDavid'], '2023-24', 76, 32, 100, 132, 21, 24, 0, 0, 0, 0.0, 0.0, 0),
        # Nathan MacKinnon
        (player_ids['Nathan MacKinnon'], '2023-24', 82, 51, 89, 140, 28, 94, 0, 0, 0, 0.0, 0.0, 0),
        # Jeremy Swayman (goalie stats)
        (player_ids['Jeremy Swayman'], '2023-24', 44, 0, 0, 0, 0, 0, 25, 10, 1114, 0.916, 2.53, 3),
        # Andrei Vasilevskiy (goalie stats)
        (player_ids['Andrei Vasilevskiy'], '2023-24', 53, 0, 0, 0, 0, 0, 28, 19, 1387, 0.900, 2.90, 4),
    ]

    cursor.executemany('''
        INSERT INTO player_stats
        (player_id, season, games_played, goals, assists, points, plus_minus, penalty_minutes,
         wins, losses, saves, save_percentage, goals_against_average, shutouts)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', stats_data)

    # Add some fantasy users
    users_data = [
        ('admin', 'admin@hockey.com', 'hashed_password_1'),
        ('hockey_fan', 'fan@hockey.com', 'hashed_password_2'),
        ('commissioner', 'commish@hockey.com', 'hashed_password_3'),
        ('player1', 'player1@hockey.com', 'hashed_password_4'),
        ('player2', 'player2@hockey.com', 'hashed_password_5'),
    ]

    cursor.executemany(
        'INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)',
        users_data
    )

    # Add a fantasy league
    cursor.execute(
        'INSERT INTO fantasy_leagues (name, commissioner_id, max_teams, scoring_system, season) VALUES (?, ?, ?, ?, ?)',
        ('Test League 2024', 3, 8, 'standard', '2024-25')
    )

    # Add some fantasy teams
    fantasy_teams_data = [
        ('Ice Breakers', 1, 1),
        ('Goal Diggers', 2, 1),
        ('Puck Dynasty', 4, 1),
        ('Stick Handlers', 5, 1),
    ]

    cursor.executemany(
        'INSERT INTO fantasy_teams (name, owner_id, league_id) VALUES (?, ?, ?)',
        fantasy_teams_data
    )

    # Add some players to fantasy rosters
    fantasy_roster_data = [
        # Ice Breakers roster
        (1, player_ids['Connor McDavid'], 'starter'),
        (1, player_ids['David Pastrnak'], 'starter'),
        (1, player_ids['Jeremy Swayman'], 'starter'),
        (1, player_ids['Cale Makar'], 'starter'),

        # Goal Diggers roster
        (2, player_ids['Auston Matthews'], 'starter'),
        (2, player_ids['Nathan MacKinnon'], 'starter'),
        (2, player_ids['Andrei Vasilevskiy'], 'starter'),

        # Puck Dynasty roster
        (3, player_ids['Leon Draisaitl'], 'starter'),
        (3, player_ids['Mikko Rantanen'], 'starter'),
        (3, player_ids['Victor Hedman'], 'starter'),
    ]

    cursor.executemany(
        'INSERT INTO fantasy_team_players (fantasy_team_id, player_id, position_type) VALUES (?, ?, ?)',
        fantasy_roster_data
    )

    conn.commit()
    conn.close()
    print("Test data added successfully!")


if __name__ == '__main__':
    init_test_data()
