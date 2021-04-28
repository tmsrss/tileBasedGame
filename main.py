import random
import sys
from os import path
from settings import *
from sprites import *
from map import *
import pytmx
from game import *
import mysql.connector
import hashlib
from configparser import ConfigParser
import database

config = ConfigParser()



def start_game():
    g = Game()
    g.load_data()
    #g.show_start_screen()
    g.new()  #is being called by the menu, kept here for logical sense.
    g.run()
    g.show_over_screen()
    database.update_statistics(LOGGEDIN_PLAYERID, g)
    g.stop()
    main()

    #pg.quit()
    # fro menu hierarchy https://www.youtube.com/watch?v=0RryiSjpJn0



sys.path.insert(0, '../../')

import os
import pygame
import pygame_menu

# -----------------------------------------------------------------------------
# Constants and global variables
# -----------------------------------------------------------------------------
FPS = 60
WINDOW_SIZE = (WIDTH, HEIGHT)

sound = None  # type: pygame_menu.sound.Sound
surface = None  # type: pygame.Surface
main_menu = None  # type: pygame_menu.Menu


# -----------------------------------------------------------------------------
# Methods
# -----------------------------------------------------------------------------
def main_background():
    """
    Background color of the main menu, on this function user can plot
    images, play sounds, etc.
    :return: None
    """
    global surface
    surface.fill((40, 80, 150))


def check_name_test(value):
    """
    This function tests the text input widget.
    :param value: The widget value
    :type value: str
    :return: None
    """
    print('User name: {0}'.format(value))


# noinspection PyUnusedLocal
def update_menu_sound(value, enabled):
    """
    Update menu sound.
    :param value: Value of the selector (Label and index)
    :type value: tuple
    :param enabled: Parameter of the selector, (True/False)
    :type enabled: bool
    :return: None
    """
    global main_menu
    global sound
    print(enabled)
    config.set('MENU', 'sound', str(enabled))
    with open('config.ini', 'w') as configfile:
        config.write(configfile)
    if enabled:
        main_menu.set_sound(sound, recursive=True)
        print('Menu sounds were enabled')
    else:
        main_menu.set_sound(None, recursive=True)
        print('Menu sounds were disabled')


def storyline():
    # -------------------------------------------------------------------------
    # Globals
    # -------------------------------------------------------------------------
    global main_menu
    global sound
    global surface
    global logged_in
    global storyline_change

    # -------------------------------------------------------------------------
    # Init pygame
    # -------------------------------------------------------------------------
    pygame.init()
    os.environ['SDL_VIDEO_CENTERED'] = '1'

    # Create pygame screen and initialise objects
    surface = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption('Storyline')
    clock = pygame.time.Clock()

    # -------------------------------------------------------------------------
    # Set sounds
    # -------------------------------------------------------------------------
    sound = pygame_menu.sound.Sound()

    # Load example sounds
    sound.load_example_sounds()

    # Disable a sound
    sound.set_sound(pygame_menu.sound.SOUND_TYPE_ERROR, None)

    # -------------------------------------------------------------------------
    # Create menus: Storyline menu
    # -------------------------------------------------------------------------
    pygame_menu.themes.THEME_BLUE = pygame_menu.themes.THEME_BLUE.copy()
    pygame_menu.themes.THEME_BLUE.widget_offset = (0, 0.09)
    pygame_menu.themes.THEME_BLUE.title_font = pygame_menu.font.FONT_COMIC_NEUE
    pygame_menu.themes.THEME_BLUE.widget_font = pygame_menu.font.FONT_COMIC_NEUE
    pygame_menu.themes.THEME_BLUE.widget_font_size = 30

    storyline_menu = pygame_menu.Menu(
        height=WINDOW_SIZE[1],
        width=WINDOW_SIZE[0],
        onclose=pygame_menu.events.EXIT,  # User press ESC button
        title='Storyline',
        theme=pygame_menu.themes.THEME_BLUE,
    )

    STORY = "You are a hacker. \n"\
            "You have been able to gain access to top-secret government files which have evidence against each parliament member of the world. "\
            "The FBI, CIA, KGB and INTERPOL are after you, they are sending waves of hitmen trying to kill you. "\
            "Survive as many waves of hitmen as you can. "\
            "There are several powerups which you can pick up, including: health and different weapons. "\
            "Move your character with wasd or arrow keys. "\
            "Shoot using the space bar. " \
            "Cycle between different weapons using the 1, 2, 3, number keys. "
    storyline_menu.add_label(STORY, max_char=-1, font_size=20, selectable=True)

    def back():
        global storyline_change
        storyline_menu.disable()
        storyline_change = False

    storyline_menu.add_button('Back', back)
    storyline_menu.add_button('Quit', pygame_menu.events.EXIT)

    while True:

        # Tick
        clock.tick(FPS)

        # Paint background
        main_background()

        # Main menu
        storyline_menu.mainloop(surface, main_background, fps_limit=FPS)

        # Flip surface
        pygame.display.flip()

        if storyline_change == False:
            main()


