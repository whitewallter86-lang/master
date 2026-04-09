import arcade
import random
from collections import deque


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
CELL_SIZE = 60
MAP_WIDTH = SCREEN_WIDTH // CELL_SIZE
MAP_HEIGHT = SCREEN_HEIGHT // CELL_SIZE

PLAYER_COLOR = arcade.color.BLUE
WALL_COLOR = arcade.color.BLACK
PATH_COLOR = arcade.color.WHITE
ENEMY1_COLOR = arcade.color.RED
ENEMY2_COLOR = arcade.color.ORANGE
ENEMT3_COLOR = arcade.color.PURPLE


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
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
        ]

def bfs_path(maze,start,target):
    rows,cols = len(maze), len(maze[0])
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
                step = parent(step)
            path.reverse
            return path[1] if len(path) > 1 else None
        for dx, dy in [(0,1), (1,0), (0,-1), (-1,0)]:
            nx,ny = current[0] + dx, current[1] + dy
            if 0 <= nx < cols and 0 <= ny < rows:
                if maze[ny][nx] == 0 and (nx,ny) not in visited:
                    visited.add(ny,nx)
                    parent[(nx,ny)] = current
                    queue.appent(nx,ny)
    return None
class Enemy:
    def __init__(self,x,y,color,speed,maze):
        self.x = x
        self.y = y
        self.color = color
        self.speed = speed
        self.maze = maze
        self.next_step = None

    def Update(self,player_x,player_y):
        current_grid = (self.x, self.y)
        target_grid  = (player_X, player_y)

        next_grid = bfs_path(self.maze,current_grid, target_grid)
        if next_grid:
            dx = next_grid[0] - self.x
            dy = next_grid[1] - self.y
            self.x += dx * self.speed
            self.y += dy * self.speed
    def Draw(self):
        arcade.draw_rectangle_filled(
            self.x * CELL_SIZE + CELL_SIZE // 2,
            self.y * CELL_SIZE + CELL_SIZE // 2,
            CELL_SIZE * 0.8, CELL_SIZE * 0.8, self.color
        )
    def get_center(self):
        return (self.x * CELL_SIZE + CELL_SIZE // 2,
                self.y * CELL_SIZE + CELL_SIZE // 2)
class FastEnemy(Enemy):
    def __init__(self,x,y,maze):
        super().__init__(x,y,ENEMY1_COLOR,0.7,maze)



class SlowEnemy(Enemy):
    def __init__(self,x,y,maze):
        super().__init__(x,y,ENEMY2_COLOR,0.3,maze)



class DelayedEnemy(Enemy):
    def __init__(self,x,y,maze,delay_seconds=5):
        super().__init__(x,y,ENEMY3_COLOR,0.5,maze)
        self.active = False
        self.spawn_time = delay_seconds
    def on_update(self,player_x,player_y,current_time):
        if not self.active:
            if current_time >= self.spawn_time:
                self.active = True
            return
        super().update(player_x,player_y)
    
    def on_draw(self):
        if self.active:
            super().draw()



class GameWindow():
    def __init__(self):
        super().__init__(SCREEN_HEIGHT,SCREEN_WIDTH,'лаборотория и три годзиллы')

        arcade.set_background_color(arcade.color.LIGHT_GRAY)
        self.player_x, self.player_y = 1,1

        self.enemies = []

        self.enemies.append(FastEnemy(18,1,MAZE))

        self.enemies.append(SlowEnemy(1,13,MAZE))

        self.delayed_enemy = DelayedEnemy(10,7,MAZE,delay_seconds = 5)

        self.game_over = False
        self.start_time = 0
        self.setup()
    
    def setup(self):
        self.start_time = 0
        self.game_over = False
        self.player_x,self.player_y = 1,1
        self.enemies = [
            FastEnemy(18, 1, MAZE),
            SlowEnemy(1, 13, MAZE),
        ]
        self.delayed_enemy = DelayedEnemy(10,7,MAZE,delay_seconds = 5)


    def on_draw(self):
        arcade.start_render()

        for row in range(MAP_HEIGHT):
            for col in range(MAP_WIDTH):
                if MAZE[row][col] == 1:
                    arcade.draw_rectangle_filled(col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2, CELL_SIZE, CELL_SIZE, WALL_COLOR)
                else:
                    arcade.draw_rectangle_filled(col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2, CELL_SIZE, CELL_SIZE, PATH_COLOR)
                arcade.draw_rectange_filled(
                    self.player_x * CELL_SIZE + CELL_SIZE // 2,
                    self.player_y * CELL_SIZE + CELL_SIZE // 2,
                    CELL_SIZE * 0.7, CELL_SIZE * 0.7, PLAYER_COLOR
                )
        for enemy in self.enemies:
            enemy.draw()
        self.delayed_enemy.draw()
        if self.game_over:
            arcade.Text(
                'GG BRO',
                SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                arcade.color.RED, 54, anchor_x='center',anchor_y ='center'

            )
            arcade.Text(
                'кликни R для респавна',
                SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50,
                arcade.color.BLACK, anchor_x='center',anchor_y='center'
            )
    def on_update(self,delta_time):
        if self.game_over:
            return
        if self.start_time == 0:
            self.start_time = arcade.get_time() - self.start_time
        for enemy in self.enemies:
            enemy.on_update(self.player_x, self.player_y)
            self.delayed_enemy.on_update(self.player_x, self.player_y, current_time)
        player_center = (self.player_x * CELL_SIZE + CELL_SIZE // 2, self.player_y * CELL_SIZE + CELL_SIZE // 2)
        all_creeps = self.enemies.copy()
        if self.delayed_enemy.active:
            all_creeps.append(self.delayed_enemy)
        for enemy in all_creeps:
            enemy_center = enemy.get_center
            if abs(player_center[0] - enemy_center[0]) < CELL_SIZE * 0.8 and abs(player_center[1] - enemy_center[1]) < CELL_SIZE * 0.8:
                self.game_over = True
                break
    def on_key_press(self,symbol,modifiers):
        if self.game_over:
            if symbol == arcade.key.R:
                self.setup
            return
        
        new_x,new_y = self.player_x,self.player_y
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
                self.player_x,self.player_y = new_x,new_y
def main():
    window = GameWindow
    arcade.run()
if __name__ == '__main__':
    main()







        

