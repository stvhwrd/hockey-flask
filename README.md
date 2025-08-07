# Fantasy Hockey Platform

A Flask-based fantasy hockey web application with a SQLite database.

## Features

- **NHL Teams**: Browse all NHL teams organized by conference and division
- **Players**: View player profiles with stats and team information
- **Fantasy Leagues**: Manage fantasy hockey leagues with teams and rosters
- **Database**: Complete hockey database schema with teams, players, stats, and fantasy data

## Quick Start

1. Activate your virtual environment:

   ```bash
   source .venv/bin/activate
   ```

2. Initialize the database (first time only):

   ```bash
   export FLASK_APP=flaskr
   flask init-db
   ```

3. Populate with test data (first time only):

   ```bash
   python populate_test_data.py
   ```

4. Run the application:

   ```bash
   python app.py
   ```

5. Visit <http://localhost:5000> in your browser

## Application Structure

```
├── app.py                    # Main application entry point
├── flaskr/                   # Flask application package
│   ├── __init__.py          # Application factory
│   ├── db.py                # Database functions
│   ├── schema.sql           # Database schema
│   ├── players.py           # Players blueprint
│   ├── teams.py             # Teams blueprint
│   └── leagues.py           # Fantasy leagues blueprint
├── populate_test_data.py    # Script to add test data
├── setup.py                 # Setup script
└── instance/                # Instance folder (created automatically)
    └── hockey.sqlite        # SQLite database
```

## Database Schema

The application includes:

- **NHL Teams**: All 32 NHL teams with conference/division info
- **Players**: Player profiles with positions, stats, and team affiliations
- **Player Stats**: Season statistics including goals, assists, points
- **Fantasy Users**: User accounts for fantasy league participation
- **Fantasy Leagues**: League management with commissioners and settings
- **Fantasy Teams**: Team rosters within leagues
- **Fantasy Rosters**: Player assignments to fantasy teams

## API Endpoints

- `GET /players/api` - JSON list of all players
- `GET /teams/api` - JSON list of all teams
- `GET /leagues/api` - JSON list of all leagues

## Test Data

The application comes with sample data including:

- All 32 NHL teams
- Star players from various teams
- Sample fantasy league with teams and rosters
- Player statistics for the 2023-24 season

## Next Steps

Potential enhancements:

- User authentication and registration
- Draft functionality
- Scoring calculations
- Trade management
- Waiver wire system
- Season management
- Statistics tracking and analysis
