import arcade
import random

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
SCREEN_TITLE = "Platformer Game"

PLAYER_MOVEMENT_SPEED = 5
PLAYER_JUMP_SPEED = 20
GRAVITY = 1

ENEMY_SPEED = 2
COIN_COUNT = 10

class Enemy(arcade.Sprite):
    def __init__(self, image_path, scale=0.5):
        super().__init__(image_path, scale)
        self.speed = random.uniform(100, 300)
        self.direction = random.choice([-1, 1])
        
    def update(self, delta_time=1/60):
        self.center_x += self.speed * self.direction * delta_time
        
        if self.left <= 0 or self.right >= SCREEN_WIDTH:
            self.direction *= -1
            
        if hasattr(self, 'parent') and hasattr(self.parent, 'platform_list'):
            hit_list = arcade.check_for_collision_with_list(self, self.parent.platform_list)
            if hit_list:
                self.direction *= -1
            
        if hasattr(self, 'parent') and hasattr(self.parent, 'enemy_list'):
            enemy_hit_list = arcade.check_for_collision_with_list(self, self.parent.enemy_list)
            for enemy in enemy_hit_list:
                if enemy != self:
                    self.direction *= -1
                    enemy.direction *= -1

class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        
        self.player_list = None
        self.platform_list = None
        self.enemy_list = None
        self.coin_list = None
        
        self.player_sprite = None
        self.physics_engine = None
        
        self.score = 0
        
        self.jump_sound = None
        self.coin_sound = None
        self.game_over_sound = None
        self.background_music = None
        
        arcade.set_background_color(arcade.color.SKY_BLUE)
        
    def setup(self):
        self.player_list = arcade.SpriteList()
        self.platform_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        
        self.player_sprite = arcade.Sprite(":resources:images/animated_characters/female_adventurer/femaleAdventurer_idle.png", 0.5)
        self.player_sprite.center_x = 100
        self.player_sprite.center_y = 200
        self.player_list.append(self.player_sprite)
        
        platform_positions = [
            (0, 32, 200, 64),
            (300, 150, 200, 32),
            (600, 250, 200, 32),
            (200, 350, 150, 32),
            (500, 450, 200, 32),
            (800, 200, 200, 32),
            (100, 500, 150, 32),
            (700, 350, 150, 32),
            (0, 600, 300, 32),
            (600, 600, 400, 32)
        ]
        
        for x, y, width, height in platform_positions:
            platform = arcade.Sprite(":resources:images/tiles/grassMid.png", 0.5)
            platform.center_x = x + width // 2
            platform.center_y = y + height // 2
            platform.width = width
            platform.height = height
            self.platform_list.append(platform)
            
        ground = arcade.Sprite(":resources:images/tiles/grassMid.png", 0.5)
        ground.center_x = SCREEN_WIDTH // 2
        ground.center_y = 32
        ground.width = SCREEN_WIDTH
        ground.height = 64
        self.platform_list.append(ground)
        
        enemy_spawn_points = [
            (400, 200 + 32),
            (700, 300 + 32),
            (275, 400 + 32),
            (600, 500 + 32),
            (175, 600 + 32),
        ]
        
        enemy_sprites = [
            ":resources:images/enemies/slimeBlue.png",
            ":resources:images/enemies/slimeGreen.png",
            ":resources:images/enemies/wormGreen.png"
        ]
        
        for x, y in enemy_spawn_points:
            enemy = Enemy(random.choice(enemy_sprites), 0.5)
            enemy.center_x = x
            enemy.center_y = y
            enemy.parent = self
            self.enemy_list.append(enemy)
            
        for _ in range(COIN_COUNT):
            coin = arcade.Sprite(":resources:images/items/coinGold.png", 0.3)
            coin.center_x = random.randint(50, SCREEN_WIDTH - 50)
            coin.center_y = random.randint(100, SCREEN_HEIGHT - 100)
            self.coin_list.append(coin)
            
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite, self.platform_list, gravity_constant=GRAVITY
        )
        
        self.load_sounds()
        self.play_background_music()
        
    def load_sounds(self):
        try:
            self.jump_sound = arcade.load_sound(":resources:sounds/jump1.wav")
            self.coin_sound = arcade.load_sound(":resources:sounds/coin1.wav")
            self.game_over_sound = arcade.load_sound(":resources:sounds/gameover1.wav")
            self.background_music = arcade.load_sound(":resources:music/funkyrobot.mp3")
        except:
            print("Could not load sounds. Continuing without sound.")
            
    def play_background_music(self):
        if self.background_music:
            arcade.play_sound(self.background_music, volume=0.3)
        
    def on_draw(self):
        self.clear()
        
        self.platform_list.draw()
        self.enemy_list.draw()
        self.coin_list.draw()
        self.player_list.draw()
        
        arcade.draw_text(f"Score: {self.score}", 10, SCREEN_HEIGHT - 30, 
                        arcade.color.WHITE, 20)
        
    def on_update(self, delta_time):
        self.physics_engine.update()
        self.enemy_list.update(delta_time)
        
        coin_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.coin_list)
        for coin in coin_hit_list:
            coin.remove_from_sprite_lists()
            self.score += 10
            if self.coin_sound:
                arcade.play_sound(self.coin_sound, volume=0.5)
            
        enemy_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.enemy_list)
        if enemy_hit_list:
            if self.game_over_sound:
                arcade.play_sound(self.game_over_sound)
            game_over_view = GameOverView()
            self.window.show_view(game_over_view)
            
    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.UP:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
                if self.jump_sound:
                    arcade.play_sound(self.jump_sound, volume=0.4)
                
    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0

class GameOverView(arcade.View):
    def on_draw(self):
        self.clear()
        arcade.draw_text("GAME OVER", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                        arcade.color.RED, 50, anchor_x="center")
        arcade.draw_text("Press R to restart", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 75,
                        arcade.color.WHITE, 20, anchor_x="center")
                        
    def on_key_press(self, key, modifiers):
        if key == arcade.key.R:
            game_view = GameView()
            game_view.setup()
            self.window.show_view(game_view)

def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game_view = GameView()
    game_view.setup()
    window.show_view(game_view)
    arcade.run()

if __name__ == "__main__":
    main()