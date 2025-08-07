import json
import unittest
from tests.test_base import HockeyTestCase


class RoutesTestCase(HockeyTestCase):
    """Test web routes and endpoints."""

    def test_home_page(self):
        """Test that the home page loads correctly."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Fantasy Hockey Platform', response.data)
        self.assertIn(b'Players', response.data)
        self.assertIn(b'Teams', response.data)
        self.assertIn(b'Leagues', response.data)

    def test_players_list(self):
        """Test the players list page."""
        response = self.client.get('/players/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Players', response.data)
        self.assertIn(b'Connor McDavid', response.data)
        self.assertIn(b'Auston Matthews', response.data)
        self.assertIn(b'David Pastrnak', response.data)

    def test_player_detail(self):
        """Test individual player detail pages."""
        # Test McDavid's page (player ID 1)
        response = self.client.get('/players/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Connor McDavid', response.data)
        self.assertIn(b'Position', response.data)
        self.assertIn(b'Team', response.data)
        self.assertIn(b'Stats', response.data)

    def test_player_not_found(self):
        """Test that non-existent player returns 404."""
        response = self.client.get('/players/999')
        self.assertEqual(response.status_code, 404)

    def test_teams_list(self):
        """Test the teams list page."""
        response = self.client.get('/teams/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'NHL Teams', response.data)
        self.assertIn(b'Boston Bruins', response.data)
        self.assertIn(b'Toronto Maple Leafs', response.data)
        self.assertIn(b'Edmonton Oilers', response.data)

    def test_team_detail(self):
        """Test individual team detail pages."""
        # Test Oilers page (team ID 3)
        response = self.client.get('/teams/3')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Edmonton Oilers', response.data)
        self.assertIn(b'Conference', response.data)
        self.assertIn(b'Division', response.data)
        self.assertIn(b'Roster', response.data)
        self.assertIn(b'Connor McDavid', response.data)

    def test_team_not_found(self):
        """Test that non-existent team returns 404."""
        response = self.client.get('/teams/999')
        self.assertEqual(response.status_code, 404)

    def test_leagues_list(self):
        """Test the fantasy leagues list page."""
        response = self.client.get('/leagues/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Fantasy Leagues', response.data)
        self.assertIn(b'Test League', response.data)

    def test_league_detail(self):
        """Test individual league detail pages."""
        response = self.client.get('/leagues/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test League', response.data)
        self.assertIn(b'Commissioner', response.data)
        self.assertIn(b'Teams', response.data)
        self.assertIn(b'Test Team', response.data)

    def test_fantasy_team_detail(self):
        """Test fantasy team detail pages."""
        response = self.client.get('/leagues/1/teams/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Team', response.data)
        self.assertIn(b'Owner', response.data)
        self.assertIn(b'Roster', response.data)
        self.assertIn(b'Connor McDavid', response.data)

    def test_league_not_found(self):
        """Test that non-existent league returns 404."""
        response = self.client.get('/leagues/999')
        self.assertEqual(response.status_code, 404)

    def test_fantasy_team_not_found(self):
        """Test that non-existent fantasy team returns 404."""
        response = self.client.get('/leagues/1/teams/999')
        self.assertEqual(response.status_code, 404)


class APITestCase(HockeyTestCase):
    """Test API endpoints."""

    def test_players_api(self):
        """Test the players API endpoint."""
        response = self.client.get('/players/api')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')

        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 4)

        # Check McDavid's data
        mcdavid = next(p for p in data if p['name'] == 'Connor McDavid')
        self.assertEqual(mcdavid['position'], 'C')
        self.assertEqual(mcdavid['jersey_number'], 97)

    def test_teams_api(self):
        """Test the teams API endpoint."""
        response = self.client.get('/teams/api')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')

        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 3)

        # Check Oilers data
        oilers = next(t for t in data if t['abbreviation'] == 'EDM')
        self.assertEqual(oilers['city'], 'Edmonton')
        self.assertEqual(oilers['name'], 'Oilers')

    def test_leagues_api(self):
        """Test the leagues API endpoint."""
        response = self.client.get('/leagues/api')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')

        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['name'], 'Test League')


if __name__ == '__main__':
    unittest.main()
