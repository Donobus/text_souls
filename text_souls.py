import random
import time
import os
import msvcrt
import math
import ctypes

### Universal functions

def blankline(count=1):

    for _ in range(count):
        print("")

def wait(seconds):

    time.sleep(seconds)
  
def clear_console():

    os.system("cls" if os.name == "nt" else "clear")

def clear_input_buffer():

    try:
        while msvcrt.kbhit():
            msvcrt.getch()

    except ImportError:
        pass

def timed_input(prompt, timeout):

    clear_input_buffer()
    print(prompt, end='', flush=True)
    start_time = time.time()
    input_str = ''
    while True:

        if msvcrt.kbhit():
            char = msvcrt.getche()

            if char == b'\r':
                print('')
                return input_str.lower()

            elif char == b'\x08':
                input_str = input_str[:-1]
                print(' \b', end='', flush=True)

            else:
                input_str += char.decode()

        if time.time() - start_time > timeout:
            return None
        
def get_console_size():

    h = ctypes.windll.kernel32.GetStdHandle(-12)
    csbi = ctypes.create_string_buffer(22)
    res = ctypes.windll.kernel32.GetConsoleScreenBufferInfo(h, csbi)
    if res:
        import struct
        (bufx, bufy, curx, cury, wattr,
         left, top, right, bottom,
         maxx, maxy) = struct.unpack("hhhhHhhhhhh", csbi.raw)
        sizex = right - left + 1
        sizey = bottom - top + 1
        return sizex, sizey
    else:
        return 80, 25

def get_cursor_position():

    h = ctypes.windll.kernel32.GetStdHandle(-11)
    csbi = ctypes.create_string_buffer(22)
    res = ctypes.windll.kernel32.GetConsoleScreenBufferInfo(h, csbi)
    if res:
        import struct
        (bufx, bufy, curx, cury, wattr,
         left, top, right, bottom,
         maxx, maxy) = struct.unpack("hhhhHhhhhhh", csbi.raw)
        return curx, cury
    else:
        return 0, 0

def clear_room_test():

    sizex, sizey = get_console_size()
    curx, cury = get_cursor_position()
    return cury >= sizey - 20

### Difficulty selection

def select_difficulty():

    global pause_mode
    pause_mode = False

    global difficulty
    global dodge_difficulty_multiplier
    global counterattack_difficulty_multiplier
    global damage_difficulty_multiplier
    global impossible_damage_difficulty_multiplier

    blankline(1)
    wait(1)
    clear_input_buffer()
    print("Select difficulty:")
    wait(1)
    blankline(1)
    print("\tBaby Mode")
    print("\tEasy")
    print("\tStandard")
    print("\tChallenging")
    print("\tImpossible")
    blankline(1)
    clear_input_buffer()
    difficulty_input = input("").lower()
    while True:
        if "ba" in difficulty_input:
            difficulty = 1
            break

        elif "ea" in difficulty_input:
            difficulty = 2
            break
    
        elif "st" in difficulty_input:
            difficulty = 3
            break

        elif "ch" in difficulty_input:
            difficulty = 4
            break

        elif "im" in difficulty_input:
            difficulty = 5
            break

        elif any(no_phrase in difficulty_input for no_phrase in ["no", "na", "won", "don"]):
            blankline(1)
            clear_input_buffer()
            difficulty_input = input("Error: smartass alert. Please try again. ")

        else:
            blankline(1)
            clear_input_buffer()
            difficulty_input = input("Please select a valid difficulty. ").lower()
    
    if difficulty == 1:
        dodge_difficulty_multiplier = 2
        counterattack_difficulty_multiplier = 1.5
        damage_difficulty_multiplier = 0.5
        impossible_damage_difficulty_multiplier = 1


    elif difficulty == 2:
        dodge_difficulty_multiplier = 1.5
        counterattack_difficulty_multiplier = 1.25
        damage_difficulty_multiplier = 0.75
        impossible_damage_difficulty_multiplier = 1
    
    elif difficulty == 3:
        dodge_difficulty_multiplier = 1
        counterattack_difficulty_multiplier = 1
        damage_difficulty_multiplier = 1
        impossible_damage_difficulty_multiplier = 1

    elif difficulty == 4:
        dodge_difficulty_multiplier = 0.8
        counterattack_difficulty_multiplier = 0.85
        damage_difficulty_multiplier = 1.5
        impossible_damage_difficulty_multiplier = 1

    else:
        dodge_difficulty_multiplier = 0.6
        counterattack_difficulty_multiplier = 0.7
        damage_difficulty_multiplier = 2
        impossible_damage_difficulty_multiplier = 0.7

