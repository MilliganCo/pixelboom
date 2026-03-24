# player.py

import pygame
import random
from config import PLAYER_COLOR, WIDTH, HEIGHT, EXPLOSION_TYPES
from pixel import Pixel

class Player:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT - 50
        self.size = 15
        self.color = PLAYER_COLOR
        self.speed = 4
        self.pixels = []
        self.max_pixels = 10
        self.health = 50

    def move(self, keys):
        if keys[pygame.K_a] and self.x > 0:
            self.x -= self.speed
        if keys[pygame.K_d] and self.x < WIDTH - self.size:
            self.x += self.speed
        if keys[pygame.K_w] and self.y > 0:
            self.y -= self.speed
        if keys[pygame.K_s] and self.y < HEIGHT - self.size:
            self.y += self.speed

    def place_pixel(self):
        """Ставит пиксель под игроком"""
        if self.max_pixels > 0:
            explosion_type = random.choice(EXPLOSION_TYPES)
            self.pixels.append(Pixel(self.x, self.y, self.color, explosion_type, static=True))
            self.max_pixels -= 1

    def explode_pixels(self):
        """Взрывает все установленные пиксели"""
        for p in self.pixels[:]:
            p.explode(self.pixels)
        self.pixels = [p for p in self.pixels if p.lifetime > 0]

    def restore_pixels(self, amount):
        self.max_pixels += amount

    def take_damage(self):
        """Получение урона от пикселей врага"""
        self.health -= 1
        if self.health <= 0:
            print("Game Over")

    def update(self):
        for p in self.pixels[:]:
            p.update()
            if p.lifetime <= 0:
                self.pixels.remove(p)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))
        for p in self.pixels:
            p.draw(screen)

        # Отображение здоровья и количества пикселей
        font = pygame.font.Font(None, 24)
        text = font.render(f"HP: {self.health} | Pixels: {self.max_pixels}", True, (255, 255, 255))
        screen.blit(text, (10, 10))