def satisticsMenu():
    # -------------------------------------------------------------------------
    # Globals
    # -------------------------------------------------------------------------
    global main_menu
    global sound
    global surface
    global logged_in
    global stats_menu_change
    global storyline_change

    # -------------------------------------------------------------------------
    # Init pygame
    # -------------------------------------------------------------------------
    pygame.init()
    os.environ['SDL_VIDEO_CENTERED'] = '1'

    # Create pygame screen and initialise objects
    surface = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption('Storyline')
    clock = pygame.time.Clock()

    # -------------------------------------------------------------------------
    # Set sounds
    # -------------------------------------------------------------------------
    sound = pygame_menu.sound.Sound()

    # Load example sounds
    sound.load_example_sounds()

    # Disable a sound
    sound.set_sound(pygame_menu.sound.SOUND_TYPE_ERROR, None)

    # -------------------------------------------------------------------------
    # Create menus: Storyline menu
    # -------------------------------------------------------------------------
    pygame_menu.themes.THEME_BLUE = pygame_menu.themes.THEME_BLUE.copy()
    pygame_menu.themes.THEME_BLUE.widget_offset = (0, 0.09)
    pygame_menu.themes.THEME_BLUE.title_font = pygame_menu.font.FONT_COMIC_NEUE
    pygame_menu.themes.THEME_BLUE.widget_font = pygame_menu.font.FONT_COMIC_NEUE
    pygame_menu.themes.THEME_BLUE.widget_font_size = 30

    satisticsMenu = pygame_menu.Menu(
        height=WINDOW_SIZE[1],
        width=WINDOW_SIZE[0],
        onclose=pygame_menu.events.EXIT,  # User press ESC button
        title='Statistics',
        theme=pygame_menu.themes.THEME_BLUE,
    )

    def back():
        global stats_menu_change
        satisticsMenu.disable()
        stats_menu_change = False

    def DPS():
        db = database.display_database()
        global LOGGEDIN_PLAYERID
        db.display_personal_statistics(LOGGEDIN_PLAYERID)

    def DU():
        db = database.display_database()
        db.display_users()

    def DL():
        db = database.display_database()
        db.display_leaderboard()

    satisticsMenu.add_button('|Personal Statistics|', DPS)
    satisticsMenu.add_button('|Users|', DU)
    satisticsMenu.add_button('|Leaderboard|', DL)
    satisticsMenu.add_button('Back', back)
    satisticsMenu.add_button('Quit', pygame_menu.events.EXIT)

    while True:

        # Tick
        clock.tick(FPS)

        # Paint background
        main_background()

        # Main menu
        satisticsMenu.mainloop(surface, main_background, fps_limit=FPS)

        # Flip surface
        pygame.display.flip()

        if stats_menu_change == False:
            main()


