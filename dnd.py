# This is some fun script I threw together for a Dungeons & Dragons campaign that I'm the Dungeon Master for.
# The campaign consists of three players and myself ranging from ages 7 to 32. The youngest member loves the
# idea of D&D, but doesn't always have the attention span. I built this script to go with a maze that they can
# explore. The maze is a 26x26 block and at 10 dead ends in the maze there is a "portal" the players will stumble
# on. That portal will either give them a prize (gold pieces or potions) or it will summon a number of monsters.
# All of this is determined by the luck of the roll AND the luck of the NumPy randomizer!
#
# For the initial roll, teams will use a D10 and then an average of the three rolls will be used to compare to
# the randomizer that will determine the good/bad outcome. From there if a roll is needed again (gold pieces or
# monsters), a D6 will be rolled by each player and the average taken. In an effort to make it as fair as possible,
# I wanted to make sure each player would get at least one gold piece and I wanted to make sure they wouldn't also
# summon in 12 monsters, so for the gold I took their average and multiplied it by the number of players and for the
# monsters, I took their average roll and divided it by 2 -- making the max monsters to face being 3. All of this is done
# with rounding up to ensure there would not be a 0 for the monsters and the max gold pieces would be awarded.

import numpy as np
import math

# Variables for:
#     Entering in the number of players.
#     Creating an array with the player names to be called upon each time
#     Creating an empty NumPy array to use for calculating roll data
num_players = input("Enter number of players: ")
players_array = []
roll_totals = np.zeros((int(num_players),), dtype=int)

# This gathers how many people are playing and their names.
# It will be run initally and then not again for the rest of the run time
def players(): 
    count = 1 
    while count <= int(num_players): 
        player_name = input("Enter name of player "+str(count)+": ") 
        players_array.append(player_name) 
        count = count + 1

# This will get the rolls for each player and add them to the roll_totals arrays
# It is called upon after every roll in the random_events() function
def rolling(): 
    count = 0
    while count <= (int(num_players)-1):
        for i in players_array: 
            roll = input("Please enter the roll for "+i+": ")
            roll_totals[count] = int(roll)
            count = count + 1
    return roll_totals

# This will determine whether or not it's gold or a monster that will be faced.
# Also determines how many of each one.
def random_event():
    rolling()
    avg_roll = round(np.average(roll_totals))
    threshold = np.random.randint(1,10)
    print(avg_roll)
    print(threshold)
    if avg_roll > threshold:
        if int(avg_roll) >= 9:
            print("Wow! What a roll!")
            prize = np.random.randint(1,3)
            print("Your team just received "+str(int(num_players)*int(prize))+" healing potions!")
            ending_game()
        else:
            print("Congrats! You've won gold! Please roll to determine number of pieces")
            gold_pieces = np.zeros((int(num_players),), dtype=int)
            rolling()
            gold_pieces = roll_totals
            num_gold = math.ceil(round(np.average(gold_pieces))*int(num_players))
            print(num_gold)
            print("Your team has received "+str(num_gold)+" gold pieces!")
            ending_game()
    else:
        print("Time for a monster battle! Please roll to determine how many monsters you will fight")
        monsters = np.zeros((int(num_players),), dtype=int)
        rolling()
        monsters = roll_totals
        num_monsters = math.ceil(round(np.average(monsters))/2)
        print(num_monsters)
        print("Your team will battle "+str(num_monsters)+" of monsters, prepare to fight!")
        ending_game()
    
# This is to determine whether to loop the random_event() again or end the script
# Like the rolling() function, this is called upon after every roll. 
def ending_game():
    end_game = input("Is this the end of the game? Type Y for yes, N for no: ")
    if end_game == "Y":
        exit()
    elif end_game == "y":
        exit()
    else:
        random_event()
        
players()
random_event()
