import pygame
from game_models import Direction

# graphic constants
EMPTY_COLOR = (40, 122, 44)
GOAL_COLOR = (255, 0, 0)
SNAKE_HEAD_COLOR = (40, 122, 255)
SNAKE_BODY_COLOR = (40, 255, 44)
RESTART_TXT_COLOR = (255, 255, 255)
SCREEN_WIDTH = SCREEN_HEIGHT = 576
left_px_const = 18
top_px_const = 18
class GameGraphicsWindow:
    def __init__(self):
        pygame.init()
        pygame.font.init() 
        pygame.display.set_caption("SNaiK: he just wants to be real.")
        self.screen = pygame.display.set_mode([SCREEN_HEIGHT, SCREEN_WIDTH])

    def draw_screen(self, gamestate):
        for i in range(32):
            for j in range(32):
                pygame.draw.rect(self.screen, EMPTY_COLOR, self.__get_rect_full(i, j))

        snake = gamestate.snake.as_array()
        for i in range(len(snake)):
            snake_segment = snake[i]
            color = None
            if snake_segment.is_head:
                color = SNAKE_HEAD_COLOR
            else:
                color = SNAKE_BODY_COLOR

            (l, t) = snake_segment.coords
            pygame.draw.rect(self.screen, color, self.__get_rect(l, t))


        (l, t) = gamestate.goal
        pygame.draw.rect(self.screen, GOAL_COLOR, self.__get_rect_full(l, t))
        pygame.display.flip()

    def display_restart_game_text(self):
        font = pygame.font.SysFont('Courier', 30)
        text_surface = font.render("  Press <spacebar> to restart  ", True, (0, 0, 0)) 
        self.screen.blit(text_surface, (0, 0))
        pygame.display.flip()

    @staticmethod
    def __get_rect_full(l, t):
        return (l*top_px_const, t*left_px_const, top_px_const, left_px_const)

    @staticmethod
    def __get_rect(l, t):
        return (l*top_px_const, t*left_px_const, top_px_const-2, left_px_const-2)

    @staticmethod
    def __check_if_event_occured(event):
        return any(e.type == event for e in pygame.event.get())

    @staticmethod
    def __check_if_key_pressed(key):
        return pygame.key.get_pressed()[key]

    @staticmethod
    def check_if_user_quit():
        return GameGraphicsWindow.__check_if_event_occured(pygame.QUIT)
    
    @staticmethod
    def check_if_user_restart():
        # spacebar key to reset the game
        return GameGraphicsWindow.__check_if_key_pressed(pygame.K_SPACE)

    @staticmethod
    def get_graphics_screen_move_key_input_direction():
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            return Direction.LEFT
        elif keys[pygame.K_w]:
            return Direction.UP
        elif keys[pygame.K_d]:
            return Direction.RIGHT
        elif keys[pygame.K_s]:
            return Direction.DOWN
        else:
            return None

    @staticmethod
    def close():
        pygame.quit()