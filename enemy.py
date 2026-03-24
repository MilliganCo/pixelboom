# enemy.py

import pygame
import random
from config import WIDTH, HEIGHT, ENEMY_COLOR
from pixel import Pixel

# Цвета для разных типов врагов
ENEMY_COLORS = {
    "default": (200, 50, 50),   # Обычный орк
    "fast": (255, 0, 0),        # Быстрый орк (красный)
    "heavy": (100, 100, 100),   # Тяжёлый орк (серый)
    "shaman": (0, 255, 255),    # Шаман (голубой)
    "berserk": (255, 140, 0)    # Берсерк (оранжевый)
}

class Enemy:
    def __init__(self, enemy_type="default"):
        self.x = random.randint(50, WIDTH - 50)
        self.y = random.randint(-150, -30)  # Враги появляются выше экрана
        self.enemy_type = enemy_type
        self.pixels = []
        self.exploded = False
        self.active = False  # Флаг, чтобы враг не взрывался сразу
        self.change_direction_timer = random.randint(30, 100)
        self.vx = random.choice([-1, 1]) * random.uniform(0.5, 1.5)
        self.explosion_radius = random.randint(10, 60)  # Радиус взрыва

        # Устанавливаем свойства в зависимости от типа врага
        self.color = ENEMY_COLORS.get(enemy_type, ENEMY_COLOR)
        if enemy_type == "fast":
            self.speed = 3.5
            self.health = 2
            self.size = 10
        elif enemy_type == "heavy":
            self.speed = 1.0
            self.health = 10
            self.size = 20  # Крупнее других
        elif enemy_type == "shaman":
            self.speed = 2.0
            self.health = 4
            self.size = 15
            self.totems = []  # Ловушки
        elif enemy_type == "berserk":
            self.speed = 1.8
            self.health = 7
            self.size = 18
            self.anger_level = 0
        else:
            self.speed = random.uniform(1.5, 2.5)
            self.health = 4
            self.size = 15

    def move(self, player, enemies):
        """Движение врага в зависимости от типа"""
        if not self.exploded:
            if self.enemy_type == "fast":
                # Бежит напрямую к игроку
                direction_x = player.x - self.x
                direction_y = player.y - self.y
                length = max(abs(direction_x), abs(direction_y))
                if length > 0:
                    self.x += (direction_x / length) * self.speed
                    self.y += (direction_y / length) * self.speed

            elif self.enemy_type == "heavy":
                # Двигается к игроку, но иногда взрывается
                if random.randint(1, 100) < 3:
                    self.explode()
                    self.health -= 1
                else:
                    direction_x = player.x - self.x
                    direction_y = player.y - self.y
                    length = max(abs(direction_x), abs(direction_y))
                    if length > 0:
                        self.x += (direction_x / length) * self.speed
                        self.y += (direction_y / length) * self.speed

            elif self.enemy_type == "shaman":
                # Двигается к ближайшему врагу, создаёт ловушки
                target = min(enemies, key=lambda e: abs(self.x - e.x) + abs(self.y - e.y), default=None)
                if target:
                    direction_x = target.x - self.x
                    direction_y = target.y - self.y
                    length = max(abs(direction_x), abs(direction_y))
                    if length > 0:
                        self.x += (direction_x / length) * self.speed
                        self.y += (direction_y / length) * self.speed

                    # 5% шанс создать ловушку
                    if random.randint(1, 100) < 5:
                        self.totems.append((self.x, self.y, 200))

            elif self.enemy_type == "berserk":
                # Ускоряется при получении урона, может хаотично кружиться
                if self.anger_level > 0:
                    self.speed += 0.1
                if random.randint(1, 200) < 5:
                    self.explode()
                    self.health -= 1
                    self.anger_level += 1
                    self.speed += 0.2

                direction_x = player.x - self.x
                direction_y = player.y - self.y
                length = max(abs(direction_x), abs(direction_y))
                if length > 0:
                    self.x += (direction_x / length) * self.speed
                    self.y += (direction_y / length) * self.speed

            else:
                self.y += self.speed
                self.change_direction_timer -= 1
                if self.change_direction_timer <= 0:
                    self.vx = -self.vx
                    self.change_direction_timer = random.randint(30, 100)
                if 10 < self.x + self.vx < WIDTH - 10:
                    self.x += self.vx

    def take_damage(self, player):
        """Получение урона, если здоровье кончилось - враг взрывается"""
        self.health -= 1
        if self.health <= 0:
            player.restore_pixels(2)
            self.explode()
            return True
        return False
    def explode(self):
        """Гарантированный взрыв врага"""
        if not self.exploded:
            self.exploded = True
            explosion_pixels = []
            explosion_patterns = [
                (random.randint(-self.explosion_radius, self.explosion_radius),
                 random.randint(-self.explosion_radius, self.explosion_radius)) for _ in range(8)
            ]
            for dx, dy in explosion_patterns:
                new_pixel = Pixel(self.x + dx, self.y + dy, self.color, "circle", static=False)
                new_pixel.vx = dx * random.uniform(0.3, 0.6)
                new_pixel.vy = dy * random.uniform(0.3, 0.6)
                explosion_pixels.append(new_pixel)
            self.pixels.extend(explosion_pixels)

    def update(self, player, enemies):
        """Обновление состояния врага"""
        if not self.exploded:
            self.move(player, enemies)

        for p in player.pixels[:]:
            if abs(self.x - p.x) < self.size and abs(self.y - p.y) < self.size:
                player.pixels.remove(p)
                if self.take_damage(player):
                    return False

        return not self.exploded

    def draw(self, screen):
        """Отрисовка врага и его здоровья"""
        if not self.exploded:
            pygame.draw.rect(screen, self.color, (int(self.x), int(self.y), self.size, self.size))

            # Отображение здоровья
            font = pygame.font.Font(None, 20)
            health_text = font.render(str(self.health), True, (255, 255, 255))
            screen.blit(health_text, (self.x, self.y - 10))
