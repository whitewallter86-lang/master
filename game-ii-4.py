import arcade
import time
from collections import deque

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 900
CELL_SIZE = 60
MAP_WIDTH = SCREEN_WIDTH // CELL_SIZE
MAP_HEIGHT = SCREEN_HEIGHT // CELL_SIZE

PLAYER_COLOR = arcade.color.BLUE
WALL_COLOR = arcade.color.BLACK
PATH_COLOR = arcade.color.WHITE
ENEMY1_COLOR = arcade.color.RED
ENEMY2_COLOR = arcade.color.ORANGE
ENEMY3_COLOR = arcade.color.PURPLE

MAZE = [[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,1],
        [1,0,1,1,1,0,1,0,1,1,1,1,1,0,1,0,1,1,0,1],
        [1,0,1,0,1,0,0,0,1,0,1,0,1,0,1,0,1,0,0,1],
        [1,0,1,0,1,1,1,1,1,0,0,0,1,0,1,0,1,0,1,1],
        [1,0,0,0,1,0,0,0,1,0,1,0,0,0,1,0,0,0,0,1],
        [1,1,1,0,1,0,1,0,1,0,1,1,1,0,1,1,1,0,1,1],
        [1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,1],
        [1,0,1,1,1,0,1,1,1,0,1,1,1,1,1,0,1,0,1,1],
        [1,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1],
        [1,0,1,0,1,1,1,1,1,1,1,0,1,0,1,1,1,1,0,1],
        [1,0,0,0,0,0,1,0,0,0,1,0,1,0,0,0,0,0,0,1],
        [1,1,1,1,1,0,1,0,1,0,1,0,1,1,1,1,1,0,1,1],
        [1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]]

def bfs_path(maze, start, target):
    rows, cols = len(maze), len(maze[0])
    queue = deque([start])
    visited = set([start])
    parent = {start: None}
    while queue:
        current = queue.popleft()
        if current == target:
            path = []
            step = current
            while step is not None:
                path.append(step)
                step = parent[step]
            path.reverse()
            return path[1] if len(path) > 1 else None
        for dx, dy in [(0,1), (1,0), (0,-1), (-1,0)]:
            nx, ny = current[0] + dx, current[1] + dy
            if 0 <= ny < rows and 0 <= nx < cols:
                if maze[ny][nx] == 0 and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    parent[(nx, ny)] = current
                    queue.append((nx, ny))
    return None

