
import pygame
import random
import sys

# Инициализация Pygame
pygame.init()

# Константы
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
FPS = 60

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
BROWN = (139, 69, 19)
GRAY = (128, 128, 128)

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 60
        self.vel_x = 0
        self.vel_y = 0
        self.speed = 5
        self.jump_power = 15
        self.on_ground = False
        self.gravity = 0.8
        self.rect = pygame.Rect(x, y, self.width, self.height)
        
    def update(self, platforms):
        keys = pygame.key.get_pressed()
        
        # Горизонтальное движение
        if keys[pygame.K_LEFT]:
            self.vel_x = -self.speed
        elif keys[pygame.K_RIGHT]:
            self.vel_x = self.speed
        else:
            self.vel_x = 0
            
        # Прыжок
        if keys[pygame.K_UP] and self.on_ground:
            self.vel_y = -self.jump_power
            self.on_ground = False
            
        # Применение гравитации
        self.vel_y += self.gravity
        
        # Обновление позиции
        self.x += self.vel_x
        self.y += self.vel_y
        
        # Обновление прямоугольника коллизии
        self.rect.x = self.x
        self.rect.y = self.y
        
        # Проверка коллизий с платформами
        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.vel_y > 0:  # Падение вниз
                    self.y = platform.rect.top - self.height
                    self.vel_y = 0
                    self.on_ground = True
                elif self.vel_y < 0:  # Прыжок вверх
                    self.y = platform.rect.bottom
                    self.vel_y = 0
                    
        # Ограничения экрана
        if self.x < 0:
            self.x = 0
        elif self.x > SCREEN_WIDTH - self.width:
            self.x = SCREEN_WIDTH - self.width
            
        if self.y > SCREEN_HEIGHT:
            self.y = SCREEN_HEIGHT - self.height
            self.vel_y = 0
            self.on_ground = True
            
        self.rect.x = self.x
        self.rect.y = self.y
        
    def draw(self, screen):
        pygame.draw.rect(screen, BLUE, self.rect)

class Platform:
    def __init__(self, x, y, width, height, color=BROWN):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = pygame.Rect(x, y, width, height)
        
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)

class Enemy:
    def __init__(self, x, y, speed=2, color=RED, smart=False):
        self.x = x
        self.y = y
        self.width = 30
        self.height = 30
        self.speed = speed
        self.direction = random.choice([-1, 1])
        self.color = color
        self.smart = smart
        self.rect = pygame.Rect(x, y, self.width, self.height)
        
    def update(self, platforms, enemies):
        # Движение врага
        self.x += self.speed * self.direction
        self.rect.x = self.x
        
        # Проверка столкновений со стенами экрана
        if self.x <= 0 or self.x >= SCREEN_WIDTH - self.width:
            self.direction *= -1
            
        # Проверка столкновений с платформами (стенами)
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                self.direction *= -1
                if self.direction > 0:
                    self.x = platform.rect.right
                else:
                    self.x = platform.rect.left - self.width
                self.rect.x = self.x
                break
                
        # Умный враг: проверка столкновений с другими врагами
        if self.smart:
            for enemy in enemies:
                if enemy != self and self.rect.colliderect(enemy.rect):
                    self.direction *= -1
                    break
        
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.circle(screen, BLACK, (self.rect.centerx, self.rect.centery), 5)

