TEAM_NAMES_DIC = {
  # AFC Bournemouth
  'Bournemouth': ['Bournemouth', 'AFC Bournemouth'],

  # Arsenal
  'Arsenal': ['Arsenal'],

  # Aston Villa
  'Villa': ['Aston Villa'],

  # Chelsea
  'Chelsea': ['Chelsea'],

  # Crystal Palace
  'Crystal': ['Crystal Palace'],

  # Everton
  'Everton': ['Everton'],

  # Leicester City
  'Leicester': ['Leicester City', 'Leicester'],

  # Liverpool
  'Liverpool': ['Liverpool'],

  # Manchester City
  'City': ['Manchester City'],

  # Manchester United
  'United': ['Manchester Utd', 'Manchester United'],

  # Newcastle United
  'Newcastle': ['Newcastle Utd', 'Newcastle United'],

  # Norwich City
  'Norwich': ['Norwich City', 'Norwich'],

  # Southampton
  'Southampton': ['Southampton'],

  # Stoke City
  'Stoke': ['Stoke City'],

  # Sunderland
  'Sunderland': ['Sunderland'],

  # Swansea City
  'Swansea': ['Swansea City', 'Swansea'],

  # Tottenham Hotspur
  'Tottenham': ['Tottenham', 'Tottenham Hotspur'],

  # Watford
  'Watford': ['Watford'],

  # West Bromwich Albion
  'WestBromwich': ['West Bromwich', 'West Bromwich Albion', 'West Brom'],

  # West Ham United
  'WestHam': ['West Ham Utd', 'West Ham United', 'West Ham'],
  }

TEAM_NAMES_DIC_ESPN = {
  # AFC Bournemouth
  'Bournemouth': ['AFC Bournemouth'],

  # Arsenal
  'Arsenal': ['Arsenal'],

  # Aston Villa
  'Aston Villa': ['Aston Villa'],

  # Chelsea
  'Chelsea': ['Chelsea'],

  # Crystal Palace
  'Crystal Palace': ['Crystal Palace'],

  # Everton
  'Everton': ['Everton'],

  # Leicester City
  'Leicester City': ['Leicester City'],

  # Liverpool
  'Liverpool': ['Liverpool'],

  # Manchester City
  'Manchester City': ['Manchester City'],

  # Manchester United
  'Manchester United': ['Manchester United'],

  # Newcastle United
  'Newcastle United': ['Newcastle United'],

  # Norwich City
  'Norwich City': ['Norwich City'],

  # Southampton
  'Southampton': ['Southampton'],

  # Stoke City
  'Stoke City': ['Stoke City'],

  # Sunderland
  'Sunderland': ['Sunderland'],

  # Swansea City
  'Swansea City': ['Swansea City'],

  # Tottenham Hotspur
  'Tottenham Hotspur': ['Tottenham Hotspur'],

  # Watford
  'Watford': ['Watford'],

  # West Bromwich Albion
  'West Bromwich Albion': ['West Bromwich Albion'],

  # West Ham United
  'West Ham United': ['West Ham United'],
  }


def ChangeTeamName(team):
    for key in TEAM_NAMES_DIC:
        if team in TEAM_NAMES_DIC[key]:
            return key


def ChangeESPNTeamName(team):
    for key in TEAM_NAMES_DIC_ESPN:
        if team in TEAM_NAMES_DIC_ESPN[key]:
            return key
