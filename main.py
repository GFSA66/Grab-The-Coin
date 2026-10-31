import os
import sys
import random
import pygame


def resource_path(relative_path):
    """Путь к файлу и в обычном запуске, и внутри одного exe (PyInstaller)."""
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, relative_path)


pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Coin Collector")
pygame.display.set_icon(pygame.image.load(resource_path("assets/coin.png")))
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 32, bold=True)

bg = pygame.image.load(resource_path("assets/bg.png")).convert()
player_img = pygame.image.load(resource_path("assets/player.png")).convert_alpha()
coin_img = pygame.image.load(resource_path("assets/coin.png")).convert_alpha()
coin_sound = pygame.mixer.Sound(resource_path("assets/coin.wav"))

player = player_img.get_rect(center=(WIDTH // 2, HEIGHT // 2))
SPEED = 6


def new_coin():
    return coin_img.get_rect(topleft=(random.randint(0, WIDTH - 32),
                                    random.randint(50, HEIGHT - 32)))


coin = new_coin()
score = 0
time_left = 30.0
game_over = False

running = True
while running:
    dt = clock.tick(60) / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and game_over and event.key == pygame.K_r:
            score, time_left, game_over = 0, 30.0, False
            player.center = (WIDTH // 2, HEIGHT // 2)
            coin = new_coin()

    if not game_over:
        keys = pygame.key.get_pressed()
        player.x += (keys[pygame.K_RIGHT] or keys[pygame.K_d]) * SPEED - (keys[pygame.K_LEFT] or keys[pygame.K_a]) * SPEED
        player.y += (keys[pygame.K_DOWN] or keys[pygame.K_s]) * SPEED - (keys[pygame.K_UP] or keys[pygame.K_w]) * SPEED
        player.clamp_ip(screen.get_rect())

        if player.colliderect(coin):
            score += 1
            coin_sound.play()
            coin = new_coin()

        time_left -= dt
        if time_left <= 0:
            time_left, game_over = 0, True

    screen.blit(bg, (0, 0))
    screen.blit(coin_img, coin)
    screen.blit(player_img, player)
    screen.blit(font.render(f"Монеты: {score}", True, (255, 255, 255)), (15, 10))
    screen.blit(font.render(f"Время: {time_left:.0f}", True, (255, 220, 80)), (WIDTH - 170, 10))

    if game_over:
        msg = font.render(f"Игра окончена! Счёт: {score}  (R — заново)", True, (255, 255, 255))
        screen.blit(msg, msg.get_rect(center=(WIDTH // 2, HEIGHT // 2)))

    pygame.display.flip()

pygame.quit()
