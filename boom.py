import pygame
import random
import math

# Инициализация Pygame
pygame.init()

# Настройки экрана
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pixel Explosion")

# Цвета
BLACK = (0, 0, 0)
DARK_COLORS = [(50, 50, 50), (80, 50, 50), (50, 80, 50), (50, 50, 80), (100, 100, 100)]

# Ограничение количества пикселей
MAX_PIXELS = 500


# Класс для пикселей
class Pixel:
    def __init__(self, x, y, color, explosion_type=None, static=True):
        self.x = x
        self.y = y
        self.color = color
        self.vx = 0 if static else random.uniform(-1, 1)
        self.vy = 0 if static else random.uniform(-1, 1)
        self.lifetime = random.randint(50, 100)  # Уменьшаем время жизни для оптимизации
        self.size = 6  # Увеличенный размер
        self.explosion_type = explosion_type  # Тип взрыва
        self.static = static  # Флаг, замирает ли пиксель на месте

    def explode(self, pixels):
        if len(pixels) >= MAX_PIXELS:
            return  # Ограничиваем количество пикселей

        explosion_patterns = {
            "cross": [(5, 0), (-5, 0), (0, 5), (0, -5)],
            "circle": [(math.cos(a) * 5, math.sin(a) * 5) for a in [i * (math.pi / 4) for i in range(8)]],
            "star": [(7, 0), (-7, 0), (0, 7), (0, -7), (5, 5), (-5, -5), (5, -5), (-5, 5)]
        }
        new_pixels = []
        for dx, dy in explosion_patterns[self.explosion_type]:
            if len(pixels) + len(new_pixels) >= MAX_PIXELS:
                break
            new_pixel = Pixel(self.x + dx, self.y + dy, self.color, self.explosion_type, static=False)
            new_pixel.vx = dx * random.uniform(0.5, 1.5)
            new_pixel.vy = dy * random.uniform(0.5, 1.5)
            new_pixel.lifetime = random.randint(30, 80)  # Снижаем максимальное время жизни
            new_pixels.append(new_pixel)
        pixels.extend(new_pixels)
        self.lifetime = 0

    def update(self, pixels):
        if self.lifetime > 0 and not self.static:
            self.x += self.vx
            self.y += self.vy
            self.vy += 0.1  # Гравитация
            self.lifetime -= 1

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (int(self.x), int(self.y), self.size, self.size))


# Основной цикл
running = True
pixels = []
mouse_down = False

while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_down = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                mouse_down = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                for p in pixels[:]:
                    p.explode(pixels)

    if mouse_down and len(pixels) < MAX_PIXELS:
        mx, my = pygame.mouse.get_pos()
        explosion_type = random.choice(["cross", "circle", "star"])
        pixels.append(Pixel(mx, my, random.choice(DARK_COLORS), explosion_type, static=True))

    pixels = [p for p in pixels if p.lifetime > 0]  # Удаление устаревших пикселей
    for p in pixels:
        p.update(pixels)
        p.draw(screen)

    pygame.display.flip()
    pygame.time.delay(16)

pygame.quit()
