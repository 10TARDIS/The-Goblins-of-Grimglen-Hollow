# Name: Harrison Nickles
# Date: 5/5/25
# What the program does: Runs a visual-novel type adventure game using Pygame GUI.

print("\n\n\n\033[3mThe game is compiling, one moment please.\033[0m\n\n\n")
import random
import re
import time
import sys
import os
import pygame
pygame.init()
pygame.mixer.init()





# +------------------------------------------+
# |                                          |
# |-------------------DICE-------------------|
# |                                          |
# +------------------------------------------+

# INPUT: None
# RETURN: Int
# PURPOSE: To simulate rolling a four-sided die.
def roll_d4():
    return random.choice(range(1,4))

# INPUT: None
# RETURN: Int
# PURPOSE: To simulate rolling a six-sided die.
def roll_d6():
    return random.choice(range(1,6))

# INPUT: None
# RETURN: Int
# PURPOSE: To simulate rolling an eight-sided die.
def roll_d8():
    return random.choice(range(1,8))

# INPUT: None
# RETURN: Int
# PURPOSE: To simulate rolling a twenty-sided die.
def roll_d20():
    return random.choice(range(1,20))





# +-------------------------------------------------+
# |                                                 |
# |-------------------GLOBAL DATA-------------------|
# |                                                 |
# +-------------------------------------------------+

