import unittest
from flaskr.db import get_db
from tests.test_base import HockeyTestCase


class DatabaseTestCase(HockeyTestCase):
    """Test database functionality."""

    def test_database_connection(self):
        """Test that database connection works."""
        with self.app.app_context():
            db = get_db()
            self.assertIsNotNone(db)

    def test_nhl_teams_data(self):
        """Test that NHL teams data is properly stored."""
        with self.app.app_context():
            db = get_db()
            teams = db.execute('SELECT * FROM nhl_teams ORDER BY city').fetchall()

            self.assertEqual(len(teams), 3)
            self.assertEqual(teams[0]['city'], 'Boston')
            self.assertEqual(teams[0]['name'], 'Bruins')
            self.assertEqual(teams[0]['abbreviation'], 'BOS')

    def test_players_data(self):
        """Test that players data is properly stored."""
        with self.app.app_context():
            db = get_db()
            players = db.execute('SELECT * FROM players ORDER BY name').fetchall()

            self.assertEqual(len(players), 4)

            # Test McDavid
            mcdavid = next(p for p in players if p['name'] == 'Connor McDavid')
            self.assertEqual(mcdavid['position'], 'C')
            self.assertEqual(mcdavid['jersey_number'], 97)
            self.assertEqual(mcdavid['team_id'], 3)  # Oilers

    def test_foreign_key_relationships(self):
        """Test that foreign key relationships work correctly."""
        with self.app.app_context():
            db = get_db()

            # Test player-team relationship
            result = db.execute('''
                SELECT p.name, t.city, t.name as team_name
                FROM players p
                JOIN nhl_teams t ON p.team_id = t.id
                WHERE p.name = ?
            ''', ('Connor McDavid',)).fetchone()

            self.assertEqual(result['city'], 'Edmonton')
            self.assertEqual(result['team_name'], 'Oilers')

    def test_player_stats(self):
        """Test that player statistics are stored correctly."""
        with self.app.app_context():
            db = get_db()
            stats = db.execute('''
                SELECT ps.*, p.name
                FROM player_stats ps
                JOIN players p ON ps.player_id = p.id
                WHERE p.name = ?
            ''', ('Connor McDavid',)).fetchone()

            self.assertEqual(stats['season'], '2023-24')
            self.assertEqual(stats['goals'], 32)
            self.assertEqual(stats['assists'], 100)
            self.assertEqual(stats['points'], 132)

    def test_fantasy_league_structure(self):
        """Test that fantasy league data structure is correct."""
        with self.app.app_context():
            db = get_db()

            # Test league exists
            league = db.execute('SELECT * FROM fantasy_leagues').fetchone()
            self.assertEqual(league['name'], 'Test League')
            self.assertEqual(league['max_teams'], 4)

            # Test team in league
            team = db.execute('''
                SELECT ft.*, u.username
                FROM fantasy_teams ft
                JOIN users u ON ft.owner_id = u.id
            ''').fetchone()
            self.assertEqual(team['name'], 'Test Team')
            self.assertEqual(team['username'], 'testuser')

            # Test player on roster
            roster = db.execute('''
                SELECT ftp.*, p.name
                FROM fantasy_team_players ftp
                JOIN players p ON ftp.player_id = p.id
            ''').fetchone()
            self.assertEqual(roster['name'], 'Connor McDavid')
            self.assertEqual(roster['position_type'], 'starter')


if __name__ == '__main__':
    unittest.main()
