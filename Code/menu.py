# menu.py

from graphics import *
from button2 import Button
from PIL import Image as PILImage
from os.path import join

win = GraphWin("Game",1000,800)

class Menu():
        
    def __init__(self, win, levels):
        self.levels = levels
        self.win = win
        self.win.setBackground("orange")
        heading = Text(Point(500,50), "Kitchen Adventures")
        heading.setSize(30)
        heading.setTextColor("red")
        heading.draw(self.win)
        self.path_1 = join("simple_game", "kirby_1.gif")
        self.path_2 = join("simple_game", "kirby_2.gif")
        self.draw_images()
        
    def convert_and_resize(self, new_width, new_height, path):
        img = PILImage.open(path)
        img_resized = img.resize((new_width, new_height), PILImage.LANCZOS)
        img_resized.save(path, "GIF")
        
    def draw_images(self):
        self.convert_and_resize(150,150, self.path_1)
        self.convert_and_resize(150,150, self.path_2)
        kirby_1 = Image(Point(200,700), self.path_1)
        kirby_1.draw(self.win)
        kirby_2 = Image(Point(800,700), self.path_2)
        kirby_2.draw(self.win)

    def menu_loop(self):
        self.load_buttons()
        win.getMouse()
        
    def load_buttons(self):
        quit_button = Button(self.win, Point(500, 700), 200, 100, "Quit")
        button_level_1 = Button(self.win, Point(170,200), 200, 200, "Level 1")
        button_level_2 = Button(self.win, Point(390,200), 200, 200, "Level 2")
        button_level_3 = Button(self.win, Point(610,200), 200, 200, "Level 3")
        button_level_4 = Button(self.win, Point(830,200), 200, 200, "Level 4")
        button_level_5 = Button(self.win, Point(170,430), 200, 200, "Level 5")
        button_level_6 = Button(self.win, Point(390,430), 200, 200, "Level 6")
        button_level_7 = Button(self.win, Point(610,430), 200, 200, "Level 7")
        button_level_8 = Button(self.win, Point(830,430), 200, 200, "To be continued..")
        self.buttons = [quit_button, button_level_1, button_level_2, button_level_3, button_level_4, button_level_5, button_level_6, button_level_7]
        for button in self.buttons:
            button.activate()
    
    def load_level(self):
        level = self.handle_click()
        self.game_loop(click)
        
    def undraw_level(self):
        for obstacle in self.obstacles:
            obstacle.undraw()
        for ingredient in self.ingredients:
            ingredient.undraw()
        
    def game_loop(self, level):
        run = True
        level()
        while run:
            self.handle_movement()
            
if __name__  == "__main__":
    menu = Menu(win,[1])
    menu.menu_loop()