# INPUT: None
# RETURN: None
# PURPOSE: To initialize a bunch of global variables, so that they can be used in other functions.
def init_globals():
    pygame.display.set_caption("The Goblins of Grimglen Hollow")
    global WIDTH, HEIGHT, SCREEN, FONT, CLOCK, BACKGROUND, CURRENT_BACKGROUND, TEXT_BACKGROUND, NAME_HEADER, BOX, WHITE, BLACK, TEXT, BLUE, RED, YELLOW, GREEN, PURPLE, CURRENT_CHARACTER, CURRENT_CHARACTER_PATH, CHARACTER_FRAME, GAME_RUNNING, DEATH_DAMAGE_BONUS, STORY_FLAGS, STORY_UNLOCKS, TYPING_SOUND, CURRENT_SONG, CURRENT_PLAYLIST, STATBLOCKS
    WIDTH, HEIGHT = 1280, 720
    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.SCALED | pygame.RESIZABLE)
    FONT = pygame.font.Font("assets/fonts/Tagesschrift-Regular.ttf", 20)
    CLOCK = pygame.time.Clock()
    BACKGROUND = (pygame.image.load("assets/backgrounds/forest.jpg")).convert_alpha()
    CURRENT_BACKGROUND = "forest"
    TEXT_BACKGROUND = (pygame.image.load("assets/backgrounds/text_box.png")).convert_alpha()
    NAME_HEADER = pygame.image.load("assets/backgrounds/name_header.png")
    BOX = pygame.Rect(0, HEIGHT - HEIGHT // 4, WIDTH, HEIGHT // 4)
    WHITE, BLACK, TEXT, BLUE, RED, YELLOW, GREEN, PURPLE = (255, 255, 255), (0, 0, 0), (20, 20, 50), (0, 0, 225), (255, 0, 0), (255, 255, 0), (0, 190, 0), (178, 102, 255)
    CURRENT_CHARACTER = None
    CURRENT_CHARACTER_PATH = None
    CHARACTER_FRAME = pygame.transform.scale(pygame.image.load("assets/characters/frame.png"), (270, 270))
    GAME_RUNNING = True
    DEATH_DAMAGE_BONUS = 0
    STORY_FLAGS = {}
    STORY_UNLOCKS = {}
    TYPING_SOUND = pygame.mixer.Sound("assets/sounds/sfx/other/typing_sound.mp3")
    CURRENT_SONG = None
    CURRENT_PLAYLIST = None
    STATBLOCKS = {
    "goblin": {
        "name": "Goblin",
        "hp": 8,
        "ac": 10,
        "attack_bonus": 5,
        "damage": roll_d4,
        "attack_sound": "dagger",
        "roar_sound": "goblin_roar",
        "death_sound": "goblin_death",
        "portrait": "goblin.png"
    },

    "goblin_king": {
        "name": "King Snik",
        "hp": 36,
        "ac": 14,
        "attack_bonus": 5,
        "damage": roll_d6,
        "attack_sound": "fireball",
        "roar_sound": "goblin_roar",
        "death_sound": "goblin_death",
        "portrait": "goblin_king.png"
    },


    "guard": {
        "name": "Guard",
        "hp": 11,
        "ac": 14,
        "attack_bonus": 5,
        "damage": roll_d6,
        "attack_sound": "sword",
        "roar_sound": "human_roar",
        "death_sound": "human_death",
        "portrait": "guard.png"
    },

    "warrior": {
        "name": "Warrior",
        "hp": 33,
        "ac": 16,
        "attack_bonus": 5,
        "damage": roll_d8,
        "attack_sound": "sword",
        "roar_sound": "human_roar",
        "death_sound": "human_death",
        "portrait": "warrior.png"
    },

    "assassin": {
        "name": "Assassin",
        "hp": 21,
        "ac": 14,
        "attack_bonus": 5,
        "damage": roll_d8,
        "attack_sound": "dagger",
        "roar_sound": "human_roar",
        "death_sound": "human_death",
        "portrait": "assassin.png"
    },

    "owlbear cub": {
        "name": "Owlbear Cub",
        "hp": 15,
        "ac": 12,
        "attack_bonus": 5,
        "damage": roll_d6,
        "attack_sound": "bear",
        "roar_sound": "bear_roar",
        "death_sound": "bear_death",
        "portrait": "owlbear.jpg"
    },

    "brown bear": {
        "name": "Brown Bear",
        "hp": 33,
        "ac": 13,
        "attack_bonus": 6,
        "damage": roll_d8,
        "attack_sound": "bear",
        "roar_sound": "bear_roar",
        "death_sound": "bear_death",
        "portrait": "bear.jpg"
    },

}
init_globals()





# +-----------------------------------------------------+
# |                                                     |
# |-------------------PYGAME GRAPHICS-------------------|
# |                                                     |
# +-----------------------------------------------------+

# INPUT: None
# RETURN: None
# PURPOSE: To check if the user has clicked the exit button, and to quit the game if they have.
def check_quit():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            global GAME_RUNNING
            GAME_RUNNING = False
            pygame.quit()
            sys.exit()

# INPUT: None
# RETURN: None
# PURPOSE: To draw the box that the text will be rendered onto.
def draw_textbox():
    SCREEN.blit(TEXT_BACKGROUND, (-30, 510))    

# INPUT: A bool variable
# RETURN: None
# PURPOSE: To draw the background image for the screen, depending on which bool variable was set to True.
def draw_background(forest=False, village=False, tavern=False, forest_pool=False, goblin_camp=False):
    global BACKGROUND, CURRENT_BACKGROUND
    
    # Load the new background
    if forest:
        if CURRENT_BACKGROUND == "forest":
            return
        CURRENT_BACKGROUND = "forest"
        new_background = pygame.image.load("assets/backgrounds/forest.jpg")
    elif village:
        if CURRENT_BACKGROUND == "village":
            return
        CURRENT_BACKGROUND = "village"
        new_background = pygame.image.load("assets/backgrounds/village.jpg")
    elif tavern:
        if CURRENT_BACKGROUND == "tavern":
            return
        CURRENT_BACKGROUND = "tavern"
        new_background = pygame.image.load("assets/backgrounds/tavern.jpg")
    elif forest_pool:
        if CURRENT_BACKGROUND == "forest_pool":
            return
        CURRENT_BACKGROUND = "forest_pool"
        new_background = pygame.image.load("assets/backgrounds/forest_pool.jpg")
    elif goblin_camp:
        if CURRENT_BACKGROUND == "goblin_camp":
            return
        CURRENT_BACKGROUND = "goblin_camp"
        new_background = pygame.image.load("assets/backgrounds/goblin_camp.jpg")
    else:
        return

    if BACKGROUND is None:
        BACKGROUND = new_background
        BACKGROUND.convert_alpha()
        SCREEN.blit(BACKGROUND, (0, 0))
        pygame.display.flip()
        CLOCK.tick(60)
        return

    for alpha in range(0, 256, 10):
        SCREEN.blit(BACKGROUND, (0, 0))

        # Set the current opacity
        temp = new_background.copy()
        temp.set_alpha(alpha)
        SCREEN.blit(temp, (0, 0))

        pygame.display.flip()
        CLOCK.tick(60)
        pygame.time.delay(16)
        time.sleep(0.05)

    # Draw the new background fully
    BACKGROUND = new_background
    SCREEN.blit(BACKGROUND, (0, 0))
    pygame.display.flip()
    CLOCK.tick(60)

# INPUT: A string of text, and a color code tuple.
# RETURN: None
# PURPOSE: To draw or refresh the entire frame: background, textbox, text, and a character portrait.
def draw_frame(output_text, color):
    SCREEN.blit(BACKGROUND, (0, 0))
    refresh_character()
    draw_textbox()
    render_wrapped_text(output_text, color, 40, BOX.top + 40, WIDTH - 80)
    pygame.display.flip()
    CLOCK.tick(60)       

# INPUT: A string of text, a color code tuple, two number coordinates, and a number denoting the max width for the text. 
# RETURN: None
# PURPOSE: To write text on the screen, and to wrap it around the edge if it were to go off screen.
def render_wrapped_text(text, color, x, y, max_width):
    check_music()
    words = text.split(" ")
    lines = []
    current_line = ""

    # wrapping text around the edge
    for word in words:
        test_line = current_line + word + " "
        if FONT.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word + " "
    lines.append(current_line) 

    # Write the text
    for i, line in enumerate(lines):
        render = FONT.render(line.strip(), True, color)
        SCREEN.blit(render, (x, y + i * (FONT.get_height() + 5)))





# +---------------------------------------------------------+
# |                                                         |
# |-------------------CHARACTER PORTRAITS-------------------|
# |                                                         |
# +---------------------------------------------------------+

# INPUT: None
# RETURN: None
# PURPOSE: To "slide out" a character portrait from the screen with a smooth animation.
def slide_out_character():
    
    global CURRENT_CHARACTER
    target_x = 1020
    target_y = 282
    frame_target_x = 1010
    frame_target_y = 270
    start_x = 1280

    # Slide out animation
    if not CURRENT_CHARACTER is None:
        x = target_x
        while x < start_x:
            
            SCREEN.blit(BACKGROUND, (0, 0))
            draw_textbox()
            SCREEN.blit(CHARACTER_FRAME, (x, frame_target_y))
            SCREEN.blit(CURRENT_CHARACTER, (x, target_y))
            pygame.display.flip()
            pygame.time.delay(16)
            x += 12
        CURRENT_CHARACTER = None 

# INPUT: a string containing the file name for the character portrait, and a string with the name of the character
# RETURN: None
# PURPOSE: To display a character portrait with a smooth animation.
def show_character(file_name, character_name):
    
    global CURRENT_CHARACTER, CURRENT_CHARACTER_NAME, CURRENT_CHARACTER_PATH
    CURRENT_CHARACTER_NAME = character_name 
    
    # Load new character
    path = f"assets/characters/{file_name}"
    image = pygame.image.load(path)
    image = pygame.transform.scale(image, (250, 250)) 
    if CURRENT_CHARACTER_PATH == path:
        return
    CURRENT_CHARACTER_PATH = path
    slide_out_character()
    CURRENT_CHARACTER = image

    target_x = 1020
    target_y = 282
    frame_target_x = 1010
    frame_target_y = 270
    start_x = 1280

    # Slide in animation
    x = start_x
    while x > target_x:
         
        SCREEN.blit(BACKGROUND, (0,0))
        draw_textbox()
        SCREEN.blit(CHARACTER_FRAME, (x, frame_target_y))
        SCREEN.blit(CURRENT_CHARACTER, (x, target_y))

        pygame.display.flip()
        pygame.time.delay(16)
        x -= 8                   

# INPUT: None
# RETURN: None
# PURPOSE: To remove the current character portrait from the screen, if there is one
def clear_character():
    global CURRENT_CHARACTER, CURRENT_CHARACTER_PATH
    if not CURRENT_CHARACTER == None:
        slide_out_character()
    CURRENT_CHARACTER_PATH = None
    CURRENT_CHARACTER = None
    SCREEN.blit(BACKGROUND, (0,0))
    draw_textbox()

# INPUT: None
# RETURN: None
# PURPOSE: To refresh a character portrait so that it doesn't get lost when the background image refreshes.
def refresh_character():   
    if CURRENT_CHARACTER:
        FONT.set_italic(False)
        FONT.set_bold(False)
        SCREEN.blit(CHARACTER_FRAME, (1010, 270))
        SCREEN.blit(CURRENT_CHARACTER, (1020, 282))
        SCREEN.blit(NAME_HEADER, (1050, 490))
        render_wrapped_text(CURRENT_CHARACTER_NAME, BLACK, 1080, 505, 1280)





# +------------------------------------------------------+
# |                                                      |
# |-------------------FUNDAMENTAL MATH-------------------|
# |                                                      |
# +------------------------------------------------------+

# INPUT: A string containing the ability type for the modifier.
# RETURN: An int, the modifier for that ability
# PURPOSE: To calculate the ability modifier for skill checks and attack rolls.
def modifier(ability):
    strip_pattern = r'(\.0)$'
    score = PLAYER_STATS[ability]
    modifier = (score - 10) / 2

    modifier = str(modifier)

    modifier = re.sub(strip_pattern, "", modifier)
    modifier = int(modifier)
    return modifier

# INPUT: A string containing the ability type for the modifier, a number denoting the difficulty class, a string denoting if the check is in a specific skill, and an int bonus to add to the roll.
# RETURN: A string of the percent chance of success for that check.
# PURPOSE: To calculate the chance of success of a certain ability check.
def chance(ability, dc, skill=None, bonus=0):
    ability_bonus = modifier(ability)
    if skill:
        if skill in PLAYER_SKILLS:
            ability_bonus += 3

    chance = (((21 - (dc - ability_bonus - bonus)) / 20) * 100)
    chance = round(chance) 
    return str(chance) + "%"

# INPUT: A  number denoting the bonus for the check, and a number denoting the difficulty class of the check.
# RETURN: A string of the percent chance of success for that check.
# PURPOSE: To calculate the chance of success of a generic check, not related to any ability or skill.
def generic_chance(bonus, dc):
    chance = (((21 - (dc - bonus)) / 20) * 100)
    chance = round(chance) 
    return str(chance) + "%"

# INPUT: A string denoting the ability used for the check, a number denoting the difficulty class of the roll, a string denoting if the check is in a specific skill, and an int bonus to be added to the roll.
# RETURN: A boolean value, either True or False.
# PURPOSE: To perform an ability check, then return whether or not the check was successful.
def check(ability, dc, skill=None, bonus=0):
    roll = roll_d20()
    if skill:
        if skill in PLAYER_SKILLS:
            roll = roll + 3
    if roll + modifier(ability) + bonus >= dc:
        return True
    elif roll + modifier(ability) + bonus < dc:
        return False

# INPUT: A number denoting how the bonus should be changed
# RETURN: None
# PURPOSE: To update the player's current attack bonus value.
def update_attack_bonus(num):
    old_bonus = PLAYER_STATS["attack bonus"]
    new_bonus = num + old_bonus
    PLAYER_STATS.update({"attack bonus": new_bonus})

# INPUT: A number denoting how the bonus should be changed
# RETURN: None
# PURPOSE: To update the player's current damage bonus value.
def update_damage_bonus(num):
    old_bonus = PLAYER_STATS["damage bonus"]
    new_bonus = (num + old_bonus)
    PLAYER_STATS.update({"damage bonus": new_bonus})

# INPUT: A number denoting how the hp should be changed
# RETURN: None
# PURPOSE: To update the player's health points.
def update_hp(num):
    old_hp = PLAYER_STATS["hp"]
    new_hp = num + old_hp
    PLAYER_STATS.update({"hp": new_hp})

# INPUT: A number denoting how the ac should be changed
# RETURN: None
# PURPOSE: To update the player's armor class value.
def update_ac(num):
    old_ac = PLAYER_STATS["ac"]
    new_ac = num + old_ac
    PLAYER_STATS.update({"ac": new_ac})

# INPUT: A number denoting how the gold should be changed
# RETURN: None
# PURPOSE: To update the player's current gold value.
def update_gold(num):
    gold = PLAYER_INVENTORY["gold"]
    gold = gold + num
    PLAYER_INVENTORY.update({"gold": gold})
    write(f"You now have {gold} gold.")

# INPUT: None
# RETURN: An int of the player's current gold value.
# PURPOSE: To check the player's current amount of gold.
def check_gold():
    return PLAYER_INVENTORY["gold"]

# INPUT: None
# RETURN: An int of the damage the player deals with their unique attack, based on their class.
# PURPOSE: To calculate the damage the player does with their unique attack, based on their class.
def class_attack():
    if PLAYER_CLASS == "Bard":
        return (roll_d4()) + PLAYER_STATS["damage bonus"]
    elif PLAYER_CLASS == "Rogue":
        return (roll_d6()) + PLAYER_STATS["damage bonus"]
    elif PLAYER_CLASS == "Warrior":
        return (roll_d6()) + PLAYER_STATS["damage bonus"]
    elif PLAYER_CLASS == "Wizard":
        return (roll_d4()) + PLAYER_STATS["damage bonus"]

# INPUT: None
# RETURN: None
# PURPOSE: To display a message and sound effect denoting that the player succeeded an ability check.
def check_success():
    sound_effect("success")
    write("You succeeded the check!")
    rest()

# INPUT: None
# RETURN: None
# PURPOSE: To display a message and sound effect denoting that the player failed an ability check.
def check_failure():
    sound_effect("failure")
    write("You failed the check.")
    rest()





# +------------------------------------------+
# |                                          |
# |-------------------TIME-------------------|
# |                                          |
# +------------------------------------------+

# INPUT: None
# RETURN: None
# PURPOSE: To give a short pause in the program, usually so that the user has time to read dialogue before it disappears.
def rest():
    time.sleep(0.7)

# INPUT: None
# RETURN: None
# PURPOSE: To give a longer pause in the program, usually so that the user has time to read dialogue before it disappears.
def wait():
    time.sleep(1.5)






# +-------------------------------------------+
# |                                           |
# |-------------------AUDIO-------------------|
# |                                           |
# +-------------------------------------------+

# INPUT: A string denoting which sound should be played
# RETURN: None
# PURPOSE: To play a specific sound effect.
def sound_effect(sound):
    
    # Menu sounds
    if sound == "select":
        path = "assets/sounds/sfx/other/ui_menu_ok.wav"
    elif sound == "skip":
        path = "assets/sounds/sfx/other/ui_menu_cancel.wav"
    elif sound == "hover":
        path = "assets/sounds/sfx/other/hover.wav"
    elif sound == "success":
        path = "assets/sounds/sfx/other/success.wav"
    elif sound == "failure":
        path = "assets/sounds/sfx/other/failure.wav"

    # Weapon sounds:
    elif sound == "lute":
        path = random.choice(["assets/sounds/sfx/attacks/lute/bard_spell.wav", "assets/sounds/sfx/attacks/lute/bard_spell_2.wav", "assets/sounds/sfx/attacks/lute/bard_spell_3.wav", "assets/sounds/sfx/attacks/lute/bard_spell_4.wav", "assets/sounds/sfx/attacks/lute/bard_spell_5.wav"])
    elif sound == "dagger":
        path = random.choice(["assets/sounds/sfx/attacks/dagger/dagger-scrape-and-hit.mp3", "assets/sounds/sfx/attacks/dagger/knife-slice.mp3", "assets/sounds/sfx/attacks/dagger/metal-dagger-hit.mp3"])
    elif sound == "sword":
        path = random.choice(["assets/sounds/sfx/attacks/sword/sword-clang.mp3", "assets/sounds/sfx/attacks/sword/sword-clash.mp3", "assets/sounds/sfx/attacks/sword/sword-slash-and-swing.mp3"])
    elif sound == "fireball":
        path = random.choice(["assets/sounds/sfx/attacks/fireball/elemental-spell.mp3", "assets/sounds/sfx/attacks/fireball/short-fire-whoosh.mp3", "assets/sounds/sfx/attacks/fireball/confringo.wav", "assets/sounds/sfx/attacks/fireball/fireball_sound_1.wav"])
    elif sound == "bear":
        path = "assets/sounds/sfx/attacks/bear/slash1.mp3"

    # Roar sounds:
    elif sound == "goblin_roar":
        path = random.choice(["assets/sounds/sfx/roars/goblin/goblin_laugh_1.wav", "assets/sounds/sfx/roars/goblin/goblin_laugh_2.wav"])
    elif sound == "bear_roar":
        path = random.choice(["assets/sounds/sfx/roars/bear/Bear_Vo_Roar01.wav", "assets/sounds/sfx/roars/bear/Bear_Vo_Roar02.wav", "assets/sounds/sfx/roars/bear/Bear_Vo_Roar03.wav"])
    elif sound == "human_roar":
        path = random.choice(["assets/sounds/sfx/roars/human/Assassin_Junior_Vo_Sign00_edit.wav", "assets/sounds/sfx/roars/human/Assassin_Junior_Vo_Sign00_edit.wav", "assets/sounds/sfx/roars/human/Assassin_Junior_Vo_Sign02.wav"])

    # Death sounds:
    elif sound == "goblin_death":
        path = "assets/sounds/sfx/death/goblin/Bokoblin_Vo_Dead02.wav"
    elif sound == "bear_death":
        path = "assets/sounds/sfx/death/bear/Bear_Vo_Dead01.wav"
    elif sound == "human_death":
        path = random.choice(["assets/sounds/sfx/death/human/Assassin_Junior_Vo_DamageL01.wav", "assets/sounds/sfx/death/human/Assassin_Junior_Vo_DamageL00.wav"])
    elif sound == "player_death":
        path = "assets/sounds/sfx/death/player/death.mp3"
    else:
        return

    sound = pygame.mixer.Sound(path)
    sound.play()

# INPUT: A boolean value denoting which song or playlist should be played
# RETURN: None
# PURPOSE: To play a specific music song or playlist, assuming it isn't already playing.
def music(combat=False, village=False, explore=False, goofy=False, title=False, epilogue=False, ending=False, volume=None, turn_off=False):
    
    global CURRENT_SONG
    global CURRENT_PLAYLIST
    global CURRENT_PLAYLIST_INDEX
    global CURRENT_MAX_INDEX

    if not GAME_RUNNING:
        return

    if combat:
        if CURRENT_SONG == "combat":
            return
        CURRENT_SONG = "combat"
        CURRENT_PLAYLIST = ["assets/sounds/music/combat/battle_02.mp3", "assets/sounds/music/combat/battle_03.mp3", "assets/sounds/music/combat/battle_04.mp3", "assets/sounds/music/combat/battle_05.mp3", "assets/sounds/music/combat/battle_07.mp3"]
        CURRENT_MAX_INDEX = 4

    elif village:
        if CURRENT_SONG == "village":
            return
        CURRENT_SONG = "village"
        CURRENT_PLAYLIST = ["assets/sounds/music/village/town_02.mp3", "assets/sounds/music/village/town_03.mp3", "assets/sounds/music/village/town_04.mp3"]
        CURRENT_MAX_INDEX = 2

    elif explore:
        if CURRENT_SONG == "explore":
            return
        CURRENT_SONG = "explore"
        CURRENT_PLAYLIST = ["assets/sounds/music/explore/atmosphere_01.mp3", "assets/sounds/music/explore/atmosphere_03.mp3", "assets/sounds/music/explore/atmosphere_04.mp3", "assets/sounds/music/explore/atmosphere_06.mp3", "assets/sounds/music/explore/atmosphere_07.mp3"]
        CURRENT_MAX_INDEX = 5

    elif goofy:
        if CURRENT_SONG == "goofy":
            return
        CURRENT_SONG = "goofy"
        CURRENT_PLAYLIST = ["assets/sounds/music/other/goofy_fight.mp3"]
        CURRENT_MAX_INDEX = 0
    
    elif title:
        if CURRENT_SONG == "title":
            return
        CURRENT_SONG = "title"
        CURRENT_PLAYLIST = ["assets/sounds/music/explore/atmosphere_08.mp3"]
        CURRENT_MAX_INDEX = 0
    
    elif epilogue:
        if CURRENT_SONG == "epilogue":
            return
        CURRENT_SONG = "epilogue"
        CURRENT_PLAYLIST = ["assets/sounds/music/village/town_01.mp3"]
        CURRENT_MAX_INDEX = 0
    
    elif ending:
        if CURRENT_SONG == "ending":
            return
        CURRENT_PLAYLIST = ["assets/sounds/music/other/tes4title.mp3"]
        CURRENT_MAX_INDEX = 0

    elif turn_off:
        if CURRENT_SONG == None:
            return
        CURRENT_SONG = None
        CURRENT_PLAYLIST = None
        CURRENT_MAX_INDEX = None
        pygame.mixer.music.fadeout(1000)
        return

    pygame.mixer.music.fadeout(1000)
    volume = 0.3 if not volume else volume
    random.shuffle(CURRENT_PLAYLIST)
    CURRENT_PLAYLIST = dict(enumerate(CURRENT_PLAYLIST))


    if GAME_RUNNING:
        
        CURRENT_PLAYLIST_INDEX = 0
        if not pygame.mixer.music.get_busy():
            song = CURRENT_PLAYLIST[CURRENT_PLAYLIST_INDEX]

            pygame.mixer.music.fadeout(1000)
            pygame.mixer.music.load(song)
            pygame.mixer.music.set_volume(volume)
            pygame.mixer.music.play(fade_ms=500)
            rest()
            CURRENT_PLAYLIST_INDEX += 1
            if CURRENT_PLAYLIST_INDEX > CURRENT_MAX_INDEX:
                CURRENT_PLAYLIST_INDEX = 0

# INPUT: None
# RETURN: None
# PURPOSE: To play the next song in the playlist if the previous one is finished.
def check_music():
    global CURRENT_PLAYLIST, CURRENT_PLAYLIST_INDEX, CURRENT_MAX_INDEX
    if GAME_RUNNING:
        if CURRENT_PLAYLIST:
            if not pygame.mixer.music.get_busy():
                song = CURRENT_PLAYLIST[CURRENT_PLAYLIST_INDEX]

                pygame.mixer.music.fadeout(1000)
                pygame.mixer.music.load(song)
                pygame.mixer.music.set_volume(0.5)
                pygame.mixer.music.play(fade_ms=500)
                rest()
                CURRENT_PLAYLIST_INDEX += 1
                if CURRENT_PLAYLIST_INDEX > CURRENT_MAX_INDEX:
                    CURRENT_PLAYLIST_INDEX = 0





# +------------------------------------------+
# |                                          |
# |-------------------TEXT-------------------|
# |                                          |
# +------------------------------------------+

# INPUT: A string of text, a color code tuple, boolean values denoting the stylization of the text, and an int denoting how fast the text is written.
# RETURN: None
# PURPOSE: To write text into the textbox while making sure not to mess up the layering of the display.
def write(text, color=TEXT, italic=False, bold=False, delay=45):
    check_music()
    refresh_character()

    if italic:
        FONT.set_italic(True)
    if bold:
        FONT.set_bold(True)
    output = ""
    TYPING_SOUND.play(loops=-1)
    
    # Write each character in the text
    i = 0
    while i < len(text):
        c = text[i]
        pygame.event.pump()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            output = text
            sound_effect("skip")
            break
        output += c
        check_quit()

        # Blit background + textbox
        draw_frame(output, color)
        if c in ",:;":
            TYPING_SOUND.set_volume(0)
            pygame.time.delay(300)
            TYPING_SOUND.set_volume(1)
        elif c == '"':
            try:
                text[i+1]
                pygame.time.delay(delay)
            except:
                TYPING_SOUND.set_volume(0)
                pygame.time.delay(600)
                TYPING_SOUND.set_volume(1)        

        elif c == ".":
            try:
                if text[i+1] == '"':
                    pygame.time.delay(delay)
                elif text[i+1] == " ":
                    TYPING_SOUND.set_volume(0)
                    pygame.time.delay(600)
                    TYPING_SOUND.set_volume(1)
            except:
                try:
                    if (text[i] == "." and text[i+1] == ".") or (text[i-1] == "." and text[i] == "."):

                        pygame.time.delay(delay)
                    else:
                        TYPING_SOUND.set_volume(0)
                        pygame.time.delay(600)
                        TYPING_SOUND.set_volume(1)
                except:
                    TYPING_SOUND.set_volume(0)
                    pygame.time.delay(600)
                    TYPING_SOUND.set_volume(1)
        elif c in "!?":
            try:
                if not text[i+1] == '"':
                    TYPING_SOUND.set_volume(0)
                    pygame.time.delay(600)
                    TYPING_SOUND.set_volume(1)
                else:
                    pygame.time.delay(delay)
            except:
                TYPING_SOUND.set_volume(0)
                pygame.time.delay(600)
                TYPING_SOUND.set_volume(1)
        else:
            pygame.time.delay(delay)
        i += 1

    # Write full line
    draw_frame(output, color)
    TYPING_SOUND.stop()

    # Reset and wait
    FONT.set_italic(False)
    FONT.set_bold(False)
    check_quit()
    pygame.event.clear()

# INPUT: A string denoting the person talking, and a string denoting the words they are saying.
# RETURN: None
# PURPOSE: To format text being written as character dialogue
def talk(person, words): 
    words = f"\"{words}\""
    write(words)

# INPUT: A string of text, a color code tuple, and a boolean value denoting whether the text should bolded.
# RETURN: None
# PURPOSE: To format text as italic by default.
def explain(text, color=TEXT, bold=False):
    write(text, italic=True, color=color, bold=bold)
    




# +----------------------------------------------+
# |                                              |
# |-------------------DIALOGUE-------------------|
# |                                              |
# +----------------------------------------------+

# INPUT: A string of text for the prompt
# RETURN: A string of the user's input
# PURPOSE: To get the player's input
def get_input(prompt):
    pygame.event.clear()
    user_text = ""

    while True:
        pygame.event.pump()

        SCREEN.blit(BACKGROUND, (0, 0))
        refresh_character()
        draw_textbox()
        
        prompt_surface = FONT.render(prompt, True, TEXT)
        input_surface = FONT.render(user_text + "|", True, TEXT)

        SCREEN.blit(prompt_surface, (40, BOX.top + 40))
        SCREEN.blit(input_surface, (40, BOX.top + 70))

        pygame.display.flip()
        CLOCK.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return user_text.strip()
                elif event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                else:
                    if len(event.unicode) == 1 and event.unicode.isprintable():
                        user_text += event.unicode

# INPUT: A string of text for the prompt, a list of dialogue options, each one being a list of the option's name and value, and a boolean denoting if the main menu should be displayed.
# RETURN: An int/bool/string, depending on what was passed into it.
# PURPOSE: To display a menu dialogue for the player, then return the option they select.
def dialogue(prompt, options, menu=True):
    check_music()

    global GAME_RUNNING
    selected = 0
    options = [opt for opt in options if opt]
    if menu:
        pass
    pygame.event.clear()
    while True:
        
        # Blit dialogue box
        pygame.draw.rect(SCREEN, (20, 40, 60), (200, 25, WIDTH - 400, HEIGHT - 300))
        pygame.draw.rect(SCREEN, WHITE, (200, 25, WIDTH - 400, HEIGHT - 300), 2)

        # Write prompt
        prompt_render = FONT.render(prompt, True, WHITE)
        SCREEN.blit(prompt_render, (220, 50))

        # Write options
        for i, (text, value) in enumerate(options):
            color = YELLOW if i == selected else WHITE
            text = text + " <—" if i == selected else text
            render_wrapped_text(text, color, 240, 90 + i * 30, WIDTH - 400)
        
        pygame.display.flip()
        CLOCK.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    sound_effect("hover")
                    selected = (selected + 1) % len(options)
                elif event.key == pygame.K_UP:
                    sound_effect("hover")
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    sound_effect("select") 
                    result = options[selected][1]
                    return result
            elif event.type == pygame.QUIT:
                GAME_RUNNING = False
                pygame.quit()
                sys.exit()

# INPUT: A string containing the option name, a string/bool/value or anything else denoting the option's value, and two strings denoting the classes and/or flags that the player must have.
# RETURN: A list containing the option's name and value, or None if the player doesn't have access to the option.
# PURPOSE: To format each dialogue option and also filter out ones the player doesn't have access to.
def opt(name, value, classes=None, flag=None):
    option = {f"name": f"- {name}", "value": value}
    if classes:
        option["classes"] = classes
    if flag:
        option["flag"] = flag
    if ("classes" not in option or PLAYER_CLASS in option["classes"]) and ("flag" not in option or STORY_FLAGS.get(option["flag"])):
        option = [name, value]
        return option
    else:
        return None

# INPUT: A string containing the flag for the option, and a list containing the option.
# RETURN: A list containing the option, or None if the player has already selected that option before.
# PURPOSE: To make a dialogue option available to select only if its flag is not raised.
def once(flag, opt):
    return opt if not STORY_FLAGS.get(flag) else None





# +-------------------------------------------------+
# |                                                 |
# |-------------------STORY FLAGS-------------------|
# |                                                 |
# +-------------------------------------------------+

# INPUT: One or more string flags in a tuple
# RETURN: None
# PURPOSE: to set a global flag for other functions.
def flag(*flags):
    for flag in flags:
        STORY_FLAGS[flag] = True

# INPUT: One or more string flags in a tuple
# RETURN: None
# PURPOSE: to remove a global flag for other functions.
def remove_flag(*flags):
    for flag in flags:
        STORY_FLAGS.pop(flag)

# INPUT: One or more string flags in a tuple
# RETURN: None
# PURPOSE: to set a global flag for other functions, separate from the other group.
def unlock(*unlocks):
    for unlock in unlocks:
        STORY_UNLOCKS[unlock] = True

# INPUT: A string of a flag.
# RETURN: A boolean value: True or False
# PURPOSE: To check if a certain unlock flag has been raised or not.
def check_unlock(unlock):
    if STORY_FLAGS.get(unlock) == True:
        return True
    else: 
        return False





# +--------------------------------------------+
# |                                            |
# |-------------------COMBAT-------------------|
# |                                            |
# +--------------------------------------------+

# INPUT: A list of tuples that each have a string of the statblock name, a boolean denoting whether the creature is an enemy or ally, an int denoting how many of that creature to add, and a string giving that creature a name.
# RETURN: A boolean value: True or False
# PURPOSE: To run combat encounters.
def run_combat(encounter, death=True):
    global DEATH_DAMAGE_BONUS
    player = {
        "name": PLAYER_NAME,
        "hp": PLAYER_STATS["hp"],
        "ac": PLAYER_STATS["ac"],
        "attack_bonus": PLAYER_STATS["attack bonus"],
        "damage_bonus": PLAYER_STATS["damage bonus"],
        "damage": class_attack,
        "number_of_attacks": PLAYER_STATS["number of attacks"],
        "skip_turn": False,
        "attack_sound": PLAYER_ATTACK_SOUND,
        "death_sound": "skip"
    }


    # Create enemy/ally groups
    enemies = []
    allies = []
    for group in encounter:
        creature_type, enemy, number_of_creatures, name, = group
        base = STATBLOCKS[creature_type]
        if enemy:
            i = 0
            while i < number_of_creatures:
                enemy = {
                    "name": (f"{base['name']} {i + 1}" if not name else (name if number_of_creatures == 1 else f"{name} {i + 1}")),
                    "hp": base["hp"],
                    "ac": base["ac"],
                    "attack_bonus": base["attack_bonus"],
                    "damage": base["damage"],
                    "skip_turn": False,
                    "attack_sound": base["attack_sound"],
                    "roar_sound": base["roar_sound"],
                    "death_sound": base["death_sound"],
                    "portrait": base["portrait"]
                }
                enemies.append(enemy)
                i += 1
        if not enemy:
            i = 0
            while i < number_of_creatures:
                ally = {
                    "name": (f"{base['name']} {i + 1}" if not name else (name if number_of_creatures == 1 else f"{name} {i + 1}")),
                    "hp": base["hp"],
                    "ac": base["ac"],
                    "attack_bonus": base["attack_bonus"],
                    "damage": base["damage"],
                    "skip_turn": False,
                    "attack_sound": base["attack_sound"],
                    "roar_sound": base["roar_sound"],
                    "death_sound": base["death_sound"]
                }
                allies.append(ally)
                i += 1 

    # Check if the player has any other allies with them
    for player_ally in PLAYER_ALLIES:
        creature_type, creature_name = player_ally
        base = STATBLOCKS[creature_type]
        ally = {
            "name": (f"{creature_name}"),
            "hp": base["hp"],
            "ac": base["ac"],
            "attack_bonus": base["attack_bonus"],
            "damage": base["damage"],
            "skip_turn": False,
            "attack_sound": base["attack_sound"],
            "roar_sound": base["roar_sound"],
            "death_sound": base["death_sound"]
        } 
        allies.append(ally)

    write(f"Combat begins!")
    wait()

    # Main combat loop
    music(combat=True)
    while True:
        
    
        # Player turn
        write("--- Your Turn ---", GREEN)
        rest()
        player_attacks = player["number_of_attacks"]
        
        # Check if the player is stunned
        if player["skip_turn"] == True:
            write("You are stunned...", PURPLE)
            rest()
            continue

        while player_attacks > 0:
            
            # Selecting a target
            targets = []
            for enemy in enemies:
                if enemy["hp"] > 0:
                    targets.append(opt(f"{enemy["name"]}. ({enemy["hp"]} HP) [{generic_chance(player["attack_bonus"], enemy["ac"])} chance]", enemy))
                
            target = dialogue("Choose a target to attack:", targets)

            show_character(target["portrait"], target["name"])

            attack_roll = roll_d20() + player["attack_bonus"]
            if PLAYER_CLASS == "Bard":
                write(f"You cast a musical spell at {target["name"]}.")
            elif PLAYER_CLASS == "Rogue":
                if player_attacks == 2:
                    write(f"You swipe at {target["name"]} with one of your daggers.")
                elif player_attacks == 1:
                    write(f"You swipe at {target["name"]} with your other dagger.")
            elif PLAYER_CLASS == "Warrior":
                write(f"You swipe at {target["name"]} with your sword.")
            elif PLAYER_CLASS == "Wizard":
                write(f"You cast a fireball at {target["name"]}!")
            sound_effect(player["attack_sound"])

            # Player attack
            if not PLAYER_CLASS == "Wizard":     
                if attack_roll >= target["ac"]:
                    if PLAYER_CLASS == "Rogue" and player_attacks == 1:
                        if (player["damage_bonus"] - 4) > 0:
                            damage_bonus = (player["damage_bonus"] - 4)
                        else:
                            damage_bonus = 0
                        damage = roll_d4() + damage_bonus + DEATH_DAMAGE_BONUS
                    else:
                        damage = player["damage"]() + DEATH_DAMAGE_BONUS
                    target["hp"] -= damage
                    write(f"You hit {target['name']} for {damage} damage.")
                    rest()
                    if target["hp"] <= 0:
                        if death:
                            write(f"{target['name']} is defeated!")
                            rest()
                        elif not death:
                            write(f"{target['name']} yields.")
                            rest()
                        sound_effect(target["death_sound"])

                    if PLAYER_CLASS == "Bard":
                        target["skip_turn"] = True

                    if all(enemy["hp"] <= 0 for enemy in enemies):
                        
                        rest()
                        DEATH_DAMAGE_BONUS = 0
                        clear_character()
                        return True    
                else:
                    write("You missed!")
                    rest()
                
                player_attacks -= 1    

            # Wizard's attack
            elif PLAYER_CLASS == "Wizard":    

                # Roll for primary target
                attack_roll = roll_d20() + player["attack_bonus"]
                if attack_roll >= target["ac"]:
                    damage = player["damage"]() + DEATH_DAMAGE_BONUS
                    target["hp"] -= damage
                    write(f"You hit {target['name']} for {damage} damage.")
                    rest()
                    if target["hp"] <= 0:
                        if death:
                            write(f"{target['name']} is burned to a crisp!")
                            rest()
                        elif not death:
                            write(f"{target['name']} yields.")
                            rest()
                        sound_effect(target["death_sound"])
                else:
                    write(f"Your fireball misses {target['name']}.")
                    rest()

                # Roll for other targets
                for aoe_target in enemies:
                    if aoe_target["hp"] > 0 and aoe_target is not target:

                        aoe_attack = roll_d20() + player["attack_bonus"]
                        if aoe_attack >= enemy["ac"]:
                            aoe_damage = round((player["damage"]() // 2)) 
                            aoe_damage = 2 if aoe_damage > 2 else aoe_damage
                            aoe_target["hp"] -= aoe_damage
                            show_character(aoe_target["portrait"], aoe_target["name"])
                            write(f"{aoe_target["name"]} is caught in the explosion and takes {aoe_damage} damage.")
                            rest()
                            if aoe_target["hp"] <= 0:
                                sound_effect(aoe_target["death_sound"])
                                if death:
                                    write(f"{aoe_target["name"]} is burned to a crisp!")
                                    rest()
                                elif not death:
                                    write(f"{aoe_target["name"]} yields.")
                                    rest()
                clear_character()
                if all(enemy["hp"] <= 0 for enemy in enemies):
                    
                    rest()
                    DEATH_DAMAGE_BONUS = 0
                    clear_character()
                    return True 
                player_attacks -= 1

        # Allies' turn 
        for ally in allies:
            if ally["hp"] > 0:
                
                # Check if stunned
                if ally["skip_turn"] == True:
                    write(f"{ally["name"]} is stunned...", PURPLE)
                    rest()
                    continue
                
                else:
                    write(f"--- {ally["name"]}'s Turn ---", BLUE)
                    rest()
                    target_options = [enemy for enemy in enemies if enemy["hp"] > 0]
                    if not target_options:
                        break

                    target = random.choice(target_options)
                    show_character(target["portrait"], target["name"])
                    write(f"{ally["name"]} attacks {target["name"]}!")
                    rest()

                    attack_roll = roll_d20() + ally["attack_bonus"]
                    if attack_roll >= target["ac"]:
                        damage = ally["damage"]()
                        target["hp"] -= damage
                        sound_effect(ally["attack_sound"])
                        if target["hp"] > 0:
                            write(f"{ally["name"]} hits {target["name"]} for {damage} damage. {target["name"]} has {target['hp']} HP left.")
                        else:
                            write(f"{ally["name"]} hits {target["name"]} for {damage} damage.")
                            rest()
                            sound_effect(target["death_sound"])
                            if death:
                                write(f"{target['name']} is defeated!")
                                rest()
                            elif not death:
                                write(f"{target['name']} yields.")
                                rest()

                        if all(enemy["hp"] <= 0 for enemy in enemies):
                            
                            rest()
                            DEATH_DAMAGE_BONUS = 0
                            clear_character()
                            return True    
                    else:
                        write(f"{ally["name"]} misses.")
                    
                clear_character()
                wait()


        # Enemies' turn
        for enemy in enemies:
            clear_character()
            if enemy["hp"] > 0:
                show_character(enemy["portrait"], enemy["name"])
                # Check if stunned
                if enemy["skip_turn"] == True:
                    write(f"{enemy["name"]} is stunned...", PURPLE)
                    rest()
                    clear_character()
                    enemy["skip_turn"] = False
                    continue
                else:
                    write(f"--- {enemy["name"]}'s Turn ---", RED)
                    rest()
                    target_options = [ally for ally in allies if ally["hp"] > 0]
                    target_options.append(player)
                    if not target_options:
                        break

                    target = random.choice(target_options)
                    write(f"{enemy["name"]} attacks {target["name"]}!")
                    sound_effect(enemy["roar_sound"])
                    rest()

                    attack_roll = roll_d20() + enemy["attack_bonus"]
                    if attack_roll >= target["ac"]:
                        damage = enemy["damage"]()
                        target["hp"] -= damage
                        sound_effect(enemy["attack_sound"])
                        if target["hp"] > 0:
                            write(f"{enemy["name"]} hits {target["name"]} for {damage} damage. {target["name"]} has {target['hp']} HP left.")
                        else:
                            write(f"{enemy["name"]} hits {target["name"]} for {damage} damage.")
                            rest()
                            if death:
                                write(f"{target['name']} is defeated!")
                                rest()
                            elif not death:
                                write(f"{target['name']} yields.")
                                rest()
                            sound_effect(target["death_sound"])
                        if player["hp"] <= 0:
                            
                            rest()
                            DEATH_DAMAGE_BONUS += 1
                            clear_character()
                            return False
                    else:
                        write(f"{enemy["name"]} misses.")
                    
                rest()
            clear_character()

# INPUT: None
# RETURN: None
# PURPOSE: To display a message upon death in combat, and to keep track of the total number of deaths.
def death_message():
    global PLAYER_DEATHS
    PLAYER_DEATHS += 1
    clear_character()
    music(turn_off=True)
    sound_effect("player_death")
    write("You died...", delay=75, color=RED)
    wait()
    rest()
    if PLAYER_DEATHS > 1:
        write(f"You have now died {PLAYER_DEATHS} times.")
    else:
        write("You have now died 1 time.")
    wait()
    get_input("Press enter to continue.")
    write("Restarting combat...")
    wait()    

# INPUT: A string denoting the type of creature, and a string denoting that creature's name
# RETURN: None
# PURPOSE: To add a creature as the player's ally, which will automatically be included in combats.
def friend(creature_type, creature_name):
    PLAYER_ALLIES.append((creature_type, creature_name))





# +-------------------------------------------+
# |                                           |
# |-------------------GAMES-------------------|
# |                                           |
# +-------------------------------------------+

# INPUT: A boolean value: True or False, that denotes whether the player is cheating or not.
# RETURN: A boolean value: True or False
# PURPOSE: To run a dice game and return the result of the game.
def dice_game(cheat=False):
    player_wins = 0
    npc_wins = 0
    while not player_wins > 1 and not npc_wins > 1:
        
        get_input("Press enter to roll your die.")
        npc_roll = roll_d20()
        if not cheat:
            player_roll = roll_d20()
        elif cheat:
            player_roll = npc_roll + random.choice(range(1,5))
            if player_roll > 20:
                player_roll = 20
            if player_roll == 12:
                player_roll = 13
            if npc_roll == 4:
                player_roll = 4
        write(f"You rolled a {player_roll}.")
        rest()
        write(f"Your opponent rolled a {npc_roll}.")
        rest()

        if player_roll == 4 and not npc_roll == 4:
            player_wins += 2
            break

        elif player_roll == 12 and not npc_roll == 12:
            npc_wins += 2
            break
        
        elif player_roll > npc_roll and not npc_roll == 12 and not npc_roll == 4:
            player_wins += 1
            write("You win the round.")

        elif npc_roll == 4 and not player_roll == 4:
            npc_wins += 2
            break

        elif npc_roll == 12 and not player_roll == 12:
            player_wins += 2
            break

        elif npc_roll > player_roll and not player_roll == 4 and not player_roll == 12:
            npc_wins += 1
            write("The opponent wins the round.")

        elif player_roll == npc_roll or npc_roll == player_roll:
            write("No one wins the round.")

        rest()
        write(f"The scores are {player_wins} to {npc_wins}.")
        rest()



    if player_wins >= 2:
        write("You won the game!")
        rest()
        update_gold(1)
        return True
    
    elif npc_wins >= 2:
        write("Your opponent won the game.")
        rest()
        update_gold(-1)
        return False

# INPUT: A string of the opponent's name.
# RETURN: A boolean value: True or False
# PURPOSE: To run a magical duel game and return the result of the game.
def magical_duel_game(enemy_name):

    music(goofy=True, volume=0.2)

    moves = {
        "Flashfire Burst": {
            "beats": ["Glimmerglaze Chill", "Mystic Windstep"],
            "loses": ["Phantasmal Echo", "Vinecall Charm"]
        },
        "Glimmerglaze Chill": {
            "beats": ["Phantasmal Echo", "Vinecall Charm"],
            "loses": ["Flashfire Burst", "Mystic Windstep"]
        },
        "Mystic Windstep": {
            "beats": ["Glimmerglaze Chill", "Vinecall Charm"],
            "loses": ["Flashfire Burst", "Phantasmal Echo"]
        },
        "Phantasmal Echo": {
            "beats": ["Mystic Windstep", "Flashfire Burst"],
            "loses": ["Glimmerglaze Chill", "Vinecall Charm"]
        },
        "Vinecall Charm": {
            "beats": ["Flashfire Burst", "Phantasmal Echo"],
            "loses": ["Mystic Windstep", "Glimmerglaze Chill"]
        },
    }
        
    player_wins = 0
    enemy_wins = 0
    round_number = 1

    while player_wins < 3 and enemy_wins < 3:
        
        write(f" ---Round {round_number}---")

        player_choice = dialogue("Choose your spell:", [
            opt("Flashfire Burst", "Flashfire Burst"),
            opt("Glimmerglaze Chill", "Glimmerglaze Chill"),
            opt("Mystic Windstep", "Mystic Windstep"),
            opt("Phantasmal Echo", "Phantasmal Echo"),
            opt("Vinecall Charm", "Vinecall Charm")
        ])
        rest()
        

        enemy_choice = random.choice(list(moves.keys()))

        write(f"You cast: {player_choice}")
        rest()
        write(f"{enemy_name} casts: {enemy_choice}")
        rest()
        

        if player_choice == enemy_choice:
            write("It's a tie.")
            rest()

        elif enemy_choice in moves[player_choice]["beats"]:
            write(f"{player_choice} defeats {enemy_choice}! You win this round!")
            player_wins += 1
            rest()
            

        elif enemy_choice in moves[player_choice]["loses"]:
            write(f"{enemy_choice} defeats {player_choice}! You lose this round.")
            enemy_wins += 1
            rest()

        write(f"The scores are {player_wins} to {enemy_wins}.")
        wait()
        round_number += 1

    if player_wins == 3:
        return True
    if enemy_wins == 3:
        return False





# +-------------------------------------------+
# |                                           |
# |-------------------OTHER-------------------|
# |                                           |
# +-------------------------------------------+

# INPUT: A string of the flag, and one or more lambda functions in a tuple.
# RETURN: None
# PURPOSE: To run the passed functions only if their flag has not been raised.
def run_once(flag, *functions):
    if not STORY_FLAGS.get(flag):
        for function in functions:
            function()
        STORY_FLAGS[flag] = True

# INPUT: A string with the player's class choice.
# RETURN: None
# PURPOSE: To initialize the player's stats and other things, based on their class choice.
def initialize_character(class_choice):
    global PLAYER_CLASS, PLAYER_STATS, PLAYER_SKILLS, PLAYER_INVENTORY, PLAYER_DEATHS, PLAYER_ALLIES, PLAYER_ATTACK_SOUND

    if class_choice == "Bard":
        PLAYER_CLASS = "Bard" 
        PLAYER_STATS = {"hp": 27, "max hp": 27, "ac": 13, "str": 10, "dex": 12, "con": 12, "int": 10, "wis": 12, "cha": 18, "attack bonus": 6, "damage bonus": 4, "number of attacks": 1}
        PLAYER_SKILLS = ["animal handling", "deception", "intimidation", "performance", "persuasion"]
        PLAYER_ATTACK_SOUND = "lute"

    elif class_choice == "Rogue":
        PLAYER_CLASS = "Rogue"
        PLAYER_STATS = {"hp": 25, "max hp": 25, "ac": 15, "str": 8, "dex": 18, "con": 10, "int": 12, "wis": 12, "cha": 14, "attack bonus": 6, "damage bonus": 4, "number of attacks": 2}
        PLAYER_SKILLS = ["acrobatics", "sleight of hand", "stealth", "insight", "investigation"]
        PLAYER_ATTACK_SOUND = "dagger"

    elif class_choice == "Warrior":
        PLAYER_CLASS = "Warrior"
        PLAYER_STATS = {"hp": 36, "max hp": 36, "ac": 16, "str": 18, "dex": 12, "con": 14, "int": 10, "wis": 12, "cha": 8, "attack bonus": 6, "damage bonus": 4, "number of attacks": 1}
        PLAYER_SKILLS = ["athletics", "perception", "survival", "intimidation"]
        PLAYER_ATTACK_SOUND = "sword"

    elif class_choice == "Wizard":
        PLAYER_CLASS = "Wizard"
        PLAYER_STATS = {"hp": 24, "max hp": 24, "ac": 14, "str": 8, "dex": 14, "con": 12, "int": 18, "wis": 14, "cha": 8, "attack bonus": 6, "damage bonus": 4, "number of attacks": 1}
        PLAYER_SKILLS = ["arcana", "history", "nature", "religion"]
        PLAYER_ATTACK_SOUND = "fireball"

    PLAYER_INVENTORY = {"gold": 0}
    PLAYER_DEATHS = 0
    PLAYER_ALLIES = []
    # PLAYER_ALLIES = [("goblin", "Ella")]

# INPUT: None
# RETURN: None
# PURPOSE: To display the final scene of act 3, made into a function because I call if multiple times.
def final_scene():
    explain("Except...")
    rest()
    explain("As the dust clears on your battle, you notice the nearly-dead King Snik crawling towards the Arc Node.")
    rest()
    show_character("goblin_king.png", "King Snik")
    talk("King Snik", "I.")
    rest()
    talk("King Snik", "Will.")
    rest()
    talk("King Snik", "Not.")
    rest()
    talk("King Snik", "Lose!")
    rest()
    explain("He rips the shell off the the Arc Node, and reaches into it.")
    rest()
    explain("As he does, blue sparks and lightning start enveloping him as he starts laughing.")
    rest()
    talk("King Snik", "I might had power before...")
    rest()
    explain("His skin starts glowing with lightning.")
    rest()
    talk("King Snik", "But I have REAL power now.")
    wait()
    explain("His skin continues to glow brighter and brighter...")
    rest()
    talk("King Snik", "wait...")
    rest()
    talk("King Snik", "Wait...")
    rest()
    talk("King Snik", "WAIT...")
    rest()
    explain("You get one more look at his betrayed face before he combusts, the power consuming him.")
    rest()
    clear_character()
    explain("The Arc Node explodes, knocking you off your feet.")
    wait()
    explain("Silence rings across the camp for a moment.")
    rest()
    explain("Then...")
    rest()
    explain("The remaining goblins scatter.")
    wait()
    write("You have defeated the goblins of Grimglen Hollow.")
    wait()
    flag("moving to epilogue")





# +---------------------------------------------------+
# |                                                   |
# |-------------------GAME CHAPTERS-------------------|
# |                                                   |
# +---------------------------------------------------+

# INPUT: None
# RETURN: None
# PURPOSE: To run the prologue of the game
def prologue():
    music(title=True)
    # welcome
    if FIRST_TIME:
        write("Welcome traveler.")
        rest()
        write("This game uses music and sound effects, so make sure you have your volume on.")
        rest()
        write("You can press the spacebar to skip dialogue at any time.")
        rest()
        write("When asked a multiple choice question, use the arrow and enter keys to select an option.")
        rest()
        global TUTORIAL
        TUTORIAL = dialogue("Is this your first time playing?", [
                    opt("Yes.", 1),
                    opt("No.", 2)
                    ], False)
        rest()
        
        if TUTORIAL == 1:
            TUTORIAL = True
            write("Awesome! The tutorial mode will be enabled during character creation.")
            rest()
            write("During this game, you will navigate an adventure through social interactions, exploration, and combat.")
            rest()
            write("This adventure is heavily modeled after Dungeons and Dragons, both in story and mechanics.")
            rest()
            write("However, you do not need to have any prior knowledge of D&D in order to play and understand this game. Most of the mechanical stuff in handled in the background.")
            wait()
            write("There will be combat in this game, but do not worry too much about dying. If you die in combat, you will simply restart at the beginning of the encounter and get to retry.")
            wait()
            write("Without further ado, please enjoy my adventure game!")
            rest()
        elif TUTORIAL == 2:
            TUTORIAL = False
            write("Alright then, we'll get right into it!")
            rest()

    elif not FIRST_TIME:
        TUTORIAL = False
        write("Welcome back, traveler.")
        rest()
        write("Alright, you know the drill.")
        rest()

    # name selection
    if FIRST_TIME:
        write("Before we can begin, I need to know who you are.")
    global PLAYER_NAME
    first_time_choosing_name = True
    while True:
        rest()
        PLAYER_NAME = get_input("What is your name?")
        if PLAYER_NAME == "":
            if first_time_choosing_name:
                write(f"You can't just leave that blank. You gotta have some name.")
                first_time_choosing_name = False
                continue
            elif not first_time_choosing_name:
                write("You really don't want a name, huh? Well, we can't have that. I will name you Doug.")
                PLAYER_NAME = "Doug"
                break
        elif PLAYER_NAME.isdigit():
            write("It's a bit odd for your name to be a number, but I suppose it will do.")
            break
        else:
            write(f"{PLAYER_NAME}...")
            rest()
            name_evaluation = ("What a lovely name!", "Not my favorite, but it will work.", "Ooh, so creative. I love it!", "Huh, what an odd choice.", "How.... unique.")
            write(f"{random.choice(name_evaluation)}")
            rest()
            break

    # Class Selection
    write("Now that you have a name, you will need to choose a class!")
    rest()
    
    if TUTORIAL:
        write("In this adventure you can pick from four classes to play from.")
        rest()
        write("Each class comes with different strengths and weaknesses, as well as different ways to play the game (including unique side quests!).")
        rest()
        write("Option 1 -- The Bard")
        rest()
        write("Bards are charismatic fellows who love to charm those around them with their wondrous musical performances.")
        rest()
        write("Bards attack by playing musical spells that stun their enemies.")
        rest()
        write("Option 2 -- The Rogue")
        rest()
        write("Rogues excel at sneaking around where they aren't supposed to. They are light on their feet and make master thieves and assassins.")
        rest()
        write("Rogues attack with a dagger in each hand, allowing them to attack twice on each turn. Though, their second attack deals less damage than the first.")
        rest()
        write("Option 3 -- The Warrior")
        rest()
        write("Warriors are trained to be the best fighters in town. They are fearsome, and even though they may seem simple, they are very effective.")
        rest()
        write("Warriors attack with a sword and shield, allowing them to have the best defense while in combat.")
        rest()
        write("Option 4 -- The Wizard")
        rest()
        write("Wizards have spent years studying the ancient arts of magic. They have become masters at all things arcane, and are highly revered.")
        rest()
        write("Wizards attack by flinging fireballs onto the battlefield. These fireballs target all enemies, though they do less damage to creatures that aren't the main target of the fireball.")
        rest()
    elif not TUTORIAL:
        flag("no tutorial")
    while True:
        class_selection = dialogue("Which class would you like to play?", [
            opt("Bard.", 1),
            opt("Rogue.", 2),
            opt("Warrior.", 3),
            opt("Wizard.", 4),
            opt("Read Class Descriptions.", 5, flag="no tutorial")
            ], False)
        rest()
        

        if class_selection == 1:
            initialize_character("Bard")
            break
        elif class_selection == 2:
            initialize_character("Rogue")
            break
        elif class_selection == 3:
            initialize_character("Warrior")
            break
        elif class_selection == 4:
            initialize_character("Wizard")
            break
        elif class_selection == 5:
            while True:
                
                class_description = dialogue("Which class do you want to learn about?", [
                    opt("Bard.", 1),
                    opt("Rogue.", 2),
                    opt("Warrior.", 3),
                    opt("Wizard.", 4),
                    opt("Go back.", 5)
                ], False)
                rest()
                

                if class_description == 1:
                    write("Bards are charismatic fellows who love to charm those around them with their wondrous musical performances.")
                    rest()
                    write("Bards attack by playing musical spells that stun their enemies.")
                    rest()
                    continue
                elif class_description == 2:
                    write("Rogues excel at sneaking around where they aren't supposed to. They are light on their feet and make master thieves and assassins.")
                    rest()
                    write("Rogues attack with a dagger in each hand, allowing them to attack twice on each turn. Though, their second attack deals less damage than the first.")
                    rest()
                    continue
                elif class_description == 3:
                    write("Warriors are trained to be the best fighters in town. They are fearsome, and even though they may seem simple, they are very effective.")
                    rest()
                    write("Warriors attack with a sword and shield, allowing them to have the best defense while in combat.")
                    rest()
                    continue
                elif class_description == 4:
                    write("Wizards have spent years studying the ancient arts of magic. They have become masters at all things arcane, and are highly revered.")
                    rest()
                    write("Wizards attack by flinging fireballs onto the battlefield. These fireballs target all enemies, though they do less damage to creatures that aren't the main target of the fireball.")
                    rest()
                    continue
                elif class_description == 5:
                    break

    rest()
    if not FIRST_TIME:
        write(f"So, we have {PLAYER_NAME} the {PLAYER_CLASS}.")
        rest()
        if OLD_NAME == PLAYER_NAME and not OLD_CLASS == PLAYER_CLASS:
            write("You picked the same name again?")
            rest()
            write("You know what, I respect it. You know what you like and do not waiver.")
            rest()

        elif OLD_CLASS == PLAYER_CLASS and not OLD_NAME == PLAYER_NAME:
            write("You picked the same class again?")
            rest()
            write("You know what, I respect it. You know what you like and do not waiver.")
            rest()

        elif OLD_NAME == PLAYER_NAME and OLD_CLASS == PLAYER_CLASS:
            write("You picked the exact same name and class as last time?")
            rest()
            write("You know what, I respect it. You know what you like and do not waiver.")
            rest()

    else:
        write(f"So, we have {PLAYER_NAME} the {PLAYER_CLASS}. This is gonna be awesome!")

    while True:
        
        continue_story = dialogue("Are you ready to begin your adventure?", [
            opt("Yes.", 1, None),
            opt("No.", 2, None)
            ], False)

        if continue_story == 1:
                write("Alright then, now we can begin...")
                rest()
                break
        elif continue_story == 2:
            write("Alright, that's understandable. I'll give you some time.")
            time.sleep(random.choice(range(5,10)))
            write("What about now?")
            continue
    
    write("The Goblins of Grimglen Hollow", delay=75)
    wait()

# INPUT: None
# RETURN: None
# PURPOSE: To run act 1 of the game
def act_1():
    music(explore=True)
    # Premise
    if True:
        write("Act 1: To Care", delay=75)
        wait()
        write("The quiet farming village of Hearthstone has a problem. Goblins have begun raiding their supply wagons and attacking outlying farms. As food and other supplies are starting to run thin, the mayor has put out a reward for anyone brave (or foolish) enough to deal with the growing threat.")
        wait()
        write("The goblins are more organized than usual, and rumors spread of a new goblin leader calling himself \"King Snik\", and he's planning something bigger.")
        wait()
        write("You arrive to investigate.")
        rest()
        draw_background(village=True)
        
        explain("The sun shines from above as you approach the quiet village of Hearthstone, nestled between forested hills. Smoke rises from chimneys, but so do faint wisps from burned fields beyond the fence. People look anxious. Children are kept indoors. The goblin raids have taken their toll.")
        wait()
        explain("You're directed to the town hall, where Mayor Thorne, a pudgy man with a comb-over and sweat-stained shirt, is nervously pacing. He greets you with relief.")
        wait()
        show_character("thorne.jpg", "Mayor Thorne")
        talk("Mayor Thorne", f"Thank the stars someone answered our call. Goblins have hit us three times in a week. We lost two supply wagons and a dozen goats. If they keep this up, we won't last the month. I can only imagine what would happen if we didn't get you here, {PLAYER_NAME}.")
        wait()
        explain("He pulls out a hand-drawn map and taps a marked field on the outskirts.")
        rest()
        talk("Mayor Thorne", "We think they're hiding out in the hills near Grimglen Hollow, but we don't know anything specific. Please—anything you can do to help us prepare or learn would be a blessing.")
        rest()
        explain("He reaches into one of his pockets and pulls out some gold coins.")
        rest()
        talk("Mayor Thorne", "This isn't much, but hopefully it will help you on your journey.")
        rest()
        update_gold(5)
        wait()
        talk("Mayor Thorne", "I would suggest visiting the village before heading out. Not many of our shops our open at the moment, but you may find some people in the Hollow Hearth tavern that are of interest to you.")
        wait()
        clear_character()

    
    # Main loop for act 1
    while True:
        music(explore=True)
        if STORY_FLAGS.get("moving to act 2"):
            explain("You get your things together and take one last look at Hearthstone before heading out.")
            rest()
            explain("The people are scared, the buildings are worn down, and the atmosphere is grim.")
            rest()
            explain("They need a hero.")
            rest()
            explain("So, you set out.")
            wait()
            
            break  
        

        prep_before_leaving = dialogue("What do you want to do before heading out?", [
            opt("Ask the mayor some questions.", 1),
            opt("Explore the village.", 2),
            opt("Set out for Grimglen Forest.", 3, flag="explored hearthstone"),
        ])
        rest()
         
        
        while True:
            
            # Asking the mayor questions          
            if prep_before_leaving == 1:
                draw_background(village=True)
                show_character("thorne.jpg", "Mayor Thorne")
                run_once("walking up to the mayor", lambda: talk("Mayor Thorne", f"Hello, {PLAYER_NAME}. Is there anything I can help you with?"))
                
                ask_mayor_questions = dialogue("What do you ask the mayor?", [
                    once("when did the attacks start", opt("When did the goblin attacks start?", 1)),
                    once("what do you know about these goblins", opt("What do you know about these goblins?", 2)),
                    once("what are the goblins stealing", opt("What are the goblins taking?", 3)),
                    once("what are the city defenses", opt("[Warrior] How strong are Hearthstone's defenses?", 4, classes="Warrior")),                    
                    once("any signs of magical effects", opt("[Wizard] Have there been any signs of magical during the attacks?", 5, classes="Wizard")),
                    once("any stories or songs", opt("[Bard] Have there been any stories, songs, or rumors passed around about these goblins?", 6, classes="Bard")),
                    once("who are the goblins working with", opt("[Rogue] Any idea who might be working with them?", 7, classes="Rogue")),
                    opt("Leave the conversation.", 8)

                ])
                rest()
                
                if ask_mayor_questions == 1:
                    flag("when did the attacks start")
                    talk("Mayor Thorne", "The attacks started recently, only a couple weeks back if I recall correctly. As ar as I know, we didn't do anything to upset them; they just attacked out of the blue.")
                    wait()
                if ask_mayor_questions == 2:
                    flag("what do you know about these goblins")
                    talk("Mayor Thorne", "We don't know much about these particular goblins. They seem to be more organized than usual, serving under some leader named King Snik.")
                    wait()
                if ask_mayor_questions == 3:
                    flag("what are the goblins stealing")
                    talk("Mayor Thorne", "As far as we can tell, the goblins are mostly taking food and building supplies. They're targeting our farms and mines.")
                    wait()
                if ask_mayor_questions == 4:
                    flag("what are the city defenses")
                    talk("Mayor Thorne", "We have some guards, but not many. Most people here in Hearthstone learn how to farm instead of fight. It's possible we could fend off an attack, but not likely.")                
                if ask_mayor_questions == 5:
                    flag("any signs of magical effects")
                    talk("Mayor Thorne", "No magic that we know of… but some villagers claimed to hear strange chanting in the woods. Could be superstition… or something more.")
                if ask_mayor_questions == 6:
                    flag("any stories or songs")
                    talk("Mayor Thorne", "Old Molly says she heard them chanting like soldiers… and there's a tale about goblins who once found a dwarven warhorn deep in the hills. Probably nonsense, but still...")
                if ask_mayor_questions == 7:
                    flag("who are the goblins working with")
                    talk("Mayor Thorn", "I hate to say it… but there are rumors someone from town told them where to strike. I don't know who to trust.")
                if ask_mayor_questions == 8:
                    remove_flag("walking up to the mayor")
                    rest()
                    clear_character()
                    break
            
            # Explore the village
            if prep_before_leaving == 2:
                music(village=True)
                draw_background(village=True)
                run_once("Hearthstone description", lambda: explain("The streets are tense. Villagers whisper, doors are bolted shut, and signs of recent raids are everywhere."))
                
                exploring_hearthstone = dialogue("What would you like to do in town?", [
                    opt("Visit the tavern.", 1),
                    once("talk to the guards", opt("[Warrior] Talk to the village guards.", 2, classes="Warrior")),
                    opt("[Rogue] Scout the outskirts of the village.", 3, classes="Rogue"),
                    once("check out the play", opt("[Bard] Check out the local play.", 4, classes="Bard")),
                    opt("[Wizard] Seek out a wizard to practice your skills.", 5, classes="Wizard"),
                    opt("Leave the village.", 6)
                ])
                rest()
                
                
                # Tavern
                if exploring_hearthstone == 1:
                    draw_background(tavern=True)
                    flag("explored hearthstone")
                    run_once("entering the tavern", 
                        lambda: explain("As you push open the creaky door of The Hollow Hearth, a wave of warmth and conversation washes over you. A low fire crackles in the hearth, casting flickering shadows on the stone walls. Locals huddle around wooden tables, hunched over mugs of ale and half-eaten meals. Tension clings to the air like smoke. Everyone is talking about the goblins."),
                        lambda: wait(),
                        lambda: explain("Behind the bar, a stout, bald barkeep polishes a mug with little enthusiasm. A travel-worn merchant sits alone in the corner, watching the room with wary eyes. A couple of off-duty guards toss dice near the back, while an older farmer grumbles into his cup."),
                        lambda: wait()
                        )

                    while True:
                        clear_character()
                        
                        tavern_action = dialogue("What do you want to do in the tavern?", [
                            opt("Talk to the barkeeper.", 1),
                            opt("Listen to the conversation", 2),
                            opt("Talk to the merchant.", 3),
                            once("angered the guard", opt("Play dice with the guards.", 4)),
                            once("arm wrestle", opt("Arm wrestle someone.", 5)),
                            once("inspect the hearth", opt("Inspect the hearth.", 6)),
                            once("sneak into a private room", opt("Sneak into a private room", 7)),
                            once("perform for the tavern", opt("[Bard] Perform for the tavern", 8, classes="Bard")),
                            opt("Leave the tavern", 9)
                        ])
                        rest()
                        

                        # Talk with the the barkeeper
                        if tavern_action == 1:
                            show_character("barkeeper.png", "Barkeeper")
                            run_once("barkeep opening dialogue", 
                                lambda: explain("The barkeep sets down a mug he was polishing and turns to you."),
                                lambda: rest(),
                                lambda: talk("Barkeep", "Hmm..."),
                                lambda: rest(),
                                lambda: talk("Barkeep", "You'll be the hero Thorne dragged in to save us, 'wont ya? Well, we need a hero. I've never seen folks this spooked since the fire a few years back."),
                                lambda: wait()
                                )

                            while True:
                                
                                talk_with_barkeep = dialogue("What do you want to say to the barkeep?",[
                                    once("ask about goblins", opt("Ask about recent goblin activity.", 1)),
                                    once("ask about stolen goods", opt("Ask about what the goblins stole.", 2, flag="asked about goblins")),
                                    opt("Order a drink", 3),
                                    opt("Go back.", 4)
                                ])
                                rest()
                                

                                if talk_with_barkeep == 1:
                                    flag("ask about goblins")
                                    explain("His eyes shimmer with fear for a moment before he answers.")
                                    rest()
                                    talk("Barkeep", "Well, they've been raiding our farms and supplies. Just yesterday they hit a supply wagon heading for Hearthstone.")
                                    flag("asked about goblins")
                                if talk_with_barkeep == 2:  
                                    flag("ask about stolen goods")
                                    talk("Barkeep", "Well, they mostly stole military supplies like grain, weapons, armor, and some raw materials. But they also took a strange crate that belonged to her.")
                                    rest()
                                    explain("The barkeep points to the dreary-eyed merchant in the corner.")
                                    rest()
                                    talk("Barkeep", "She never received her last shipment, which isn't unusual, but she seems more distressed than normal. We never saw what happened, but, with everything else that's going on, we assumed the goblins took it.")
                                    wait()
                                if talk_with_barkeep == 3:
                                    flag("order a drink")
                                    talk("Barkeep", "It's 1 gold for a mug of ale. I know it's a little steep but, with the goblin attacks, there isn't much left to go around.")
                                    order_drink = dialogue("Do you want to order a mug of ale?", [
                                        opt("Yes", 1),
                                        opt("No", 2)
                                    ])
                                    rest()
                                    
                                    if order_drink == 1:
                                        if check_gold() > 0:
                                            explain("He grabs the mug he's been polishing and fills it up with ale.")
                                            rest()
                                            talk("Barkeep", "Here 'ya are. One mug of ale.")
                                            rest()
                                            explain("As you drink the ale, the mood in the tavern seems to lighten a bit. The tension from the goblins seems to disappear, if only for a moment.")
                                            wait()
                                            update_gold(-1)
                                        elif check_gold() == 0:
                                            talk("Barkeep", "Sorry, but you don't have enough gold. I can't just give out ale for free, I got a tavern to run!")
                                            write(f"You have {check_gold()} gold")
                                    if order_drink == 2:
                                        write("Well then, is there anything else I can help 'ya with?")
                                        rest()
                                if talk_with_barkeep == 4:
                                    rest()
                                    clear_character()
                                    break

                        # Listen to the conversation    
                        if tavern_action == 2:
                            explain("You listen into the conversations of those around you...")
                            wait()
                            conversation = random.choice(["You overhear talk about how a local trapper claims he saw goblins carrying blueprints for something.",
                                                        "You overhear rumors suggesting that there are people in Hearthstone working with the goblins.",
                                                        "You overhear someone talking about how they saw the goblins carrying a flag, like an army would."])
                            explain(f"{conversation}")
                            wait()

                        # Talk to the merchant
                        if tavern_action == 3:
                            show_character("merchant.png", "Merchant")
                            run_once("tavern merchant opening dialogue", 
                                lambda: explain("As you approach, you see a merchant in a light blue cloak sipping from a chipped mug, eyes sharp despite the drink."),
                                lambda: rest(),
                                lambda: talk("Merchant", "If you're heading into those hills, you'd best be well-stocked. The goblins took my best crate of goods—iron tools and something I don't think they even understood."),
                                lambda: rest()
                                )        

                            while True:
                                
                                merchant_dialogue = dialogue("What do you want to say to the merchant?", [
                                    once("ask about stolen crate", opt("Ask about her stolen crate.", 1)),
                                    once("press her", opt(f"Press her about the crate [{chance("cha", 13, "persuasion")} chance of success].", 2, flag="asked about crate")),
                                    opt("See her wares", 3),
                                    opt("Go back.", 4)
                                ])
                                rest()
                                

                                if merchant_dialogue == 1:
                                    flag("ask about stolen crate")
                                    explain("She shifts in her chair before answering.")
                                    rest()
                                    talk("Merchant", "Well, it was private stock. Rare goods. Things goblins shouldn't want—or know about.")
                                    rest()
                                    flag("asked about crate")
                                    
                                if merchant_dialogue == 2:
                                    persuade_merchant = check("cha", 13, "persuasion")
                                    if persuade_merchant:
                                        explain("You persuaded the merchant!")
                                        rest()
                                        talk("Merchant", "Well, it was some ancient, clockwork machine made by dwarves. I took it to some experts and they couldn't figure it out. And if we couldn't understand it, I can't fathom how the goblins ever would, but still...")
                                        wait()
                                    elif not persuade_merchant:
                                        explain("You were unable to persuade the merchant.")
                                        rest()
                                        talk("Merchant", "Sorry, but I don't feel like talking about it.")
                                        rest()
                                        remove_flag("asked about crate")
                                if merchant_dialogue == 3:
                                    while True:
                                        
                                        stock = dialogue("Merchant stock:", [
                                            once("merchant healing potion", opt("[3 gold] Health Boost Potion.", 1)),
                                            once("merchant rations", opt("[1 gold] Food rations.", 3)),
                                            opt("Go back.", 4)
                                        ])
                                        rest()
                                        

                                        # Potion of healing
                                        if stock == 1:
                                            certainty = dialogue("Are you sure you want to buy a Health Boost Potion for 3 gold?", [
                                                opt("Yes.", 1),
                                                opt("No.", 2)
                                            ])
                                            rest()
                                            
                                            if certainty == 1:
                                                if check_gold() > 2:
                                                    update_gold(-3)
                                                    flag("merchant healing potion")
                                                    write("You bought a Health Boost Potion!")
                                                    rest()
                                                    talk("Merchant", "Thank you.")
                                                    rest()
                                                    explain("As you drink the Health Boost Potion, you feel warmth flooding over you.")
                                                    update_hp(5)
                                                    write("You now have more health points!")
                                                    rest()
                                                elif check_gold() < 3:
                                                    talk("Merchant", "Sorry gancho, but you don't have enough gold for that.")
                                                    write(f"You currently have {check_gold()} gold")

                                        # Rations
                                        if stock == 3:
                                            certainty = dialogue("Are you sure you want to buy food rations for 1 gold?", [
                                                opt("Yes.", 1),
                                                opt("No.", 2)
                                            ])
                                            rest()
                                            

                                            if certainty == 1:
                                                if check_gold() > 2:
                                                    update_gold(-1)
                                                    PLAYER_INVENTORY.update({"food rations": 1})
                                                    flag("merchant rations")
                                                    write(f"You bought some food rations!")
                                                    rest()
                                                    talk("Merchant", "Thank you.")
                                                    rest()
                                                elif check_gold() < 3:
                                                    talk("Sorry gancho, but you don't have enough gold for that.")
                                                    write(f"You currently have {check_gold()} gold")

                                        # Go back
                                        if stock == 4:
                                            break
                                
                                if merchant_dialogue == 4:
                                    rest()
                                    clear_character()
                                    break            
        
                        # Play dice 
                        if tavern_action == 4:
                            show_character("guard.png", "Guard")
                            run_once("dice guards opening", 
                                lambda: explain("You walk up to a group of off-duty guards playing a dice game."),
                                lambda: rest(),
                                lambda: talk("Guard", "You look like someone young and dumb enough to gamble your money away."),
                                lambda: rest()
                                )

                            cheated_gold = 0
                            while True:
                                
                                gamble = dialogue("Do you want to join in the dice game?", [
                                    opt("Yes.", 1),
                                    opt("No.", 2),
                                    opt("Read the rules", 3),
                                ])
                                rest()
                                

                                if gamble == 1:
                                    if check_gold() > 0:
                                        talk("Guard", "Ah, excellent. Lets do this!")
                                        rest()
                                        cheat = False
                                        successfully_cheated = None
                                        if PLAYER_CLASS == "Rogue":
                                            cheat = dialogue(f"[Rogue] Do you want to cheat? [{ chance("dex", 13, "sleight of hand")} chance of not getting caught.]", [
                                                opt("Yes.", True),
                                                opt("No.", False)
                                            ])
                                            rest()
                                            
                                        if cheat:
                                            win = dice_game(cheat=True)
                                            successfully_cheated = check("dex", 13, "sleight of hand")
                                            if win: 
                                                cheated_gold += 1

                                        elif not cheat:
                                            win = dice_game()

                                        
                                        if win:
                                            talk("Guard", "Well, I suppose it was beginner's luck...")
                                            rest()
                                        elif not win:
                                            talk("Guard", "Haha, I won.")
                                            rest()
                                        if not successfully_cheated == None:
                                            if successfully_cheated:
                                                explain("The guard didn't realize that you cheated...")

                                            elif not successfully_cheated:
                                                explain("The guard caught you cheating...")
                                                rest()
                                                talk("Guard", "Wait a second, you cheated, didn't you?")
                                                rest()
                                                talk("Guard", "That's it, give me my money back now!")
                                                rest()
                                                return_money = dialogue("What do you do?", [
                                                    opt(f"Return his money. [{cheated_gold} gold]", True),
                                                    opt(f"Refuse.", False)
                                                ])
                                                rest()
                                            

                                                if return_money:
                                                    explain("The guard quickly takes his money back and walks out of the tavern.")
                                                    rest()
                                                    update_gold(-cheated_gold)
                                                    flag("angered the guard")
                                                    
                                                    break
                                                elif not return_money:
                                                    talk("Guard", "How dare you!")
                                                    rest()
                                                    explain("The guard picks up his spear and grabs two of his friends, then charges at you.")
                                                    while True: 
                                                        win = run_combat({("guard", True, 3, None)}, death=False)
                                                        if win:
                                                            music(village=True)
                                                            break
                                                        elif not win:
                                                            death_message()
                                                            continue

                                                
                                                rest()
                                                
                                                explain("The guards walk out of the tavern with their weapons.")
                                                rest()
                                                explain("All is silent for a moment as everyone stares at you.")
                                                rest()
                                                clear_character()
                                                explain("Then they turn away. After everything that has happened recently, tavern brawls are the least of anyone's concerns.")
                                                flag("angered the guard")                                                
                                                break


                                    elif check_gold() < 1:
                                        talk("Guard", "You don't have any money...")
                                        rest()
                                        clear_character()
                                        break
                                if gamble == 2:
                                    talk("Guard", "Ah, shucks. I was hoping to play a game against you...")
                                    rest()
                                    clear_character()
                                    break
                                if gamble == 3:
                                    write("Tavern dice game rules:")
                                    rest()
                                    write("Before the game starts, you and your opponent will bet 1 gold coin.")
                                    rest()
                                    write("Then, you and your opponent will each roll a d20.")
                                    rest()
                                    write("Whoever rolls higher wins the round.")
                                    rest()
                                    write("Whoever wins best 2 out of 3 wins the game.")
                                    rest()
                                    write("If a player ever rolls a 12, they lose the entire game.")
                                    rest()
                                    write("If a player ever rolls a 4, they win the entire game.")
                                    rest()
                                    write("If a round results in a tie, then nothing happens that round.")
                                    rest()
                                    write("Whoever wins the game wins the bet.")
                                    rest()

                        # Arm wrestle
                        if tavern_action == 5:
                            flag("arm wrestle")
                            explain("A burly lumberjack slaps his hand down on a table near you.")
                            show_character("lumberjack.png", "Lumberjack")
                            rest()
                            talk("Lumberjack", "Hey you, why don't you come here and show me what you got!")
                            arm_wrestling = dialogue("What do you do?", [
                                opt(f"Accept his challenge. [{chance("str", 15, "athletics")} chance of success]", 1),
                                opt(f"Back down.", 2)
                            ])
                            rest()
                            
                            
                            if arm_wrestling == 1:
                                talk("Lumberjack", "Splendid!")
                                success = check("str", 15, "athletics")
                                explain("You grasp hands with the stranger as you begin the arm wrestle.")
                                wait()
                                explain("He's stronger than he looks...")
                                wait()
                                explain("Your pushing as hard as you can, but your arm is slipping downward...")
                                wait()
                                explain("He grins.")
                                rest()
                                explain("Then...")
                                wait()
                                if success:
                                    explain("You slam his arm onto the table!")
                                    rest()
                                    explain("The tavern erupts into joyful shouts as you take down the challenger.")
                                    rest()
                                    talk("Challenger", "Blood of my fathers! You're strong. Stronger than you look. Congrats dude.")
                                    rest()
                                    explain("He quickly hands you a couple coins, then runs out of the tavern without saying another word.")
                                    rest()
                                    update_gold(2)
                                    rest()
                                elif not success:
                                    explain("He slams your arm onto the table!")
                                    rest()
                                    talk("Challenger", "Well, you gave me a run for my money. I wasn't expecting to have to try that hard. Good job.")
                                    rest()
                                    explain("He gets up and leaves.")
                                    rest()
                                
                            if arm_wrestling == 2:
                                talk("Challenger", "Pathetic.")
                                rest()
                                explain("He gets up and walks out of the tavern.")
                                rest()

                            clear_character()

                        # Inspect the hearth
                        if tavern_action == 6:
                            while True:
                                
                                run_once("approach the hearth", lambda: explain("As you approach the roaring hearth, something seems odd about the symbols around the base."))
                                rest()
                                inspect_hearth = dialogue("What do you do?", [
                                    once("translate the symbols", opt(f"Attempt to translate the symbols. [{chance("int", 13, "history")} chance of success]", 1)),
                                    once("infuse the symbols", opt(f"[Wizard] Attempt to infuse the symbols with your magic. [{chance("int", 12, "arcana")} chance of success]", 2, classes="Wizard")),
                                    opt("Go back.", 3)
                                ])
                                rest()
                                
                                if inspect_hearth == 1:
                                    flag("translate the symbols")
                                    if not PLAYER_CLASS == "Wizard":
                                        flag("inspect the hearth")
                                    translate = check("int", 13, "history")
                                    if translate:
                                        check_success()
                                        rest()
                                        explain("You flip through some of your books, and eventually find some information on these symbols.")
                                        rest()
                                        explain('They seem to be words written in an ancient dwarven script. Translated, they say "The first step to filling the hearts of men is to first fill their stomachs."')
                                        wait()
                                        explain("This seems to suggest that Hearthstone used to be a dwarven village, though few of its residents are dwarves nowadays.")
                                    elif not translate:
                                        check_failure()
                                        rest()
                                        explain("You try to translate the symbols, but are unable to find the right dictionary.")
                                        wait()
                                        explain("However, you get the sense that this is some ancient form of the dwarvish script.")
                                        rest()
                                if inspect_hearth == 2:
                                    flag("inspect the hearth")
                                    flag("infuse the symbols")
                                    infusing = check("int", 12, "arcana")
                                    if infusing:
                                        check_success()
                                        rest()
                                        explain("You reach towards the symbols with your arcane power and, surprisingly, find them ready to accept it.")
                                        rest()
                                        explain("Suddenly, all the light goes out in the tavern.")
                                        rest()
                                        explain("Then...")
                                        wait()
                                        explain("Everything comes alight in a burst of radiance from the hearth.")
                                        rest()
                                        show_character("barkeeper.png", "Barkeeper")
                                        talk("Barkeep", "Storms! What did you do? Was it with the runes around the hearth? I always wondered...")
                                        rest()
                                        clear_character()
                                        explain("Everyone starts muttering as you look into the hearth and see an enormous pot. Coming from it is the most glorious smelling stew one could imagine.")
                                        wait()
                                        show_character("barkeeper.png", "Barkeeper")
                                        talk("Barkeep", "Well everyone, this stew isn't going to eat itself. Have at it!")
                                        rest()
                                        clear_character()
                                        explain("Immediately people start lining up to fill their empty ale mugs with stew.")
                                        wait()
                                        explain("Ten minutes later the atmosphere of the room has completely changed. Everyone is participating in hearty, light-hearted conversation.")
                                        rest()
                                        explain("You try some of the stew, and you've never had something simultaneously so appalling and delicious. It seems that however this stew was made, it has a little bit of everything in it.")
                                        wait()
                                        explain("Everything seems perfect, if only for a minute.")
                                        wait()
                                    elif not infusing:
                                        check_failure()
                                        rest()
                                        explain("You reach towards the symbols with your arcane power. You feel them reaching out, as if you're missing their hands by a few inches...")
                                        rest()
                                        explain("But alas, it doesn't connect. Nothing happens.")
                                        rest()
                                if inspect_hearth == 3:
                                    break
                        
                        # Sneak into a private room
                        if tavern_action == 7:
                            flag("sneak into a private room")
                            explain("You make your way to the back of the tavern.")
                            rest()
                            explain("You find a few locked doors, and hear muffled voices coming from one of them.")
                            rest()
                            while True:
                                
                                if STORY_FLAGS.get("done with the backrooms") == True:
                                    break
                                backrooms = dialogue("What do you do?", [
                                    once("try to eavesdrop", opt(f"Try to eavesdrop at one of the doors. [{chance("int", 10, "investigation")} chance of success]", 1)),
                                    once("try to pick the lock", opt(f"Try to pick the lock on the door. [{chance("dex", 12, "sleight of hand")} chance of success]", 2)),
                                    once("walk into the room", opt(f"Walk into the room.", 3, flag="picked the lock")),
                                    opt("Walk away before you're caught.", 4)

                                ])
                                rest()
                                

                                # Eavesdropping
                                if backrooms == 1:
                                    flag("try to eavesdrop")
                                    eavesdrop = check("int", 10, "investigation")
                                    if eavesdrop:
                                        check_success()
                                        rest()
                                        explain("You press your ear against the door and can just barely make out some words.")
                                        rest()
                                        talk("Muffled voices", "sold...dwarven...blueprints...goblins...")
                                        rest()
                                        explain("You can't make anything else out.")

                                    elif not eavesdrop:
                                        check_failure()
                                        rest()
                                        explain("You try to listen into the conversation through the door, but you just can't make out the words.")
                                
                                # Picking the lock
                                if backrooms == 2:
                                    flag("try to pick the lock")
                                    if PLAYER_CLASS == "Rogue":
                                        explain("You bring out your tools and begin working in the door.")
                                    elif PLAYER_CLASS == "Bard":
                                        explain("You pull out your lute and start strumming certain rhythms into the keyhole.")
                                    elif PLAYER_CLASS == "Warrior":
                                        explain("You grab your sword and jam it into the lock.")
                                    elif PLAYER_CLASS == "Wizard":
                                        explain("You fill the lock with magical energy, and attempt to force it open.")
                                    rest()
                                    pick_lock = check("dex", 12, "sleight of hand")
                                    if pick_lock:
                                        check_success()
                                        rest()
                                        if PLAYER_CLASS == "Rogue":
                                            explain("You maneuver the tools through the lock mechanism with expert precision.")
                                        elif PLAYER_CLASS == "Bard":
                                            explain("You hit the locks resonant frequency, and the lock starts rattling.")
                                        elif PLAYER_CLASS == "Warrior":
                                            explain("You maneuver your sword through the lock and, somehow, feel it pushing against the pins.")
                                        elif PLAYER_CLASS == "Wizard":
                                            explain("You feel the lock conforming to your magical will.")
                                        rest()
                                        explain("After about a minute you hear a small *click*.")
                                        rest()
                                        write("The door is now unlocked")
                                        flag("picked the lock")
                                    elif not pick_lock:
                                        check_failure()
                                        rest()
                                        if PLAYER_CLASS == "Rogue":
                                            explain("As you maneuver the tools through the lock mechanism, you get snagged on something you can't quite crack.")
                                        elif PLAYER_CLASS == "Bard":
                                            explain("You try to hit the right frequency to rattle the lock, but just can't get it right.")
                                        elif PLAYER_CLASS == "Warrior":
                                            explain("Unsurprisingly, your sword is unable to hit the pins in the lock.")
                                        elif PLAYER_CLASS == "Wizard":
                                            explain("The lock starts smoking for a second, then rejects your magic.")
                                        rest()

                                # Walk into the room
                                if backrooms == 3:
                                    explain("You open the door to the private room. You see 3 people huddled around a small table, who all jump when you enter.")
                                    rest()
                                    explain('"What are you doing?" they shout as they reach for their weapons.')
                                    rest()
                                    response_to_private_room = dialogue("How do you respond?", [
                                        opt(f"Act like you walked into the wrong room and leave. [{chance("cha", 15, "deception")} chance of success]", 1),
                                        opt(f"Run away and hide before they memorize your face. [{chance("dex", 15, "stealth")} chance of success]", 2),
                                        opt(f"Question them about what you heard.", 3),
                                        opt(f"Fight them.", 4)
                                    ])
                                    rest()
                                    
                                    
                                    if response_to_private_room == 1:
                                        deception_check = check("cha", 15, "deception")
                                        if deception_check:
                                            check_success()
                                            rest()
                                            explain("They seem suspicious, but accept your lie.")
                                            rest()
                                            explain("Your turn around, and walk back to the main lobby.")
                                            flag("done with the backrooms")
                                            rest()

                                        elif not deception_check:
                                            write("You failed the check")
                                            rest()
                                            show_character("assassin.png", "Shady Figure")
                                            talk("Shady Figure", "Yeah right.")
                                            rest()
                                            clear_character()
                                            explain("They rush towards you.")
                                            response_to_private_room = 4

                                    if response_to_private_room == 2:
                                        stealth_check = check("dex", 15, "stealth")
                                        if stealth_check:
                                            check_success()
                                            rest()
                                            explain("You bolt back into the main lobby before they get a good look at you.")
                                            rest()
                                            explain("They run after you, but once they get to the lobby, they turn back, unable to pick you out from the crowd.")
                                            flag("done with the backrooms")
                                            rest()
                                            break

                                        elif not stealth_check:
                                            write("You failed the check")
                                            rest()
                                            show_character("assassin.png", "Shady Figure")
                                            talk("Shady Figure", "Oh no you don't!")
                                            rest()
                                            clear_character()
                                            explain("You try to run, but one of them catches your hand and drags you back into the room.")
                                            rest()
                                            explain("The others rush towards you with their weapons, ready to fight.")
                                            rest()
                                            response_to_private_room = 4

                                    if response_to_private_room == 3:
                                        show_character("assassin.png", "Shady Figure")
                                        talk("Shady Figure", "And why should we listen to you?")
                                        rest()
                                        persuade_backrooms = dialogue("How do you respond?", [
                                            opt(f"Intimidate them into giving answers. [{chance("cha", 15, "intimidation")} chance of success]", 1),
                                            opt(f"Persuade them that you mean no harm. [{chance("cha", 15, "persuasion")} chance of success]", 2),
                                        ])
                                        rest()
                                        
                                        
                                        if persuade_backrooms == 1:
                                            intimidate = check("cha", 15, "intimidation")
                                            if intimidate:
                                                check_success()
                                                rest()
                                                explain("They all back down, scared of you.")
                                                rest()
                                                talk("Shady Figure", "Okay okay, don't hurt us. What do you want to know?")
                                                rest()
                                                persuade_backrooms = 3
                                            elif not intimidate:
                                                check_failure()
                                                rest()
                                                talk("Shady Figure", "Yeah, okay buddy.")
                                                rest()
                                                explain("The figures rush towards you with their weapons.")
                                                rest()
                                                clear_character()
                                                response_to_private_room = 4

                                        if persuade_backrooms == 2:
                                            persuade = check("cha", 15, "persuasion")
                                            if persuade:
                                                check_success()
                                                rest()
                                                explain("They lower their weapons.")
                                                rest()
                                                talk("Shady Figure", "Okay, what do you want to know?")
                                                rest()
                                                persuade_backrooms = 3
                                            elif not persuade:
                                                check_failure()
                                                rest()
                                                talk("Shady Figure", "Yeah, okay buddy.")
                                                rest()
                                                clear_character()
                                                explain("The figures rush towards you with their weapons.")
                                                rest()
                                                response_to_private_room = 4

                                        if persuade_backrooms == 3:
                                            while True:
                                                
                                                talk_with_backroom = dialogue("What do you ask them?", [
                                                    once("backrooms question 1", opt("What are you doing here?", 1)),
                                                    once("backrooms question 2", opt("What do you know about the goblins?", 2)),
                                                    opt("Leave the room.", 3)

                                                ])
                                                rest()
                                                

                                                if talk_with_backroom == 1:
                                                    flag("backrooms question 1")
                                                    talk("Shady Figure", "Nothing important, we're just travelers stopping in for the night. We don't like the noise of the lobby and got a private room. Nothing nefarious, I swear.")
                                                    rest()

                                                if talk_with_backroom == 2:
                                                    flag("backrooms question 2")
                                                    talk("Shady Figure", "Nothing much...")
                                                    rest()
                                                    explain("They all share a glance with each other.")
                                                    wait()
                                                    talk("Shady Figure", "Well, there is something. We got ambushed by those buggers on our way into town. We took them out, and found a letter on one of them. It looks like some sort of trade they were making with someone for old dwarven siege engine schematics.")
                                                    wait()
                                                    talk("Shady Figure", "That's all we know, I swear.")
                                                    rest()
                                                    

                                                if talk_with_backroom == 3:
                                                    clear_character()
                                                    explain("You walk away from the private rooms, and back into the lobby.")
                                                    rest()
                                                    flag("done with the backrooms")
                                                    break
                                            clear_character()
                                                    
                                    if response_to_private_room == 4:
                                        clear_character()
                                        while True:
                                            
                                            win = run_combat([("guard", True, 3, "Shady Figure")])
                                            if win:
                                                write("You won the battle.")
                                                music(village=True)
                                                break
                                            elif not win:
                                                death_message()
                                                continue
                                            explain("The room becomes silent as the last figure is slain.")
                                            rest()
                                        while True:
                                            
                                            after_killing_private_room = dialogue("What do you do now?", [
                                                once("inspecting the room", opt("Inspect the room.", 1)),
                                                opt("Flee the scene.", 2)
                                            ])
                                            rest()
                                            
                                            
                                            if after_killing_private_room == 1:
                                                flag("inspecting the room")
                                                explain("You look around the room, but nothing seems unusual.")
                                                rest()
                                                explain("However, you do find some letters on one of the bodies that talks about goblins buying some old dwarven siege engine schematics.")
                                                rest()
                                            
                                            if after_killing_private_room == 2:
                                                flag("done with the backrooms")
                                                explain("You leave the room, lock the door, and walk away.")
                                                rest()
                                                break



                                
                                # leave
                                if backrooms == 4:
                                    explain("You walk away from the private rooms and back into the main lobby before anyone starts getting suspicious.")
                                    break

                        # Perform for the tavern
                        if tavern_action == 8:
                            flag("perform for the tavern")

                            explain("You climb up on a stool and pull out your lute.")
                            rest()
                            explain("Heads start turning.") 
                            rest()
                            explain("All becomes silent...")
                            rest()
                            explain("They look at you, expectant...")
                            rest()
                            music_performance = dialogue("What do you play for the crowd?", [
                                opt(f"A sad song to remember what was lost. [{chance("cha", 12, "performance")} chance of success]", 1),
                                opt(f"A sweet melody to lighten the mood. [{chance("cha", 13, "performance")} chance of success]", 2),
                                opt(f"A motivational tune to encourage and inspire. [{chance("cha", 14, "performance")} chance of success]", 3),
                                opt(f"An epic ballad to give confidence. [{chance("cha", 15, "performance")} chance of success]", 4)
                            ])
                            rest()
                            

                            if music_performance == 1:
                                perform = check("cha", 12, "performance")
                                if perform:
                                    check_success()
                                    rest()
                                    explain("You strum up a slow, nostalgic song.")
                                    wait()
                                    explain("People start quietly humming to the melody as you continue.")
                                    wait()
                                    explain("The people start silently weeping as the song reaches its climax.")
                                    wait()
                                    explain("You reach the end of your song.")
                                    wait()
                                    explain("There's a quiet outbreak of clapping, then silence.")
                                    rest()
                                    explain("You feel saddened, but accepting. You are ready to take on whatever is thrown at you.")
                                    rest()
                                    write("You are now harder to hit!")
                                    update_ac(1)

                                elif not perform:
                                    check_failure()
                                    rest()
                                    explain("As you attempt to string up a tune, you suddenly forget the notes. You try to improvise the song...")
                                    wait()
                                    explain("But you just can't get it right.")
                                    rest()
                                    explain("People start turning back to their activities with a sigh...")
                                    wait()
                            if music_performance == 2:
                                perform = check("cha", 13, "performance")
                                if perform:
                                    check_success()
                                    rest()
                                    explain("You start playing a vibrant, happy tune.")
                                    wait()
                                    explain("More and more people start singing along to your melody.")
                                    wait()
                                    explain("People start dancing along as the song reaches its climax.")
                                    wait()
                                    explain("You reach the end of your song.")
                                    wait()
                                    explain("Everyone gets up and claps.")
                                    rest()
                                    explain("You feel happy, despite the dreary mood in the tavern earlier. You are filled full of life.")
                                    rest()
                                    write("You now have more health points!")
                                    update_hp(5)

                                elif not perform:
                                    check_failure()
                                    rest()
                                    explain("As you attempt to string up a tune, you suddenly forget the notes. You try to improvise the song...")
                                    wait()
                                    explain("But you just can't get it right.")
                                    rest()
                                    explain("People start turning back to their activities with a sigh...")
                                    wait()
                            if music_performance == 3:
                                perform = check("cha", 14, "performance")
                                if perform:
                                    check_success()
                                    rest()
                                    explain("You start playing a motivational, inspiring tune.")
                                    wait()
                                    explain("More and more people start standing up and dancing to your melody.")
                                    wait()
                                    explain("Almost everyone in the tavern is dancing along as the song reaches its climax.")
                                    wait()
                                    explain("You reach the end of your song.")
                                    wait()
                                    explain("Everyone starts clapping loudly.")
                                    rest()
                                    explain("You feel inspired. You can do anything you set your mind to.")
                                    rest()
                                    write("You now have a higher chance to land your attacks!")
                                    update_attack_bonus(1)
                                elif not perform:
                                    check_failure()
                                    rest()
                                    explain("As you attempt to string up a tune, you suddenly forget the notes. You try to improvise the song...")
                                    wait()
                                    explain("But you just can't get it right.")
                                    rest()
                                    explain("People start turning back to their activities with a sigh...")
                                    wait()
                            if music_performance == 4:
                                perform = check("cha", 15, "performance")
                                if perform:
                                    check_success()
                                    rest()
                                    explain("You strum up an epic, fulfilling ballad.")
                                    wait()
                                    explain("People start clapping along as you continue.")
                                    wait()
                                    explain("The people start line dancing and shouting for joy as the song reaches its climax.")
                                    wait()
                                    explain("You reach the end of your song.")
                                    wait()
                                    explain("There's an outburst of clapping and joyous shouts.")
                                    rest()
                                    explain("You feel empowered. You are ready to defeat all who stand in your way.")
                                    rest()
                                    write("You now deal more damage with your attacks!")
                                    update_damage_bonus(1)
                                elif not perform:
                                    check_failure()
                                    rest()
                                    explain("As you attempt to string up a tune, you suddenly forget the notes. You try to improvise the song...")
                                    wait()
                                    explain("But you just can't get it right.")
                                    rest()
                                    explain("People start turning back to their activities with a sigh...")
                                    wait()

                        # Leave the tavern
                        if tavern_action == 9:
                            rest()
                            break                
                
                # Guards
                if exploring_hearthstone == 2:
                    flag("talk to the guards")
                    explain("As you approach the Hearthstone barracks, you see a rough training yard near the town's edge; just some straw dummies, wooden weapons, and nervous villagers pretending they know how to fight. A weary village guard is barking instructions.")
                    wait()
                    explain("The guard turns to you.")
                    rest()
                    show_character("trainer.png", "Trainer")
                    talk("Trainer", "You look like you know how to swing steel. These folks could use a real lesson. Want to lend a hand?")
                    rest()
                    while True:
                        training_the_guards = dialogue("What do you do?", [
                            once("training 1", opt(f"Teach them a new attack pattern.", 1)),
                            once("training 2", opt("Spar with the best fighter.", 2)),
                            opt("Ask the trainer questions.", 3),
                            opt("Go back.", 4)                        

                        ])
                        rest()
                        clear_character()

                        if training_the_guards == 1:
                                flag("training 1")
                                explain("You rally up the recruits and show them an attack pattern with the spear.")
                                rest()
                                explain("You show them how to stand, how to hold their spears, how to walk, and how to fight.")
                                wait()
                                explain("After an hour or two the group is able to replicate the pattern on their own, without you.")
                                wait()
                                explain("You watch as they rush forward in unison, everyone moving with precision and intent, spear raised and ready to strike any goblin that stands in their way.")
                                wait()
                                explain("They all start cheering.")
                                rest()
                                show_character("trainer.png", "Trainer")
                                talk("Trainer", f"Wow. I didn't think this lot would ever be able to do that. You must be a storming good warrior. And teacher, for that matter.")
                                rest()
                                clear_character()

                        if training_the_guards == 2:
                            flag("training 2")
                            show_character("trainer.png", "Trainer")
                            talk("Trainer", "Well, this will be interesting.")
                            rest()
                            clear_character()
                            explain('After briefly fighting over who was considered the "best", a tall, stalky man walks up to you, spear in hand.')
                            rest()
                            show_character("warrior.png", "Wayne")
                            talk("Wayne", f"Hello {PLAYER_NAME}, I'm Wayne. I probably won't be able to defeat you, but this will be fun!")
                            rest()
                            clear_character()
                            explain("You both get in position, staring at each other...")
                            rest()
                            explain("Then...")
                            rest()
                            explain("You both rush forward!")
                            rest()
                            defeat_recruit = run_combat([("warrior", True, 1, "Wayne")], death=False)
                            
                            if defeat_recruit:
                                music(village=True)
                                write("You won the fight!")
                                rest()
                                show_character("warrior.png", "Wayne")
                                talk("Wayne", "Well, I didn't think I could beat you anyway. Good game though!")
                                wait()
                                clear_character()
                                
                            elif not defeat_recruit:
                                write("Wayne has defeated you in battle.")
                                rest()
                                show_character("warrior.png", )
                                talk("Wayne", "Wow, I actually beat you. I didn't think that was possible. Thanks for the practice!")
                                rest()
                                clear_character()
                            
                            show_character("trainer.png", "Trainer")
                            talk("Trainer", "Thanks for the display. Seeing a warrior's expertise in action ought to inspire them to train harder. ")
                            rest()
                            explain("You feel confident and inspired after the training session.")
                            rest()
                            write("Your attacks now deal more damage!")
                            update_damage_bonus(1)
                            unlock("wayne")

                        if training_the_guards == 3:
                            show_character("trainer.png", "Trainer")
                            talk("Trainer", "Is there anything I can help you with?")
                            rest()
                            while True:
                                talk_with_trainer = dialogue("What do you want to say to the trainer?", [
                                    once("trainer dialogue 1", opt("Ask about the strength of the guard.", 1)),
                                    once("trainer dialogue 2", opt("Ask if he knows anything new about the goblins.", 2)),
                                    opt("Go back.", 3)
                                ])
                                rest()
                                

                                if talk_with_trainer == 1:
                                    flag("trainer dialogue 1")
                                    talk("Trainer", "To be frank, we aren't doing super well at the moment.")
                                    rest()
                                    talk("Trainer", "We don't have more than a dozen or two guards, and our current attempts at training aren't working as well as we had hoped...")
                                    wait()
                                    explain("He glances over at the group of recruits before continuing.")
                                    rest()
                                    talk("Trainer", "They are improving, but it will be a while before they are ready for actual battle. And we know nothing about the goblin's strategy. They could strike any storming minute.")
                                    wait()

                                if talk_with_trainer == 2:
                                    flag("trainer dialogue 2")
                                    talk("Trainer", "I don't know much. Only that these goblins mean business. No one really knows why, because we never angered them, as far as we know. But they are here for something.")
                                    wait()
                                    talk("Trainer", "They must have some sort of agenda. Only if we could figure it out...")
                                    wait()


                                if talk_with_trainer == 3:
                                    talk("Trainer", "Well, thanks for coming out. It was nice to see an actual warrior for once.")
                                    rest()
                                    clear_character()
                                    break
                        if training_the_guards == 4:
                            rest()
                            clear_character()
                            break

                # Scouting the outskirts
                if exploring_hearthstone == 3:
                    explain("As the village focuses inward—fortifying doors, stacking crates, and preparing defenses—you slip away to the outskirts.")
                    wait()
                    explain("The grass is undisturbed, the shadows deep. It's too quiet out here.")
                    rest()
                    explain("Just the way you like it.")
                    rest()
                    while True:
                        draw_background(village=True)
                        scouting_village = dialogue("What do you do?", [
                            once("scouting village 1", opt("Look for suspicious footprints.", 1)),
                            once("scouting village 2", opt("Climb to the top of a roof for recon.", 2)),
                            once("scouting village 3", opt("Watch for suspicious figures.", 3)),
                            opt("Return to the village.", 4)
                        ])

                        # Looking for footprints
                        if scouting_village == 1:
                            flag("scouting village 1")
                            explain("You crouch at the edge of the village near the muddy path where wagons come and go. Most tracks are human—boots, hooves, or cart wheels.")
                            rest()
                            explain("But you spot something odd near the tall grass...")
                            rest()
                            explain("Three-toed prints, deep at the heel, light at the toes. Goblin.")

                            follow_goblin_tracks = dialogue("What do you do?", [
                                opt("Follow the tracks.", 1),
                                opt("Turn back.", 2)
                            ])
                            rest()
                            

                            if follow_goblin_tracks == 1:
                                draw_background(forest=True)
                                explain("As you quietly follow the trail, slipping between trees and brush, the sounds of the village fade behind you.")
                                wait()
                                explain("The tracks grow fresher. A broken branch is still swaying gently, as if someone had passed just minutes before.")
                                wait()
                                explain("Ahead, in a shallow dip beneath a low ridge, you find a strange scene...")
                                wait()
                                explain("A crude circle of stones surrounds a half-eaten deer carcass.")
                                rest()
                                explain("Scattered feathers, trinkets made of bone and string, and a doll made from hay and goblin hair lie nearby.")
                                wait()
                                explain("Whatever happened here, it just proves how crazy the goblins have become.")
                                wait()
                                explain("You freeze as a sound snaps through the forest behind you.")
                                rest()
                                explain("A bird? A twig?")
                                rest()
                                explain("You sit in silence for a few minutes, heart pounding out of your chest. But nothing follows.")
                                wait()
                                explain("Still, you feel watched.")
                                wait()
                                explain("You take a quick mental note of the scene and head back the way you came, quiet as a breath.")
                                wait()
                                explain("When you return to the village, the world feels just a little more fragile. Like you've seen a crack in it.")
                                rest()

                            if follow_goblin_tracks == 2:
                                explain("You turn away before you get involved.")
                                rest()

                        # Climbing on a roof
                        if scouting_village == 2:
                            flag("scouting village 2")
                            explain("You scan the street, looking for the tallest building that isn't swarming with villagers.")
                            rest()
                            explain("You come across a storage barn with a slanted roof and a stack of crates nearby.")
                            rest()
                            explain("With a quick glance to make sure no one's watching too closely, you climb.")
                            rest()
                            explain("Your fingers grip the edges of weathered wood. A ledge here, a window frame there.")
                            rest()
                            explain("You hoist yourself up and settle into a crouch on the roof, surveying the landscape.")
                            wait()
                            explain("The forest stretches out in the distance. Birds flap lazily over the treetops. No goblins. No movement. Just wind and trees.")
                            wait()
                            explain("It's peaceful up here")
                            rest()
                            explain("Then...")
                            rest()
                            show_character("kid.png", "Tien")
                            talk("Stranger", "Hey, you spying too?")
                            rest()
                            explain("You look up and see a barefoot kid sitting on the roof, grinning.")
                            rest()
                            talk("Kid", "My name's Tien. Bet you can't beat me to the baker's chimney!")
                            rest()
                            clear_character()
                            explain("Before you can reply, he leaps off of the roof and starts running across the Hearthstone rooftops.")

                            chase_the_kid = dialogue("What do you do?", [
                                opt("Jump after him!", 1),
                                opt("Leave the kid. You have more important work.", 2)
                            ])
                            rest()
                            

                            if chase_the_kid == 1:
                                explain("You hesitate for a moment before grinning and chasing after him across the rooftops.")
                                wait()
                                explain("You leap across a narrow alley, landing with a soft thud on old shingles.")
                                rest()
                                explain("Tien is a step ahead of you, already moving onto the next roof.")
                                rest()
                                explain("A flock of pigeons bursts into the air, as if the kid was trying to distract you. You dash right through them.")
                                wait()
                                explain("You catch yourself on a wooden beam and swing up just in time to see Tien running for a chimney ahead of you.")
                                wait()
                                explain("This is the toughest challenge you've faced in a while. The kid's fast.")
                                wait()
                                explain("But you're faster.")
                                rest()
                                explain("You summon up strength from deep inside you. Then...")
                                rest()
                                explain("You leap into the air, soaring with unnatural grace.")
                                rest()
                                explain("You pass over Tien, just barely.")
                                rest()
                                explain("You both land atop the chimney, panting.")
                                rest()
                                show_character("kid.png", "Tien")
                                talk("Kid", "Okay, you win. That was a mighty fine leap back there. See you around.")
                                rest()
                                clear_character()
                                explain("Then he hops down and vanishes into the night.")
                                rest()
                                explain("You're left alone on the roof, wind tugging at your cloak, a smirk on your face.")
                                wait()
                                unlock("tien")

                            elif chase_the_kid == 2:
                                explain("You climb off the roof, and notice the kid looking back at you, disappointment on his face.")
                                rest()

                        # Watch for sus figures
                        if scouting_village == 3:
                            flag("scouting village 3")
                            explain("You blend into the bustle of the market square, hood up, hands in your pockets. You're not in the crowd. You're part of it. Watching.")
                            wait()
                            explain("At first, it's the usual village stuff. A farmer haggles over apples. A boy chases a chicken. Two elders argue about goats.")
                            wait()
                            explain("Then...")
                            rest()
                            explain("A hooded figure stands near the tavern. Not buying, not talking. Just… watching.")
                            wait()
                            explain("You notice they keep glancing toward the path out of town. The one leading to Grimglen Forest.")
                            wait()
                            
                            follow_sus_guy = dialogue("What do you do?", [
                                opt("Follow the suspicious figure.", 1),
                                opt("Turn back.", 2)
                            ])
                            rest()
                            

                            if follow_sus_guy == 1:
                                explain("You trail them from a distance, ducking between stalls and carts.")
                                rest()
                                explain("They make their way around the edge of the village and disappear into a small shed.")
                                rest()
                                explain("You wait a beat. Then peek inside, still hidden.")
                                rest()
                                explain("The shed is mostly empty, except for the two goblins conversing with the person you followed.")
                                rest()
                                show_character("goblin.png", "Goblin")
                                talk("Goblin", "Thank you for meeting, Iyatil. You know how much we need this.")
                                rest()
                                show_character("assassin.png", "Iyatil")
                                talk("Iyatil", "I have the schematics. Do you have the dagger we discussed?")
                                rest()
                                show_character("goblin.png", "Goblin")
                                talk("Goblin", "Yes, of course.")
                                rest()
                                clear_character()
                                explain("The goblins and the stranger, Iyatil, exchange. She gives them a stack of blueprints, and they give her a dagger.")
                                wait()
                                explain("The dagger is unlike anything you have ever seen. It shines with an ethereal light and shines as if it repelled dirt.")
                                wait()
                                explain("Then, as Iyatil inspects the dagger, you lock eyes with her reflection.")
                                rest()
                                show_character("assassin.png", "Iyatil")
                                talk("Iyatil", "Thank you spy. I was hoping to test out this new dagger.")
                                rest()
                                clear_character()
                                explain("She turns around, dagger in hand, and rushes towards you, goblins scrambling to follow behind.")
                                wait()
                                while True:
                                    defeat_shed_goblins = run_combat([("goblin", True, 2, None), ("assassin", True, 1, "Iyatil")])
                                    

                                    if defeat_shed_goblins:
                                        music(village=True)
                                        write("You won the battle!")
                                        break
                                    elif not defeat_shed_goblins:
                                        death_message()
                                        continue
                                wait()
                                what = dialogue("What do you do now?", [
                                    once("after killing shed goblins", opt("Search the bodies.", 1)), 
                                    opt("Leave the shed.", 2)
                                ])
                                rest()
                                

                                if what == 1:
                                    flag("after killing shed goblins")
                                    rest()
                                    explain("You look through the goblins, but they don't carry much other than some crude weapons and the schematics they just traded for.")
                                    wait()
                                    explain("The schematics seem to be for some sort of dwarven machine, but it's hard to tell what it's function is.")
                                    wait()
                                    explain("Iyatil also has little on her, except for her shiny new dagger.")
                                    rest()
                                    explain("You pick it up, and feel a sense of power washing over you.")
                                    rest()
                                    explain("You also feel a slight calling, as if the dagger was made for you.")
                                    wait()
                                    explain("You pocket the dagger.")
                                    rest()
                                    write("You now deal extra damage when attacking!")
                                    update_damage_bonus(1)
                                    wait()
                                    
                                if what == 2:
                                    explain("You leave, acting like nothing happened.")
                                    rest()
                            
                            elif follow_sus_guy == 2:
                                explain("You turn away before you get yourself into any more trouble.")
                                rest()

                        # Leaving
                        if scouting_village == 4:
                            explain("Done with your sneakery, you return to the village square.")
                            rest()
                            break
                
                # Check out the play
                if exploring_hearthstone == 4:
                    flag("check out the play")
                    explain("In the village square, a small wooden stage is being set up. There's a colorful banner reading:")
                    rest()
                    explain("The Hearthstone Spectacle Presents: The Goblin and the Goose")
                    rest()
                    explain("One of the actors, looking frantic and out of breath, comes up to you.")
                    rest()
                    show_character("tress.png", "Tress")
                    talk("Tress", "Hello, I'm Tress. You look like someone with presence. Our lead actor twisted his ankle trying to impress a barmaid, and the understudy's delivery makes turnips look expressive.")
                    rest()
                    talk("Tress", "I know this doesn't really seem like the right time for a play, but we feel like Hearthstone could use some cheering up.")
                    rest()
                    talk("Tress", "Please, could you step in? We're desperate!")
                    rest()
                    do_the_play = dialogue("What do you say?", [
                        opt("Join the play.", 1),
                        opt("Leave them. You have your own problems to deal with.", 2)
                    ])
                    rest()
                    

                    if do_the_play == 1:
                        talk("Tress", "Wonderful! Here is your script.")
                        rest()
                        clear_character()
                        explain("She hands you a stack of papers that form a makeshift script.")
                        rest()
                        explain("After looking through the script, you notice two things.")
                        rest()
                        explain("This is a comically poor written play.")
                        rest()
                        explain("And you're playing the goose.")
                        rest()
                        explain("This will be fun.")
                        wait()
                        explain("Tress throws you a makeshift goose costume.")
                        rest()
                        talk("Tress", "We're live in two minutes, so get this costume on and get those lines memorized!")
                        rest()
                        clear_character()
                        explain("You put on the itchy goose costume, then take a look at your lines.")
                        rest()
                        write("You have 15 seconds to memorize each line.")
                        wait()
                        write("Line 1: \"For though I may honk and waddle, I carry a secret most fowl...\"")
                        time.sleep(15)
                        write("Line 2: \"One egg for my freedom? Make it two and a scone!\"")
                        time.sleep(15)
                        write("line 3: \"A goblin's greed is only matched by his smell.\"")
                        time.sleep(15)
                        write("Line 4: \"GASP! My egg has been stolen!\"")
                        time.sleep(15)
                        write("Line 5: \"HONK HONK! Justice is served!\"")
                        time.sleep(15)               
                        show_character("tress.png", "Tress")
                        talk("Tress", f"Alright, show's on. Get up there {PLAYER_NAME}!")
                        wait()
                        clear_character()
                        explain("You follow her onto the stage.")
                        rest()
                        explain("As you come out from behind the curtains, you see a small crowd gathered in anticipation.")
                        rest()
                        explain("Tress appears from the other side of the stage, dressed in a horrible goblin costume.")
                        wait()
                        write("Tress will speak, and each time it's your turn, you're presented with three possible responses.")
                        rest()
                        write("Only one of the lines is the correct line (the one you memorized).")
                        rest()
                        write("Here we go!")
                        wait()


                        # Play scene

                        accuracy = 0
                        show_character("tress.png", "Tress")
                        # Line 1:
                        write("---Line 1---")
                        rest()
                        talk("Tress", "Goose! Why do you waddle so nervously?")
                        rest()
                        lines = [opt("For though I may honk and waddle, I carry a secret most fowl...", 1), 
                                opt("Because my feathers itch and I've lost my slippers.", 2), 
                                opt("I'm waiting for my cue, you overgrown toad.", 3)]
                        random.shuffle(lines)
                        line = dialogue("What do you say?", lines, False)
                        rest()
                        

                        if line == 1:
                            accuracy += 1

                        # Line 2:
                        write("---Line 2---")
                        rest()
                        talk("Tress", "I want that golden egg, bird. I'll give you a turnip and a handshake.")
                        rest()
                        lines = [opt("One egg for my freedom? Make it two and a scone!", 1), 
                                opt("You can't afford my yolk, goblin trash.", 2), 
                                opt("You drive a hard bargain. Deal.", 3)]
                        random.shuffle(lines)
                        line = dialogue("What do you say?", lines, False)
                        rest()
                        

                        if line == 1:
                            accuracy += 1
                                            
                        # Line 3:
                        write("---Line 3---")
                        rest()
                        talk("Tress", "You think you're better than me, feather-brain?")
                        rest()
                        lines = [opt("A goblin's greed is only matched by his smell.", 1), 
                                opt("Says the guy wearing a fish on his head.", 2), 
                                opt("Better than you? No. Smellier? Definitely", 3)]
                        random.shuffle(lines)
                        line = dialogue("What do you say?", lines, False)
                        rest()
                        

                        if line == 1:
                            accuracy += 1

                        # Line 4:
                        write("---Line 4---")
                        rest()
                        explain("Goblin sneaks around and steals your prop egg.")
                        rest()
                        lines = [opt("GASP! My egg has been stolen!", 1), 
                                opt("My goose egg! Nooo!", 2), 
                                opt("That's it! Time for the final honk!", 3)]
                        random.shuffle(lines)
                        line = dialogue("What do you say?", lines, False)
                        rest()
                        

                        if line == 1:
                            accuracy += 1

                        # Line 5:
                        write("---Line 5---")
                        rest()
                        explain("Goblin trips, you stand tall.")
                        rest()
                        lines = [opt("HONK HONK! Justice is served!", 1), 
                                opt("That's what you get for yolk crimes.", 2), 
                                opt("Your curtain has fallen, goblin.", 3)]
                        random.shuffle(lines)
                        line = dialogue("What do you say?", lines, False)
                        rest()
                        clear_character()

                        if line == 1:
                            accuracy += 1
                        
                        write("---END OF THE PLAY---")
                        rest()
                        write(f"You said {accuracy} lines correctly.")
                        rest()

                        if accuracy == 5:
                            explain("As you stand there, basking in the heat of the moment, the crowd stands up and cheers.")
                            rest()
                            explain("Tears form in Tress' eyes as she walks up to you.")
                            rest()
                            show_character("tress.png", "Tress")
                            talk("Tress", "That was perfect. You really are talented.")
                            rest()
                            talk("Tress", "Thank you so much for your help! That would have been a train wreck without you.")
                            rest()
                            talk("Tress", "Here, take these coins. It's not much, but it's the least I can do after a performance like that.")
                            rest()
                            update_gold(3)
                        
                        if accuracy == 3 or accuracy == 4:
                            explain("You stand there proud. The audience warmly applauds you for your performance.")
                            rest()
                            show_character("tress.png", "Tress")
                            talk("Tress", "That was wonderful. Nearly perfect. You did really well.")
                            rest()
                            talk("Tress", "Thank you so much for your help!")
                            rest()
                            talk("Tress", "Here's some coin for your trouble.")
                            rest()
                            update_gold(2)

                        if accuracy == 1 or accuracy == 2:
                            explain("A few people in the crowd awkwardly clap.")
                            rest()
                            show_character("tress.png", "Tress")
                            talk("Tress", "Well, that was something. Thanks for trying.")

                        if accuracy == 0:
                            explain("The crowd is completely silent.")
                            rest()
                            explain("Except for a small child, who is crying.")
                            rest()
                            show_character("tress.png", "Tress")
                            talk("Tress", "Wow. That was a train wreck.")
                            rest()
                            talk("Tress", "I knew we shouldn't have done the play...")
                        
                        clear_character()
                        explain("As the crowd disperses, you feel warmth growing inside of you.")
                        rest()
                        explain("It feels nice to pretend, even if it was just for a few moments.")
                        wait()
                        unlock("tress")

                    elif do_the_play == 2:
                        explain("Tress storms off without saying another word.")
                        clear_character()
                        wait()
                    
                # Wizard Duel
                if exploring_hearthstone == 5:
                    if STORY_FLAGS.get("meeting hoid dialogue"):
                        show_character("hoid.png", "Hoid")
                        talk("Hoid", f"Back for more, {PLAYER_NAME}?")

                    run_once("meeting hoid dialogue", 
                        lambda: explain("You start wandering Hearthstone, looking for another wizard to talk to."),
                        lambda: rest(),
                        lambda: explain("It's not long before you spot a crowd gathering near a makeshift stage where a flamboyantly dressed traveling magician is dazzling villagers."),
                        lambda: wait(),
                        lambda: explain("He spots you and dramatically bows."),
                        lambda: rest(),
                        lambda: show_character("hoid.png", "Hoid"),
                        lambda: talk("Magician", "Ah, do my ever-waning eyes deceive me, or is that a wizard I see?"),
                        lambda: rest(),
                        lambda: talk("Magician", "Come, good wizard, and test your might in a duel of mystic magnificence! See if you can best the legendary Hoid!"),
                        lambda: rest()
                        )
                    

                    participate = dialogue("What do you say?", [
                        opt("Accept his challenge.", 1),
                        opt("Decline. You have more important matters to attend to.", 2)
                    ])
                    rest()
                    

                    if participate == 1:
                        talk("Hoid", "Splendid! Get up on the stage, and we shall begin!"),
                        wait(),
                        run_once("accepting hoid's offer",
                            lambda: write("You will be presented with 5 different spells to cast. Each spell loses to two other spells, and beats two others."),
                            lambda: rest(),
                            lambda: write("You will both cast spells against each other to see who wins."),
                            lambda: rest(),
                            lambda: write("This is magical rock, paper, scissors."),
                            lambda: rest()
                            )
                            
                        
                        write("The game begins!")
                        show_character("hoid.png", "Hoid")
                        win = magical_duel_game("Hoid")
                        unlock("hoid")
                        music(village=True)

                        if win:
                            write("You won!")
                            rest()
                            talk("Hoid", "Bravo! You truly are a wizard of wonder. The crowd is yours!")
                            rest()
                            
                            run_once("hoid's reward", 
                                lambda: talk("Hoid", "Well, you deserve something after that spectacular show!"),
                                lambda: rest(),
                                lambda: explain("He hands you a peculiar flute that's made from a wood you've never seen before."),
                                lambda: rest(),
                                lambda: talk("Hoid", "Take care of that little bugger. It may not seem like much, but I promise it makes you better at magic."),
                                lambda: rest(),
                                lambda: update_damage_bonus(1),
                                lambda: write("Your fireballs now deal more damage."),
                                lambda: rest()
                                )

                            talk("Hoid", "Please, come back anytime for a rematch.")

                        elif not win:
                            write("You lost")
                            rest()
                            talk("Hoid", "A valiant performance! Come back anytime for a rematch.")
                            rest()
                        
                        clear_character()

                    elif participate == 2:
                        talk("Hoid", "That's rather unfortunate. Perhaps another time, then.")
                        rest()
                        clear_character()

                # Going back
                if exploring_hearthstone == 6:
                    break

            # Setting out for grimglen hollow
            if prep_before_leaving == 3:
                certainty = dialogue("Are you sure you are ready to leave? You will not be able to return.", [
                    opt("Yes. I am done exploring the village and would like to continue the adventure.", 1),
                    opt("No.", 2)
                    ])
                rest()
                
                if certainty == 1:
                    flag("moving to act 2")
                    break
                else:
                    break

# INPUT: None
# RETURN: None
# PURPOSE: To run act 2 of the game
def act_2():
    music(explore=True)
    draw_background(forest=True)

    # Premise
    if True:    
        write("Act 2: To Walk", delay=75)
        wait()
        
        explain("You leave the village behind, the sounds of daily life fading as you follow the dirt path into the woods.")
        wait()
        explain("Sunlight filters through the trees, casting shifting patterns on the ground. Wildflowers and tall grass brush your boots as you walk.")
        wait()
        explain("The forest thickens. Birds call overhead, but something about the silence between their songs puts you on edge.")
        wait()
        explain("A twig snaps in the distance. You're not alone out here.")
        wait()
        explain("Somewhere ahead is Grimglen Hollow. And beyond that... the goblins.")

    # Main loop for Act 2
    encounters = ["tracks", "trap", "tea", "bear", "pool", "goblins"]
    while True:
        music(explore=True)
        draw_background(forest=True)
        

        if encounters == []:
            wait()
            explain("You continue on the path to Grimglen Hollow for a couple hours.")
            rest()
            explain("Then...")
            rest()
            explain("You finally reach it.")
            wait() 
            break
        elif not encounters == []:
            current_encounter = random.choice(encounters)
            encounters.remove(current_encounter)
        
            explain("You continue on the path to Grimglen Hollow for a couple hours.")
            rest()
            explain("Then...")
            rest()

            # Owlbear tracks
            if current_encounter == "tracks":
                explain("As you push past a thick cluster of brambles, your boot catches something in the earth. Not quite a trap, just a set of tracks.")
                rest()
                explain("But these aren't goblin prints. They're broad, heavy, and slightly avian… claws like a bird, but the depth and shape are all wrong.")
                rest()
                explain("The tracks lead off the main path into a denser patch of forest.")
                
                while True:
                    follow = dialogue("What do you do?", [
                        opt("Follow the tracks into the forest.", 1),
                        once("inspect owlbear tracks", opt(f"Inspect the tracks more closely. [{chance("int", 12, "nature")} chance of success]", 2)),
                        opt("Ignore the tracks and keep going.", 3)
                    ])

                    # Follow the tracks
                    if follow == 1:
                        explain("You go off the path into the forest.")
                        rest()
                        explain("The air feels heavier here—damp with moss and silence.")
                        rest()
                        explain("You hear nothing but the faint rustling of wind in the trees… and something else. A soft, rhythmic grunt. Breathing.")
                        rest()
                        explain("Following the trail, you press between two thick tree trunks and find yourself in a small clearing.")
                        rest()
                        explain("Curled beside a hollow stump is a creature you didn't expect to see this close to the village:")
                        rest()
                        explain("An owlbear cub.")
                        rest()
                        explain("Its feathery coat is matted with leaves and dirt, and its wide, golden eyes lock onto yours immediately.")
                        rest()
                        explain("It lets out a low, warbling growl. Not quite a roar, but enough to show its beak and claws.")
                        rest()
                        explain("You're close enough to see that one of its back legs is scraped raw. It's not seriously hurt, but it might not be able to flee.")
                        rest()
                        explain("It's trembling… scared, but willing to fight if it has to.")
                        rest()

                        if PLAYER_INVENTORY.get("food rations"):
                            flag("has rations")
                        owlbear_encounter = dialogue("What do you do?", [
                            opt(f"Approach gently and try to calm it down. [{chance("wis", 12, "animal handling")} chance of success]", 1),
                            opt("Offer it the food rations you bought from the merchant.", 2, flag="has rations"),
                            opt(f"[Bard] Play it a comforting song. [{chance("cha", 12, "performance")}]", 3, classes="Bard"),
                            opt("Fight it off.", 4),
                            opt("Walk away before it attacks you.", 5)
                        ])
                        rest()
                        

                        # Calm the owlbear down
                        if owlbear_encounter == 1:
                            animal_handling = check("wis", 12, "animal handling")

                            if animal_handling:
                                check_success()
                                rest()
                                explain("You crouch low and offer a hand.")
                                rest()
                                explain("The owlbear watches you with intense, blinking eyes. Its muscles are still taut, but its growl softens into a questioning trill.")
                                rest()
                                explain("It carefully sniffs your hand.")
                                rest()
                                explain("Then, with a soft hoot, it flops beside you, letting out a small sigh.")
                                rest()
                                explain("It doesn't speak, of course. But its eyes are full of meaning.")
                                rest()
                                explain("From now on, it seems, you're not walking the path alone.")
                                wait()
                                while True:
                                    global owlbear_name
                                    owlbear_name = get_input("What do you want to call the owlbear cub?")
                                    if owlbear_name == "":
                                            write(f"The owlbear cub needs some sort of name, don't name it nothing.")
                                            rest()
                                            continue
                                    else:
                                        write(f"The owlbear cub's name is now {owlbear_name}")
                                        rest()
                                        write(f"{owlbear_name} will now follow you and fight with you.")
                                        rest()
                                        break
                                unlock("owlbear")
                                friend("owlbear cub", owlbear_name)
                                break

                            elif not animal_handling:
                                check_failure()
                                rest()
                                explain("You make a move, but you're too fast and too loud. The cub shrieks and lunges.")
                                rest()
                                explain("Claws rake your arm as you stagger back. It's scared, not cruel. But fear makes it dangerous.")
                                rest()
                                explain("No time to calm it now. You'll have to defend yourself.")
                                owlbear_encounter = 5

                        # Feed the owlbear
                        if owlbear_encounter == 2:
                            PLAYER_INVENTORY.pop("food rations", None)
                            explain("You crouch low and offer some food.")
                            rest()
                            explain("The owlbear watches you with intense, blinking eyes. Its muscles are still taut, but its growl softens into a questioning trill.")
                            rest()
                            explain("It carefully sniffs your hand, then eats the food.")
                            rest()
                            explain("Then, with a soft hoot, it flops beside you, letting out a small sigh.")
                            rest()
                            explain("It doesn't speak, of course. But its eyes are full of meaning.")
                            rest()
                            explain("From now on, it seems, you're not walking the path alone.")
                            wait()

                            while True:
                                
                                owlbear_name = input("What do you want to call the owlbear cub? ")
                                if owlbear_name == "":
                                        write(f"The owlbear cub needs some sort of name, don't name it nothing.")
                                        rest()
                                        continue
                                else:
                                    write(f"The owlbear cub's name is now {owlbear_name}")
                                    rest()
                                    write(f"{owlbear_name} will now follow you and fight with you.")
                                    rest()
                                    break
                            friend("owlbear cub", owlbear_name)
                            break                   
                            
                        # Play a song for the owlbear
                        if owlbear_encounter == 3:
                            performance_check = check("cha", 12, "performance")
                            if performance_check:
                                check_success()
                                rest()
                                explain("You pull out your lute and start playing a slow, friendly song.")
                                rest()
                                explain("The owlbear watches you with intense, blinking eyes. Its muscles are still taut, but its growl softens into a questioning trill.")
                                rest()
                                explain("As you continue playing, it slowly starts walking up to you.")
                                rest()
                                explain("Then, with a soft hoot, it flops beside you, letting out a small sigh.")
                                rest()
                                explain("It doesn't speak, of course. But its eyes are full of meaning.")
                                rest()
                                explain("From now on, it seems, you're not walking the path alone.")
                                wait()
                                while True:
                                    
                                    owlbear_name = input("What do you want to call the owlbear cub? ")
                                    if owlbear_name == "":
                                            write(f"The owlbear cub needs some sort of name, don't name it nothing.")
                                            rest()
                                            continue
                                    else:
                                        write(f"The owlbear cub's name is now {owlbear_name}")
                                        rest()
                                        write(f"{owlbear_name} will now follow you and fight with you.")
                                        rest()
                                        break
                                friend("owlbear cub", owlbear_name)
                                break

                            elif not performance_check:
                                check_failure()
                                rest()
                                explain("You pull out your lute and start to play, but the cub goes berserk at the noise. It shrieks and lunges at you.")
                                rest()
                                explain("Claws rake your arm as you stagger back. It's scared, not cruel. But fear makes it dangerous.")
                                rest()
                                explain("No time to calm it now. You'll have to defend yourself.")
                                owlbear_encounter = 5

                        # Fight the owlbear
                        if owlbear_encounter == 4:
                            explain("It charges forward, claws ready to strike.")
                            rest()
                            while True:
                                defeat_owlbear = run_combat([("owlbear cub", True, 1, None)])
                                
                                if defeat_owlbear:
                                    music(explore=True)
                                    explain("You have murdered the owlbear cub...")
                                    wait()
                                    break
                                if not defeat_owlbear:
                                    death_message()
                                    rest()
                                    continue
                            explain("You leave the clearing, and continue on the path to Grimglen Hollow.")
                            break
                        
                        # Walk away
                        if owlbear_encounter == 5:
                            explain("You back off before it has the chance to attack.")
                            rest()
                            break

                    # Inspect the tracks
                    elif follow == 2:
                        flag("inspect owlbear tracks")
                        nature_check = check("int", 12, "nature")
                        
                        if nature_check:
                            check_success()
                            rest()
                            explain("You lean down and take a closer look at the tracks.")
                            rest()
                            explain("You notice that, while this creature most certainly has talons, the tracks are far too big and padded to be a bird.")
                            rest()
                            explain("They look almost like bear paws...")
                            rest()
                            explain("But if they belong to a bear, then it must be a cub, because the tracks aren't much bigger than your hand.")
                            rest()
                            explain("Then it comes to you...")
                            rest()
                            explain("It must be an owlbear cub!")
                            rest()
                            explain("They're fearsome beasts with the size and body of a bear, but the head, claws, and feathers of an owl.")
                            rest()
                            explain("Most travelers would try to avoid one at all costs, but this one seems like a cub, all alone...")
                            rest()

                        
                        elif not nature_check:
                            check_failure()
                            rest()
                            explain("You lean down and take a closer look at the tracks, but are unable to determine what they belong to.")
                            rest()
                    
                    # Ignore the tracks
                    elif follow == 3:
                        explain("You continue on your way, hoping that whatever it was that made those tracks will stay far away from you.")
                        rest()
                        break

            # Goblin trap
            elif current_encounter == "trap":
                explain("As you walk along the path, something feels off.")
                rest()
                explain("There's an eerie silence. The usual sounds of the forest seem muted, and the air is heavy with tension.")
                rest()
                explain("Suddenly, you notice the faint outline of a tripwire hidden among the underbrush.")
                rest()
                explain("It's expertly camouflaged, but not enough to fool a trained eye. If you step on it, you're sure a trap will spring.")
                while True:
                    oh_no_its_a_trap = dialogue("What do you do?", [
                        once("forest trap option 2", opt(f"Look around to try and identify the trap. [{chance("wis", 12, "perception")} chance of success]", 1)),
                        once("forest trap option 3", opt(f"Try to disarm the trap. [{chance("dex", 13, "sleight of hand")} chance of success]", 2)),
                        opt("Step forward. You aren't afraid of a goblin trap.", 3)
                    ])
                    rest()
                    

                    # Identify the trap
                    if oh_no_its_a_trap == 1:
                        flag("forest trap option 2")
                        perception_check = check("wis", 11, "perception")
                        if perception_check:
                            check_success()
                            rest()
                            explain("You look around the area, and spot a large log poised to swing down, sharp spikes attached to it.")
                            rest()
                            explain("It's a crude but effective goblin mechanism, designed to crush anything that dares to approach.")
                            rest()
                        elif not perception_check:
                            check_failure()
                            rest()
                            explain("You look around the area, but are unable to figure out what the tripwire triggers.")
                            rest()
                    
                    # Disarm the trap
                    if oh_no_its_a_trap == 2:

                        disarm_trap = ("dex", 13, "sleight of hand")

                        if disarm_trap:
                            check_success()
                            rest()
                            if PLAYER_CLASS == "Bard":
                                explain("You keep playing your lute until you find its resonant frequency.")
                                rest()
                                explain("Then, you yank on the resonant connection to break the mechanism.")
                                rest()
                            elif PLAYER_CLASS == "Rogue":
                                explain("With your expert finesse, you carefully disarm the trap with your tools.")
                                rest()
                            elif PLAYER_CLASS == "Warrior":
                                explain("You slam your sword into the trap, and somehow it works. The mechanism breaks.")
                                rest()
                            elif PLAYER_CLASS == "Wizard":
                                explain("You use your magic to make a ethereal connection to the trap's mechanism.")
                                rest()
                                explain("Then, you yank on that connection to break the mechanism.")
                                rest()
                            write("The trap is disarmed.")
                            rest()
                            explain("The tripwire comes loose, and a string comes loose.")
                            rest()
                            explain("Then, a big log with spikes falls harmlessly to the ground.")
                            rest()
                            write("The path is now clear.")
                            rest()
                            break

                        elif not disarm_trap:
                            check_failure()
                            rest()
                            if PLAYER_CLASS == "Bard":
                                explain("You keep playing your lute, trying to find its resonant frequency.")
                                rest()
                                explain("But then you play a tone too harsh, and the trap triggers.")
                                rest()
                            elif PLAYER_CLASS == "Rogue":
                                explain("You attempt to use your tools to disarm the trap, but you accidentally tap part of the wire in the mechanism, and the trap triggers.")
                                rest()
                            elif PLAYER_CLASS == "Warrior":
                                explain("You slam your sword into the trap.")
                                rest()
                                explain("Unsurprisingly, this triggers the trap.")
                                rest()
                            elif PLAYER_CLASS == "Wizard":
                                explain("You use your magic to make a ethereal connection to the trap's mechanism.")
                                rest()
                                explain("But when you try to use that connection to break the mechanism, you're a little too harsh, and the trap triggers.")
                                rest()
                            oh_no_its_a_trap == 3

                    # Walk into the trap
                    if oh_no_its_a_trap == 3:
                        explain("A giant log covered in spikes swings from a tree, coming straight towards you.")
                        rest()
                        falling_log = dialogue("What do you do?", [
                            opt(f"Try to dodge out of the way. [{chance("dex", 16, "acrobatics")} success ]", 1),
                            opt(f"[Wizard] Try to cast a spell on the log before it hits you. [{chance("int", 16, "arcana")} of success]", 2, classes="Wizard"),
                            opt("Accept your fate and embrace the log.", 3)
                        ])
                        rest()
                        

                        if falling_log == 1:
                            dodge = check("dex", 17, "acrobatics")
                            if dodge:
                                check_success()
                                rest()
                                explain("As the log swings, you manage to roll to the side just in time.")
                                rest()
                            elif not dodge:
                                check_failure()
                                rest()
                                explain("You try to dodge the log, but it swings too fast.")
                                falling_log = 3

                        if falling_log == 2:
                            transform = check("int", 17, "arcana")
                            if transform:
                                check_success()
                                rest()
                                explain("As the log swings, you stand your ground, and cast a spell on the log.")
                                rest()
                                explain("Just before it hits you, it transforms into a puff of mist.")
                                rest()
                            elif not transform:
                                check_failure()
                                rest()
                                explain("You try to cast a spell on the log, but it swings too fast.")
                                rest()
                                falling_log = 3
                        
                        if falling_log == 3:
                            explain("The log collides into the side of your face, and everything goes dark...")
                            wait()
                            explain("You wake up a few hours later to a lot of pain in your side.")
                            rest()
                            explain("And to a group of goblins attempting to tie you up.")
                            rest()
                            show_character("goblin.png", "Goblin")
                            talk("Goblin", "Hey, they woke up! Attack!")
                            clear_character()
                            rest()
                            while True:
                                goblin_trap_ambush = run_combat([("goblin", True, 4, None)])
                                
                                if goblin_trap_ambush:
                                    music(explore=True)
                                    write("You defeated the goblins!")
                                    rest()
                                    explain("You take a moment to rest, then get going again.")
                                    break

                                elif not goblin_trap_ambush:
                                    death_message()
                                    rest()
                                    continue
                            break

            # Bubblenook            
            elif current_encounter == "tea":
                explain("As you travel through the woods, a sudden breeze carries the scent of warm cinnamon, honeybloom petals, and peppermint.")
                rest()
                explain("It's strange, yet inviting. Utterly out of place in this forest.")
                rest()
                explain("Ahead you see a porcelain teapot sitting atop a mossy tree stump.")
                rest()
                explain("There's no fire beneath it, yet steam curls from the spout.")
                rest()
                explain("The pot jiggles slightly, then a voice squeaks out.")
                rest()
                show_character("teapot.jpg", "Teapot")
                talk("Bubblenook", "Ah! Finally! An intelligent living being! My name is Bubblenook and I'm terribly oversteeped. Help! Please!")
                rest()
                clear_character()
                explain("From the spout emerges a tiny creature made of steam and swirling herbs, its eyes two tiny floating tea leaves.")
                rest()
                show_character("teapot.jpg", "Bubblenook")
                talk("Bubblenook", "A wizard made me to bring comfort to travelers, but he forgot to unbind me before he vanished!")
                rest()
                talk("Bubblenook", "I've been boiling for… I don't even know how long!")
                rest()

                while True:
                    spill_the_tea = dialogue("What do you do?", [
                        opt("Offer to help the creature.", 1),
                        opt("Walk away.", 2),
                    ])
                    rest()
                    

                    if spill_the_tea == 1:
                        talk("Bubblenook", "By the boiled leaf! Thank you so very much!")
                        rest()
                        talk("Bubblenook", "The only way to undo my binding is to recreate my perfect blend: five herbs, in the right order.")
                        rest()
                        talk("Bubblenook", "The only issue is that I don't exactly remember the recipe...")
                        rest()
                        talk("Bubblenook", "There are clues carved around the stump. Use your senses, your wit, and your nose!")
                        rest()
                        clear_character()
                        explain("You notice five small stone bowls around the stump, each filled with a different dried herb, as well as five clues about the order.")
                        rest()
                        write("Try to put the herbs in the right order with the following clues.")
                        rest()
                        clue_number = 1
                        herb_order = ""
                        while True:
                            
                            write(f"Clue {clue_number}:")
                            rest()
                            if clue_number == 1:
                                explain("First comes the leaf that soothes the soul and cools the tongue.")
                                rest()
                            if clue_number == 2:
                                explain("Second, the blossom that calms even thunderous thoughts.")
                                rest()
                            if clue_number == 3:
                                explain("The root that bites, but chases chill away—third in line.")
                                rest()
                            if clue_number == 4:
                                explain("The scent of sleep, next it must be.")
                                rest()
                            if clue_number == 5:
                                explain("Last, the bark of spice, for warmth at the end.")
                                rest()
                            clue_number +=1

                            options = [once("peppermint", opt("Peppermint", 1)),
                                    once("chamomile", opt("Chamomile", 2)),
                                    once("ginger", opt("Ginger", 3)),
                                    once("lavender", opt("Lavender", 4)),
                                    once("cinnamon", opt("Cinnamon", 5)),
                                    ]
                            random.shuffle(options)
                            make_the_tea = dialogue("Which herb do you add?", options)
                            rest()
                            

                            if make_the_tea == 1:
                                flag("peppermint")
                                herb_order += "1"
                            if make_the_tea == 2:
                                flag("chamomile")
                                herb_order += "2"
                            if make_the_tea == 3:
                                flag("ginger")
                                herb_order += "3"
                            if make_the_tea == 4:
                                flag("lavender")
                                herb_order += "4"
                            if make_the_tea == 5:
                                flag("cinnamon")
                                herb_order += "5"
                            

                            if clue_number == 6:
                                if herb_order == "12345":
                                    explain("You mix all the ingredients in the tea.")
                                    rest()
                                    show_character("teapot.jpg", "Bubblenook")
                                    talk("Bubblenook", "Well infuse me in chamomile and call me cursed! You've found it! These herbs mix wonderfully!")
                                    rest()                
                                    explain("The teapot shudders once, then pops its lid.")
                                    rest()
                                    explain("Bubblenook leaps out and spins around you in a swirl of joyful steam before settling in a warm puff, floating in the air.")
                                    rest()
                                    talk("Bubblenook", "Thank you so much for freeing me! I thought I would spend the rest of my life in that bitter teapot!")
                                    rest()
                                    talk("Bubblenook", "I have nothing to offer you, for now. But I'm sure we'll meet again!")
                                    rest()
                                    talk("Bubblenook", "Toodaloo!")
                                    rest()
                                    clear_character()
                                    spill_the_tea = 3
                                    unlock("bubblenook")
                                    break
                                else:
                                    explain("You mix all the ingredients in the tea.")
                                    rest()
                                    explain("The tea begins to bubble violently.")
                                    rest()
                                    show_character("teapot.jpg", "Bubblenook")
                                    talk("Bubblenook", "Crumbling crumpets! Those don't blend well at all! That's disgusting!")
                                    rest()
                                    explain("The tea bursts in a cloud of scalding steam.")
                                    rest()
                                    talk("Bubblenook", "You'll have to try again.")
                                    
                                    try_tea_again = dialogue("What do you do?", [
                                        opt("Try again.", 1),
                                        opt("Give up and leave.", 2)
                                    ])

                                    if try_tea_again == 1:
                                        clue_number = 1
                                        herb_order = ""
                                        remove_flag("peppermint", "chamomile", "ginger", "lavender", "cinnamon")
                                        continue
                                    elif try_tea_again == 2:
                                        spill_the_tea = 2
                                        break
                    if spill_the_tea == 2:
                        talk("Bubblenook", "Fine! I guess I'll just lay here to boil forevermore!")
                        rest()
                        break
                    if spill_the_tea == 3:
                        rest()
                        break
                clear_character()

            # Bear
            elif current_encounter == "bear":
                explain("As the winding forest trail dips into a quiet glade, the underbrush suddenly rustles—then parts.")
                rest()
                explain("A massive brown bear lumbers into view. Its fur is matted with leaves, and a deep scar runs down one shoulder.")
                rest()
                explain("It pauses, sniffing the air, then lets out a low, guttural grunt.")
                rest()
                explain("It hasn't noticed you yet… but it's a matter of seconds.")
                rest()
                explain("The forest holds its breath.")
                rest()

                thats_a_bear = dialogue("What do you do?", [
                    opt(f"Try to scare it off. [{chance("cha", 14, "intimidation")} chance of success]", 1),
                    opt(f"Try to sneak around it. [{chance("dex", 14, "stealth")} chance of success]", 2),
                    opt("Fight the bear.", 3)
                ])
                rest()
                

                # Scare the bear
                if thats_a_bear == 1:
                    scare_the_bear = check("cha", 14, "intimidation")
                    if scare_the_bear:
                        check_success()
                        rest()
                        if PLAYER_CLASS == "Bard":
                            explain("You strum up an intimidating song on your lute.")
                            rest()
                            explain("The bear backs away, terror on its face.")
                            rest()
                            explain("Then, it breaks into a sprint, getting as far away from you as it can.")
                            rest()
                        if PLAYER_CLASS == "Rogue":
                            explain("You toss a rock into the shadows behind the bear.")
                            rest()
                            explain("The bear jumps, terrified.")
                            rest()
                            explain("Then, it breaks into a sprint, getting as far away from you as it can.")
                            rest()
                        if PLAYER_CLASS == "Warrior":
                            explain("You raise your sword up high and let out a primal roar.")
                            rest()
                            explain("The bear backs away, terror on its face.")
                            rest()
                            explain("Then, it breaks into a sprint, getting as far away from you as it can.")
                            rest()
                        if PLAYER_CLASS == "Wizard":
                            explain("You summon fire to your hand, concentrating solar light as it keeps getting brighter.")
                            rest()
                            explain("The bear is blinded by the light and stumbles away, terror on its face.")
                            rest()
                            explain("Then, it breaks into a sprint, getting as far away from the light as it can.")
                            rest()

                    elif not scare_the_bear:
                        check_failure()
                        rest()

                        if PLAYER_CLASS == "Bard":
                            explain("You try to strum up an intimidating song on your lute.")
                            rest()
                        if PLAYER_CLASS == "Rogue":
                            explain("You toss a rock into the shadows behind the bear.")
                            rest()
                        if PLAYER_CLASS == "Warrior":
                            explain("You raise your sword up high and let out a primal roar.")
                            rest()
                        if PLAYER_CLASS == "Wizard":
                            explain("You summon fire to your hand, concentrating solar light as it keeps getting brighter.")
                            rest()
                            
                        thats_a_bear = 3

                # Sneak around the bear
                if thats_a_bear == 2:
                    sneak_around_bear = check("dex", 14, "stealth")
                    if sneak_around_bear:
                        check_success()
                        rest()
                        if not PLAYER_CLASS == "Wizard":
                            explain("You dash towards the trees before it sees you.")
                        elif PLAYER_CLASS == "Wizard":
                            explain("You quickly cast an invisibility spell on yourself before it sees you.")
                        rest()
                        explain("You're able to go around the bear without getting caught.")
                        rest()
                    elif not sneak_around_bear:
                        check_failure()
                        rest()
                        if not PLAYER_CLASS == "Wizard":
                            explain("You try to dash towards the trees before it sees you, but it's too late...")
                        elif PLAYER_CLASS == "Wizard":
                            explain("You try to cast an invisibility spell on yourself before it sees you, but it's too late...")
                        thats_a_bear = 3

                # Fight the bear        
                if thats_a_bear == 3:
                    explain("The bear notices you, lets out a big roar, then comes running at you.")
                    rest()

                    while True:
                        kill_the_bear = run_combat({("brown bear", True, 1, "Brown Bear")})
                        
                        if kill_the_bear:
                            music(explore=True)
                            write("You defeated the bear!")
                            rest()
                            explain("You take a moment to gaze at the bear's corpse, then get up and leave.")
                            rest()
                            break
                        elif not kill_the_bear:
                            death_message()
                            rest()
                            continue
            
            # Pool
            elif current_encounter == "pool":
                explain("As you make your way through the thickening trees, the sound of birdsong gives way to silence.")
                rest()
                explain("A clearing opens ahead, revealing a perfectly still pool of water nestled in mossy stones and luminous blue flowers.")
                rest()
                draw_background(forest_pool=True)
                explain("Something about the pool draws your eye. You feel… watched.")
                rest()
                while True:
                    pool = dialogue("What do you do?", [
                        once("pool dialogue 1", opt("Inspect the pool closely.", 1)),
                        once("pool dialogue 2", opt("Touch the water.", 2)),
                        once("pool dialogue 3", opt(f"[Wizard] Try to sense any magic in the pool. [{chance("int", 12, "arcana")} chance of success]", 3, classes="Wizard")),
                        opt("Leave the pool and continue on your journey.", 4)
                    ])
                    rest()
                    

                    # Inspect the pool
                    if pool == 1:
                        flag("pool dialogue 1")
                        explain("As you approach, your reflection looks... odd.")
                        rest()
                        explain("You step carefully to the water's edge, the moss squelching softly under your boots. As you lean in, you expect to see your reflection gazing back.")
                        rest()
                        explain("At first, you do.")
                        rest()
                        explain("But after a heartbeat... something feels wrong.")
                        rest()
                        explain("Your reflection blinks a moment too late. When you tilt your head, it mirrors you—but with a slight, deliberate delay.")
                        rest()
                        explain("It's subtle at first. Then, unmistakable.")
                        rest()
                        explain("Then it smiles.")
                        rest()
                        explain("Not a normal smile. A knowing, mischievous grin.")
                        rest()
                        weird_reflection = dialogue("What do you do?", [
                            opt("Smile back.", 1),
                            opt("Reach out towards your reflection.", 2),
                            opt("Speak to your reflection.", 3),
                            opt("Step away.", 4),
                        ])
                        rest()
                        
                        
                        # Smile
                        if weird_reflection == 1:
                            explain("Your reflection winks at you, then reaches out a hand, as if it wants to pull you into the pool.")
                            rest()
                            grab_hand = dialogue("What do you do?", [
                                opt("Accept its offer.", 1),
                                opt("Back away.", 2)
                            ])
                            rest()
                            

                            if grab_hand == 1:
                                explain("As you grab its hand, excitement flashes across your reflection's face.")
                                rest()
                                explain("Then it pulls you into the water with unnatural strength.")
                                rest()
                                flag("that way (pool)")
                                pool = 2
                            elif grab_hand == 2:
                                rest()
                                pool = 4

                        # Reach out
                        if weird_reflection == 2:
                            explain("As you reach out your hand, excitement flashes across your reflection's face.")
                            rest()
                            explain("It grabs your hand and pulls you into the water with unnatural strength.")
                            rest()
                            flag("that way (pool)")
                            pool = 2

                        # Talk to it
                        if weird_reflection == 3:
                            explain("Before you can get a sentence out, your reflection suddenly looks disappointed.")
                            rest()
                            show_character("reflection.png", "Reflection")
                            talk("Reflection", "What a shame, I though we had something there...")
                            rest()
                            talk("Reflection", "Relying on language is so distasteful... that's not how these things work.")
                            rest()
                            explain("After one more look from your reflection, it fades away into the water.")
                            rest()
                            clear_character()

                        # Walk away (still in encounter)
                        if weird_reflection == 4:
                            explain("The reflection's grin fades. It watches you retreat, disappointment flickering across its face before the pool's surface returns to normal.")
                            rest()
                            continue
                    
                    # Touch the water
                    if pool == 2:
                        flag("pool dialogue 1", "pool dialogue 2", "pool dialogue 3")
                        
                        if not STORY_FLAGS.get("that way (pool)"):
                            explain("You reach your hand into the water.")
                            rest()
                        explain("As your skin touches the water, you feel a cold jolt of energy shooting through your body.")
                        rest()
                        explain("Instantly your mind is enveloped with... ")
                        rest()
                        explain("Everything.", True)
                        rest()
                        explain("Space and time become irrelevant as your consciousness is taken by the pool.")
                        rest()
                        explain("Some how you feel everything all at once.")
                        rest()
                        explain("Right and wrong.")
                        rest()
                        explain("Pain and healing.")
                        rest()
                        explain("Chaos and silence.")
                        rest()
                        explain("Youth and age.")
                        rest()
                        explain("Hot and cold.")
                        rest()
                        explain("Joy and sorrow.")
                        rest()
                        explain("Together and alone.")
                        rest()
                        explain("Everything...")
                        rest()
                        explain("And nothing.")
                        wait()
                        explain("Then waves of flashing lights and blurred images flash in front of your eyes, before settling on a specific scene.")
                        rest()
                        explain("You see Hearthstone, but not as you've come to know it.")
                        rest()
                        explain("The village is engulfed in smoke and flame.")
                        rest()
                        explain("Buildings crumble as fire sweeps through the streets. The familiar stone houses, the cheerful banners, the bustling tavern.")
                        rest()
                        explain("You watch them all blacken and collapse.")
                        rest()
                        explain("Through the smoke march creatures you've never seen: goblins cloaked in crackling magic, their hands sparking with fire and shadow.")
                        rest()
                        explain("Behind them trundle clanking dwarven machines: stolen war-engines, now twisted for destruction.")
                        rest()
                        explain("Iron jaws snap, gears shriek, and heavy cannons belch fire into the heart of the town.")
                        rest()
                        explain("You spot Mayor Thorne rallying a group of desperate, untrained villagers.")
                        rest()
                        explain("But a blast of magic tears through their line, scattering them like leaves on a windy day.")
                        wait()

                        explain("Then you feel everything rush past you as you're pulled back into the present.")
                        rest()
                        explain("Your mind is almost too overwhelmed to notice that you're laying beside the pool.")
                        rest()
                        explain("You look back into the water, but only your pale reflection remains, staring back in stunned silence.")
                        wait()

                    # Sense magic
                    if pool == 3:
                        flag("pool dialogue 3")
                        sense_pool_magic = check("int", 12, "arcana")

                        if sense_pool_magic:
                            check_success()
                            rest()
                            explain("As you reach out to the pool with your magic, you feel an overwhelming sense of power.")
                            rest()
                            explain("The pool contains more magic than you've ever seen in one place.")
                            rest()
                            explain("You sense that the magic is trying to reach out, as if it wants to show you something...")
                            rest()
                        elif not sense_pool_magic:
                            check_failure()
                            rest()
                            explain("As you reach out to the pool with your magic, you receive no response.")
                            rest()

                    # Walk away from encounter
                    if pool == 4:
                        explain("You walk away from the pool.")
                        break

            # Goblins
            elif current_encounter == "goblins":
                explain("As you make your way through the forrest, drawing ever closer to the goblin hideout, you start to hear voices.")
                rest()
                explain("Harsh, tonal voices sound from somewhere up ahead, getting closer.")
                rest()
                explain("Then, you spot their source.")
                rest()
                explain("Rounding the corner is a goblin patrol, no-doubt from Grimglen Hollow.")
                rest()
                explain("They notice you as soon as you see them, and without a second thought they immediately charge with their spears.")
                rest()

                while True:
                    goblin_encounter = run_combat([("goblin", True, 4, None)])
                    
                    if goblin_encounter:
                        music(explore=True)
                        explain("You have defeated the goblin patrol.")
                        rest()
                        break
                    elif not goblin_encounter:
                        death_message()
                        rest()
                        continue       

# INPUT: None
# RETURN: None
# PURPOSE: To run act 3 of the game
def act_3():
    music(explore=True)
    draw_background(forest=True)

    # Premise
    if True:
        write("Act 3: To Kill", delay=75)
        wait()
        explain("You push through a final thicket of gnarled trees, and the woods open into a sunken clearing.")
        rest()
        explain("Before you, carved into a rocky hillside, sprawls the goblin hideout.")
        rest()
        draw_background(goblin_camp=True)
        explain("Various huts and barricades form a camp within the forest.")
        rest()
        explain("Strange dwarven machines jut from the ground like broken bones, belching lazy plumes of smoke.")
        rest()
        explain("A few goblins clatter around the camp, hammering scrap into hulking mechanical frames.")
        rest()
        explain("But that's not the worst of it.")
        rest()
        explain("Near the center of the camp, a glowing mass of twisting metal and fractured stone hums with energy — a dwarven Arc Node")
        rest()
        explain("Blue sparks crackle along the ground around it, and you spot goblins nearby levitating stones and conjuring fire in their hands.")
        rest()
        explain("Some of them have grown strange: their skin slightly translucent, their eyes glowing faintly.")
        rest()
        explain("Whatever they've tapped into, it's changing them.")
        rest()
        explain("A heavy, half-finished siege machine, almost the size of a small house, sits dormant near the archway, iron plates bolted crudely over dwarven craftsmanship.")
        rest()
        explain("The air itself feels... unstable. The ground vibrates faintly beneath your boots.")
        rest()
        explain("This is no simple goblin raid.")
        rest()
        explain("Something ancient has been disturbed.")
        wait()
    
    # Main Loop for Act 3
    while True:
        if STORY_FLAGS.get("moving to epilogue"):
            break
        music(explore=True)
        draw_background(goblin_camp=True)
        goblin_camp = dialogue("What's your plan?", [
            opt("Run out and attack the goblins.", 1),
            opt("[Bard] Disguise yourself as a goblin and talk to them.", 2, classes = "Bard"),
            opt('[Rogue] Let the goblins "capture" you.', 3, classes = "Rogue"),
            opt("[Warrior] Challenge the goblin leader to a duel.", 4, classes = "Warrior"),
            opt("[Wizard] Try to disrupt the Arc Node with your magic.", 5, classes = "Wizard")
        ])
        rest()
        
        # Attack the goblins
        if goblin_camp == 1:
            explain("You run out into the camp, taking the goblins by surprise.")
            rest()
            explain("You're able to take out a few goblins as you rampage through the camp, but eventually King Snik finds you.")
            rest()
            show_character("goblin_king.png", "King Snik")
            talk("King Snik", "It seems we have ourselves a little hero.")
            rest()
            talk("King Snik", "It's admirable, really.")
            rest()
            talk("King Snik", "But now you will pay the price.")
            rest()
            explain("He conjures flames in his hands as he calls for reinforcements, then attacks you.")
            rest()
            clear_character()
            while True:
                fight_snik = run_combat([("goblin", True, 3, None), ("goblin_king", True, 1, "King Snik")])
                if fight_snik:
                    music(explore=True)
                    explain("You defeated the goblins!")
                    rest()
                    break
                elif not fight_snik:
                    death_message()
                    rest()
                    continue
            final_scene()
            break

        # Goblin disguise
        if goblin_camp == 2:
            explain("With a theatrical flourish and a pinch of creativity, you slap together a crude disguise from scraps of goblin armor, soot, and swamp mud.")
            rest()
            explain("A few vocal warmups later, you're ready to blend in — or at least fake it long enough to get close.")
            rest()
            explain("You swagger into camp like you own the place. One goblin tosses you a burnt rib.")
            rest()
            show_character("goblin.png", "Goblin")
            talk("Goblin", "Ey, didn't think you made it outta the mine!")
            rest()
            clear_character()
            explain("Another goblin turns his head.")
            rest()
            show_character("goblin.png", "Goblin")
            talk("Goblin", "Oi, what's yer name again?")
            rest()

            player_goblin_name = dialogue("What do you say?", [
                opt("Grubgut the Gruesome!", "Grubgut the Gruesome"),
                opt("Snaggletooth Ironpants!", "Snaggletooth Ironpants"),
                opt("Ogburt the Ugly!", "Ogburt the Ugly")
            ])
            rest()
            

            talk("Goblin", f"Ah, {player_goblin_name}. I was wonderin' where ye went.")
            rest()
            clear_character()
            explain("The goblins laugh and welcome you to the fire.")
            rest()
            explain("You hear them talk openly about their machines, magic, and plans to attack Hearthstone.")
            rest()
            explain("You get close enough to see the Arc Node — and the Goblin King himself: King Snik.")
            rest()
            explain("The king barks orders at his minions while sparks of blue light bounce off of him.")
            rest()
            explain("His small frame is draped in an oily red cloak and a strange hat.")
            rest()
            explain("He waves a staff that crackles with power, laughing as goblins scramble to obey.")
            rest()
            explain("Behind him, the Arc Node pulses, a twisting mass of dwarven tech and glowing runes.")
            rest()
            explain("You watch as he lifts his staff, and a nearby rock floats into the air, spinning wildly.")
            rest()
            explain("He hasn't seen you yet.")
            rest()
            explain("But it's clear: this goblin is no ordinary king. And he's playing with power far beyond his kind.")
            rest()

            while True:
                do_in_camp = dialogue("What do you do?", [
                    once("talk to the goblins", opt("Talk to the goblins.", 1)),
                    opt("Try to sabotage the Arc Node.", 2),
                    opt("Confront King Snik.", 3)
                ])
                rest()
                
                # Talk to the goblins
                if do_in_camp == 1:
                    flag("talk to the goblins")
                    show_character("goblin.png", "Goblin")
                    while True:
                        ask_goblins = dialogue("What do you ask the goblins?", [
                            once("goblin dialogue 1", opt("Ask about the Arc Node.", 1)),
                            once("goblin dialogue 2", opt("Ask about attacking Hearthstone.", 2)),
                            once("goblin dialogue 3", opt("Ask about King Snik.", 3)),
                            opt("[Go back]", 4)
                        ])
                        rest()
                        
                        # Arc Node
                        if ask_goblins == 1:
                            flag("goblin dialogue 1")
                            talk("goblin", "Oh, the arcy-noodle thing? Heh. Beats me. Some dwarf junk we dug up.")
                            rest()
                            talk("goblin", "Boss Snik plugged it in and boom—now he's shootin' sparks from his eyeballs.")
                            rest()
                            talk("goblin", "Says it's makin' us \"evolved\" or somethin'. I dunno.")
                            rest()
                            talk("goblin", "My cousin touched it and started speakin' backwards. He's fine now. Mostly.")
                            rest()
                            talk("goblin", "It's not dangerous, unless you're dumb enough to lick it. Which...")
                            rest()
                            talk("goblin", "Okay, a few of us were.")
                            rest()
                            talk("goblin", "Anyway, the boss says it's just the beginning.")
                            rest()
                            talk("goblin", "Pretty soon, we'll all have zappy powers. Maybe even fly! Or explode! One of those.")
                            rest()

                        # Attacking Hearthstone
                        elif ask_goblins == 2:
                            flag("goblin dialogue 2")
                            talk("goblin", "Oh, yeah, that stupid little village.")
                            rest()
                            talk("goblin", "Boss Snik's got some plan for it.")
                            rest()
                            talk("goblin", "I think we're gonna destroy it, as soon as enough of us get powers..")
                            rest()

                        # King Snik
                        elif ask_goblins == 3:
                            flag("goblin dialogue 3")
                            talk("goblin", "King Snik? Well, lets just say he really likes his big, evil plans.")
                            rest()
                            talk("goblin", "I don't even know how long he's been looking for the dwarf box thing, but it's been a long time..")
                            rest()
                            talk("goblin", "I doubt he would stop for anything, now that we've found it.")
                            rest()
    

                        # Go back
                        elif ask_goblins == 4:
                            rest()
                            clear_character()
                            break
                
                # Sabotage the Arc Node
                if do_in_camp == 2:
                    explain("You approach the Arc Node, and inspect it for a few moments.")
                    rest()
                    explain("It pulses with a strange, otherworldly force.")
                    rest()
                    explain("Something within it reaches out to you, as though it wants to connect somehow.")
                    rest()
                    explain("Then...")
                    show_character("goblin_king.png", "King Snik")
                    talk("King Snik", "What do you think you're doing, young goblin?")
                    rest()
                    explain("You turn to see King Snik a few feet behind you, staring suspiciously.")
                    rest()
                    talk("King Snik", "The Arc Node was not to be messed with by any except me.")
                    rest()
                    explain("He looks at you more closely...")
                    rest()
                    talk("King Snik", "Oh, what do we have here?")
                    rest()
                    talk("King Snik", "A spy? In my camp?")
                    rest()
                    talk("King Snik", "I don't think so.")
                    rest()
                    explain("He calls for his goblins, conjures flames in his hands, then charges at you.")
                    rest()
                    clear_character()
                    while True:
                        fight_snik = run_combat([("goblin", True, 3, None), ("goblin_king", True, 1, "King Snik")])
                        if fight_snik:
                            music(explore=True)
                            explain("You defeated the goblins!")
                            rest()
                            break
                        elif not fight_snik:
                            death_message()
                            rest()
                            continue
                    final_scene()
                    break

                # Confront the king
                if do_in_camp == 3:
                    explain("You walk up to King Snik, who isn't hard to find.")
                    rest()
                    explain("He turns to you as you approach.")
                    rest()
                    show_character("goblin_king.png", "King Snik")
                    talk("King Snik", "What can I do for you, young goblin?")
                    rest()
                    explain("But before you can respond, he interrupts.")
                    talk("King Snik", "Wait a moment...")
                    rest()
                    talk("King Snik", "Your no goblin, are you?")
                    answer = dialogue("What do you say?", [
                                      opt(f"What do you mean? My name is {player_goblin_name}.", 1),
                                      opt("Of course I'm not.", 2),
                                      opt("[Attack him].", 3)
                                      ])
                    rest()

                    if answer == 1:
                        talk("King Snik", "Well that's interesting, because I keep a very close record of my people.")
                        rest()
                        talk("King Snik", f"And I happen to know that {player_goblin_name} is not one of them.")
                        rest()
                        talk("King Snik" "You are not a goblin. You are a spy.")
                        rest()
                        talk("King Snik", "And now you will pay the price.")
                        rest()
                        explain("He conjures flames in his hands as he calls for reinforcements, then attacks you.")
                        rest()
                    elif answer == 2:
                        talk("King Snik", "Well, that makes things easy for me.")
                        rest()
                        explain("He conjures flames in his hands as he calls for reinforcements, then attacks you.")
                        rest()
                    elif answer == 3:
                        rest()
                    clear_character()
                    while True:
                        fight_snik = run_combat([("goblin", True, 3, None), ("goblin_king", True, 1, "King Snik")])
                        if fight_snik:
                            music(explore=True)
                            explain("You defeated the goblins!")
                            rest()
                            break
                        elif not fight_snik:
                            death_message()
                            rest()
                            continue
                    final_scene()
                    break

        # Let the goblins capture you
        if goblin_camp == 3:
            explain("You gather your resolve, then come up with a plan.")
            rest()
            explain("You step from the trees, hands raised, weapon sheathed.")
            rest()
            explain("Goblins spot you instantly, shrieking with alarm and drawing crude blades.")
            rest()
            explain("\"I surrender!\" you shout, trying to look weak, tired—like a perfect little prize.")
            rest()
            explain("They swarm you, jeering and jabbing, then bind your hands with itchy rope and march you to the heart of the camp.")
            rest()
            explain("You're shoved into a filthy tent and tied to a post.")
            wait()
            explain("Eventually a goblin officer with fancy bones in their hat grunts.")
            rest()
            show_character("goblin.png", "Goblin Officer")
            talk("Goblin Officer", "Tell the King, we got a catch.")
            rest()
            clear_character()
            explain("The goblins walk out to get the king, giving you a moment alone...")
            rest()
            captured = dialogue("What do you do?", [
                opt(f"Slip off the ropes and ambush the king. [{chance("dex", 13, "sleight of hand")} chance of success]", 1),
                opt(f"Wait for the King.", 2),
            ])
            rest()

            # Try to escape
            if captured == 1:
                escape = check("dex", 13, "sleight of hand")
                
                if escape:
                    check_success()
                    rest()
                    explain("You're able to slip the ropes off.")
                    rest()
                    explain("You quickly get up and hide in the corner, waiting for the king to return...")
                    rest()
                    explain("After a few minutes, King Snik walks in.")
                    rest()
                    explain("Silence rings throughout the room for a few moments.")
                    show_character("goblin_king.png", "King Snik")
                    rest()
                    talk("King Snik", "I thought we had a prisoner.")
                    rest()
                    show_character("goblin.png", "Goblin")
                    talk("Goblin", "What? They were right here I swear.")
                    rest()
                    show_character("goblin_king.png", "King Snik")
                    talk("King Snik", "Well, you obviously didn't tie them down properly.")
                    rest()
                    talk("King Snik", "Search the camp, they can't be far.")
                    rest()
                    clear_character()
                    explain("Then, the king turns his back.")
                    rest()
                    explain("It's the perfect opportunity...")
                    rest()
                    explain("And you take it!")
                    rest()
                    explain("You lash out with your dagger and stab the goblin king in the back.")
                    rest()
                    explain("He shouts out in pain and turns back around")
                    show_character("goblin_king.png", "King Snik")
                    rest()
                    talk("King Snik", "It seems that we've found the human.")
                    rest()
                    explain("He conjures flames in his hands and fights back.")
                    rest()
                    clear_character()
                    while True:
                        fight_snik = run_combat([("goblin", True, 3, None), ("goblin_king", True, 1, "King Snik")])
                        if fight_snik:
                            music(explore=True)
                            explain("You defeated the goblins!")
                            rest()
                            break
                        elif not fight_snik:
                            death_message()
                            rest()
                            continue
                    final_scene()
                    break



                elif not escape:
                    check_failure()
                    rest()
                    explain("You try to slip the ropes off, but the goblins tied them tight.")
                    rest()
                    explain("You're stuck.")
                    rest()
                    captured = 2
            
            # Wait for the King
            if captured == 2:
                explain("After a few minutes, King Snik walks in, followed by a group of goblins.")
                rest()
                show_character("goblin_king.png", "King Snik")
                talk("King Snik", "Oh dear, what do we have here?")
                rest()
                talk("King Snik", "A human?")
                rest()
                talk("King Snik", "In my camp?")
                rest()
                explain("He looks around at his goblins, then grins.")
                rest()
                talk("King Snik", "It seems that we get to practice.")
                rest()
                clear_character()
                explain("The goblins lead you out to the middle of the camp.")
                rest()
                explain("You notice the Arc Node nearby, emitting lightning and blue sparks.")
                rest()
                explain("Then the goblins... untie you.")
                rest()
                show_character("goblin_king.png", "King Snik")
                talk("King Snik", "We shall see what this human is made of.")
                rest()
                explain("He conjures flames in his hands, signaling to his goblins, then rushes towards you.")
                rest()
                clear_character()
                while True:
                        fight_snik = run_combat([("goblin", True, 3, None), ("goblin_king", True, 1, "King Snik")])
                        if fight_snik:
                            music(explore=True)
                            explain("You defeated the goblins!")
                            rest()
                            break
                        elif not fight_snik:
                            death_message()
                            rest()
                            continue
                final_scene()
                break 

        # Challenge the goblin leader
        if goblin_camp == 4:
            explain("You step into the open, loud and defiant.")
            rest()
            explain("Then you say: \"I'm not here to sneak or beg. I'm here to challenge your King to a duel. One-on-one!\"")
            rest()
            explain("The goblins freeze.") 
            rest()
            explain("Then the jeering starts. Laughter, shouts, chants of “Snik! Snik! Snik!” echo through the camp.")
            rest()
            explain("From atop a platform of gears and stone, the goblin king rises.")
            rest()
            explain("His staff crackles with unstable magic, and his patchwork armor gleams with metal plates fused from dwarven scrap.")
            rest()
            explain("He grins wide, sharp teeth glinting.")
            show_character("goblin_king.png", "King Snik")
            rest()
            talk("King Snik", "A duel?")
            rest()
            talk("King Snik", "You got guts, I'll give you that.")
            rest()
            talk("King Snik", "Fine. Lets make a show of it.")
            rest()
            explain("He hands his staff off to another goblin, conjures flames into his hands, then attacks.")
            rest()
            while True:
                fight_snik = run_combat([("goblin_king", True, 1, "King Snik")])
                if fight_snik:
                    clear_character()
                    music(explore=True)
                    explain("As Snik hits the ground, on his last breath, he calls out to the goblins.")
                    rest()
                    explain("They throw him his staff, which glows with an otherworldly light.")
                    rest()
                    explain("Snik takes it, and snaps it in half.")
                    rest()
                    explain("Immediately blue light begins to surge around him, and his wounds begins to heal.")
                    rest()
                    show_character("goblin_king.png", "King Snik")
                    talk("King Snik", "You think I would let you defeat me, while I'm surrounded by my people?")
                    rest()
                    talk("King Snik", "Get him my goblins!")
                    rest()
                    break
                elif not fight_snik:
                    death_message()
                    rest()
                    continue
            while True:
                fight_snik = run_combat([("goblin", True, 3, None), ("goblin_king", True, 1, "King Snik")])
                if fight_snik:
                    music(explore=True)
                    explain("You defeated the goblins!")
                    rest()
                    break
                elif not fight_snik:
                    death_message()
                    rest()
                    continue
            final_scene()
            break

        # Disrupt the Arc Node
        if goblin_camp == 5:
            explain("You reach out to the Arc Node with your magic.")
            rest()
            explain("It responds, forging a connection between you two.")
            rest()
            explain("You feel the magic in your bones: wild, stolen, and wrong.")
            rest()
            explain("With steady breath, you raise your hands and begin to weave a counterspell.")
            rest()
            explain("The moment your magic touches the node's aura, the reaction is instant.")
            rest()
            explain("The Arc Node screeches. Not audibly; in your mind.")
            rest()
            explain("Magic bends. Sparks fly. The sky above the camp flickers with unnatural lightning.")
            rest()
            explain("Goblins shriek. Some flee. Others race toward the node to stabilize it. But it's too late—you've begun unraveling it.")
            rest()
            explain("Then, the king comes charging towards you.")
            rest()
            show_character("goblin_king.png", "King Snik")
            rest()
            talk("King Snik", "NO! What are you doing?")
            rest()
            talk("King Snik", "We're using that!")
            rest()
            talk("King Snik", "Get away.")
            rest()
            talk("King Snik", "GET AWAY!")
            rest()
            explain("King Snik struggles as he tries to conjure flames to his hands.")
            rest()
            talk("King Snik", "This is YOUR fault.")
            rest()
            talk("King Snik", "You will pay with your life.")
            rest()
            clear_character()
            while True:
                fight_snik = run_combat([("goblin", True, 3, None), ("goblin_king", True, 1, "King Snik")])
                if fight_snik:
                    music(explore=True)
                    explain("You defeated the goblins!")
                    rest()
                    break
                elif not fight_snik:
                    death_message()
                    rest()
                    continue
            final_scene()
            break     

# INPUT: None
# RETURN: None
# PURPOSE: To run the epilogue of the game
def epilogue():
    music(epilogue=True)
    draw_background(village=True)
 
    write("Epilogue: To Live", delay=75)
    wait()
    write("Two weeks later.", italic=True, delay=75)
    wait()
    explain("The sun shines from above as you approach the bustling village of Hearthstone, nestled between forested hills. Smoke rises from chimneys, but so do faint wisps that remain from last night's firework display. People look joyful. Children are running about, playing with each other. The goblin raids are over.")
    rest()
    explain("As you walk through the village, you notice the people.")
    rest()
    explain("The barkeeper hitches a toothy grin and raises a filthy glass towards you.")
    rest()
    explain("The merchant from the tavern waves at you, smiling.")
    rest()
    if STORY_UNLOCKS.get("wayne"):
        explain("The soldier you challenged earlier, Wayne, smiles at you as you pass, inspired by your victory.")
        rest()
    if STORY_UNLOCKS.get("tien"):
        explain("The kid from the rooftops, Tien, grins at you from the roof of the local blacksmith.")
        rest()
    if STORY_UNLOCKS.get("tress"):
        explain("Tress waves at you from a stage wearing a ridiculous goose costume.")
        rest()
    if STORY_UNLOCKS.get("hoid"):
        explain("Hoid, playing a flute for a small crowd, nods in your direction.")
        rest()
    if STORY_UNLOCKS.get("bubblenook"):
        explain("A new tea shop is being built, and from it you see Bubblenook sharing samples.")
        rest()
    if STORY_UNLOCKS.get("owlbear"):
        explain(f"{owlbear_name} is walking alongside you, occasionally stopping to play with a cat or dog.")
        rest()
    explain("Mayor Thorne beams at you while helping rebuild a house.")
    wait()
    explain("All is well.")
    wait()
    write("")
    music(ending=True)
    wait()
    

# INPUT: None
# RETURN: A boolean: True or False
# PURPOSE: To see if the player wants to play again.
def play_again():
    write("Thank you for playing the Goblins of Grimglen Hollow, by Harrison Nickles.")
    wait()
    write(f"You died {PLAYER_DEATHS} times during the adventure.")
    wait()
    write("Almost all the music in this game was taken from The Elder Scrolls IV: Oblivion.")
    rest()
    write("Many of the sound effects were taken from The Legend of Zelda: Breath of the Wild.")
    rest()
    write("Other effects were from various creators in the community.")
    rest()
    write("Most of the graphics were taken from google.")
    rest()
    write("I claim no right to any of the assets in this game.")
    rest()
    
    play_again = dialogue("Would you like to play again?", [
        opt("Yes.", 1),
        opt("No.", 2)
    ])
    rest()
    
    
    if play_again == 1:
        global OLD_NAME, OLD_CLASS
        write("Alright, here we go again!")
        wait()
        OLD_NAME = PLAYER_NAME
        OLD_CLASS = PLAYER_CLASS
        
        return True
    elif play_again == 2:
        rest()
        return False

# INPUT: None
# RETURN: None
# PURPOSE: To run the game in it's entirety.
def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    global FIRST_TIME
    FIRST_TIME = True

    # Main game functions:
    while True:
        prologue()

        act_1()
        act_2()
        act_3()

        epilogue()

        again = play_again()
        if again:
            FIRST_TIME = False
            continue
        elif not again:
            break
            
    write("Thank you for playing my game.")
    rest()

main()