class Coin:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 20
        self.height = 20
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.collected = False
        
    def draw(self, screen):
        if not self.collected:
            pygame.draw.circle(screen, YELLOW, self.rect.center, 10)
            pygame.draw.circle(screen, BLACK, self.rect.center, 10, 2)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Платформер")
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_over = False
        self.score = 0
        
        # Создание игрока
        self.player = Player(100, 600)
        
        # Создание платформ на разных высотах с разными текстурами
        self.platforms = [
            Platform(0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, 40, GRAY),  # Земля
            Platform(200, 650, 200, 20, BROWN),  # Платформа 1
            Platform(500, 550, 150, 20, GREEN),  # Платформа 2
            Platform(800, 450, 200, 20, BROWN),  # Платформа 3
            Platform(300, 400, 100, 20, GREEN),  # Платформа 4
            Platform(600, 300, 180, 20, BROWN),  # Платформа 5
            Platform(100, 200, 120, 20, GREEN),  # Платформа 6
            Platform(900, 200, 150, 20, BROWN),  # Платформа 7
            # Препятствия (ящики, блоки)
            Platform(450, 600, 40, 40, GRAY),    # Ящик 1
            Platform(750, 500, 40, 40, GRAY),    # Ящик 2
            Platform(350, 350, 40, 40, GRAY),    # Ящик 3
        ]
        
        # Создание врагов с разными скоростями и умностью
        self.enemies = [
            Enemy(250, 630, speed=1, color=RED),           # Медленный враг
            Enemy(550, 530, speed=3, color=(255, 100, 100)), # Быстрый враг
            Enemy(850, 430, speed=2, color=(200, 0, 0)),   # Средний враг
            Enemy(650, 280, speed=2, color=(150, 0, 0), smart=True), # Умный враг
            Enemy(150, 180, speed=1, color=(100, 0, 0), smart=True), # Умный медленный враг
        ]
        
        # Создание монет
        self.coins = [
            Coin(250, 620),
            Coin(570, 520),
            Coin(880, 420),
            Coin(350, 370),
            Coin(680, 270),
            Coin(180, 170),
            Coin(950, 170),
            Coin(480, 580),
        ]
        
        # Инициализация звука
        try:
            pygame.mixer.init()
            # Здесь можно загрузить звуковые файлы
            # self.jump_sound = pygame.mixer.Sound("jump.wav")
            # self.coin_sound = pygame.mixer.Sound("coin.wav")
            # self.game_over_sound = pygame.mixer.Sound("game_over.wav")
        except:
            pass
            
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and self.game_over:
                    self.__init__()  # Перезапуск игры
                    
    def update(self):
        if not self.game_over:
            self.player.update(self.platforms)
            
            # Обновление врагов
            for enemy in self.enemies:
                enemy.update(self.platforms, self.enemies)
                
            # Проверка столкновений с врагами
            for enemy in self.enemies:
                if self.player.rect.colliderect(enemy.rect):
                    self.game_over = True
                    # Воспроизведение звука окончания игры
                    # pygame.mixer.Sound.play(self.game_over_sound)
                    
            # Проверка сбора монет
            for coin in self.coins:
                if not coin.collected and self.player.rect.colliderect(coin.rect):
                    coin.collected = True
                    self.score += 10
                    # Воспроизведение звука сбора монеты
                    # pygame.mixer.Sound.play(self.coin_sound)
                    
    def draw(self):
        # Заливка фона градиентом
        for y in range(SCREEN_HEIGHT):
            color_value = int(135 + (120 * y / SCREEN_HEIGHT))
            color = (color_value, color_value + 20, 255)
            pygame.draw.line(self.screen, color, (0, y), (SCREEN_WIDTH, y))
            
        # Отрисовка платформ
        for platform in self.platforms:
            platform.draw(self.screen)
            
        # Отрисовка монет
        for coin in self.coins:
            coin.draw(self.screen)
            
        # Отрисовка врагов
        for enemy in self.enemies:
            enemy.draw(self.screen)
            
        # Отрисовка игрока
        self.player.draw(self.screen)
        
        # Отрисовка интерфейса
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Счет: {self.score}", True, BLACK)
        self.screen.blit(score_text, (10, 10))
        
        if self.game_over:
            game_over_text = font.render("ИГРА ОКОНЧЕНА! Нажмите R для перезапуска", True, RED)
            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            pygame.draw.rect(self.screen, WHITE, text_rect.inflate(20, 10))
            self.screen.blit(game_over_text, text_rect)
            
        pygame.display.flip()
        
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
            
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()