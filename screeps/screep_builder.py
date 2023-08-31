class screep_builder():
    def __init__(self, role, energy):
        self.role = role
        self.energy = energy
        self.cost = 0
        self.parts = self.get_parts()
        self.part_dict = self.get_part_dict()
        self.body = self.get_body()

    def get_parts(self):
        WORK = 'WORK'
        CARRY = 'CARRY'
        MOVE = 'MOVE'
        ATTACK = 'ATTACK'
        RANGED_ATTACK = 'RANGED_ATTACK'
        HEAL = 'HEAL'
        TOUGH = 'TOUGH'
        CLAIM = 'CLAIM'

        worker_roles = ['harvester', 'upgrader', 'builder']

        if self.role in worker_roles:
            return {WORK: -1, CARRY: -1, MOVE: -1}
        elif self.role == 'guard':
            return {WORK: -1, CARRY: -1, ATTACK: 1, MOVE: -1}
        elif self.role == 'ranged_guard':
            return {WORK: -1, CARRY: -1, RANGED_ATTACK: 1, MOVE: -1}
        elif self.role == 'defender':
            return {ATTACK: -1, MOVE: -1}
        elif self.role == 'ranged_defender':
            return {RANGED_ATTACK: -1, MOVE: -1}
        else:
            return {WORK: -1, CARRY: -1, MOVE: -1}

    def get_part_dict(self):
        return {part: self.parts[part] for part in self.parts}

    def get_body(self):
        costs = {
            'WORK': 100,
            'CARRY': 50,
            'MOVE': 50,
            'ATTACK': 80,
            'RANGED_ATTACK': 150,
            'HEAL': 250,
            'TOUGH': 10,
            'CLAIM': 600
        }
        cost_list = [costs[part] for part in self.part_dict]
        min_cost = min(cost_list)
        body = []
        while self.cost < self.energy:
            print(self.cost, self.energy)
            for part in self.part_dict:
                print(part, self.part_dict[part])
                part_name = part
                part_count = self.part_dict[part]
                if part_count != 0 and self.cost + costs[part] <= self.energy:
                    body.extend([part_name])
                    self.part_dict[part] -= 1
                    self.cost += costs[part]
            if self.cost + min_cost > self.energy:
                break
        return body
