from classes.game import Person, bcolors
from classes.magic import Spell
from classes.inventory import Item
import random


# Create Black Magic
fire = Spell("Fire", 10, 100, "Black Magic")
thunder = Spell("Thunder", 10, 100, "Black Magic")
blizzard = Spell("Blizzard", 10, 100, "Black Magic")
meteor = Spell("Meteor", 20, 200, "Black Magic")
quake = Spell("Quake", 14, 140, "Black Magic")

# Create White Magic
cure = Spell("Cure", 12, 120, "White Magic")
cura = Spell("Cura", 18, 200, "White Magic")


# Create Items
potion = Item("Potion", "potion", "Heals 50 HP", 50)
hipotion = Item("Hi-Potion", "potion", "Heals 100 HP", 100)
superpotion = Item("Super Potion", "potion", "Heals 500 HP", 100)
elixer = Item("Elixir", "elixer", "Fully Restores HP/MP of one party member", 9999)
hielixer = Item("MegaElixer", "elixer", "Fully restore party's HP/MP", 9999)
grenade = Item("Grenade", "attack", "Deals 500 damage", 500)

# Create Players spells/items
player_spells = [fire, thunder, blizzard, meteor, cure, cura]
player_items = [{"item" : potion, "quantity": 15}, 
                {"item" : hipotion, "quantity": 5}, 
                {"item" : superpotion, "quantity": 5}, 
                {"item" : elixer, "quantity": 5}, 
                {"item" : hielixer, "quantity": 2}, 
                {"item" : grenade, "quantity": 5}]

#Create Enemies spells/items
enemy_spells = [fire, meteor, cura]
enemy_items = [{"item" : potion, "quantity": 15}, 
                {"item" : hipotion, "quantity": 5}, 
                {"item" : superpotion, "quantity": 5}, 
                {"item" : elixer, "quantity": 5}, 
                {"item" : hielixer, "quantity": 2}, 
                {"item" : grenade, "quantity": 5}]



#Instantiate People
player1 = Person("Zé cueca", 300, 70, 60, 34, player_spells, player_items)
player2 = Person("Zé ximia", 500, 50, 40, 14, player_spells, player_items)
player3 = Person("Zé manga", 200, 80, 30, 44, player_spells, player_items)

enemy1 = Person("Marquinhos", 999, 65, 45, 25, enemy_spells, enemy_items)
enemy2 = Person("Fiote maior", 300, 70, 70, 30, enemy_spells, enemy_items)
enemy3 = Person("Fio do diabo", 250, 80, 50, 95, enemy_spells, enemy_items)

players = [player1, player2, player3]
enemies = [enemy1, enemy2, enemy3]

running = True
i = 0

print(bcolors.FAIL + bcolors.BOLD + "AN ENEMY ATTACKS!" + bcolors.ENDC)

while running:
    print("=======================")

    print("\n\n")

    for player in players:
        player.get_stats()
    
    print("\n")

    for enemy in enemies:
        enemy.get_enemy_stats()

    for player in players:
        player.choose_action()
        choice = input("Choose action:")
        index = int(choice) - 1

        if index == 0:
            dmg = player.generate_damage()
            enemy = player.choose_target(enemies)
            enemies[enemy].take_damage(dmg)

            print("You attacked "+ enemies[enemy].name + " for " + str(dmg) + " points of damage.")

            if enemies[enemy].get_hp() == 0:
                print(enemies[enemy].name + " has died.")
                del enemies[enemy]
        
        elif index == 1:
            player.choose_magic()
            magic_choice = int(input("Choose magic:")) - 1

            if magic_choice == -1:
                continue


            spell = player.magic[magic_choice]
            magic_dmg = spell.generate_damage()

            current_mp = player.get_mp()

            if spell.cost > current_mp:
                print(bcolors.FAIL + "\nYou don't have enough Mana!\n" + bcolors.ENDC)
                continue

            player.reduce_mp(spell.cost)

            if spell.type == "White Magic":
                player.heal(magic_dmg)
                print(bcolors.OKGREEN + "\n" + spell.name + " heals for", str(magic_dmg), "HP" + bcolors.ENDC)

            elif spell.type == "Black Magic":
                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(magic_dmg)

                print(bcolors.OKBLUE + "\n" + spell.name + " deals", str(magic_dmg), "points of damage to " + enemies[enemy].name + bcolors.ENDC)

                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name + " has died.")
                    del enemies[enemy]


        elif index == 2:
            player.choose_item()
            item_choice = int(input("Choose item: ")) - 1

            if item_choice == -1:
                continue

            item = player.items[item_choice]["item"]


            if player.items[item_choice]["quantity"] == 0:
                print(bcolors.FAIL + "\n" + "None left..." + bcolors.ENDC)
                continue

            player.items[item_choice]["quantity"] -= 1

            if item.type == "potion":
                player.heal(item.prop)
                print(bcolors.OKGREEN + "\n" + item.name + " heals for", str(item.prop), "HP" + bcolors.ENDC)

            elif item.type == "attack":

                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(item.prop)

                print(bcolors.FAIL + "\n" + item.name + " deals", str(item.prop), "points of damage to " + enemies[enemy].name + bcolors.ENDC)

                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name + " has died.")
                    del enemies[enemy]

            elif item.type == "elixer":
                if item.name == "MegaElixer":
                    for i in players:
                        i.hp = i.maxhp
                        i.mp = i.maxmp
                else:
                    player.hp = player.maxhp
                    player.mp = player.maxmp

                print(bcolors.OKGREEN + "\n" + item.name + " fully restores HP/MP" + bcolors.ENDC)


    #check if battle is over
    defeated_enemies = 0
    defeated_players = 0

    for enemy in enemies:
        if enemy.get_hp() == 0:
            defeated_enemies += 1

    for player in players:
        if player.get_hp() == 0:
            defeated_players += 1

    #Check if player won
    if defeated_enemies == 2:
        print(bcolors.OKGREEN + "You win!" + bcolors.ENDC)
        running = False

    #Check if enemy won
    if defeated_players == 2:
        print(bcolors.OKGREEN + "Your enemies have defeated you!" + bcolors.ENDC)
        running = False

    # Enemy attack phase
    for enemy in enemies:
        enemy_choice = random.randrange(0, 2)

        if enemy_choice == 0:
            #Chose attack
            target = random.randrange(0, 2)
            enemy_damage = enemy.generate_damage()

            players[target].take_damage(enemy_damage)
            print(enemy.name + " attacks " + players[target].name + " for ", enemy_damage)

        elif enemy_choice == 1:
            spell, magic_dmg = enemy.choose_enemy_spell()
            enemy.reduce_mp(spell.cost)

            if spell.type == "White Magic":
                enemy.heal(magic_dmg)
                print(bcolors.OKGREEN + "\n" + spell.name + " heals "+ enemy.name + " for ", str(magic_dmg), "HP" + bcolors.ENDC)

            elif spell.type == "Black Magic":

                target = random.randrange(0, 3)
                players[target].take_damage(magic_dmg)


                print(bcolors.OKBLUE + "\n" + enemy.name + " uses " + spell.name + " and deals", str(magic_dmg), "points of damage to " + players[target].name + bcolors.ENDC)

                if players[target].get_hp() == 0:
                    print(players[target].name + " has died.")
                    del players[target]
                
                #print("Enemy chosed", spell.name, "damage is", magic_dmg)







    



    