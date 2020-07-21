'''
for display purposes
only has game running once,
no sql, no log in and main screen
'''
from game import *


g = Game()
g.load_data()
#g.show_start_screen()
g.new()  #is being called by the menu, kept here for logical sense.
g.run()
g.show_over_screen()
g.stop()
pg.quit()