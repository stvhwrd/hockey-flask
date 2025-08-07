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

    html = '<h1>NHL Teams</h1>'

    for conf_name, divisions in conferences.items():
        html += f'<h2>{conf_name} Conference</h2>'
        for div_name, div_teams in divisions.items():
            html += f'<h3>{div_name} Division</h3><ul>'
            for team in div_teams:
                html += f'<li><a href="/teams/{team["id"]}">{team["city"]} {team["name"]} ({team["abbreviation"]})</a></li>'
            html += '</ul>'

    html += '<a href="/">Back to Home</a>'
    return html


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

    html = f'''
    <h1>{team["city"]} {team["name"]}</h1>
    <p><strong>Abbreviation:</strong> {team["abbreviation"]}</p>
    <p><strong>Conference:</strong> {team["conference"]}</p>
    <p><strong>Division:</strong> {team["division"]}</p>

    <h2>Roster</h2>
    '''

    if players:
        # Group players by position
        positions = {}
        for player in players:
            pos = player['position']
            if pos not in positions:
                positions[pos] = []
            positions[pos].append(player)

        for pos, pos_players in positions.items():
            html += f'<h3>{pos}</h3><ul>'
            for player in pos_players:
                html += f'<li><a href="/players/{player["id"]}">{player["name"]} #{player["jersey_number"] or "N/A"}</a></li>'
            html += '</ul>'
    else:
        html += '<p>No players found</p>'

    html += '<br><a href="/teams">Back to Teams</a> | <a href="/">Home</a>'
    return html


@bp.route('/api')
def api():
    """API endpoint for teams data."""
    db = get_db()
    teams = db.execute(
        'SELECT * FROM nhl_teams ORDER BY conference, division, city'
    ).fetchall()

    return jsonify([dict(team) for team in teams])