### Basic Stats

global knight_attacks
knight_attacks = ["hit", "bash", "stab", "thrust"]
global knight_attack_damage
knight_attack_damage = [1, 2, 4, 5]

global samurai_attacks
samurai_attacks = ["cut", "slash", "slice", "riposte"]
global samurai_attack_damage
samurai_attack_damage = [2, 4, 5, 7]

global mage_attacks
mage_attacks = ["curse", "fireball", "ice shard", "lightning bolt"]
global mage_attack_damage
mage_attack_damage = [2, 4, 6, 8]

def set_player_stats():

    global restart
    restart = False

    global player_health
    player_health = 25

    global monster_health
    
    if difficulty == 5:
        monster_health = 50

    else:
        monster_health = 35

### Buff stats

def set_player_buffs():

# Defense buffs
    # Multiplier of (1 - defense_buff)

    global defense_buff

    if player_class == "knight":
        defense_buff = 0.4

    elif player_class == "samurai":
        defense_buff = -0.25
    
    else:
        defense_buff = 0

# Dodge buffs
    # Multiplier of (1 + dodge_buff)

    global dodge_buff

    if player_class == "samurai":
        dodge_buff = 0.33
    
    else:
        dodge_buff = 0

# Counterattack buffs
    # Multiplier of (1 + counterattack_buff)

    global counterattack_buff

    if player_class == "samurai":
        counterattack_buff = -0.25

    else:
        counterattack_buff = 0

# Invincibility buff
    # Chance of (1-invincibility_buff)

    global invincibility_buff

    if player_class == "mage":
        invincibility_buff = 0.35
    
    else:
        invincibility_buff = 0


### Player class descriptions

def print_knight_description():

    blankline(2)
    print("""You have chosen the Knight class.
                  
    The Knight class is a balanced class with a sword and shield.
        It deals moderate damage and takes reduced damage from all attacks.""")
    wait(1)
    blankline(1)

    for attack, damage in zip(knight_attacks, knight_attack_damage):
        print(f"{attack.upper()} deals {damage} damage.")

    blankline(2)
    wait(1)

def print_samurai_description():

    blankline(2)
    print("""You have chosen the Samurai class.
                  
    The Samurai class is a nimble class with two katanas.
        It deals high damage and takes high damage from all attacks.
        The Samurai class has an easier time dodging attacks,
        however it also has a more difficult time counterattacking.""")
    wait(1)
    blankline(1)

    for attack, damage in zip(samurai_attacks, samurai_attack_damage):
        print(f"{attack.upper()} deals {damage} damage.")

    blankline(2)
    wait(1)

def print_mage_description():

    blankline(2)
    print("""You have chosen the Mage class.
                  
    The Mage class is a complex class with a magic staff.
        It deals high damage and takes standard damage from all attacks.
        The Mage class has a chance to not take damage even when hit,
        however its spells are more difficult to cast.""")
    wait(1)
    blankline(1)

    for attack, damage in zip(mage_attacks, mage_attack_damage):
        print(f"{attack.upper()} deals {damage} damage.")

    blankline(2)
    wait(1)

### Player class selection

def select_player_class():

    global player_class
    blankline(1)
    wait(1)
    clear_input_buffer()
    player_class_input = input("Select player class: Knight, Samurai, or Mage? ").lower()
    while True:

        if "k" in player_class_input or player_class_input == "1":
            player_class = "knight"
            print_knight_description()
            break

        elif "s" in player_class_input or player_class_input == "2":
            player_class = "samurai"
            print_samurai_description()
            break

        elif "mag" in player_class_input or player_class_input == "3":
            player_class = "mage"
            print_mage_description()
            break

        else:
            blankline(1)
            clear_input_buffer()
            player_class_input = input("Please choose a valid class. ").lower()

    confirm_phrases = ["ready", "go", "start", "begin", "fight", "ye", "sure", "ok", "alright", "fine", "yup", "guess", "confirm"]

    clear_input_buffer()
    confirm_class = input("Confirm this choice, or choose another class. ").lower()
    while not any(confirm_phrase in confirm_class for confirm_phrase in confirm_phrases):

        if "k" in confirm_class or confirm_class == "1":
            player_class = "knight"
            print_knight_description()
            clear_input_buffer()
            confirm_class = input("Confirm this choice, or choose another class. ").lower()
            blankline(1)
            continue

        elif "s" in confirm_class or confirm_class == "2":
            player_class = "samurai"
            print_samurai_description()
            clear_input_buffer()
            confirm_class = input("Confirm this choice, or choose another class. ").lower()
            blankline(1)
            continue

        elif "mag" in confirm_class or confirm_class == "3":
            player_class = "mage"
            print_mage_description()
            clear_input_buffer()
            confirm_class = input("Confirm this choice, or choose another class. ").lower()
            blankline(1)
            continue

        else:
            blankline(1)
            confirm_class = input("Please confirm your class, or choose a different one. ").lower()
    
    blankline(1)

