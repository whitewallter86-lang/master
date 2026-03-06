import arcade

SPRITE_SIZE = 64
SPRITE_SCALING = 0.5
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW_TITLE = "2D Platformer Forest Level"

MOVEMENT_SPEED = 5
JUMP_SPEED = 14
GRAVITY = 0.5


class ForestPlatformer(arcade.View):
    """Главный класс платформера"""
    def __init__(self):
        super().__init__()
        self.wall_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()
        self.player_sprite = None
        self.physics_engine = None
        self.game_over = False
        self.player_walk_textures = []
        self.player_idle_texture = None

    def setup(self):
        for x in range(0, WINDOW_WIDTH, SPRITE_SIZE):
            wall = arcade.Sprite(":resources:images/tiles/grassMid.png", scale=SPRITE_SCALING)
            wall.bottom = 0
            wall.left = x
            self.wall_list.append(wall)

        for x in range(2 * SPRITE_SIZE, 6 * SPRITE_SIZE, SPRITE_SIZE):
            platform = arcade.Sprite(":resources:images/tiles/boxCrate.png", scale=SPRITE_SCALING)
            platform.bottom = 3 * SPRITE_SIZE
            platform.left = x
            self.wall_list.append(platform)

        tree = arcade.Sprite(":resources:images/tiles/boxCrate.png", scale=SPRITE_SCALING)
        tree.bottom = SPRITE_SIZE
        tree.left = 5 * SPRITE_SIZE
        self.wall_list.append(tree)

        self.player_sprite = arcade.Sprite(scale=SPRITE_SCALING)

        self.player_idle_texture = arcade.load_texture(":resources:images/animated_characters/female_person/femalePerson_idle.png")

        for i in range(8):
            texture = arcade.load_texture(f":resources:images/animated_characters/female_person/femalePerson_walk{i}.png")
            self.player_walk_textures.append(texture)

        self.player_sprite.texture = self.player_idle_texture
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = SPRITE_SIZE * 2
        self.player_list.append(self.player_sprite)

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite,
            self.wall_list,
            gravity_constant=GRAVITY
        )

        self.background_color = arcade.color.SKY_BLUE

    def on_draw(self):
        self.clear()
        self.wall_list.draw()
        self.player_list.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = MOVEMENT_SPEED
        elif key == arcade.key.UP:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = JUMP_SPEED

    def on_key_release(self, key, modifiers):
        if key in (arcade.key.LEFT, arcade.key.RIGHT):
            self.player_sprite.change_x = 0

    def on_update(self, delta_time):
        if self.player_sprite.left < 0:
            self.player_sprite.left = 0
        elif self.player_sprite.right > WINDOW_WIDTH:
            self.player_sprite.right = WINDOW_WIDTH
        if self.player_sprite.change_x == 0:
            self.player_sprite.texture = self.player_idle_texture
        else:
            frame = int(self.player_sprite.center_x / 10) % len(self.player_walk_textures)
            self.player_sprite.texture = self.player_walk_textures[frame]

            if self.player_sprite.change_x < 0:
                self.player_sprite.angle = 180 
            else:
                self.player_sprite.angle = 0 
        
        self.physics_engine.update()


def main():
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
    game = ForestPlatformer()
    game.setup()
    window.show_view(game)
    arcade.run()


if __name__ == "__main__":
    main()