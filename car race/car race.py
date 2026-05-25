import pygame
import time
import random

pygame.init()

w_width = 500
w_height = 500

window = pygame.display.set_mode((w_width, w_height))
pygame.display.set_caption("Car race")

# game variables
clock = pygame.time.Clock()
font = pygame.font.SysFont("helvetica", 50, 1)
font2 = pygame.font.SysFont("helvetica", 20, 1)
font3 = pygame.font.SysFont(None, 30)

bg_speed = 5
score = 0
level = 1
next_level = 5

# importing images
car_img = pygame.image.load("img/car1.png")
grass = pygame.image.load("img/grass.jpg")
yellow_line = pygame.image.load("img/yellow_line.jpg")
white_line = pygame.image.load("img/white_line.jpg")
enemy_car_imgs = [
    pygame.image.load("img/car2.png"),
    pygame.image.load("img/car3.png")
]

bg = pygame.image.load("img/bg.jpeg")
bg = pygame.transform.scale(bg, (w_width, w_height))


# displaying text on the screen
def text_display(score, level):
    score_text = font2.render("Score : " + str(score), True, "black")
    level_text = font2.render("Level : " + str(level), True, "black")

    window.blit(score_text, (10, 10))
    window.blit(level_text, (w_width - level_text.get_width() - 10, 10))


# Button class
class Button():
    def __init__(self, x, y, width, height, text, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.is_hovered = False

    def draw(self):
        color = "gray" if self.is_hovered else "white"

        pygame.draw.rect(window, color, self.rect)
        pygame.draw.rect(window, "black", self.rect, 3)

        text_surface = font3.render(self.text, True, "black")
        text_rect = text_surface.get_rect(center=self.rect.center)

        window.blit(text_surface, text_rect)

    def check_hover(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def perform_action(self):
        self.action()


# Car class
class Car():
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.width = 28
        self.height = 54
        self.vel = 5

    def draw(self):
        window.blit(self.img, (self.x, self.y))


# Enemy car class
class EnemyCar(Car):
    def __init__(self, x, y, img):
        super().__init__(x, y, img)
        self.height = 69
        self.vel = 5

    def move(self):
        self.y += self.vel

    def draw(self):
        window.blit(self.img, (self.x, self.y))


# drawing background
def drawing_background():
    bg_y = pygame.time.get_ticks() // bg_speed

    # top part
    window.blit(grass, (0, bg_y % w_height - w_height))
    window.blit(grass, (420, bg_y % w_height - w_height))

    window.blit(white_line, (90, bg_y % w_height - w_height))
    window.blit(white_line, (405, bg_y % w_height - w_height))

    for i in range(5):
        window.blit(yellow_line, (225, (bg_y + i * 100) % w_height - w_height))

    # bottom part
    window.blit(grass, (0, bg_y % w_height))
    window.blit(grass, (420, bg_y % w_height))

    window.blit(white_line, (90, bg_y % w_height))
    window.blit(white_line, (405, bg_y % w_height))

    for i in range(5):
        window.blit(yellow_line, (225, (bg_y + i * 100) % w_height))


# start game
def start_game():

    global score, level, next_level, bg_speed

    score = 0
    level = 1
    next_level = 5
    bg_speed = 5

    # main car
    maincar = Car(250, 350, car_img)

    # enemy cars
    enemy_cars = []

    for i in range(3):
        x = random.randint(100, 370)
        y = random.randint(-600, -100)

        enemy_car = EnemyCar(
            x,
            y,
            random.choice(enemy_car_imgs)
        )

        enemy_cars.append(enemy_car)

    # crash screen
    def crash_screen():
        crashed = True

        restart_button = Button(120, 320, 120, 60, "Restart", None)
        quit_button = Button(270, 320, 120, 60, "Quit", None)

        while crashed:

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                elif event.type == pygame.MOUSEMOTION:
                    mouse_pos = pygame.mouse.get_pos()

                    restart_button.check_hover(mouse_pos)
                    quit_button.check_hover(mouse_pos)

                elif event.type == pygame.MOUSEBUTTONDOWN:

                    mouse_pos = pygame.mouse.get_pos()

                    # restart game
                    if restart_button.rect.collidepoint(mouse_pos):
                        crashed = False
                        start_game()

                    # quit game
                    elif quit_button.rect.collidepoint(mouse_pos):
                        pygame.quit()
                        quit()

            window.fill((150, 150, 150))

            crash_text = font.render("CAR CRASHED", True, "black")
            text_rect = crash_text.get_rect(center=(w_width // 2, 200))

            window.blit(crash_text, text_rect)

            restart_button.draw()
            quit_button.draw()

            pygame.display.update()

    # game loop
    running = True

    while running:

        clock.tick(60)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()

        # movement
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and maincar.x > 95:
            maincar.x -= maincar.vel

        if keys[pygame.K_RIGHT] and maincar.x < 405 - maincar.width:
            maincar.x += maincar.vel

        if keys[pygame.K_UP] and maincar.y > 0:
            maincar.y -= maincar.vel

        if keys[pygame.K_DOWN] and maincar.y < w_height - maincar.height:
            maincar.y += maincar.vel

        # check road boundaries
        if maincar.x < 95 or maincar.x > 405 - maincar.width:
            crash_screen()

        # enemy cars
        for enemy_car in enemy_cars:

            enemy_car.move()

            # collision detection
            if (
                enemy_car.x < maincar.x + maincar.width
                and enemy_car.x + enemy_car.width > maincar.x
                and enemy_car.y < maincar.y + maincar.height
                and enemy_car.y + enemy_car.height > maincar.y
            ):
                crash_screen()

            # respawn enemy car
            if enemy_car.y > w_height:

                enemy_car.x = random.randint(100, 370)
                enemy_car.y = random.randint(-600, -100)
                enemy_car.img = random.choice(enemy_car_imgs)

                score += 1

                # level system
                if score >= next_level:
                    level += 1
                    next_level += 5

                    for car in enemy_cars:
                        car.vel += 1

        # draw everything
        window.fill((136, 134, 134))

        drawing_background()

        maincar.draw()

        for enemy_car in enemy_cars:
            enemy_car.draw()

        text_display(score, level)

        pygame.display.update()


# quit game
def quit_game():
    pygame.quit()
    quit()


# buttons
start_button = Button(200, 200, 100, 60, "Start", start_game)
quit_button = Button(200, 300, 100, 60, "Quit", quit_game)


# menu loop
menu_running = True

while menu_running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        elif event.type == pygame.MOUSEMOTION:

            mouse_pos = pygame.mouse.get_pos()

            start_button.check_hover(mouse_pos)
            quit_button.check_hover(mouse_pos)

        elif event.type == pygame.MOUSEBUTTONDOWN:

            mouse_pos = pygame.mouse.get_pos()

            if start_button.rect.collidepoint(mouse_pos):
                start_button.perform_action()

            elif quit_button.rect.collidepoint(mouse_pos):
                quit_button.perform_action()

    # draw menu
    window.blit(bg, (0, 0))

    title = font.render("CAR RACE", True, "white")
    title_rect = title.get_rect(center=(w_width // 2, 100))

    window.blit(title, title_rect)

    start_button.draw()
    quit_button.draw()

    pygame.display.update()