### Fight initialization

def initialize_fight():

    start_phrases = ["ready", "go", "start", "begin", "fight", "ye", "sure", "ok", "alright", "fine", "yup", "guess", "confirm"]
    wait_phrases = ["wait", "hold", "stop", "pause", "no", "na", "don", "won"]

    clear_input_buffer()
    start = input("Are you ready to fight? ").lower()
    while True:

        if any(start_phrase in start for start_phrase in start_phrases):
            break

        elif any(wait_phrase in start for wait_phrase in wait_phrases):
            print("You wait for a moment.")
            wait(2)
            print("")
            start = input("Are you ready to fight? ").lower()

        elif start == "":
            print(f"You couldn't think of anything to say.")
            wait(2)
            print("...")
            wait(3)
            blankline(1)
            start = input("But are you ready to fight? ").lower()

        else:
            print(f"You couldn't think of anything to say, so you just said '{start}'.")
            wait(2)
            print("...")
            wait(3)
            blankline(1)
            start = input("But are you ready to fight? ").lower()

    clear_console()
    wait(2)
    blankline(1)
    print("The monster climbs up from out of the shadows and roars.")
    wait(3)
    blankline(2)
    print("The monster makes its way over to you.")
    wait(5)
    blankline(1)

### Battle mechanics

# Return damage values

def attack_damage(player_class, attack):

    if player_class == "knight":
        attacks = knight_attacks
        damages = knight_attack_damage

    elif player_class == "samurai":
        attacks = samurai_attacks
        damages = samurai_attack_damage

    elif player_class == "mage":
        attacks = mage_attacks
        damages = mage_attack_damage

    else:
        return None

    for attack_value, damage_value in zip(attacks, damages):
        if attack_value == attack:
            return damage_value

    return None

# Counterattack

def counterattack(time_window):

    counterattack = timed_input("Looks like the monster is vulnerable to a counterattack. ", time_window*counterattack_difficulty_multiplier*(1+counterattack_buff))

    if counterattack is not None:
        counterattack = counterattack.lower()
    blankline(1)
    damage = attack_damage(player_class, counterattack)

    if damage is not None:

        if difficulty == 5:
            if damage == math.ceil(damage*impossible_damage_difficulty_multiplier):
                impossible_damage = False
            else:
                impossible_damage = True
            damage = math.ceil(damage*impossible_damage_difficulty_multiplier)

        global monster_health

        if monster_health >= damage:
            print(f"""You {counterattack} the monster{f', but you were so scared that you only dealt {damage} damage.' if difficulty == 5 and impossible_damage == True else f' and deal {damage} damage!'}
    The monster has {monster_health-damage} health remaining.""")
            monster_health = monster_health-damage

        else:
            print(f"""You {counterattack} the monster and deal {monster_health} damage!
    The monster has 0 health remaining.""")
            monster_health = 0

    else:
        print("""
    You missed the opportunity to counterattack.""")

# Invincibility chance

def invincibility_chance():

    global invincibility
    invincibility_roll = random.randint(1, 100)

    if invincibility_roll > 100*(1-invincibility_buff):
            invincibility = True

    else:
            invincibility = False
    
### Monster attacks

# Swing from left