class Enemy:
    def __init__(self, x, y, color, speed, maze):
        self.x = float(x)
        self.y = float(y)
        self.color = color
        self.speed = speed
        self.maze = maze

    def update(self, player_x, player_y, delta_time):
        current_grid = (int(round(self.x)), int(round(self.y)))
        target_grid = (player_x, player_y)
        next_grid = bfs_path(self.maze, current_grid, target_grid)
        if next_grid:
            dx = next_grid[0] - self.x
            dy = next_grid[1] - self.y
            length = (dx*dx + dy*dy)**0.5
            if length > 0:
                dx /= length
                dy /= length
            self.x += dx * self.speed * delta_time
            self.y += dy * self.speed * delta_time

    def draw(self):
        center_x = self.x * CELL_SIZE + CELL_SIZE // 2
        center_y = self.y * CELL_SIZE + CELL_SIZE // 2
        half = CELL_SIZE * 0.8 / 2
        left = center_x - half
        right = center_x + half
        bottom = center_y - half
        top = center_y + half
        arcade.draw_lrbt_rectangle_filled(left, right, bottom, top, self.color)

    def get_center(self):
        return (self.x * CELL_SIZE + CELL_SIZE // 2,
                self.y * CELL_SIZE + CELL_SIZE // 2)

class FastEnemy(Enemy):
    def __init__(self, x, y, maze):
        super().__init__(x, y, ENEMY1_COLOR, 1.5, maze)

class SlowEnemy(Enemy):
    def __init__(self, x, y, maze):
        super().__init__(x, y, ENEMY2_COLOR, 0.8, maze)

class DelayedEnemy(Enemy):
    def __init__(self, x, y, maze, delay_seconds=5):
        super().__init__(x, y, ENEMY3_COLOR, 1.2, maze)
        self.active = False
        self.spawn_time = delay_seconds

    def update(self, player_x, player_y, current_time, delta_time):
        if not self.active:
            if current_time >= self.spawn_time:
                self.active = True
            return
        super().update(player_x, player_y, delta_time)

    def draw(self):
        if self.active:
            super().draw()

class GameWindow(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, 'лаборатория и три годзиллы')
        arcade.set_background_color(arcade.color.LIGHT_GRAY)
        self.player_x, self.player_y = 1, 1
        self.enemies = []
        self.enemies.append(FastEnemy(18, 1, MAZE))
        self.enemies.append(SlowEnemy(1, 13, MAZE))
        self.delayed_enemy = DelayedEnemy(10, 7, MAZE, delay_seconds=5)
        self.game_over = False
        self.start_time = None
        self.setup()

    def setup(self):
        self.start_time = None
        self.game_over = False
        self.player_x, self.player_y = 1, 1
        self.enemies = [
            FastEnemy(18, 1, MAZE),
            SlowEnemy(1, 13, MAZE),
        ]
        self.delayed_enemy = DelayedEnemy(10, 7, MAZE, delay_seconds=5)

    def on_draw(self):
        self.clear()
        for row in range(MAP_HEIGHT):
            for col in range(MAP_WIDTH):
                left = col * CELL_SIZE
                right = left + CELL_SIZE
                bottom = row * CELL_SIZE
                top = bottom + CELL_SIZE
                if MAZE[row][col] == 1:
                    arcade.draw_lrbt_rectangle_filled(left, right, bottom, top, WALL_COLOR)
                else:
                    arcade.draw_lrbt_rectangle_filled(left, right, bottom, top, PATH_COLOR)
        center_x = self.player_x * CELL_SIZE + CELL_SIZE // 2
        center_y = self.player_y * CELL_SIZE + CELL_SIZE // 2
        half_w = CELL_SIZE * 0.7 / 2
        half_h = CELL_SIZE * 0.7 / 2
        left = center_x - half_w
        right = center_x + half_w
        bottom = center_y - half_h
        top = center_y + half_h
        arcade.draw_lrbt_rectangle_filled(left, right, bottom, top, PLAYER_COLOR)
        for enemy in self.enemies:
            enemy.draw()
        self.delayed_enemy.draw()
        if self.game_over:
            arcade.draw_text('GG BRO', SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                             arcade.color.RED, 54, anchor_x='center', anchor_y='center')
            arcade.draw_text('кликни R для респавна', SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50,
                             arcade.color.BLACK, 20, anchor_x='center', anchor_y='center')

    def on_update(self, delta_time):
        if self.game_over:
            return
        current_time = time.time()
        if self.start_time is None:
            self.start_time = current_time
        for enemy in self.enemies:
            enemy.update(self.player_x, self.player_y, delta_time)
        elapsed = current_time - self.start_time
        self.delayed_enemy.update(self.player_x, self.player_y, elapsed, delta_time)
        player_center = (self.player_x * CELL_SIZE + CELL_SIZE // 2,
                         self.player_y * CELL_SIZE + CELL_SIZE // 2)
        all_creeps = self.enemies.copy()
        if self.delayed_enemy.active:
            all_creeps.append(self.delayed_enemy)
        for enemy in all_creeps:
            enemy_center = enemy.get_center()
            if (abs(player_center[0] - enemy_center[0]) < CELL_SIZE * 0.8 and
                abs(player_center[1] - enemy_center[1]) < CELL_SIZE * 0.8):
                self.game_over = True
                break

    def on_key_press(self, symbol, modifiers):
        if self.game_over:
            if symbol == arcade.key.R:
                self.setup()
            return
        new_x, new_y = self.player_x, self.player_y
        if symbol == arcade.key.UP:
            new_y += 1
        elif symbol == arcade.key.DOWN:
            new_y -= 1
        elif symbol == arcade.key.LEFT:
            new_x -= 1
        elif symbol == arcade.key.RIGHT:
            new_x += 1
        if 0 <= new_x < MAP_WIDTH and 0 <= new_y < MAP_HEIGHT:
            if MAZE[new_y][new_x] == 0:
                self.player_x, self.player_y = new_x, new_y

def main():
    window = GameWindow()
    arcade.run()

if __name__ == '__main__':
    main()