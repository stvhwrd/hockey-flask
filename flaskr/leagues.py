from flask import Blueprint, render_template, request, jsonify
from flaskr.db import get_db

bp = Blueprint('leagues', __name__, url_prefix='/leagues')


@bp.route('/')
def index():
    """Show all fantasy leagues."""
    db = get_db()
    leagues = db.execute(
        'SELECT fl.*, u.username as commissioner_name'
        ' FROM fantasy_leagues fl'
        ' JOIN users u ON fl.commissioner_id = u.id'
        ' ORDER BY fl.created_at DESC'
    ).fetchall()

    html = '<h1>Fantasy Leagues</h1>'

    if leagues:
        html += '<ul>'
        for league in leagues:
            html += f'<li><a href="/leagues/{league["id"]}">{league["name"]} (Commissioner: {league["commissioner_name"]})</a></li>'
        html += '</ul>'
    else:
        html += '<p>No fantasy leagues found</p>'

    html += '<a href="/">Back to Home</a>'
    return html


@bp.route('/<int:id>')
def detail(id):
    """Show details for a specific fantasy league."""
    db = get_db()
    league = db.execute(
        'SELECT fl.*, u.username as commissioner_name'
        ' FROM fantasy_leagues fl'
        ' JOIN users u ON fl.commissioner_id = u.id'
        ' WHERE fl.id = ?',
        (id,)
    ).fetchone()

    if league is None:
        return "League not found", 404

    # Get teams in this league
    teams = db.execute(
        'SELECT ft.*, u.username as owner_name'
        ' FROM fantasy_teams ft'
        ' JOIN users u ON ft.owner_id = u.id'
        ' WHERE ft.league_id = ?'
        ' ORDER BY ft.name',
        (id,)
    ).fetchall()

    html = f'''
    <h1>{league["name"]}</h1>
    <p><strong>Commissioner:</strong> {league["commissioner_name"]}</p>
    <p><strong>Max Teams:</strong> {league["max_teams"]}</p>
    <p><strong>Scoring System:</strong> {league["scoring_system"]}</p>
    <p><strong>Season:</strong> {league["season"]}</p>
    <p><strong>Created:</strong> {league["created_at"]}</p>

    <h2>Teams ({len(teams)}/{league["max_teams"]})</h2>
    '''

    if teams:
        html += '<ul>'
        for team in teams:
            html += f'<li><a href="/leagues/{id}/teams/{team["id"]}">{team["name"]} (Owner: {team["owner_name"]})</a></li>'
        html += '</ul>'
    else:
        html += '<p>No teams in this league yet</p>'

    html += '<br><a href="/leagues">Back to Leagues</a> | <a href="/">Home</a>'
    return html


@bp.route('/<int:league_id>/teams/<int:team_id>')
def team_detail(league_id, team_id):
    """Show details for a specific fantasy team."""
    db = get_db()

    # Get team info
    team = db.execute(
        'SELECT ft.*, u.username as owner_name, fl.name as league_name'
        ' FROM fantasy_teams ft'
        ' JOIN users u ON ft.owner_id = u.id'
        ' JOIN fantasy_leagues fl ON ft.league_id = fl.id'
        ' WHERE ft.id = ? AND ft.league_id = ?',
        (team_id, league_id)
    ).fetchone()

    if team is None:
        return "Team not found", 404

    # Get team roster
    roster = db.execute(
        'SELECT ftp.position_type, p.name, p.position, t.abbreviation as team_abbr'
        ' FROM fantasy_team_players ftp'
        ' JOIN players p ON ftp.player_id = p.id'
        ' LEFT JOIN nhl_teams t ON p.team_id = t.id'
        ' WHERE ftp.fantasy_team_id = ?'
        ' ORDER BY ftp.position_type, p.position, p.name',
        (team_id,)
    ).fetchall()

    html = f'''
    <h1>{team["name"]}</h1>
    <p><strong>Owner:</strong> {team["owner_name"]}</p>
    <p><strong>League:</strong> <a href="/leagues/{league_id}">{team["league_name"]}</a></p>

    <h2>Roster</h2>
    '''

    if roster:
        # Group by position type
        position_types = {}
        for player in roster:
            pos_type = player['position_type']
            if pos_type not in position_types:
                position_types[pos_type] = []
            position_types[pos_type].append(player)

        for pos_type, players in position_types.items():
            html += f'<h3>{pos_type.title()}</h3><ul>'
            for player in players:
                html += f'<li>{player["name"]} ({player["position"]}) - {player["team_abbr"] or "FA"}</li>'
            html += '</ul>'
    else:
        html += '<p>No players on roster</p>'

    html += f'<br><a href="/leagues/{league_id}">Back to League</a> | <a href="/leagues">Back to Leagues</a> | <a href="/">Home</a>'
    return html


@bp.route('/api')
def api():
    """API endpoint for leagues data."""
    db = get_db()
    leagues = db.execute(
        'SELECT fl.*, u.username as commissioner_name'
        ' FROM fantasy_leagues fl'
        ' JOIN users u ON fl.commissioner_id = u.id'
        ' ORDER BY fl.created_at DESC'
    ).fetchall()

    return jsonify([dict(league) for league in leagues])
