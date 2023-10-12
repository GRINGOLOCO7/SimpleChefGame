from graphics import *
from button2 import Button
# from menu import Menu
from timer import timer
from os.path import join
from PIL import Image as PILImage
import time
#import cv2

class GraphicalInterface:
    brown = color_rgb(139, 69, 19)
    pink = color_rgb(223, 109, 169)

    def __init__(self):
        # Class initialization
        # We need a few things so we can create our level,like the window, our white window
        # Some variables we will access and that are going to be instance variables of the object
        # As well as our character, velocity, a buttons class so we can handle the clicks
        self.video_played = True
        self.already_cooked = True
        self.win_or_loss = False
        self.time_left = True
        self.ingredient_count = 0
        self.ingredients_level = 0
        self.win = GraphWin("Game", 1000, 800)  # --> to adapt
        self.win.setBackground("orange")
        self.path_stove = join("stove.gif")  # "simple_game", "stove.gif"
        self.path_1 = join("kirby_1.gif")  # "simple_game", "kirby_1.gif"
        self.path_2 = join("kirby_2.gif")  # "simple_game", "kirby_2.gif"
        #self.video_path = join("simple_game","chef_intro_cinematic_final.mp4")
        self.convert_and_resize(50, 50, self.path_stove)
        self.vel = 15

    def start_timer(self):
        self.start_time = time.time()
        self.last_update_time = self.start_time
        self.last_seconds = 60
        self.seconds = self.last_seconds

        self.timer_text = Text(Point(800, 150), "Ready?")  # Adjust position as needed
        self.timer_text.setSize(36)
        self.timer_text.draw(self.win)

    def update_timer(self, start_seconds=5):
        current_time = time.time()
        if current_time - self.last_update_time >= 1:  # Only update once per second
            elapsed_time = current_time - self.start_time
            self.seconds = start_seconds - int(elapsed_time)

            # Check if a second has passed since last update
            if self.seconds != self.last_seconds:
                if self.seconds < 0:  # If the time has run out
                    self.seconds = 0  # Keep the time at 0

                self.timer_text.setText(f"Time left: {self.seconds:02d}")
                self.last_seconds = self.seconds

            self.last_update_time = current_time  # Record the time of this update

        if self.seconds <= 0:  # exit if the window is clicked or time is up
            self.time_left = False
            self.times_up()
            
    def times_up(self):
        self.times_up_screen = Rectangle(Point(200, 300), Point(800, 600))
        self.times_up_screen.setFill("lightgrey")
        self.label_time = Text(Point(500, 365), "Oops!")
        self.label_time.setSize(20)
        self.label_time2 = Text(
        Point(500, 400), "Your time ran out! Go to the menu to try again!")
        self.label_time2.setSize(20)
        self.times_up_screen.draw(self.win)
        button_menu = Button(
        self.win, Point(500, 500), 200, 50, 'Press "M" to go the Menu!')
        button_menu.activate()
        self.buttons.append(button_menu)
        self.label_time.draw(self.win)
        self.label_time2.draw(self.win)
        



    # This function is used to resize the images to our desired size.
    # We need to input an image that is in GIF format!!!

    def convert_and_resize(self, new_width, new_height, path):
        img = PILImage.open(path)
        img_resized = img.resize((new_width, new_height), PILImage.LANCZOS)
        img_resized.save(path, "GIF")

    def handle_movement(self):
        key = self.win.getKey()
        new_x, new_y = (
            self.character.getCenter().getX(),
            self.character.getCenter().getY(),
        )

        if key == "d":
            new_x += self.vel
        elif key == "a":
            new_x -= self.vel
        elif key == "w":
            new_y -= self.vel
        elif key == "s":
            new_y += self.vel
            
        # CASES FOR WHEN TIME RUNS OUT
        elif key == "m" and self.level == 1 and not self.time_left:
            self.undraw_level()
            self.tutorial.undraw()
            self.timer_text.undraw()
            for arrow in self.arrows:
                arrow.undraw()
            self.label_time.undraw()
            self.label_time2.undraw()
            self.times_up_screen.undraw()
            self.full_loop()
        elif key == "m" and not self.time_left:
            self.undraw_level()
            self.timer_text.undraw()
            self.label_time.undraw()
            self.label_time2.undraw()
            self.times_up_screen.undraw()
            self.full_loop()

        # CASES FOR WHEN YOU PRESS M AFTER WINNING
        elif key == "m" and self.level == 1 and self.win_or_loss:
            self.timer_text.undraw()
            self.undraw_level()
            for arrow in self.arrows:
                arrow.undraw()
            self.tutorial.undraw()
            self.win_screen.undraw()
            self.label2.undraw()
            self.label.undraw()
            self.full_loop()
        
        elif key == "m" and self.win_or_loss:
            self.timer_text.undraw()
            self.undraw_level()
            self.win_screen.undraw()
            self.label2.undraw()
            self.label.undraw()
            self.full_loop()
            
         # CASES FOR WHEN YOU PRESS M WHILE PLAYING
        elif key == "m" and self.level == 1:
            self.timer_text.undraw()
            self.undraw_level()
            for arrow in self.arrows:
                arrow.undraw()
            self.tutorial.undraw()
            self.full_loop()
            
        elif key == "m":
            self.timer_text.undraw()
            self.undraw_level()
            self.full_loop()
            
        
            
            
        if (
                self.room_example.getP1().getX() + 10 <= new_x <= self.room_example.getP2().getX() - 10
                and self.room_example.getP1().getY() + 10 <= new_y <= self.room_example.getP2().getY() - 10
                and not self.check_collision(new_x, new_y)
                and not self.stove_check(new_x, new_y, 20, 20)
        ):
            self.last_move = self.character.move(
                new_x - self.character.getCenter().getX(),
                new_y - self.character.getCenter().getY(),
            )
        
        elif self.stove_check(new_x, new_y, 20, 20) and self.already_cooked:
            self.cooking()
            self.already_cooked = False
        ingredient_check = self.check_ingredients(new_x, new_y)
        if ingredient_check[0]:
            self.into_inventory(ingredient_check[1])

    # This methods creates the levels. We will need to call these methods
    # In our main loop when we have the menu created.
    # They will be called when we click on the level on the menu
    # As you can see, when calling these methods, we create a series of graphical objects
    # That are part of the level
    # We also need to create a function to undraw everything in the level before creating a new one.
    def level_1_set(self):  # --> 3 ingredients and some instruction for the user
        self.level = 1
        self.ingredients_level = 3
        self.win.setBackground("lightgrey")
        self.main_screen = Rectangle(Point(50, 50), Point(950, 750))
        self.main_screen.setFill("white")
        self.main_screen.draw(self.win)
        self.inventory()
        self.buttons = []
        self.quit = Button(self.win, Point(950, 50), 100, 25, "Pres \"M\" for Menu")
        self.quit.activate()
        self.room_example = Rectangle(Point(100, 300), Point(900, 500))
        self.room_example.setFill(self.brown)
        self.room_example.draw(self.win)

        ## put character in the left center
        self.character = Circle(Point(120, 400), 10)
        self.character.setFill(self.pink)
        self.character.draw(self.win)

        self.stove = Image(Point(130, 450), self.path_stove)
        self.stove.draw(self.win)

        self.tutorial = Text(Point(365, 280),"Collect all the ingredients and bring them in the stove before the time runs out",).draw(self.win)
        self.arrow1= Text(Point(205, 340), "==>").draw(self.win)
        self.arrow2 = Text(Point(565, 410), "<==").draw(self.win)
        self.arrow3 = Text(Point(665, 460), "==>").draw(self.win)
        self.arrows = [self.arrow1, self.arrow2, self.arrow3]

        obstacle1 = Rectangle(Point(450, 350), Point(480, 450))
        obstacle1.setFill("gray")
        obstacle1.draw(self.win)
        self.obstacles = [obstacle1]

        ingredient_1 = Oval(Point(500, 400), Point(550, 420))
        ingredient_1.setFill("green")
        ingredient_1.draw(self.win)

        ingredient_2 = Polygon(Point(250, 330), Point(220, 350), Point(220, 330))
        ingredient_2.setFill("yellow")
        ingredient_2.draw(self.win)

        ingredient_3 = Rectangle(Point(680, 450), Point(700, 470))
        ingredient_3.setFill("red")
        ingredient_3.draw(self.win)

        self.ingredients = [ingredient_1, ingredient_2, ingredient_3]

    def level_2_set(self):  # --> 3 ingredients
        self.level = 2
        self.ingredients_level = 3
        self.win.setBackground("lightgrey")
        self.main_screen = Rectangle(Point(50, 50), Point(950, 750))
        self.main_screen.setFill("white")
        self.main_screen.draw(self.win)
        self.inventory()
        self.buttons = []
        self.quit = Button(self.win, Point(950, 50), 100, 25, "Pres \"M\" for Menu")
        self.quit.activate()
        self.room_example = Rectangle(Point(100, 300), Point(900, 500))
        self.room_example.setFill("red")
        self.room_example.draw(self.win)

        ## put character in the left center
        self.character = Circle(Point(120, 400), 10)
        self.character.setFill(self.pink)
        self.character.draw(self.win)

        self.stove = Image(Point(130, 450), self.path_stove)
        self.stove.draw(self.win)

        obstacle1 = Rectangle(Point(400, 450), Point(900, 500))
        obstacle1.setFill("gray")
        obstacle1.draw(self.win)

        obstacle2 = Rectangle(Point(250, 300), Point(300, 450))
        obstacle2.setFill("gray")
        obstacle2.draw(self.win)

        obstacle3 = Rectangle(Point(330, 360), Point(400, 500))
        obstacle3.setFill("gray")
        obstacle3.draw(self.win)

        obstacle4 = Rectangle(Point(600, 400), Point(680, 450))
        obstacle4.setFill("gray")
        obstacle4.draw(self.win)

        obstacle5 = Rectangle(Point(600, 300), Point(680, 350))
        obstacle5.setFill("gray")
        obstacle5.draw(self.win)

        self.obstacles = [obstacle1, obstacle2, obstacle3, obstacle4, obstacle5]

        ingredient_1 = Oval(Point(700, 320), Point(750, 340))
        ingredient_1.setFill("green")
        ingredient_1.draw(self.win)

        ingredient_2 = Polygon(Point(330, 320), Point(350, 320), Point(330, 310))
        ingredient_2.setFill("yellow")
        ingredient_2.draw(self.win)

        ingredient_3 = Rectangle(Point(450, 350), Point(470, 370))
        ingredient_3.setFill("purple")
        ingredient_3.draw(self.win)

        self.ingredients = [ingredient_1, ingredient_2, ingredient_3]

    def level_3_set(self):  # --> 4 ingredients
        self.level = 3
        self.ingredients_level = 4
        self.win.setBackground("lightgrey")
        self.main_screen = Rectangle(Point(50, 50), Point(950, 750))
        self.main_screen.setFill("white")
        self.main_screen.draw(self.win)
        self.inventory()
        self.buttons = []
        self.quit = Button(self.win, Point(950, 50), 100, 25, "Pres \"M\" for Menu")
        self.quit.activate()
        self.room_example = Rectangle(Point(100, 300), Point(900, 500))
        self.room_example.setFill("cyan")
        self.room_example.draw(self.win)

        ## put character in the left center
        self.character = Circle(Point(170, 320), 10)
        self.character.setFill(self.pink)
        self.character.draw(self.win)

        self.stove = Image(Point(130, 340), self.path_stove)
        self.stove.draw(self.win)

        obstacle1 = Rectangle(Point(100, 370), Point(370, 430))
        obstacle1.setFill("gray")
        obstacle1.draw(self.win)

        obstacle2 = Rectangle(Point(400, 370), Point(750, 430))
        obstacle2.setFill("gray")
        obstacle2.draw(self.win)

        obstacle3 = Rectangle(Point(780, 370), Point(900, 430))
        obstacle3.setFill("gray")
        obstacle3.draw(self.win)

        obstacle4 = Rectangle(Point(400, 300), Point(460, 370))
        obstacle4.setFill("gray")
        obstacle4.draw(self.win)

        obstacle5 = Rectangle(Point(200, 450), Point(260, 500))
        obstacle5.setFill("gray")
        obstacle5.draw(self.win)

        self.obstacles = [obstacle1, obstacle2, obstacle3, obstacle4, obstacle5]

        ingredient_1 = Oval(Point(120, 445), Point(150, 455))
        ingredient_1.setFill("green")
        ingredient_1.draw(self.win)

        ingredient_2 = Polygon(Point(250, 330), Point(220, 350), Point(220, 330))
        ingredient_2.setFill("yellow")
        ingredient_2.draw(self.win)

        ingredient_3 = Rectangle(Point(680, 450), Point(700, 470))
        ingredient_3.setFill("red")
        ingredient_3.draw(self.win)

        ingredient_4 = Polygon(
            Point(587, 334),
            Point(593, 344),
            Point(607, 344),
            Point(613, 334),
            Point(607, 324),
            Point(593, 324),
        )
        ingredient_4.setFill("blue")
        ingredient_4.draw(self.win)

        self.ingredients = [ingredient_1, ingredient_2, ingredient_3, ingredient_4]

    def level_4_set(self):  # --> 4 ingredients
        self.level = 4
        self.ingredients_level = 4
        self.win.setBackground("lightgrey")
        self.main_screen = Rectangle(Point(50, 50), Point(950, 750))
        self.main_screen.setFill("white")
        self.main_screen.draw(self.win)
        self.inventory()
        self.buttons = []
        self.quit = Button(self.win, Point(950, 50), 100, 25, "Pres \"M\" for Menu")
        self.quit.activate()
        self.room_example = Rectangle(Point(100, 300), Point(900, 500))
        self.room_example.setFill("green")
        self.room_example.draw(self.win)

        ## put character in the left center
        self.character = Circle(Point(120, 390), 10)
        self.character.setFill(self.pink)
        self.character.draw(self.win)

        self.stove = Image(Point(130, 340), self.path_stove)
        self.stove.draw(self.win)

        obstacle1 = Rectangle(Point(200, 300), Point(240, 410))
        obstacle1.setFill("gray")
        obstacle1.draw(self.win)

        obstacle2 = Rectangle(Point(200, 410), Point(370, 450))
        obstacle2.setFill("gray")
        obstacle2.draw(self.win)

        obstacle3 = Rectangle(Point(400, 370), Point(440, 500))
        obstacle3.setFill("gray")
        obstacle3.draw(self.win)

        obstacle4 = Rectangle(Point(270, 330), Point(440, 370))
        obstacle4.setFill("gray")
        obstacle4.draw(self.win)

        obstacle5 = Rectangle(Point(440, 380), Point(700, 420))
        obstacle5.setFill("gray")
        obstacle5.draw(self.win)

        obstacle6 = Rectangle(Point(640, 450), Point(680, 500))
        obstacle6.setFill("gray")
        obstacle6.draw(self.win)

        obstacle7 = Rectangle(Point(730, 300), Point(770, 460))
        obstacle7.setFill("gray")
        obstacle7.draw(self.win)

        self.obstacles = [
            obstacle1,
            obstacle2,
            obstacle3,
            obstacle4,
            obstacle5,
            obstacle6,
            obstacle7,
        ]

        ingredient_1 = Oval(Point(510, 470), Point(530, 480))
        ingredient_1.setFill("blue")
        ingredient_1.draw(self.win)

        ingredient_2 = Rectangle(Point(830, 390), Point(850, 410))
        ingredient_2.setFill("yellow")
        ingredient_2.draw(self.win)

        ingredient_3 = Rectangle(Point(580, 340), Point(590, 350))
        ingredient_3.setFill("red")
        ingredient_3.draw(self.win)

        ingredient_4 = Rectangle(Point(260, 480), Point(275, 495))
        ingredient_4.setFill("purple")
        ingredient_4.draw(self.win)

        self.ingredients = [ingredient_1, ingredient_2, ingredient_4,ingredient_3 ]

    def level_5_set(self):  # --> 4 ingredients
        self.level = 5
        self.ingredients_level = 4
        self.win.setBackground("lightgrey")
        self.main_screen = Rectangle(Point(50, 50), Point(950, 750))
        self.main_screen.setFill("white")
        self.main_screen.draw(self.win)
        self.inventory()
        self.buttons = []
        self.quit = Button(self.win, Point(950, 50), 100, 25, "Pres \"M\" for Menu")
        self.quit.activate()
        self.room_example = Rectangle(Point(100, 300), Point(900, 600))
        self.room_example.setFill("yellow")
        self.room_example.draw(self.win)

        ## put character in the left center
        self.character = Circle(Point(120, 390), 10)
        self.character.setFill(self.pink)
        self.character.draw(self.win)

        self.stove = Image(Point(130, 340), self.path_stove)
        self.stove.draw(self.win)

        obstacle1 = Rectangle(Point(100, 450), Point(300, 490))
        obstacle1.setFill("gray")
        obstacle1.draw(self.win)

        obstacle2 = Rectangle(Point(330, 300), Point(370, 490))
        obstacle2.setFill("gray")
        obstacle2.draw(self.win)

        obstacle3 = Rectangle(Point(730, 500), Point(900, 540))
        obstacle3.setFill("gray")
        obstacle3.draw(self.win)

        obstacle4 = Rectangle(Point(460, 420), Point(500, 600))
        obstacle4.setFill("gray")
        obstacle4.draw(self.win)

        obstacle5 = Rectangle(Point(400, 380), Point(700, 420))
        obstacle5.setFill("gray")
        obstacle5.draw(self.win)

        obstacle6 = Rectangle(Point(640, 450), Point(680, 600))
        obstacle6.setFill("gray")
        obstacle6.draw(self.win)

        obstacle7 = Rectangle(Point(730, 300), Point(770, 460))
        obstacle7.setFill("gray")
        obstacle7.draw(self.win)

        self.obstacles = [
            obstacle1,
            obstacle2,
            obstacle3,
            obstacle4,
            obstacle5,
            obstacle6,
            obstacle7,
        ]

        ingredient_1 = Oval(Point(510, 470), Point(530, 480))
        ingredient_1.setFill("blue")
        ingredient_1.draw(self.win)

        ingredient_2 = Rectangle(Point(830, 390), Point(850, 410))
        ingredient_2.setFill("green")
        ingredient_2.draw(self.win)

        ingredient_3 = Rectangle(Point(140, 550), Point(150, 570))
        ingredient_3.setFill("red")
        ingredient_3.draw(self.win)

        ingredient_4 = Rectangle(Point(820, 550), Point(850, 560))
        ingredient_4.setFill("purple")
        ingredient_4.draw(self.win)

        self.ingredients = [ingredient_1, ingredient_2, ingredient_3, ingredient_4]

    def level_6_set(self):  # --> 4 ingredients
        self.level = 6
        self.ingredients_level = 4
        self.win.setBackground("lightgrey")
        self.main_screen = Rectangle(Point(50, 50), Point(950, 750))
        self.main_screen.setFill("white")
        self.main_screen.draw(self.win)
        self.inventory()
        self.buttons = []
        self.quit = Button(self.win, Point(950, 50), 100, 25, "Pres \"M\" for Menu")
        self.quit.activate()
        self.room_example = Rectangle(Point(100, 300), Point(900, 650))
        self.room_example.setFill("pink")
        self.room_example.draw(self.win)

        ## put character in the left center
        self.character = Circle(Point(120, 390), 10)
        self.character.setFill(self.pink)
        self.character.draw(self.win)

        self.stove = Image(Point(130, 340), self.path_stove)
        self.stove.draw(self.win)

        obstacle1 = Rectangle(Point(100, 450), Point(300, 490))
        obstacle1.setFill("gray")
        obstacle1.draw(self.win)

        obstacle2 = Rectangle(Point(330, 300), Point(370, 490))
        obstacle2.setFill("gray")
        obstacle2.draw(self.win)

        obstacle3 = Rectangle(Point(450, 350), Point(490, 600))
        obstacle3.setFill("gray")
        obstacle3.draw(self.win)

        obstacle4 = Rectangle(Point(490, 490), Point(900, 530))
        obstacle4.setFill("gray")
        obstacle4.draw(self.win)

        obstacle5 = Rectangle(Point(700, 300), Point(740, 450))
        obstacle5.setFill("gray")
        obstacle5.draw(self.win)

        obstacle6 = Rectangle(Point(700, 580), Point(740, 650))
        obstacle6.setFill("gray")
        obstacle6.draw(self.win)

        obstacle7 = Rectangle(Point(250, 540), Point(300, 650))
        obstacle7.setFill("gray")
        obstacle7.draw(self.win)

        self.obstacles = [
            obstacle1,
            obstacle2,
            obstacle3,
            obstacle4,
            obstacle5,
            obstacle6,
            obstacle7,
        ]

        ingredient_1 = Oval(Point(510, 470), Point(530, 480))
        ingredient_1.setFill("blue")
        ingredient_1.draw(self.win)

        ingredient_2 = Rectangle(Point(830, 390), Point(850, 410))
        ingredient_2.setFill("green")
        ingredient_2.draw(self.win)

        ingredient_3 = Rectangle(Point(140, 550), Point(150, 570))
        ingredient_3.setFill("red")
        ingredient_3.draw(self.win)

        ingredient_4 = Rectangle(Point(820, 550), Point(850, 560))
        ingredient_4.setFill("purple")
        ingredient_4.draw(self.win)

        self.ingredients = [ingredient_1, ingredient_2, ingredient_3, ingredient_4]

    def level_7_set(self):  # --> 4 ingredients
        self.level = 7
        self.ingredients_level = 5
        self.win.setBackground("lightgrey")
        self.main_screen = Rectangle(Point(50, 50), Point(950, 750))
        self.main_screen.setFill("white")
        self.main_screen.draw(self.win)
        self.inventory()
        self.buttons = []
        self.quit = Button(self.win, Point(950, 50), 100, 25, "Pres \"M\" for Menu")
        self.quit.activate()
        self.room_example = Rectangle(Point(100, 300), Point(900, 650))
        self.room_example.setFill("orange")
        self.room_example.draw(self.win)

        ## put character in the left center
        self.character = Circle(Point(530, 475), 10)
        self.character.setFill(self.pink)
        self.character.draw(self.win)

        self.stove = Image(Point(500, 475), self.path_stove)
        self.stove.draw(self.win)

        obstacle1 = Rectangle(Point(440, 520), Point(560, 560))
        obstacle1.setFill("gray")
        obstacle1.draw(self.win)

        obstacle2 = Rectangle(Point(440, 420), Point(560, 380))
        obstacle2.setFill("gray")
        obstacle2.draw(self.win)

        obstacle3 = Rectangle(Point(360, 420), Point(400, 520))
        obstacle3.setFill("gray")
        obstacle3.draw(self.win)

        obstacle4 = Rectangle(Point(600, 420), Point(640, 520))
        obstacle4.setFill("gray")
        obstacle4.draw(self.win)

        obstacle5 = Rectangle(Point(480, 300), Point(520, 380))
        obstacle5.setFill("gray")
        obstacle5.draw(self.win)

        obstacle6 = Rectangle(Point(480, 560), Point(520, 650))
        obstacle6.setFill("gray")
        obstacle6.draw(self.win)

        obstacle7 = Rectangle(Point(360, 450), Point(170, 490))
        obstacle7.setFill("gray")
        obstacle7.draw(self.win)

        obstacle8 = Rectangle(Point(640, 450), Point(830, 490))
        obstacle8.setFill("gray")
        obstacle8.draw(self.win)

        obstacle9 = Rectangle(Point(210, 300), Point(250, 450))
        obstacle9.setFill("gray")
        obstacle9.draw(self.win)

        self.obstacles = [
            obstacle1,
            obstacle2,
            obstacle3,
            obstacle4,
            obstacle5,
            obstacle6,
            obstacle7,
            obstacle8,
            obstacle9,
        ]

        ingredient_1 = Oval(Point(150, 320), Point(180, 330))
        ingredient_1.setFill("blue")
        ingredient_1.draw(self.win)

        ingredient_2 = Rectangle(Point(830, 390), Point(850, 410))
        ingredient_2.setFill("green")
        ingredient_2.draw(self.win)

        ingredient_3 = Rectangle(Point(140, 550), Point(150, 570))
        ingredient_3.setFill("red")
        ingredient_3.draw(self.win)

        ingredient_4 = Rectangle(Point(820, 550), Point(850, 560))
        ingredient_4.setFill("purple")
        ingredient_4.draw(self.win)

        ingredient_5 = Polygon(Point(300, 320), Point(320, 320), Point(320, 355))
        ingredient_5.setFill("yellow")
        ingredient_5.draw(self.win)

        self.ingredients = [ingredient_1, ingredient_2, ingredient_3, ingredient_4, ingredient_5]

    # This function checks the collisions
    # It checks if our character's coordinates intersect with the obstacle's coordinates.
    # new_x and new_y are the current coordinates of our character.
    # If we are colliding, we return True
    def check_collision(self, new_x, new_y):
        for obstacle in self.obstacles:
            if (obstacle.getP1().getX()) <= new_x <= (obstacle.getP2().getX()) and (
                obstacle.getP1().getY()
            ) <= new_y <= (obstacle.getP2().getY()):
                return True
        return False

    # This functions checks collisions with ingredients
    # We are doing pretty much the same thing that we do for obstacles
    # But we are adding functionality to check if our object is a Polygon
    # Because Polygons don't have the getP1 and getP2 methods.
    # Thus, we need to get our own minimum and maximum coordinates
    # We return True/False and the ingredient, as we want to move the ingredient we collide with
    # To the inventory
    def check_ingredients(self, new_x, new_y):
        for ingredient in self.ingredients:
            if isinstance(ingredient, Polygon):
                points = ingredient.getPoints()
                min_x = min(p.getX() for p in points)
                max_x = max(p.getX() for p in points)
                min_y = min(p.getY() for p in points)
                max_y = max(p.getY() for p in points)
            else:
                min_x, min_y = ingredient.getP1().getX(), ingredient.getP1().getY()
                max_x, max_y = ingredient.getP2().getX(), ingredient.getP2().getY()

            if (min_x - 10) <= new_x <= (max_x + 10) and (min_y - 10) <= new_y <= (
                max_y + 10
            ):
                return (True, ingredient)

        return (False, None)

    
    def handle_click(self):
        clicked_button = None
        while clicked_button is None:
            click_point = self.win.getMouse()
            #print(click_point)
            for button in self.buttons:
                if button.clicked(click_point):
                    clicked_button = button
                    break
        return clicked_button.getLabel()

    # This function constructs our inventory slots

    def inventory(self):
        heading = Text(Point(140, 150), "Inventory")
        heading.setSize(20)
        heading.draw(self.win)

        # Always draw the first 3 slots
        self.slot_1 = Rectangle(Point(100, 190), Point(160, 250))
        self.slot_1.setFill("lightgrey")
        self.slot_1.draw(self.win)
        self.slot_2 = Rectangle(Point(170, 190), Point(230, 250))
        self.slot_2.setFill("lightgrey")
        self.slot_2.draw(self.win)
        self.slot_3 = Rectangle(Point(240, 190), Point(300, 250))
        self.slot_3.setFill("lightgrey")
        self.slot_3.draw(self.win)
        self.slots = [self.slot_1, self.slot_2, self.slot_3]

        if self.ingredients_level == 4:
            self.slot_4 = Rectangle(Point(310, 190), Point(370, 250))
            self.slot_4.setFill("lightgrey")
            self.slot_4.draw(self.win)
            self.slots.append(self.slot_4)
        
        if self.ingredients_level == 5:
            self.slot_5 = Rectangle(Point(380, 190), Point(440, 250))
            self.slot_5.setFill("lightgrey")
            self.slot_5.draw(self.win)
            self.slots.append(self.slot_5)

    # This is a static method. It means that it is a function that could be outside of the class
    # But we decided to leave it inside because it has a certain relation with it
    # It just gets the center of the polygon so we can move it to the inventory
    @staticmethod
    def get_polygon_center(polygon):
        points = polygon.getPoints()
        center_x = sum(p.getX() for p in points) / len(points)
        center_y = sum(p.getY() for p in points) / len(points)
        return Point(center_x, center_y)

    # This method checks for the coordinates of the ingredients
    # and compares it to the coordinates of the slots
    # So we can then move the selected ingredient to our slot
    # we use the instance variable ingredient_count to check the slot we want to move our ingredient
    def into_inventory(self, ingredient):
        if isinstance(ingredient, Polygon):
            current_center = self.get_polygon_center(ingredient)
        else:
            current_center = ingredient.getCenter()
        current_x, current_y = current_center.getX(), current_center.getY()

        if self.ingredient_count == 0:
            dx, dy = 125 - current_x, 220 - current_y
            ingredient.move(dx, dy)
        elif self.ingredient_count == 1:
            dx, dy = 200 - current_x, 220 - current_y
            ingredient.move(dx, dy)
        elif self.ingredient_count == 2:
            dx, dy = 270 - current_x, 220 - current_y
            ingredient.move(dx, dy)
        elif self.ingredient_count == 3:
            dx, dy = 340 - current_x, 220 - current_y
            ingredient.move(dx, dy)
        elif self.ingredient_count == 4:
            dx, dy = 410 - current_x, 220 - current_y
            ingredient.move(dx, dy)
        # ingredient.move(dx, dy)
        self.ingredient_count += 1

    # This functions checks for collisions with the stove.
    # It is a bit complex but it functions in pretty much the same way as our other collisions.
    def stove_check(self, obj_x, obj_y, obj_width, obj_height):
        stove_p1 = self.stove.getAnchor()
        stove_width, stove_height = 15, 15
        stove_p2 = Point(stove_p1.getX() + stove_width, stove_p1.getY() - stove_height)

        # Check if the object is within the stove's boundaries
        return (
            (
                stove_p1.getX() <= obj_x <= stove_p2.getX()
                and stove_p1.getY() >= obj_y >= stove_p2.getY()
            )
            or (
                stove_p1.getX() <= obj_x + obj_width <= stove_p2.getX()
                and stove_p1.getY() >= obj_y >= stove_p2.getY()
            )
            or (
                stove_p1.getX() <= obj_x <= stove_p2.getX()
                and stove_p1.getY() >= obj_y - obj_height >= stove_p2.getY()
            )
            or (
                stove_p1.getX() <= obj_x + obj_width <= stove_p2.getX()
                and stove_p1.getY() >= obj_y - obj_height >= stove_p2.getY()
            )
        )

    # This loads up the winning screen if we collide with the stove and we have all ingredients
    # If we don't, we get the hurry message
    def cooking(self):
        if self.ingredient_count == self.ingredients_level:
            self.win_screen = Rectangle(Point(200, 300), Point(800, 600))
            self.win_screen.setFill("lightgrey")
            self.label2 = Text(Point(500, 365), "Congratulations!")
            self.label2.setSize(20)
            self.label = Text(
                Point(500, 400), "You managed to finish the dish on time!"
            )
            self.label.setSize(20)
            self.win_screen.draw(self.win)
            button_menu = Button(
                self.win, Point(500, 500), 200, 50, 'Press "M" to go the Menu!'
            )
            button_menu.activate()
            self.buttons.append(button_menu)
            self.label2.draw(self.win)
            self.label.draw(self.win)
            self.win_or_loss = True
        else:
            self.label = Text(
                Point(280, 520), "Hurry! You still have ingredients left!"
            )
            self.label.setSize(20)
            self.label.setFill("red")
            self.label.draw(self.win)
            time.sleep(1)
            self.label.undraw()

    def undraw_level(self):
        for obstacle in self.obstacles:
            obstacle.undraw()
        for ingredient in self.ingredients:
            ingredient.undraw()
        for button in self.buttons:
            button.undraw_button()
        for slot in self.slots:
            slot.undraw()
        self.stove.undraw()
        self.character.undraw()
        self.room_example.undraw()
        self.main_screen.undraw()
        self.quit.undraw_button()

    def menu_init(self):
        self.win.setBackground("orange")
        heading = Text(Point(500, 20), "Kitchen Adventures")
        heading.setSize(30)
        heading.setTextColor("red")
        heading.draw(self.win)
        self.draw_images()

    def draw_images(self):
        self.convert_and_resize(150, 150, self.path_1)
        self.convert_and_resize(150, 150, self.path_2)
        kirby_1 = Image(Point(200, 700), self.path_1)
        kirby_1.draw(self.win)
        kirby_2 = Image(Point(800, 700), self.path_2)
        kirby_2.draw(self.win)

    def load_buttons_menu(self):
        quit_button = Button(self.win, Point(500, 700), 200, 100, "Quit")
        button_level_1 = Button(self.win, Point(170, 200), 200, 200, "Level 1")
        button_level_2 = Button(self.win, Point(390, 200), 200, 200, "Level 2")
        button_level_3 = Button(self.win, Point(610, 200), 200, 200, "Level 3")
        button_level_4 = Button(self.win, Point(830, 200), 200, 200, "Level 4")
        button_level_5 = Button(self.win, Point(170, 430), 200, 200, "Level 5")
        button_level_6 = Button(self.win, Point(390, 430), 200, 200, "Level 6")
        button_level_7 = Button(self.win, Point(610, 430), 200, 200, "Level 7")
        button_level_8 = Button(
            self.win, Point(830, 430), 200, 200, "To be continued.."
        )
        self.buttons = [
            quit_button,
            button_level_1,
            button_level_2,
            button_level_3,
            button_level_4,
            button_level_5,
            button_level_6,
            button_level_7,
        ]
        for button in self.buttons:
            button.activate()

    def menu_set(self):
        self.menu_init()
        self.load_buttons_menu()
        self.draw_images()

    def full_loop(self):
        self.ingredient_count = 0
        self.menu_set()
        while True:
            level = self.handle_click()
            if level == "Level 1":
                self.already_cooked = True
                run = True
                self.level_1_set()
                self.start_timer()
                while run:
                    self.handle_movement()
                    if self.time_left:
                        self.update_timer(30)

            elif level == "Level 2":
                self.already_cooked = True
                run = True
                self.level_2_set()
                self.start_timer()
                while run:
                    self.handle_movement()
                    if self.time_left:
                        self.update_timer(40)

            elif level == "Level 3":
                self.already_cooked = True
                run = True
                self.level_3_set()
                self.start_timer()
                while run:
                    self.handle_movement()
                    if self.time_left:
                        self.update_timer(45)

            elif level == "Level 4":
                self.already_cooked = True
                run = True
                self.level_4_set()
                self.start_timer()
                while run:
                    self.handle_movement()
                    if self.time_left:
                        self.update_timer(45)

            elif level == "Level 5":
                self.already_cooked = True
                run = True
                self.level_5_set()
                self.start_timer()
                while run:
                    self.handle_movement()
                    if self.time_left:
                        self.update_timer(45)

            elif level == "Level 6":
                self.already_cooked = True
                run = True
                self.level_6_set()
                self.start_timer()
                while run:
                    self.handle_movement()
                    if self.time_left:
                        self.update_timer(200)

            elif level == "Level 7":
                self.already_cooked = True
                run = True
                self.level_7_set()
                self.start_timer()
                while run:
                    self.handle_movement()
                    if self.time_left:
                        self.update_timer(45)

            elif level == "Quit":
                self.win.close()

if __name__ == "__main__":
    game = GraphicalInterface()
    game.full_loop()
