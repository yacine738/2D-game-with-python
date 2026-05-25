import pygame
import random

pygame.init()

w_width = 660
w_height = 600

window = pygame.display.set_mode((w_width, w_height))
pygame.display.set_caption("Spaceship")

bg = pygame.image.load("media/bg.png")
bg = pygame.transform.scale(bg, (w_width, w_height))

spaceship_img = pygame.image.load("media/spaceship.png")
bullet = pygame.image.load("media/bullet.png")
enemy_img = [pygame.image.load(f"media/alien{i}.png") for i in range(1, 6)]
enemy_bullet = pygame.image.load("media/alien_bullet.png")

explosion = pygame.mixer.Sound("media/explosion.wav")
explosion2 = pygame.mixer.Sound("media/explosion2.wav")
laser = pygame.mixer.Sound("media/laser.wav")

clock = pygame.time.Clock()

rows = 4
cols = 5

alien_cooldown = 1000
last_alien_shot = pygame.time.get_ticks()

shoot_counter = 0
score = 0

font1 = pygame.font.SysFont("helvetica", 30, 1, 1)
font2 = pygame.font.SysFont("serif", 50, 1)


class Spaceship:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 75
        self.height = 75
        self.vel = 8
        self.health = 5
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, window):
        if self.health > 0:
            window.blit(spaceship_img, (self.x, self.y))

            pygame.draw.rect(
                window,
                "red",
                (self.x, self.y + self.height, self.width, 10),
            )

            pygame.draw.rect(
                window,
                "green",
                (
                    self.x,
                    self.y + self.height,
                    round(self.width * (self.health / 5)),
                    10,
                ),
            )

            self.rect = pygame.Rect(self.x, self.y, self.width, self.height)


class Projectile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 11
        self.height = 11
        self.vel = 6
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, window):
        self.y -= self.vel
        window.blit(bullet, (self.x, self.y))
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)


class Enemies:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 64
        self.height = 64
        self.image = enemy_img[random.randint(0, 4)]
        self.move_counter = 0
        self.direction = 1
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, window):
        window.blit(self.image, (self.x, self.y))

        self.x += self.direction
        self.move_counter += 1

        if abs(self.move_counter) > 100:
            self.direction *= -1
            self.move_counter *= -1

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)


class EnemyProjectile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel = 4
        self.width = 13
        self.height = 13
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, window):
        self.y += self.vel
        window.blit(enemy_bullet, (self.x, self.y))
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)


def display_score(score):
    score_text = font1.render("Score: " + str(score), True, "white")
    window.blit(score_text, (10, 10))


def game_over_screen():
    text = font2.render("GAME OVER", True, "red")
    window.blit(text, (150, 250))


def win_screen():
    text = font2.render("YOU WIN!", True, "green")
    window.blit(text, (180, 250))


def draw_restart_button():
    button_rect = pygame.Rect(220, 350, 220, 60)

    pygame.draw.rect(window, "white", button_rect)

    text = font1.render("Restart", True, "black")
    window.blit(text, (280, 365))

    return button_rect


def create_enemies():
    enemies = []

    for row in range(rows):
        for col in range(cols):
            enemies.append(Enemies(100 + col * 100, 100 + row * 70))

    return enemies


def reset_game():
    global spaceship
    global enemies
    global bullets
    global alien_bullets
    global score
    global game_over
    global game_win

    spaceship = Spaceship(round(w_width / 2) - 34, w_height - 100)

    enemies = create_enemies()

    bullets = []
    alien_bullets = []

    score = 0

    game_over = False
    game_win = False


spaceship = Spaceship(round(w_width / 2) - 34, w_height - 100)

enemies = create_enemies()

bullets = []
alien_bullets = []

game_over = False
game_win = False

run = True

while run:

    clock.tick(60)

    window.blit(bg, (0, 0))

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            run = False

        if (game_over or game_win) and event.type == pygame.MOUSEBUTTONDOWN:

            mouse_pos = pygame.mouse.get_pos()

            if restart_button.collidepoint(mouse_pos):
                reset_game()

    if not game_over and not game_win:

        time_now = pygame.time.get_ticks()

        if (
            time_now - last_alien_shot > alien_cooldown
            and len(alien_bullets) < 5
            and len(enemies) > 0
        ):

            attacking_alien = random.choice(enemies)

            alien_bullets.append(
                EnemyProjectile(
                    attacking_alien.x + 25,
                    attacking_alien.y + 50,
                )
            )

            last_alien_shot = time_now

        for alien_bullet_obj in alien_bullets[:]:

            if spaceship.rect.colliderect(alien_bullet_obj.rect):

                spaceship.health -= 1

                alien_bullets.remove(alien_bullet_obj)

                explosion.play()

        if spaceship.health <= 0:
            game_over = True

        if len(enemies) == 0:
            game_win = True

        for enemy in enemies[:]:

            for projectile in bullets[:]:

                if enemy.rect.colliderect(projectile.rect):

                    bullets.remove(projectile)

                    enemies.remove(enemy)

                    explosion2.play()

                    score += 1

                    break

        for alien_bullet_obj in alien_bullets[:]:

            if alien_bullet_obj.y > w_height:
                alien_bullets.remove(alien_bullet_obj)

        if shoot_counter > 0:
            shoot_counter += 1

        if shoot_counter > 10:
            shoot_counter = 0

        for projectile in bullets[:]:

            if projectile.y > 0:
                projectile.y -= projectile.vel
            else:
                bullets.remove(projectile)

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and spaceship.x > 0:
            spaceship.x -= spaceship.vel

        if keys[pygame.K_RIGHT] and spaceship.x < w_width - spaceship.width:
            spaceship.x += spaceship.vel

        if keys[pygame.K_SPACE] and shoot_counter == 0:

            laser.play()

            if len(bullets) < 5:

                bullets.append(
                    Projectile(
                        spaceship.x + round(spaceship.width / 2),
                        spaceship.y,
                    )
                )

            shoot_counter = 1

        display_score(score)

        spaceship.draw(window)

        for enemy in enemies:
            enemy.draw(window)

        for projectile in bullets:
            projectile.draw(window)

        for alien_bullet_obj in alien_bullets:
            alien_bullet_obj.draw(window)

    elif game_over:

        game_over_screen()

        restart_button = draw_restart_button()

    elif game_win:

        win_screen()

        restart_button = draw_restart_button()

    pygame.display.flip()

pygame.quit()