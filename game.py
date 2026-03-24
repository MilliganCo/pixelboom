# game.py

import pygame
import random
from config import WIDTH, HEIGHT, BLACK
from player import Player
from enemy import Enemy

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pixel Chaos")

clock = pygame.time.Clock()
running = True
player = Player()
enemies = []
enemy_spawn_timer = 0  # Таймер появления врагов

while running:
    screen.fill(BLACK)
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                player.place_pixel()
            if event.key == pygame.K_SPACE:
                player.explode_pixels()

    # Таймер спавна врагов
    enemy_spawn_timer += 1
    if enemy_spawn_timer > 100:  # Враги появляются каждые 100 кадров
        enemy_type = random.choices(
            ["default", "fast", "heavy", "shaman", "berserk"],
            weights=[40, 30, 10, 10, 10]  # Регулируем редкость типов врагов
        )[0]
        enemies.append(Enemy(enemy_type))
        enemy_spawn_timer = 0

    player.move(keys)
    player.update()
    player.draw(screen)

    for enemy in enemies[:]:
        if not enemy.update(player, enemies):
            enemies.remove(enemy)
        else:
            enemy.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
