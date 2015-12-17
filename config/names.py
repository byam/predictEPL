TEAM_NAMES_DIC = {
  # AFC Bournemouth
  'Bournemouth': ['Bournemouth'],

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
  'Leicester': ['Leicester City'],

  # Liverpool
  'Liverpool': ['Liverpool'],

  # Manchester City
  'City': ['Manchester City'],

  # Manchester United
  'United': ['Manchester Utd'],

  # Newcastle United
  'Newcastle': ['Newcastle Utd'],

  # Norwich City
  'Norwich': ['Norwich City'],

  # Southampton
  'Southampton': ['Southampton'],

  # Stoke City
  'Stoke': ['Stoke City'],

  # Sunderland
  'Sunderland': ['Sunderland'],

  # Swansea City
  'Swansea': ['Swansea City'],

  # Tottenham Hotspur
  'Tottenham': ['Tottenham'],

  # Watford
  'Watford': ['Watford'],

  # West Bromwich Albion
  'WestBromwich': ['West Bromwich'],

  # West Ham United
  'WestHam': ['West Ham Utd'],
  }


def ChangeTeamName(team):
    for key in TEAM_NAMES_DIC:
        if team in TEAM_NAMES_DIC[key]:
            return key
