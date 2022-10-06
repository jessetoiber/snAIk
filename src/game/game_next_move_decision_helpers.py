from src.game.game_models import Direction
from src.game.game_graphics import GameGraphicsWindow

# file contains 3 methods for deciding the snakes next move
# only one can be used at a time
# change the line in the game_driver.py with the method you'd like to use

# can be used if you want to play the game via WASD keyboard input
def get_player_manual_move_input():
    return GameGraphicsWindow.get_graphics_screen_move_key_input_direction()

# use as the next move function to demo the "always win" cheese
def always_win(x,y):
    if y == 31:
        if x % 2 == 0:
            return Direction.RIGHT
        else:
            return Direction.UP
    if y == 1:
        if x % 2 == 0:
            return Direction.DOWN
        else:
            if x != 31:
                return Direction.RIGHT
            else:
                return Direction.UP
    if y == 0:
        if x != 0:
            return Direction.LEFT
        else:
            return Direction.DOWN

    if x % 2 == 0:
        return Direction.DOWN
    else:
        return Direction.UP

## $$ ##

#
def get_direction_by_thinking(current_direction, snake, goalx, goaly):
    move_map = Direction.MOVE_MAP_DEFAULT.copy()

    # moving towards goal is good
    (snake_headx, snake_heady) = snake[0].coords
    if snake_headx > goalx:
        move_map[Direction.LEFT] += 100
    if snake_headx < goalx:
        move_map[Direction.RIGHT] += 100
    if snake_heady > goaly:
        move_map[Direction.UP] += 100
    if snake_heady < goaly:
        move_map[Direction.DOWN] += 100

    # if running into wall, bad move
    if snake_headx + 1 >= 32:
        move_map[Direction.RIGHT] = 0
    else:
        move_map[Direction.RIGHT] += 20
    if snake_headx - 1 < 0:
        move_map[Direction.LEFT] = 0
    else:
        move_map[Direction.LEFT] += 20
    if snake_heady + 1 >= 32:
        move_map[Direction.DOWN] = 0
    else:
        move_map[Direction.DOWN] += 20
    if snake_heady - 1 < 0:
        move_map[Direction.UP] = 0
    else:
        move_map[Direction.UP] += 20

    # if running into snake body segment, bad move
    for body_segment in snake:
        if (snake_headx+1, snake_heady) == body_segment.coords:
            move_map[Direction.RIGHT] = 0
        if (snake_headx-1, snake_heady) == body_segment.coords:
            move_map[Direction.LEFT] = 0
        if (snake_headx, snake_heady+1) == body_segment.coords:
            move_map[Direction.DOWN] = 0
        if (snake_headx, snake_heady-1) == body_segment.coords:
            move_map[Direction.UP] = 0

    # not die is good
    
    # if the death move, bad move
    for potential_dir in Direction.ALL_DIRECTIONS:
        if (potential_dir | current_direction) in Direction.DEATH_INPUT_COMBOS:
            # found the death move
            move_map[potential_dir] = 0
            break

    # print:
    print("{", end="")
    print("UP: " + str(move_map[Direction.UP]), end="")
    print(", DOWN: " + str(move_map[Direction.DOWN]), end="")
    print(", LEFT: " + str(move_map[Direction.LEFT]), end="")
    print(", RIGHT: " + str(move_map[Direction.RIGHT]), end="")
    print("}")
    ########

    # pass to model learner thing

    max_think = 0
    max_dir = None
    for key in move_map.keys():
        if move_map[key] > max_think:
            max_think = move_map[key]
            max_dir = key
    
    return max_dir
## $$ ##
