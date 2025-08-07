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

    # Simple HTML response for now
    html = '<h1>Players</h1><ul>'
    for player in players:
        html += f'<li><a href="/players/{player["id"]}">{player["name"]} - {player["position"]} - {player["team_name"] or "Free Agent"}</a></li>'
    html += '</ul><a href="/">Back to Home</a>'
    return html


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

    html = f'''
    <h1>{player["name"]}</h1>
    <p><strong>Position:</strong> {player["position"]}</p>
    <p><strong>Team:</strong> {player["team_name"] or "Free Agent"}</p>
    <p><strong>Jersey:</strong> #{player["jersey_number"] or "N/A"}</p>
    <p><strong>Age:</strong> {player["age"] or "N/A"}</p>
    <p><strong>Height:</strong> {player["height"] or "N/A"}</p>
    <p><strong>Weight:</strong> {player["weight"] or "N/A"} lbs</p>

    <h2>Stats</h2>
    '''

    if stats:
        html += '<table border="1"><tr><th>Season</th><th>GP</th><th>G</th><th>A</th><th>P</th><th>+/-</th><th>PIM</th></tr>'
        for stat in stats:
            html += f'''<tr>
                <td>{stat["season"]}</td>
                <td>{stat["games_played"]}</td>
                <td>{stat["goals"]}</td>
                <td>{stat["assists"]}</td>
                <td>{stat["points"]}</td>
                <td>{stat["plus_minus"]}</td>
                <td>{stat["penalty_minutes"]}</td>
            </tr>'''
        html += '</table>'
    else:
        html += '<p>No stats available</p>'

    html += '<br><a href="/players">Back to Players</a> | <a href="/">Home</a>'
    return html


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
