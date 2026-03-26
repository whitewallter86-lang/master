import arcade
from collections import deque

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_SIZE = 40
MOVE_SPEED = 3

MAZE = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

MAP_HEIGHT = len(MAZE)
MAP_WIDTH = len(MAZE[0])

def world_to_grid(x, y):
    col = int(x // TILE_SIZE)
    row = int((SCREEN_HEIGHT - y) // TILE_SIZE)
    return row, col

def grid_to_world(row, col):
    x = col * TILE_SIZE + TILE_SIZE / 2
    y = SCREEN_HEIGHT - (row * TILE_SIZE + TILE_SIZE / 2)
    return x, y

def bfs(start, goal):
    queue = deque([start])
    came_from = {start: None}
    
    while queue:
        current = queue.popleft()
        if current == goal:
            break
        
        row, col = current
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nr, nc = row + dr, col + dc
            if 0 <= nr < MAP_HEIGHT and 0 <= nc < MAP_WIDTH:
                if MAZE[nr][nc] == 0 and (nr, nc) not in came_from:
                    queue.append((nr, nc))
                    came_from[(nr, nc)] = current
    
    if goal not in came_from:
        return []
    
    path = []
    cur = goal
    while cur is not None:
        path.append(cur)
        cur = came_from[cur]
    path.reverse()
    return path

class Player(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.texture = arcade.make_soft_square_texture(TILE_SIZE - 4, arcade.color.BLUE)
        self.center_x = TILE_SIZE + TILE_SIZE / 2
        self.center_y = SCREEN_HEIGHT - (TILE_SIZE + TILE_SIZE / 2)
        self.move_up = False
        self.move_down = False
        self.move_left = False
        self.move_right = False
        self.alive = True
    
    def update(self, delta_time):
        if not self.alive:
            return
            
        prev_x = self.center_x
        prev_y = self.center_y
        
        if self.move_up:
            self.center_y += MOVE_SPEED
        if self.move_down:
            self.center_y -= MOVE_SPEED
        if self.move_left:
            self.center_x -= MOVE_SPEED
        if self.move_right:
            self.center_x += MOVE_SPEED
        
        row, col = world_to_grid(self.center_x, self.center_y)
        if 0 <= row < MAP_HEIGHT and 0 <= col < MAP_WIDTH:
            if MAZE[row][col] == 1:
                self.center_x = prev_x
                self.center_y = prev_y
        else:
            self.center_x = prev_x
            self.center_y = prev_y

class Enemy(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.texture = arcade.make_soft_square_texture(TILE_SIZE - 4, arcade.color.RED)
        self.center_x = TILE_SIZE * 13 + TILE_SIZE / 2
        self.center_y = SCREEN_HEIGHT - (TILE_SIZE + TILE_SIZE / 2)
        self.path = []
        self.current_target = 0
        self.speed = 2
    
    def update_path(self, player_x, player_y):
        enemy_row, enemy_col = world_to_grid(self.center_x, self.center_y)
        player_row, player_col = world_to_grid(player_x, player_y)
        
        self.path = bfs((enemy_row, enemy_col), (player_row, player_col))
        self.current_target = 1 if len(self.path) > 1 else 0
    
    def update(self, delta_time):
        if len(self.path) > self.current_target:
            target_row, target_col = self.path[self.current_target]
            target_x, target_y = grid_to_world(target_row, target_col)
            
            dx = target_x - self.center_x
            dy = target_y - self.center_y
            distance = (dx**2 + dy**2)**0.5
            
            if distance < self.speed:
                self.current_target += 1
            else:
                self.center_x += (dx / distance) * self.speed
                self.center_y += (dy / distance) * self.speed

class GameOverView(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view
        arcade.set_background_color(arcade.color.BLACK)
    
    def on_draw(self):
        self.clear()
        arcade.draw_text("gg ezz", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50,
                        arcade.color.RED, 54, anchor_x="center")
        arcade.draw_text("Press SPACE to restart or ESC to quit", 
                        SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50,
                        arcade.color.WHITE, 20, anchor_x="center")
    
    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            new_game = GameView()
            new_game.setup()
            self.window.show_view(new_game)
        elif key == arcade.key.ESCAPE:
            arcade.close_window()

class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.BLACK)
        
        self.wall_list = None
        self.player_list = None
        self.enemy_list = None
        self.player = None
        self.enemy = None
        self.frame_count = 0
        
    def setup(self):
        self.wall_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        
        for row in range(MAP_HEIGHT):
            for col in range(MAP_WIDTH):
                if MAZE[row][col] == 1:
                    wall = arcade.Sprite()
                    wall.texture = arcade.make_soft_square_texture(TILE_SIZE, arcade.color.WHITE)
                    wall.center_x = col * TILE_SIZE + TILE_SIZE / 2
                    wall.center_y = SCREEN_HEIGHT - (row * TILE_SIZE + TILE_SIZE / 2)
                    self.wall_list.append(wall)
        
        self.player = Player()
        self.player_list.append(self.player)
        
        self.enemy = Enemy()
        self.enemy_list.append(self.enemy)
        
        self.frame_count = 0
    
    def on_draw(self):
        self.clear()
        self.wall_list.draw()
        self.player_list.draw()
        self.enemy_list.draw()
    
    def on_update(self, delta_time):
        if not self.player.alive:
            return
            
        self.player_list.update(delta_time)
        
        self.frame_count += 1
        if self.frame_count % 30 == 0:
            self.enemy.update_path(self.player.center_x, self.player.center_y)
        
        self.enemy_list.update(delta_time)
        
        if arcade.check_for_collision(self.player, self.enemy):
            self.player.alive = False
            game_over = GameOverView(self)
            self.window.show_view(game_over)
    
    def on_key_press(self, key, modifiers):
        if not self.player.alive:
            return
            
        if key == arcade.key.UP or key == arcade.key.W:
            self.player.move_up = True
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player.move_down = True
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player.move_left = True
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player.move_right = True
    
    def on_key_release(self, key, modifiers):
        if not self.player.alive:
            return
            
        if key == arcade.key.UP or key == arcade.key.W:
            self.player.move_up = False
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player.move_down = False
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player.move_left = False
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player.move_right = False

def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, "labaran")
    game_view = GameView()
    window.show_view(game_view)
    game_view.setup()
    arcade.run()

if __name__ == "__main__":
    main()