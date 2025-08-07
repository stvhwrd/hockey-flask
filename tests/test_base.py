import os
import tempfile
import unittest
from flaskr import create_app
from flaskr.db import get_db, init_db


class HockeyTestCase(unittest.TestCase):
    """Base test case for the hockey application."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        # Create a temporary file for the test database
        self.db_fd, self.db_path = tempfile.mkstemp()

        # Create test app with temporary database
        self.app = create_app({
            'TESTING': True,
            'DATABASE': self.db_path,
        })

        # Create application context and initialize database
        with self.app.app_context():
            init_db()
            self._populate_test_data()

        # Create test client
        self.client = self.app.test_client()

    def tearDown(self):
        """Clean up after each test method."""
        os.close(self.db_fd)
        os.unlink(self.db_path)

    def _populate_test_data(self):
        """Populate the test database with minimal test data."""
        db = get_db()

        # Add a few test NHL teams
        teams_data = [
            ('Bruins', 'Boston', 'BOS', 'Eastern', 'Atlantic'),
            ('Maple Leafs', 'Toronto', 'TOR', 'Eastern', 'Atlantic'),
            ('Oilers', 'Edmonton', 'EDM', 'Western', 'Pacific'),
        ]

        db.executemany(
            'INSERT INTO nhl_teams (name, city, abbreviation, conference, division) VALUES (?, ?, ?, ?, ?)',
            teams_data
        )

        # Add test players
        players_data = [
            ('Connor McDavid', 'C', 3, 97, 27, '6-1', 193),
            ('Auston Matthews', 'C', 2, 34, 26, '6-3', 220),
            ('David Pastrnak', 'RW', 1, 88, 28, '6-0', 194),
            ('Test Player', 'LW', None, None, 25, '6-0', 185),  # Free agent
        ]

        db.executemany(
            'INSERT INTO players (name, position, team_id, jersey_number, age, height, weight) VALUES (?, ?, ?, ?, ?, ?, ?)',
            players_data
        )

        # Add test users
        users_data = [
            ('testuser', 'test@example.com', 'hashed_password'),
            ('commissioner', 'commish@example.com', 'hashed_password2'),
        ]

        db.executemany(
            'INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)',
            users_data
        )

        # Add test fantasy league
        db.execute(
            'INSERT INTO fantasy_leagues (name, commissioner_id, max_teams, scoring_system, season) VALUES (?, ?, ?, ?, ?)',
            ('Test League', 2, 4, 'standard', '2024-25')
        )

        # Add test fantasy team
        db.execute(
            'INSERT INTO fantasy_teams (name, owner_id, league_id) VALUES (?, ?, ?)',
            ('Test Team', 1, 1)
        )

        # Add player to fantasy roster
        db.execute(
            'INSERT INTO fantasy_team_players (fantasy_team_id, player_id, position_type) VALUES (?, ?, ?)',
            (1, 1, 'starter')  # McDavid to Test Team
        )

        # Add some player stats
        stats_data = [
            (1, '2023-24', 76, 32, 100, 132, 21, 24, 0, 0, 0, 0.0, 0.0, 0),  # McDavid
            (2, '2023-24', 81, 69, 38, 107, 5, 55, 0, 0, 0, 0.0, 0.0, 0),   # Matthews
        ]

        db.executemany('''
            INSERT INTO player_stats
            (player_id, season, games_played, goals, assists, points, plus_minus, penalty_minutes,
             wins, losses, saves, save_percentage, goals_against_average, shutouts)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', stats_data)

        db.commit()


if __name__ == '__main__':
    unittest.main()
