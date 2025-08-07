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

    return render_template('leagues.html', leagues=leagues)


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

    return render_template('league_detail.html', league=league, teams=teams)


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

    return render_template('team_detail.html', team=team, roster=roster, league_id=league_id)


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
