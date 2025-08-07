import os
import tempfile
import unittest
from flaskr import create_app


class AppTestCase(unittest.TestCase):
    """Test application factory and configuration."""

    def test_create_app_default(self):
        """Test creating app with default configuration."""
        app = create_app()
        self.assertIsNotNone(app)
        self.assertEqual(app.config['SECRET_KEY'], 'dev')
        self.assertTrue(app.config['DATABASE'].endswith('hockey.sqlite'))

    def test_create_app_with_test_config(self):
        """Test creating app with test configuration."""
        test_config = {
            'TESTING': True,
            'SECRET_KEY': 'test_secret',
            'DATABASE': ':memory:'
        }

        app = create_app(test_config)
        self.assertTrue(app.config['TESTING'])
        self.assertEqual(app.config['SECRET_KEY'], 'test_secret')
        self.assertEqual(app.config['DATABASE'], ':memory:')

    def test_app_has_required_blueprints(self):
        """Test that all required blueprints are registered."""
        app = create_app({'TESTING': True})

        # Check that blueprints are registered
        blueprint_names = [bp.name for bp in app.blueprints.values()]
        self.assertIn('players', blueprint_names)
        self.assertIn('teams', blueprint_names)
        self.assertIn('leagues', blueprint_names)

    def test_app_context(self):
        """Test that app context works correctly."""
        app = create_app({'TESTING': True})

        with app.app_context():
            from flask import current_app
            self.assertEqual(current_app, app)

    def test_instance_path_creation(self):
        """Test that instance path is created."""
        # Create a temporary directory for testing
        with tempfile.TemporaryDirectory() as temp_dir:
            test_config = {
                'TESTING': True,
                'INSTANCE_PATH': temp_dir
            }

            app = create_app(test_config)
            # The instance path should exist
            self.assertTrue(os.path.exists(app.instance_path))


if __name__ == '__main__':
    unittest.main()
