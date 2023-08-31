import requests

class RuneMetrics:
    def __init__(self, username):
        self.username = username
        self.skills = None
        self.status = None
        self.profile_data = None

    def fetch(self):
        profile_api = f"https://apps.runescape.com/runemetrics/profile/profile?user={self.username}" \
                        f"&activities=20"
        profile_r = requests.get(profile_api)
        self.profile_data = profile_r.json()
        quest_api = f"https://apps.runescape.com/runemetrics/quests?user={self.username}"
        quest_r = requests.get(quest_api)
        self.quest_data = quest_r.json()['quests']



    def get_skills(self):
        skill_ids = {
            0: "Attack",
            1: "Defence",
            2: "Strength",
            3: "Constitution",
            4: "Ranged",
            5: "Prayer",
            6: "Magic",
            7: "Cooking",
            8: "Woodcutting",
            9: "Fletching",
            10: "Fishing",
            11: "Firemaking",
            12: "Crafting",
            13: "Smithing",
            14: "Mining",
            15: "Herblore",
            16: "Agility",
            17: "Thieving",
            18: "Slayer",
            19: "Farming",
            20: "Runecrafting",
            21: "Hunter",
            22: "Construction",
            23: "Summoning",
            24: "Dungeoneering",
            25: "Divination",
            26: "Invention",
            27: "Archaeology"
        }
        return {
            skill_ids[skill["id"]]: {
                "level": skill["level"],
                "xp": skill["xp"],
            }
            for skill in self.profile_data["skillvalues"]
        }

    def get_combat_level(self):
        return self.profile_data["combatlevel"]

    def get_total_level(self):
        return self.profile_data["totalskill"]

class GE:
    def __init__(self, item_id):
        self.item_id = item_id
        self.item_data = None

    def fetch(self):
        url = f"https://services.runescape.com/m=itemdb_rs/api/catalogue/" \
              f"detail.json?item={self.item_id}"
        r = requests.get(url)
        self.item_data = r.json()["item"]

    def get_price(self):
        return self.item_data["current"]["price"]

    def get_name(self):
        return self.item_data["name"]

    def get_description(self):
        return self.item_data["description"]


a = RuneMetrics("Junglewise")
a.fetch()

b = RuneMetrics("JaceDrake")
b.fetch()



