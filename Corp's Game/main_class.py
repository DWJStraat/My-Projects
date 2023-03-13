import random
import json
import numpy as np
import pickle


class Character:
    def __init__(self, name, id, settings, game_name= 'game'):
        self.settings = settings
        self.list_of_characters = None
        self.id = id
        self.game_name = game_name
        self.Name = name
        self.alive = True

        self.advanced = self.settings['advanced']
        self.advance_increase = 0

        self.stats = self.settings['stats']
        deviation = self.stats['stat_deviation']
        self.Health = self.stats['health'] + np.random.normal(-1, 1) * deviation
        self.Speed = self.stats['speed'] + np.random.normal(-1, 1) * deviation
        self.Strength = self.stats['strength'] + np.random.normal(-1, 1) * deviation
        self.Skill = self.stats['skill'] + np.random.normal(-1, 1) * deviation
        self.attack_power = 0
        self.update_attack_power()

        self.action_list = []
        self.build_action_list()

        self.Hidden = False
        self.Attack_State = False
        self.Attacking = None

    def build_action_list(self):
        self.action_list = []
        for action in self.settings['action_weight']:
            self.action_list.extend([action] * self.settings['action_weight'][action])

    def advanced_weight(self):
        if self.advanced['active']:
            default_attack = max(self.stats['strength'], self.stats['speed']) + self.stats['skill']
            upper = default_attack + default_attack * self.advanced['threshold']
            lower = default_attack - default_attack * self.advanced['threshold']
            if self.attack_power > upper:
                dif = ((self.attack_power - upper) / self.advanced['step']) // 1 - self.advance_increase
                self.advance_increase += dif
                self.action_list.extend(['attack'] * int(dif * self.advanced['weight_increase']))
            elif self.attack_power < lower:
                dif = ((lower - self.attack_power) / self.advanced['step']) // 1 - self.advance_increase
                self.advance_increase -= dif
                self.action_list.extend(['hide'] * int(dif * self.advanced['weight_increase']))
            self.action_list.sort()

    def reset_action_state(self):
        self.Hidden = False
        self.Attack_State = False
        self.Attacking = None

    def get_stats(self):
        return {
            'HP': self.Health,
            'Spe': self.Speed,
            'Str': self.Strength,
            'Skl': self.Skill,
            'ATK': self.attack_power
        }

    def setup(self, list_of_characters):
        self.list_of_characters = list_of_characters
        self.list_of_characters.remove(self.id)

    def update_attack_power(self):
        self.attack_power = max(self.Strength, self.Speed) + self.Skill

    def new_day(self):
        if not self.alive:
            return
        self.advanced_weight()
        self.reset_action_state()
        self.update_attack_power()
        choice = random.choice(self.action_list)
        if choice == 'idle':
            return "Do nothing"
        elif choice == 'attack':
            self.Attacking = random.choice(self.list_of_characters)
            self.Attack_State = True
        elif choice == 'hide':
            self.Hidden = True
            return "Hide"
        elif choice == 'scavenge':
            return "Scavenge"
        elif choice == 'train':
            old_skill = self.Skill
            self.Train()
            return f"Train; Skill: {old_skill} --> {self.Skill}"
        else:
            raise ValueError("Choice is not valid")
            # This should never happen but just in case

    def Train(self):
        training_settings = self.settings['training']
        training_val = sum(
            np.random.random(1)[0] for _ in range(training_settings['rolls'])
        )
        training_val = training_val / training_settings['rolls'] * training_settings['mod'] - \
                       training_settings['threshold']
        if training_val < 0 and not training_settings['can_be_negative']:
            training_val = 0
        self.Skill += float(round(training_val, training_settings['max_decimals']))

    def set_HP(self, value):
        self.Health = value

    def get_HP(self):
        return self.Health

    def get_name(self):
        return self.Name

    def mourn(self, dead):
        if dead == self.id:
            self.alive = False
        else:
            self.list_of_characters.remove(dead)


