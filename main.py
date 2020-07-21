
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

config = ConfigParser()



def start_game():
    g = Game()
    g.load_data()
    #g.show_start_screen()
    g.new()  #is being called by the menu, kept here for logical sense.
    g.run()
    g.show_over_screen()
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


def main(test=False):
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
    main_menu.add_button('Log Out', log_out)
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
        password = 0
        db = mysql.connector.connect(host='localhost', user='root', passwd='root', database='tiled_game')
        cursor = db.cursor()
        sql = 'SELECT password FROM player WHERE username=%s;'
        val = (username,)
        cursor.execute(sql, val)
        result = cursor.fetchone()
        try:
            dbhash = result[0]
            if dbhash == passhash:
                log_in_menu.disable()
                logged_in = True
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








