import copy
import pygame
import random
import sys
import time

GAME_WIDTH = 600
GAME_HEIGHT = 600
BG_COLOR = (25, 25, 50)
BOX_SIZE = GAME_WIDTH // 3
LINE_COLOR = (90, 90, 135)
LINE_WIDTH = 12
CIRCLE_WIDTH = 10
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (239, 231, 200)
CROSS_WIDTH = 17
RADIUS = BOX_SIZE // 4

pygame.init()
screen = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
pygame.display.set_caption("Tic Tac Toe vs AI")
screen.fill(BG_COLOR)


class Board():
    def __init__(self):
        self.boxes = [[0 for _ in range(3)] for _ in range(3)]
        self.empty_boxes = self.boxes
        self.marked_boxes = 0

    def final_state(self,show = False):
        #checks if anyone has won yet, return 1 if player 1 has won and 2 if player 2 has won and 0 if noone has won

        for col in range(3):
            if self.boxes[0][col] == self.boxes[1][col] == self.boxes[2][col] != 0:
                if show:
                    pygame.draw.line(screen,CIRCLE_COLOR,(col*BOX_SIZE + BOX_SIZE//2, 20),(col*BOX_SIZE + BOX_SIZE//2,GAME_HEIGHT - 20),LINE_WIDTH-3)
                return self.boxes[0][col]
        for row in range(3):
            if self.boxes[row][0] == self.boxes[row][1] == self.boxes[row][2] != 0:
                if show:
                    pygame.draw.line(screen,CIRCLE_COLOR,(20, row*BOX_SIZE+BOX_SIZE//2),(GAME_WIDTH - 20,row*BOX_SIZE+BOX_SIZE//2),LINE_WIDTH-3)
                return self.boxes[row][0]
        if self.boxes[0][0] == self.boxes[1][1] == self.boxes[2][2] != 0:
            if show:
                pygame.draw.line(screen, CIRCLE_COLOR, (30, 30),(GAME_WIDTH - 30, GAME_WIDTH - 30), LINE_WIDTH-3)
            return self.boxes[0][0]
        if self.boxes[0][2] == self.boxes[1][1] == self.boxes[2][0] != 0:
            if show:
                pygame.draw.line(screen, CIRCLE_COLOR, (GAME_WIDTH - 30, 30),(30, GAME_HEIGHT - 30), LINE_WIDTH-3)
            return self.boxes[0][2]
        return 0

    def mark_box(self, row, col, p1_turn):
        if p1_turn:
            self.boxes[row][col] = 1
        if not p1_turn:
            self.boxes[row][col] = 2
        self.marked_boxes += 1

    def empty_box(self, row, col):
        return self.boxes[row][col] == 0

    def get_empty_box(self):
        empty_boxes = []
        for row in range(3):
            for col in range(3):
                if self.empty_box(row, col):
                    empty_boxes.append((row, col))
        return empty_boxes

    def is_full(self):
        return self.marked_boxes == 9

    def is_empty(self):
        return self.marked_boxes == 0


class AI():

    def rnd_choice(self, board):
        empty_boxes = board.get_empty_box()
        idx = random.randrange(0, len(empty_boxes))
        return empty_boxes[idx]

    def minimax(self,board, maximizing):
        case = board.final_state()

        if case ==1:
            return 1,None
        if case ==2:
            return -1,None
        elif board.is_full():
            return 0,None

        if maximizing:
            max_eval = -100
            best_move = None
            empty_boxes = board.get_empty_box()

            for (row, col) in empty_boxes:
                temp_board = copy.deepcopy(board)
                temp_board.mark_box(row, col, True)
                eval = self.minimax(temp_board, False)[0]
                if eval > max_eval:
                    max_eval = eval
                    best_move = (row, col)

            return max_eval, best_move

        elif not maximizing:
            min_eval = 100
            best_move = None
            empty_boxes = board.get_empty_box()

            for (row,col) in empty_boxes:
                temp_board = copy.deepcopy(board)
                temp_board.mark_box(row,col,False)
                eval = self.minimax(temp_board,True)[0]
                if eval < min_eval:
                    min_eval = eval
                    best_move = (row,col)

            return min_eval,best_move
    def eval(self, main_board):
        eval,move = self.minimax(main_board, False)
        return move


class Game():
    def __init__(self):
        self.board = Board()
        self.ai = AI()
        self.draw_lines()
        self.running = True
        self.p1_turn = True

    def make_move(self,row,col):
        self.board.mark_box(row, col, self.p1_turn)
        self.draw_figure(row, col)
        self.next_turn()
    def draw_lines(self):
        screen.fill(BG_COLOR)
        pygame.draw.line(screen, LINE_COLOR, (BOX_SIZE, 0), (BOX_SIZE, GAME_HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (GAME_WIDTH - BOX_SIZE, 0), (GAME_WIDTH - BOX_SIZE, GAME_HEIGHT),
                         LINE_WIDTH)

        pygame.draw.line(screen, LINE_COLOR, (0, BOX_SIZE), (GAME_WIDTH, BOX_SIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (0, GAME_HEIGHT - BOX_SIZE), (GAME_WIDTH, GAME_HEIGHT - BOX_SIZE),
                         LINE_WIDTH)

    def next_turn(self):
        self.p1_turn = not self.p1_turn

    def draw_figure(self, row, col):
        if self.p1_turn:
            center = (col * BOX_SIZE + BOX_SIZE // 2, row * BOX_SIZE + BOX_SIZE // 2)
            pygame.draw.circle(screen, CIRCLE_COLOR, center, RADIUS, CIRCLE_WIDTH)
        else:
            start_desc = (col * BOX_SIZE + 50, row * BOX_SIZE + 50)
            end_desc = (col * BOX_SIZE + BOX_SIZE - 50, row * BOX_SIZE + BOX_SIZE - 50)
            pygame.draw.line(screen, CROSS_COLOR, start_desc, end_desc, CROSS_WIDTH)

            start_asc = (col * BOX_SIZE + 50, row * BOX_SIZE + BOX_SIZE - 50)
            end_asc = (col * BOX_SIZE + BOX_SIZE - 50, row * BOX_SIZE + 50)
            pygame.draw.line(screen, CROSS_COLOR, start_asc, end_asc, CROSS_WIDTH)

    def reset(self):
        self.__init__()
    def is_over(self):
        return self.board.final_state(show=True)!=0 or self.board.is_full()

def main():
    game = Game()
    board = game.board
    ai = game.ai
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game.reset()
                    board = game.board
                    ai = game.ai
            if event.type == pygame.MOUSEBUTTONDOWN:

                click_position = event.pos
                row = click_position[1] // BOX_SIZE
                col = click_position[0] // BOX_SIZE

                if board.empty_box(row, col) and game.running ==True:
                    game.make_move(row,col)
                    if game.is_over():
                        game.running = False

        if game.p1_turn == False and game.running == True:
            pygame.display.update()
            row, col = ai.eval(board)
            game.make_move(row,col)
            if game.is_over():
                game.running = False


        pygame.display.update()


main()