class Game:
    def __init__(self, var_name):
        self.list_of_characters = None
        self.name = var_name
        self.turn = 0
        self.characters = []
        self.settings = json.load(open('settings.json'))
        self.localisation = json.load(open('localisation.json'))
        self.combat = self.settings['combat']



    def build_characters(self, character_list):
        self.characters.extend(
            Character(character_list[i], i, self.settings, self.name) for i in range(len(character_list))
        )
        self.character_count = len(self.characters)
        for character in self.characters:
            character.setup([*range(self.character_count)])

    def get_character(self, id):
        return self.characters[id]

    def new_day(self):
        self.turn += 1
        output = ''
        output += (f"Day {self.turn}\n----------------\n")
        for character in self.characters:
            new_day = character.new_day()
            if character.Attack_State:
                output += self.handle_attack(character.id, character.Attacking)
                output += "\n"
            else:
                output += (f"[{character.id}]{character.Name}: {new_day}\n")
        return output

    def handle_attack(self, attacker, defender):
        if not self.get_character(attacker).Attack_State:
            return(f"[{attacker}]{self.get_character(attacker).Name} tried to attack "
                  f"[{defender}]{self.get_character(defender).Name} but they were not in attack state "
                  f"(this should never happen)")
        if self.get_character(defender).Hidden:
            return(self.localisation['attack_failed'].format(
                attacker_name = self.get_character(attacker).Name,
                attacker_id = attacker,
                defender_name = self.get_character(defender).Name,
                defender_id = defender
            ))
        self.get_character(attacker).Attack_State = False
        self.get_character(attacker).Attacking = None
        return (self.fight(attacker, defender))

    def fight(self, attacker, defender):
        attack_HP = self.get_character(attacker).get_HP()
        defend_HP = self.get_character(defender).get_HP()
        if self.combat['defender_can_attack']:
            if self.combat('fire_emblem_mode'):
                self.handle_damage(attacker, defender)
                if self.vibe_check(defender):
                    return self.killer(attacker, defender)
                self.handle_damage(defender, attacker)
            else:
                self.handle_damage(attacker, defender)
                self.handle_damage(defender, attacker)
                if self.vibe_check(defender):
                    print(self.killer(attacker, defender))
            if self.vibe_check(attacker):
                print(self.killer(defender, attacker))
            attack_damage = attack_HP - self.get_character(attacker).get_HP()
            defend_damage = defend_HP - self.get_character(defender).get_HP()
            return self.localisation['double_attack'].format(
                attacker_name=self.get_character(attacker).get_name(),
                attacker_id=attacker,
                defender_name=self.get_character(defender).get_name(),
                defender_id=defender,
                attack_damage=attack_damage,
                defend_damage=defend_damage
            )
        else:
            self.handle_damage(attacker, defender)
            if self.vibe_check(defender):
                return(self.killer(attacker, defender))
            defend_damage = defend_HP - self.get_character(defender).get_HP()
            return self.localisation['single_attack'].format(
                attacker_name=self.get_character(attacker).get_name(),
                attacker_id=attacker,
                defender_name=self.get_character(defender).get_name(),
                defender_id=defender,
                defend_damage=defend_damage
            )

    def handle_damage(self, attacker, defender):
        attacker_stats = self.get_character(attacker).get_stats()
        defender_stats = self.get_character(defender).get_stats()
        defender_stats['HP'] -= self.calc_damage(attacker_stats, defender_stats)
        self.get_character(defender).set_HP(defender_stats['HP'])

    def killer(self, attacker, defender):
        return self.localisation['killed'].format(
            killer_name=self.get_character(attacker).get_name(),
            killer_id=attacker,
            player_name=self.get_character(defender).get_name(),
            player_id=defender
        )
    def vibe_check(self, character):
        if self.get_character(character).Health <= 0:
            self.get_character(character).alive = False
            self.get_character(character).mourn(character)
            # print(self.localisation['vibe_check_failed'].format(
            #     player_name=self.get_character(character).get_name(),
            #     player_id=character
            # ))
            return True
        return False

    def calc_damage(self, attacker_stats, defender_stats):
        defense_settings = self.combat['defense']
        damage = attacker_stats['ATK']*random.randint(self.combat['lower_roll'], self.combat['upper_roll'])
        defense = defense_settings['base']
        if defense_settings['speed']:
            defense += defender_stats['Spe']
        if defense_settings['skill']:
            defense += defender_stats['Skl']
        if defense_settings['strength']:
            defense += defender_stats['Str']
        return damage - defense

    def save(self):
        dict = self.__dict__
        with open(f'{self.name}.pkl', 'w') as f:
            pickle.dump(dict, f)

    def load(self):
        with open(f'{self.name}.pkl', 'r') as f:
            dict = pickle.load(f)
        self.__dict__ = dict

