from flask import Blueprint, render_template, request, jsonify
from flaskr.db import get_db

bp = Blueprint('teams', __name__, url_prefix='/teams')


@bp.route('/')
def index():
    """Show all NHL teams."""
    db = get_db()
    teams = db.execute(
        'SELECT * FROM nhl_teams ORDER BY conference, division, city'
    ).fetchall()

    # Group teams by conference and division
    conferences = {}
    for team in teams:
        conf = team['conference']
        div = team['division']
        if conf not in conferences:
            conferences[conf] = {}
        if div not in conferences[conf]:
            conferences[conf][div] = []
        conferences[conf][div].append(team)

    return render_template('teams.html', conferences=conferences)


@bp.route('/<int:id>')
def detail(id):
    """Show details for a specific team."""
    db = get_db()
    team = db.execute(
        'SELECT * FROM nhl_teams WHERE id = ?',
        (id,)
    ).fetchone()

    if team is None:
        return "Team not found", 404

    # Get team roster
    players = db.execute(
        'SELECT * FROM players WHERE team_id = ? ORDER BY position, name',
        (id,)
    ).fetchall()

    # Group players by position
    positions = {}
    for player in players:
        pos = player['position']
        if pos not in positions:
            positions[pos] = []
        positions[pos].append(player)

    return render_template('nhl_team_detail.html', team=team, positions=positions)


@bp.route('/api')
def api():
    """API endpoint for teams data."""
    db = get_db()
    teams = db.execute(
        'SELECT * FROM nhl_teams ORDER BY conference, division, city'
    ).fetchall()

    return jsonify([dict(team) for team in teams])