def swing_from_left(damage_taken):

    blankline(1)
    print("The monster winds up for an attack from the left...")
    if difficulty == 5:
        wait(random.uniform(1.5, 3))
    else:
        wait(random.triangular(2, 6, 4.5))
    jump = timed_input("He swings! ", 1.5*dodge_difficulty_multiplier*(1+dodge_buff))

    if jump is None:
        blankline(1)

    else:
        jump = jump.lower()  

    if jump == "jump":
        blankline(1)
        print("You jump over the monster's club.")
        if pause_mode == True:
            wait(1)
        counterattack(1.5)

    else:
        global player_health
        invincibility_chance()
        
        if invincibility == True:
            print(f"""You couldn't jump in time, but the monster's club passed straight through you!
    You have {player_health} health remaining.""")

        else:

            if player_health >=round(damage_taken*damage_difficulty_multiplier*(1-defense_buff)):
                player_health = player_health-round(damage_taken*damage_difficulty_multiplier*(1-defense_buff))
                print(f"""You couldn't jump in time and get hit by the monster's club. You get hit for {round(damage_taken*damage_difficulty_multiplier*(1-defense_buff))} damage!
    You have {player_health} health remaining.""")

            else:
                print(f"""You couldn't jump in time and get hit by the monster's club. You get hit for {player_health} damage!
    You have 0 health remaining.""")
                player_health = 0

    blankline(1)

    del jump

# Swing from above

def swing_from_above(damage_taken):

    blankline(1)
    print("The monster prepares to slam his club down on you from above...")
    if difficulty == 5:
        wait(random.uniform(2, 5))
    else:
        wait(random.triangular(3, 9, 7))
    sidestep = timed_input("He swings! ", 2*dodge_difficulty_multiplier*(1+dodge_buff))

    if sidestep is None:
        blankline(1)

    else:
        sidestep = sidestep.lower()  

    if sidestep == "sidestep":
        blankline(1)
        print("You sidestep out of the way.")
        if pause_mode == True:
            wait(1)
        counterattack(2)

    else:
        global player_health
        invincibility_chance()
        
        if invincibility == True:
            print(f"""You couldn't sidestep in time, but the monster's club passed straight through you!
    You have {player_health} health remaining.""")

        else:

            if player_health >=math.floor(damage_taken*damage_difficulty_multiplier*(1-defense_buff)):
                player_health = player_health-math.floor(damage_taken*damage_difficulty_multiplier*(1-defense_buff))
                print(f"""You couldn't sidestep in time and get hit by the monster's club. You get hit for {math.floor(damage_taken*damage_difficulty_multiplier*(1-defense_buff))} damage!
    You have {player_health} health remaining.""")

            else:
                print(f"""You couldn't sidestep in time and get hit by the monster's club. You get hit for {player_health} damage!
    You have 0 health remaining.""")
                player_health = 0

    blankline(1)

    del sidestep

# Lunge

def lunge(damage_taken):

    blankline(1)
    print("The monster prepares to lunge at you...")
    if difficulty == 5:
        wait(random.uniform(1, 2))
    else:
        wait(random.triangular(2, 4, 3.5))
    duck = timed_input("He lunges! ", 1.35*dodge_difficulty_multiplier*(1+dodge_buff))

    if duck is None:
        blankline(1)

    else:
        duck = duck.lower()

    if duck == "duck":
        blankline(1)
        print("You duck under the monster.")
        if pause_mode == True:
            wait(1)
        counterattack(1.2)

    else:
        global player_health
        invincibility_chance()
        
        if invincibility == True:
            print(f"""You couldn't duck in time, but the monster passed straight through you!
    You have {player_health} health remaining.""")

        else:

            if player_health >=math.ceil(damage_taken*damage_difficulty_multiplier*(1-defense_buff)):
                player_health = player_health-math.ceil(damage_taken*damage_difficulty_multiplier*(1-defense_buff))
                print(f"""You couldn't duck in time and get hit by the monster. You get hit for {math.ceil(damage_taken*damage_difficulty_multiplier*(1-defense_buff))} damage!
    You have {player_health} health remaining.""")

            else:
                print(f"""You couldn't duck in time and get hit by the monster. You get hit for {player_health} damage!
    You have 0 health remaining.""")
                player_health = 0

    blankline(1)

    del duck

# Headbutt

