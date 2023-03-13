import json

config = json.load(open('config.json.example', 'r'))
base_xp = json.load(open('migration_log.json', 'r'))
xp_increase = json.load(open('xp.json', 'r'))

bonus_xp = config['bonus_xp']
start = config['starting_xp']

for name in base_xp:
    xp = base_xp[name]
    if name in xp_increase:
        xp += xp_increase[name]
    xp += bonus_xp

for name in xp_increase:
    if name not in base_xp:
        xp = xp_increase[name] + bonus_xp + start
        base_xp[name] = xp

json.dump(base_xp, open('new_xp.json', 'w'), indent=4)