def main(test=False):
    # -------------------------------------------------------------------------
    # Globals
    # -------------------------------------------------------------------------
    global main_menu
    global sound
    global surface
    global logged_in
    global storyline_change
    global stats_menu_change
    storyline_change = False
    stats_menu_change = False
    # -------------------------------------------------------------------------
    # Init pygame
    # -------------------------------------------------------------------------
    pygame.init()
    os.environ['SDL_VIDEO_CENTERED'] = '1'

    # Create pygame screen and initialise objects
    surface = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption('Hitmen run')
    clock = pygame.time.Clock()

    # -------------------------------------------------------------------------
    # Set sounds
    # -------------------------------------------------------------------------
    sound = pygame_menu.sound.Sound()

    # Load example sounds
    sound.load_example_sounds()

    # Disable a sound
    sound.set_sound(pygame_menu.sound.SOUND_TYPE_ERROR, None)

    # -------------------------------------------------------------------------
    # Create menus: Main menu
    # -------------------------------------------------------------------------
    pygame_menu.themes.THEME_BLUE = pygame_menu.themes.THEME_BLUE.copy()
    pygame_menu.themes.THEME_BLUE.widget_offset = (0, 0.09)
    pygame_menu.themes.THEME_BLUE.title_font = pygame_menu.font.FONT_COMIC_NEUE
    pygame_menu.themes.THEME_BLUE.widget_font = pygame_menu.font.FONT_COMIC_NEUE
    pygame_menu.themes.THEME_BLUE.widget_font_size = 30

    main_menu = pygame_menu.Menu(
        height=WINDOW_SIZE[1],
        width=WINDOW_SIZE[0],
        onclose=pygame_menu.events.EXIT,  # User press ESC button
        title='Main menu',
        theme=pygame_menu.themes.THEME_BLUE,
    )

    config.read('config.ini')
    x = config['MENU']['sound']

    main_menu.add_button('Play', start_game)
    if x == 'True':
        main_menu.set_sound(sound, recursive=True)
        main_menu.add_selector('Menu sounds ',
                               [('On', True), ('Off', False)],
                               onchange=update_menu_sound)
    else:
        main_menu.set_sound(None, recursive=True)
        main_menu.add_selector('Menu sounds ',
                               [('Off', False), ('On', True)],
                               onchange=update_menu_sound)
    def log_out():
        global logged_in
        main_menu.disable()
        logged_in = False

    def change_storyline_menu():
        global storyline_change
        main_menu.disable()
        storyline_change = True

    def stats_menu():
        global stats_menu_change
        main_menu.disable()
        stats_menu_change = True

    main_menu.add_button('Stats', stats_menu)
    main_menu.add_button('Log Out', log_out)
    main_menu.add_button('Storyline', change_storyline_menu)
    main_menu.add_button('Quit', pygame_menu.events.EXIT)


    while True:

        # Tick
        clock.tick(FPS)

        # Paint background
        main_background()

        # Main menu
        main_menu.mainloop(surface, main_background, fps_limit=FPS)

        # Flip surface
        pygame.display.flip()

        if logged_in == False:
            start()

        if storyline_change == True:
            storyline()

        if stats_menu_change == True:
            satisticsMenu()


        # At first loop returns
        #if test:
        #    break


