# Fantasy Hockey Flask App
import os
from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'hockey.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # register database functions
    from . import db
    db.init_app(app)

    # register blueprints
    from . import players, teams, leagues
    app.register_blueprint(players.bp)
    app.register_blueprint(teams.bp)
    app.register_blueprint(leagues.bp)

    # home page
    @app.route('/')
    def index():
        from flask import render_template
        from .db import get_db

        # Get some basic stats for the dashboard
        db = get_db()
        stats = {}

        try:
            stats['total_players'] = db.execute('SELECT COUNT(*) as count FROM players').fetchone()['count']
            stats['total_teams'] = db.execute('SELECT COUNT(*) as count FROM fantasy_teams').fetchone()['count']
            stats['total_leagues'] = db.execute('SELECT COUNT(*) as count FROM fantasy_leagues').fetchone()['count']
            stats['total_nhl_teams'] = db.execute('SELECT COUNT(*) as count FROM nhl_teams').fetchone()['count']
        except Exception:
            # If tables don't exist yet, show zeros
            stats = {'total_players': 0, 'total_teams': 0, 'total_leagues': 0, 'total_nhl_teams': 0}

        return render_template('index.html', stats=stats)

    return app
