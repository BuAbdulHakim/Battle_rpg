from classes.game import Person, bcolors
from classes.magic import Spell
from classes.inventory import Item
import random

#------> CREATE BLACK MAGIC 
fire = Spell("Fire", 15, 200, "black")
thunder = Spell("Thunder", 15, 200, "black")
blizzard = Spell("Blizzard", 15, 200, "black")
meteor = Spell("Meteor", 30, 450, "black")
quake = Spell("Quake", 10, 100, "black")


#------> CREATE WHITE MAGIC
cure = Spell("Cure", 12, 684, "white")
cura = Spell("cura", 18, 1500, "white")

#------> Create Items
potion = Item("Potion", "potion", "Heals 50 HP", 50)
hipotion = Item("Hi-Potion", "potion", "Heals 100 HP", 100)
superpotion = Item("Super-Potion", "potion", "Heals 500 HP", 500)
elixir = Item("Elixir", "elixir", "Fully Restores HP/MP of one party member", 9999)
megaelixir = Item("MegaElixir", "elixir", "Fully Restores HP/MP for all party members", 9999)

grenade = Item("Grenade", "attack", "Deals 500 damage.", 500)


#Instantiate people
player_spells = [fire, thunder, blizzard, meteor, quake, cure, cura]
player_items = [{"item" : potion, "quantity": 5}, 
                {"item" : hipotion, "quantity": 5}, 
                {"item" : superpotion, "quantity": 5}, 
                {"item" : elixir, "quantity": 1}, 
                {"item" : megaelixir, "quantity": 1}, 
                {"item" : grenade, "quantity": 5}]
                
#------> Player stats
player1 = Person("Ethar:  ", 200, 70, 20, 34, player_spells, player_items)
player2 = Person("Khadgar:", 200, 70, 20, 34, player_spells, player_items)
player3 = Person("Elora:  ", 200, 70, 20, 34, player_spells, player_items)

players = [player1, player2, player3]
#------> NPC stats
enemy = Person("Volt:   ", 1000, 65, 30, 25, [], [])

running = True
i = 0
    

#------> starts the game loop
print(bcolors.FAIL + bcolors.BOLD + "AN ENEMY ATTACKED" + bcolors.ENDC)
while running:
    print("====================")
    
    print("\n\n")
    print("Name:           HP:                                               MP:")


    #------> getting stats for all players
    for player in players:
        player.get_stats()
    print("\n")

    enemy.get_enemy_stats()
    #------> looping all players
    for player in players:
        
        player.choose_action()
        choice = input("    Choose an action: ") 
        index = int(choice) - 1
        
        #------> choose attack
        if index == 0:
            dmg = player.generate_damage()
            enemy.take_dmg(dmg)
            print("you attacked for: " + str(dmg), "Points of damage. Enemy HP:", enemy.get_hp())
            enemy.get_enemy_stats()

        #------> choose magic
        elif index == 1:
            player.choose_magic()
            magic_choice = int(input("    Choose Magic:")) - 1
            
            if magic_choice == -1:
                continue

            spell = player.magic[magic_choice]
            magic_dmg = spell.generate_damage()
            

            current_mp = player.get_mp()

            if spell.cost > current_mp:
                print(bcolors.FAIL + "\nNOT enough MP \n" + bcolors.ENDC)
                continue


            #------> heals
            if spell.type == "white":
                player.heal(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + " heals for:", str(magic_dmg), "HP." + bcolors.ENDC)
            #------> deals damage
            elif spell.type == "black":
                enemy.take_dmg(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + " deals", str(magic_dmg), "points of damage"+ bcolors.ENDC)

            #------> update mana
            player.reduce_mp(spell.cost)
        
        #------> items
        elif index == 2:
            player.choose_item()
            item_choice = int(input("    Choose an item: ")) - 1
            
            if item_choice == -1:
                continue

            #------> initializing item
            item = player_items[item_choice]["item"]
        #------> check if items are available
            if player.items[item_choice]["quantity"] == 0:
                print(bcolors.FAIL + bcolors.BOLD + "You can't use that item anymore" + bcolors.ENDC)
                continue
            player.items[item_choice]["quantity"] -= 1

            #------> potions
            if item.type == "potion":
                player.heal(item.prop)
                print("\n" + bcolors.OKGREEN+ bcolors.BOLD + item.name + " heals for", str(item.prop) + bcolors.ENDC)

            #------> elixirs
            elif item.type == "elixir":
                
                if item.name == "MegaElixir":
                    for i in players:
                        i.hp = i.maxhp
                        i.mp = i.maxmp
                    print("\n" + bcolors.OKGREEN+ bcolors.BOLD  +item.name + " is used! Everyone's HP & MP is full!!" + bcolors.ENDC)

                elif item.name == "Elixir":
                    player.hp = player.maxhp
                    player.mp = player.maxmp
                    print("\n" + bcolors.OKGREEN+ bcolors.BOLD + "The " +item.name + " is used! HP & MP are full!" + bcolors.ENDC)

                
            #------> attacks
            elif item.type == "attack":
                enemy.take_dmg(item.prop)
                print(bcolors.FAIL + "\n" + item.name + " deals", str(item.prop), "points of damage"+ bcolors.ENDC)
    if enemy.get_hp() == 0:
        print(bcolors.OKGREEN + "You win!" + bcolors.ENDC)
        running = False
    elif player.get_hp() == 0:
        print(bcolors.FAIL + "You lose!" + bcolors.ENDC)
        running = False



    #------> enemy does damage   
    enemy_choice = 1
    target = random.randrange(0,3)
    enemy_dmg = enemy.generate_damage()
    players[target].take_dmg(enemy_dmg)
    print("enemy attacks for: " + str(enemy_dmg), "Hp remaining:", player.get_hp())
    print("Enemy HP:", enemy.get_hp())
