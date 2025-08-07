from flask import Blueprint, render_template, request, jsonify
from flaskr.db import get_db

bp = Blueprint('players', __name__, url_prefix='/players')


@bp.route('/')
def index():
    """Show all players."""
    db = get_db()
    players = db.execute(
        'SELECT p.id, p.name, p.position, p.jersey_number, p.age, t.name as team_name, t.abbreviation'
        ' FROM players p'
        ' LEFT JOIN nhl_teams t ON p.team_id = t.id'
        ' ORDER BY p.name'
    ).fetchall()
    
    return render_template('players.html', players=players)
@bp.route('/<int:id>')
def detail(id):
    """Show details for a specific player."""
    db = get_db()
    player = db.execute(
        'SELECT p.*, t.name as team_name, t.abbreviation'
        ' FROM players p'
        ' LEFT JOIN nhl_teams t ON p.team_id = t.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()
    
    if player is None:
        return "Player not found", 404
    
    # Get player stats
    stats = db.execute(
        'SELECT * FROM player_stats WHERE player_id = ? ORDER BY season DESC',
        (id,)
    ).fetchall()
    
    return render_template('player_detail.html', player=player, stats=stats)
@bp.route('/api')
def api():
    """API endpoint for players data."""
    db = get_db()
    players = db.execute(
        'SELECT p.id, p.name, p.position, p.jersey_number, p.age, t.name as team_name, t.abbreviation'
        ' FROM players p'
        ' LEFT JOIN nhl_teams t ON p.team_id = t.id'
        ' ORDER BY p.name'
    ).fetchall()

    return jsonify([dict(player) for player in players])
