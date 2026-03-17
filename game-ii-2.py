import arcade
import math
import random

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Survival Game"

PLAYER_SPEED = 5
ENEMY_SPEED_1 = 2
ENEMY_SPEED_2 = 3
DETECTION_DISTANCE = 150
ESCAPE_DISTANCE = 200
CHASE_TIMEOUT = 5.0

class Player(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.texture = arcade.make_soft_square_texture(20, arcade.color.BLUE)
        self.center_x = SCREEN_WIDTH // 2
        self.center_y = SCREEN_HEIGHT // 2
        
    def update(self, delta_time):  
        self.center_x += self.change_x
        self.center_y += self.change_y
        
        if self.left < 0:
            self.left = 0
        elif self.right > SCREEN_WIDTH:
            self.right = SCREEN_WIDTH
            
        if self.bottom < 0:
            self.bottom = 0
        elif self.top > SCREEN_HEIGHT:
            self.top = SCREEN_HEIGHT

class Enemy(arcade.Sprite):
    def __init__(self, x, y, speed, color):
        super().__init__()
        self.texture = arcade.make_soft_square_texture(15, color)
        self.center_x = x
        self.center_y = y
        self.speed = speed
        self.is_chasing = False
        self.chase_timer = 0
        self.patrol_direction_x = random.choice([-1, 1])
        self.patrol_direction_y = random.choice([-1, 1])
        
    def update(self, delta_time):

        if self.is_chasing and self.chase_timer > 0:
            self.chase_timer -= delta_time
            if self.chase_timer <= 0:
                self.is_chasing = False

        if self.left < 0 or self.right > SCREEN_WIDTH:
            self.patrol_direction_x *= -1
        if self.bottom < 0 or self.top > SCREEN_HEIGHT:
            self.patrol_direction_y *= -1

        if self.left < 0:
            self.left = 0
        elif self.right > SCREEN_WIDTH:
            self.right = SCREEN_WIDTH
            
        if self.bottom < 0:
            self.bottom = 0
        elif self.top > SCREEN_HEIGHT:
            self.top = SCREEN_HEIGHT
    
    def follow_player(self, player):
        distance = math.sqrt((self.center_x - player.center_x)**2 + (self.center_y - player.center_y)**2)
        
        if distance <= DETECTION_DISTANCE:
            self.is_chasing = True
            self.chase_timer = CHASE_TIMEOUT
        elif distance >= ESCAPE_DISTANCE:
            self.is_chasing = False

        if self.is_chasing and distance > 0:
            direction_x = (player.center_x - self.center_x) / distance
            direction_y = (player.center_y - self.center_y) / distance
            self.center_x += direction_x * self.speed
            self.center_y += direction_y * self.speed
        else:
            self.center_x += self.patrol_direction_x * self.speed * 0.5
            self.center_y += self.patrol_direction_y * self.speed * 0.5

class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.BLACK)
        
        self.player_list = None
        self.enemy_list = None
        self.player = None
        self.game_over = False
        self.survival_time = 0
        
    def setup(self):
        self.player_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        
        self.player = Player()
        self.player_list.append(self.player)
        
        enemy1 = Enemy(100, 100, ENEMY_SPEED_1, arcade.color.RED)
        enemy2 = Enemy(700, 500, ENEMY_SPEED_2, arcade.color.ORANGE)
        self.enemy_list.append(enemy1)
        self.enemy_list.append(enemy2)
        
        self.game_over = False
        self.survival_time = 0
        
    def on_draw(self):
        self.clear()
        
        if not self.game_over:
            self.player_list.draw()
            self.enemy_list.draw()

            arcade.draw_text(f"Survival Time: {self.survival_time:.1f}s", 10, SCREEN_HEIGHT - 30,
                           arcade.color.WHITE, 16)
        else:
            arcade.draw_text("GAME OVER", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50,
                           arcade.color.RED, 50, anchor_x="center")
            arcade.draw_text(f"You survived for {self.survival_time:.1f} seconds", 
                           SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                           arcade.color.WHITE, 20, anchor_x="center")
            arcade.draw_text("Press R to restart", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50,
                           arcade.color.WHITE, 20, anchor_x="center")
    
    def on_update(self, delta_time):
        if not self.game_over:
            self.survival_time += delta_time

            self.player_list.update(delta_time)

            for enemy in self.enemy_list:
                enemy.follow_player(self.player)
            self.enemy_list.update(delta_time)  

            hit_list = arcade.check_for_collision_with_list(self.player, self.enemy_list)
            if hit_list:
                self.game_over = True
    
    def on_key_press(self, key, modifiers):
        if not self.game_over:
            if key == arcade.key.UP or key == arcade.key.W:
                self.player.change_y = PLAYER_SPEED
            elif key == arcade.key.DOWN or key == arcade.key.S:
                self.player.change_y = -PLAYER_SPEED
            elif key == arcade.key.LEFT or key == arcade.key.A:
                self.player.change_x = -PLAYER_SPEED
            elif key == arcade.key.RIGHT or key == arcade.key.D:
                self.player.change_x = PLAYER_SPEED
        else:
            if key == arcade.key.R:
                self.setup()
    
    def on_key_release(self, key, modifiers):
        if key in (arcade.key.UP, arcade.key.DOWN, arcade.key.W, arcade.key.S):
            self.player.change_y = 0
        elif key in (arcade.key.LEFT, arcade.key.RIGHT, arcade.key.A, arcade.key.D):
            self.player.change_x = 0

def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game_view = GameView()
    window.show_view(game_view)
    game_view.setup()
    arcade.run()

if __name__ == "__main__":
    main()