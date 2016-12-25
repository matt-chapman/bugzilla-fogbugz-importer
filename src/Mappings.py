# for mapping Bugzilla usernames to FogBugz usernames
users = {'OldUser': "NewUser"}

# for mapping Bugzilla project names to Fogbugz project names
projects = {'OldProject': "NewProject"}

# for mapping Bugzilla resolutions to Fogbuz resolutions, by int ID
# see fogbugz settings panel for IDs.
resolutions = {'FIXED': 2, 'INVALID': 7, 'UNFEASIBLE': 6, 'DUPLICATE': 4, 'WORKSFORME': 3}

# all unclosed BugZilla bugs should be open in FogBugz
statuses = {'CONFIRMED': 1}

# for mapping equivalent bug priorities between Bugzilla and FogBugz
priorities = {'Low': 5, 'High': 1, 'Normal': 3}
