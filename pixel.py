# pixel.py

import pygame
import random
import math
from config import PIXEL_SIZE, GRAVITY, DARK_COLORS, MAX_PIXELS, EXPLOSION_TYPES

class Pixel:
    def __init__(self, x, y, color, explosion_type=None, static=True):
        self.x = x
        self.y = y
        self.color = color
        self.vx = 0 if static else random.uniform(-1, 1)
        self.vy = 0 if static else random.uniform(-1, 1)
        self.lifetime = random.randint(50, 100)
        self.size = PIXEL_SIZE
        self.explosion_type = explosion_type
        self.static = static

    def explode(self, pixels):
        if len(pixels) >= MAX_PIXELS:
            return

        explosion_patterns = {
            "cross": [(5, 0), (-5, 0), (0, 5), (0, -5)],
            "circle": [(math.cos(a) * 5, math.sin(a) * 5) for a in [i * (math.pi / 4) for i in range(8)]],
            "star": [(7, 0), (-7, 0), (0, 7), (0, -7), (5, 5), (-5, -5), (5, -5), (-5, 5)]
        }

        new_pixels = []
        for dx, dy in explosion_patterns[self.explosion_type]:
            if len(pixels) + len(new_pixels) >= MAX_PIXELS:
                break
            new_pixel = Pixel(self.x + dx, self.y + dy, random.choice(DARK_COLORS), self.explosion_type, static=False)
            new_pixel.vx = dx * random.uniform(0.5, 1.5)
            new_pixel.vy = dy * random.uniform(0.5, 1.5)
            new_pixel.lifetime = random.randint(30, 80)
            new_pixels.append(new_pixel)

        pixels.extend(new_pixels)
        self.lifetime = 0

    def update(self):
        if self.lifetime > 0 and not self.static:
            self.x += self.vx
            self.y += self.vy
            self.vy += GRAVITY
            self.lifetime -= 1

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (int(self.x), int(self.y), self.size, self.size))
