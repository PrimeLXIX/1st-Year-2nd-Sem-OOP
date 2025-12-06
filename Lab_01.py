class Player:
    def __init__(self, player, name, level, hp, weapon, range, special_attack, armor, defend):
        self.player = player
        self.name = name
        self.level = level
        self.hp = hp
        self.weapon = weapon
        self.range = range
        self.special_attack = special_attack
        self.armor = armor
        self.defend = defend

    def display_info(self):
        return (
            f"=== {self.player} ===\n"
            f"Name: {self.name}\n"
            f"Level: {self.level}\n"
            f"HP: {self.hp}\n"
            f"Weapon: {self.weapon.name} (Damage: {self.weapon.damage}, Type: {self.weapon.type})\n"
            f"Range: {self.range}\n"
            f"Special Attack: {self.special_attack}\n"
            f"Armor: {self.armor.name} (Defense: {self.armor.defense})\n"
            f"Durability: {self.defend}\n"
        )

class Weapon:
    def __init__(self, name, damage, type, special_attack=None):
        self.name = name
        self.damage = damage
        self.type = type
        self.special_attack = special_attack

class Armor:
    def __init__(self, name, defense):
        self.name = name
        self.defense = defense

iron_sword = Weapon("Iron Sword", 10, "Melee")
leather_armor = Armor("Leather Armor", 5)

wooden_bow = Weapon("Wooden Bow", 8, "Bow")
chain_mail = Armor("Chain Mail", 10)

iron_axe = Weapon("Iron Axe", 20, "Melee")
iron_armor = Armor("Iron Armor", 25)

player1 = Player("Player 1", "Hero_01", 1, 100, iron_sword, "Low", "Slash", leather_armor, "Low Durability")
player2 = Player("Player 2", "Archer_02", 2, 120, wooden_bow, "High", "Bowing Arrow", chain_mail, "Medium Durability")
player3 = Player("Player 3", "Axel_03", 4, 150, iron_axe, "Medium", "Heavy Slam", iron_armor, "High Durability")

print(player1.display_info())
print(player2.display_info())
print(player3.display_info())


class Guild:
    def __init__(self, guild_name, leader):
        self.guild_name = guild_name
        self.leader = leader
        self.members = []

    def add_member(self, member):
        self.members.append(member)

    def display_info(self):
        members_list = ", ".join(self.members)
        return (
            f"Guild Name: {self.guild_name}\n"
            f"Leader: {self.leader}\n"
            f"Members: {members_list}"
        )


guild = Guild("Heroes of Heroes", player3.name)
guild.add_member(player1.name)
guild.add_member(player2.name)
guild.add_member(player3.name)

print(guild.display_info())