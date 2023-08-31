import screepsapi
import time
import json
from screep_builder import screep_builder

debug = True
run = True

TOKEN = '02065424-0901-4b8d-ada3-0542a94ffad7'
api = screepsapi.API(token=TOKEN)
while run:
    update = False
    memory = api.memory('', 'shard3')['data']
    spawns = memory['spawns']
    creep_count = memory['creep_count']
    old_memory = json.load(open('memory.json'))
    roles = []
    for i in creep_count:
        roles.append(i)
    for i in spawns:
        spawn = spawns[i]
        old_spawn = old_memory['spawns'][i]
        max_energy = spawn['max_energy']
        old_max_energy = old_spawn['max_energy']
        energy = spawn['energy']
        old_energy = old_spawn['energy']
        print(f'{i} has {energy} energy out of {max_energy} max energy')
        if energy > old_energy:
            print(f'{i} has gained {energy - old_energy} energy')
        if max_energy > old_max_energy:
            print(f'{i} has gained {max_energy - old_max_energy} max energy')
            creep_types = ['harvester',
                           'upgrader',
                           'builder',
                           'guard',
                           'static_miner']
            for role in creep_types:
                creep = screep_builder(role, max_energy)
                spawn['creepSpecs'][role] = creep.body
                print(f'{i} has added {role} to its creepSpecs')
                update = True
    if update:
        api.set_memory('', memory, 'shard3')
        json.dump(memory, open('memory.json', 'w'))
    if debug:
        run = False
    else:
        time.sleep(60)