def start(test=False):
    """
        Main program.
        :param test: Indicate function is being tested
        :type test: bool
        :return: None
        """

    # -------------------------------------------------------------------------
    # Globals
    # -------------------------------------------------------------------------
    global main_menu
    global sound
    global surface
    global logged_in

    # -------------------------------------------------------------------------
    # Init pygame
    # -------------------------------------------------------------------------
    pygame.init()
    os.environ['SDL_VIDEO_CENTERED'] = '1'

    # Create pygame screen and objects
    surface = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption('Example - Multi Input')
    clock = pygame.time.Clock()

    # -------------------------------------------------------------------------
    # Set sounds
    # -------------------------------------------------------------------------
    sound = pygame_menu.sound.Sound()

    # Load example sounds
    sound.load_example_sounds()

    # Disable a sound
    sound.set_sound(pygame_menu.sound.SOUND_TYPE_ERROR, None)
    def click_sound(menu_name):
        config.read('config.ini')
        x = config['MENU']['sound']
        if x == 'True':
            menu_name.set_sound(sound, recursive=True)
        else:
            menu_name.set_sound(None, recursive=True)
    # -------------------------------------------------------------------------
    # Sign Up Menu
    # -------------------------------------------------------------------------
    sign_up_menu = pygame_menu.themes.THEME_BLUE.copy()
    sign_up_menu.widget_offset = (0, 0.09)
    sign_up_menu.title_font = pygame_menu.font.FONT_COMIC_NEUE
    sign_up_menu.widget_font = pygame_menu.font.FONT_COMIC_NEUE
    sign_up_menu.widget_font_size = 30
    sign_up_menu = pygame_menu.Menu(
        height=WINDOW_SIZE[1],
        width=WINDOW_SIZE[0],
        onclose=pygame_menu.events.EXIT,  # User press ESC button
        title='Sign Up Menu',
        theme=pygame_menu.themes.THEME_BLUE,
    )
    click_sound(sign_up_menu)
    sign_up_menu.add_text_input('Username: ',
                               textinput_id='username')
    sign_up_menu.add_text_input('Password: ',
                               password=True,
                               textinput_id='password')

    def register():
        data = sign_up_menu.get_input_data()
        username, password = data['username'], data['password']
        print(username)
        print(password)
        if username != '' and password != '':
            db = mysql.connector.connect(host='localhost', user='root', passwd='root', database='tiled_game')
            cursor = db.cursor()
            cursor.execute(
                'SELECT * FROM player WHERE username = %s', (username,)
            )
            result = cursor.fetchone()
            if result == None:
                passhash = hashlib.sha256()
                passhash.update(password.encode('utf-8'))
                passhash = passhash.hexdigest()
                password = 0
                try:
                    sql = 'INSERT INTO player (username, password) VALUES (%s, %s)'
                    val = (username, passhash)
                    cursor.execute(sql, val)
                    db.commit()
                    print('Sign up successfull, go back and log in')
                except:
                    print('sign up unsucessful')
    sign_up_menu.add_button('Sign Up', register)

    # -------------------------------------------------------------------------
    # Log In Menu
    # -------------------------------------------------------------------------
    log_in_menu = pygame_menu.themes.THEME_BLUE.copy()
    log_in_menu.widget_offset = (0, 0.09)
    log_in_menu.title_font = pygame_menu.font.FONT_COMIC_NEUE
    log_in_menu.widget_font = pygame_menu.font.FONT_COMIC_NEUE
    log_in_menu.widget_font_size = 30
    log_in_menu = pygame_menu.Menu(
        height=WINDOW_SIZE[1],
        width=WINDOW_SIZE[0],
        onclose=pygame_menu.events.EXIT,  # User press ESC button
        title='Log in menu',
        theme=pygame_menu.themes.THEME_BLUE,
    )
    click_sound(log_in_menu)
    log_in_menu.add_text_input('Username: ',
                               textinput_id='username')
    log_in_menu.add_text_input('Password: ',
                               password=True,
                               textinput_id='password')

    def check_login():
        global logged_in
        data = log_in_menu.get_input_data()
        username, password = data['username'], data['password']
        passhash = hashlib.sha256()
        passhash.update(password.encode('utf-8'))
        passhash = passhash.hexdigest()
        password = 0 #clears raw password variable
        db = mysql.connector.connect(host='localhost', user='root', passwd='root', database='tiled_game')
        cursor = db.cursor()
        sql = 'SELECT password, playerID FROM player WHERE username=%s;'
        val = (username,)
        cursor.execute(sql, val)
        result = cursor.fetchone()
        try:
            dbhash = result[0]
            if dbhash == passhash:
                log_in_menu.disable()
                logged_in = True
                global LOGGEDIN_PLAYERID
                LOGGEDIN_PLAYERID = result[1]
                print(LOGGEDIN_PLAYERID)
        except:
            pass

    log_in_menu.add_button('Log In', check_login)
    log_in_menu.add_button('Sign Up', sign_up_menu)

    # -------------------------------------------------------------------------
    # Main loop
    # -------------------------------------------------------------------------
    while True:

        # Tick
        clock.tick(FPS)

        # Paint background
        main_background()

        # Main menu
        log_in_menu.mainloop(surface, main_background, fps_limit=FPS)

        # Flip surface
        pygame.display.flip()

        if logged_in == True:
            main()

        # At first loop returns
        #if test:
        #    break


if __name__ == '__main__':
    start()
