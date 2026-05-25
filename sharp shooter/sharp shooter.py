import pygame

pygame.init()

WIDTH = 500
HEIGHT = 500
FPS = 25
MAX_BULLETS = 5

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sharp Shooter")
clock = pygame.time.Clock()

background_image = pygame.image.load("images/bg_img.jpeg")
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

player_walk_right = [pygame.image.load(f"soldier/{i}.png") for i in range(1, 10)]
player_walk_left = [pygame.image.load(f"soldier/L{i}.png") for i in range(1, 10)]

enemy_walk_right = [pygame.image.load(f"enemy/R{i}.png") for i in range(1, 10)]
enemy_walk_left = [pygame.image.load(f"enemy/L{i}.png") for i in range(1, 10)]

font = pygame.font.SysFont("helvetica", 30, bold=True)
game_over_font = pygame.font.SysFont("helvetica", 50, bold=True)
win_font = pygame.font.SysFont("helvetica", 50, bold=True)
button_font = pygame.font.SysFont("helvetica", 28, bold=True)

score = 0

bullet_sound = pygame.mixer.Sound("sounds/Bulletsound.mp3")
hit_sound = pygame.mixer.Sound("sounds/Hit.mp3")

pygame.mixer.music.load("sounds/music.mp3")
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)


class Player:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5

        self.is_jump = False
        self.jump_count = 10

        self.left = False
        self.right = False
        self.walk_count = 0
        self.standing = True

        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, screen):
        if self.walk_count + 1 >= 27:
            self.walk_count = 0

        if not self.standing:
            if self.left:
                screen.blit(player_walk_left[self.walk_count // 3], (self.x, self.y))
            elif self.right:
                screen.blit(player_walk_right[self.walk_count // 3], (self.x, self.y))

            self.walk_count += 1

        else:
            if self.right:
                screen.blit(player_walk_right[0], (self.x, self.y))
            else:
                screen.blit(player_walk_left[0], (self.x, self.y))

        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)


class Projectile:
    def __init__(self, x, y, radius, color, direction):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.direction = direction
        self.vel = 8 * direction

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)


class Enemy:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.walk_count = 0
        self.vel = 2

        self.hitbox = pygame.Rect(
            self.x + 20,
            self.y,
            self.width - 40,
            self.height - 4,
        )

        self.health = 9
        self.visible = True

    def draw(self, screen):
        if self.visible:

            if self.walk_count + 1 >= 27:
                self.walk_count = 0

            screen.blit(
                enemy_walk_left[self.walk_count // 3],
                (self.x, self.y),
            )

            self.walk_count += 1

            self.hitbox = pygame.Rect(
                self.x + 20,
                self.y,
                self.width - 40,
                self.height - 4,
            )

            # Health bar
            pygame.draw.rect(
                screen,
                "grey",
                (self.hitbox.x, self.hitbox.y + 3, 50, 10),
            )

            pygame.draw.rect(
                screen,
                "green",
                (
                    self.hitbox.x,
                    self.hitbox.y + 3,
                    50 - (5.5 * (9 - self.health)),
                    10,
                ),
            )

    # Enemy always moves RIGHT -> LEFT
    def move_toward_player(self):
        if self.visible:
            self.x -= self.vel

    def take_damage(self):
        global score

        hit_sound.play()

        if self.health > 0:
            self.health -= 1
        else:
            self.visible = False
            score += 1


class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text

    def draw(self, screen):
        pygame.draw.rect(screen, "white", self.rect, border_radius=8)
        pygame.draw.rect(screen, "black", self.rect, 2, border_radius=8)

        txt = button_font.render(self.text, True, "black")

        screen.blit(
            txt,
            (
                self.rect.x + (self.rect.width - txt.get_width()) // 2,
                self.rect.y + (self.rect.height - txt.get_height()) // 2,
            ),
        )

    def clicked(self, pos):
        return self.rect.collidepoint(pos)


def create_enemies():
    return [
        Enemy(350, HEIGHT - 64, 64, 64),
        Enemy(430, HEIGHT - 64, 64, 64),
        Enemy(510, HEIGHT - 64, 64, 64),
    ]


def reset_game():
    global score

    score = 0

    player = Player(210, 435, 64, 64)

    bullets = []

    enemies = create_enemies()

    shoot_delay = 0
    game_over = False
    game_win = False

    return player, bullets, enemies, shoot_delay, game_over, game_win


def draw_window(player, enemies, bullets):
    screen.blit(background_image, (0, 0))

    player.draw(screen)

    for enemy in enemies:
        enemy.draw(screen)

    score_text = font.render(f"Score: {score}", True, "red")
    screen.blit(score_text, (0, 10))

    for bullet in bullets:
        bullet.draw(screen)

    pygame.display.flip()


def main():
    global score

    player, bullets, enemies, shoot_delay, game_over, game_win = reset_game()

    restart_button = Button(
        WIDTH // 2 - 75,
        HEIGHT // 2 + 40,
        150,
        50,
        "Restart",
    )

    running = True

    while running:

        clock.tick(FPS)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            if (game_over or game_win) and event.type == pygame.MOUSEBUTTONDOWN:

                if restart_button.clicked(event.pos):
                    (
                        player,
                        bullets,
                        enemies,
                        shoot_delay,
                        game_over,
                        game_win,
                    ) = reset_game()

        if not game_over and not game_win:

            # Enemy movement
            for enemy in enemies:
                enemy.move_toward_player()

                if enemy.visible and player.hitbox.colliderect(enemy.hitbox):
                    game_over = True
                    break

            # WIN CONDITION
            if all(not enemy.visible for enemy in enemies):
                game_win = True

            # Bullet delay
            if shoot_delay > 0:
                shoot_delay += 1

            if shoot_delay > 3:
                shoot_delay = 0

            # Bullet movement
            for bullet in bullets[:]:

                bullet.x += bullet.vel

                if bullet.x < 0 or bullet.x > WIDTH:
                    bullets.remove(bullet)
                    continue

                for enemy in enemies:

                    if enemy.visible and (
                        bullet.y - bullet.radius < enemy.hitbox.y + enemy.hitbox.height
                        and bullet.y + bullet.radius > enemy.hitbox.y
                        and bullet.x + bullet.radius > enemy.hitbox.x
                        and bullet.x - bullet.radius < enemy.hitbox.x + enemy.hitbox.width
                    ):

                        if bullet in bullets:
                            bullets.remove(bullet)

                        enemy.take_damage()
                        break

            keys = pygame.key.get_pressed()

            # Shooting
            if keys[pygame.K_SPACE] and shoot_delay == 0:

                bullet_sound.play()

                direction = 1 if player.right else -1

                if len(bullets) < MAX_BULLETS:

                    bullets.append(
                        Projectile(
                            player.x + player.width // 2,
                            player.y + player.height // 2,
                            6,
                            "black",
                            direction,
                        )
                    )

                shoot_delay = 1

            # Movement
            if keys[pygame.K_LEFT] and player.x > 0:

                player.x -= player.vel
                player.left = True
                player.right = False
                player.standing = False

            elif keys[pygame.K_RIGHT] and player.x < WIDTH - player.width:

                player.x += player.vel
                player.right = True
                player.left = False
                player.standing = False

            else:
                player.standing = True
                player.walk_count = 0

            # Jumping
            if not player.is_jump:

                if keys[pygame.K_UP]:
                    player.is_jump = True
                    player.left = False
                    player.right = False

            else:

                if player.jump_count >= -10:

                    neg = 1

                    if player.jump_count < 0:
                        neg = -1

                    player.y -= (player.jump_count ** 2) * neg * 0.5

                    player.jump_count -= 1

                else:
                    player.jump_count = 10
                    player.is_jump = False

            draw_window(player, enemies, bullets)

        else:

            screen.blit(background_image, (0, 0))

            if game_over:
                text = game_over_font.render("GAME OVER", True, "red")

            
            elif game_win:
                text = win_font.render("YOU WIN!", True, "green")

            screen.blit(
                text,
                (
                    WIDTH // 2 - text.get_width() // 2,
                    HEIGHT // 2 - text.get_height() // 2 - 40,
                ),
            )

            restart_button.draw(screen)

            pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()