def headbutt(damage_taken):

    blankline(1)
    print("The monster ducks down to headbutt you.")
    if difficulty == 5:
        wait(random.uniform(1.5, 3))
    else:
        wait(random.triangular(2, 5, 3.5))
    jump = timed_input("He lunges at you! ", 1.45*dodge_difficulty_multiplier*(1+dodge_buff))

    if jump is None:
        blankline(1)

    else:
        jump = jump.lower()

    if jump == "jump":
        blankline(1)
        print("You jump over the monster's head.")
        if pause_mode == True:
            wait(1)
        counterattack(1.45)

    else:
        global player_health
        invincibility_chance()
        
        if invincibility == True:
            print(f"""You couldn't jump in time, but the monster's head passed straight through you!
    You have {player_health} health remaining.""")

        else:

            if player_health >=math.ceil(damage_taken*damage_difficulty_multiplier*(1-defense_buff)):
                player_health = player_health-math.ceil(damage_taken*damage_difficulty_multiplier*(1-defense_buff))
                print(f"""You couldn't jump in time and get headbutted. You get hit for {math.ceil(damage_taken*damage_difficulty_multiplier*(1-defense_buff))} damage!
    You have {player_health} health remaining.""")

            else:
                print(f"""You couldn't duck in jump and get headbutted. You get hit for {player_health} damage!
    You have 0 health remaining.""")
                player_health = 0

    blankline(1)

    del jump

# Jump

def jump_attack(damage_taken):

    blankline(1)
    print("The monster leaps into the air above you...")
    if difficulty == 5:
        wait(random.uniform(3.5, 8))
    else:
        wait(random.triangular(5, 10, 8.25))
    run_away = timed_input("He's landing! ", 2.1*dodge_difficulty_multiplier*(1+dodge_buff))

    if run_away is None:
        blankline(1)

    else:
        run_away = run_away.lower()  

    if run_away == "run away":
        blankline(1)
        print("You run out of the way.")
        if pause_mode == True:
            wait(1)
        counterattack(2.5)

    else:
        global player_health
        invincibility_chance()
        
        if invincibility == True:
            print(f"""You couldn't run away in time, but the monster got confused and missed you!
    You have {player_health} health remaining.""")

        else:

            if player_health >=math.floor(damage_taken*damage_difficulty_multiplier*(1-defense_buff)):
                player_health = player_health-math.floor(damage_taken*damage_difficulty_multiplier*(1-defense_buff))
                print(f"""You couldn't run away in time and the monster lands on you. You get hit for {math.floor(damage_taken*damage_difficulty_multiplier*(1-defense_buff))} damage!
    You have {player_health} health remaining.""")

            else:
                print(f"""You couldn't run away in time and the monster lands on you. You get hit for {player_health} damage!
    You have 0 health remaining.""")
                player_health = 0

    blankline(1)

    del run_away
    
### Game over

def test_game_over():

    restart_phrases = ["res", "ready", "go", "start", "begin", "fight", "ye", "sure", "ok", "okay", "alright", "fine", "yup", "guess"]
    global restart

    if player_health == 0:
        wait(2.5)
        clear_console()
        blankline(1)
        print("Game over!")
        wait(2)
        blankline(3)

        clear_input_buffer()
        restart_prompt = input("Would you like to play again? ").lower()
        while restart != True:

            if any(restart_confirm in restart_prompt for restart_confirm in restart_phrases):
                restart = True

            else:
                clear_input_buffer()
                restart_prompt = input("").lower()

    elif monster_health == 0:
        wait(2.5)
        clear_console()
        blankline(1)
        print("You win!")
        wait(2)
        blankline(3)

        clear_input_buffer()
        restart_prompt = input("Would you like to play again? ").lower()
        while restart != True:

            if any(restart_confirm in restart_prompt for restart_confirm in restart_phrases):
                restart = True
            else:
                clear_input_buffer()
                restart_prompt = input("").lower()

# Main execution

while True:
    clear_console()
    select_difficulty()
    clear_console()
    set_player_stats()
    select_player_class()
    initialize_fight()
    set_player_buffs()
    while True:
        monster_attacks = ["swing_from_left", "swing_from_above", "lunge", "headbutt", "jump_attack"]
        monster_attack_chance = [3, 2, 4, 3, 2]
        selected_attack = random.choices(monster_attacks, weights=monster_attack_chance, k=1)[0]
        if selected_attack == "swing_from_left":
            swing_from_left(6)

        elif selected_attack == "swing_from_above":
            swing_from_above(8)

        elif selected_attack == "lunge":
            lunge(3)

        elif selected_attack == "headbutt":
            headbutt(4)

        elif selected_attack == "jump_attack":
            jump_attack(9)

        else:
            continue



        if clear_room_test():
            wait(2*dodge_difficulty_multiplier)
            clear_console()

        wait(2*dodge_difficulty_multiplier)

        test_game_over()
        if restart == True:
            break
        else:
            continue
        
    