import pygame
import random
from math import inf as infinity
import time

purple = pygame.Rect(350, 640, 50, 50)
red = pygame.Rect(400, 640, 50, 50)
green = pygame.Rect(450, 640, 50, 50)
blue = pygame.Rect(500, 640, 50, 50)

color_arr = ['purple', 'red', 'green', 'blue']
game_turn = 0
game_over = False
red_count = 0
purple_count = 0
green_count = 0
blue_count = 0

purple_active = True
green_active = True
red_active = True
blue_active = True

HUMAN = -1
COMP = 1

state = [[0, 0, 0, -1],
         [0, 0, 0, 0],
         [0, 0, 0, 0],
         [1, 0, 0, 0]]


def set_color():
    global red_count, blue_count, green_count, purple_count
    color = color_arr[random.randint(0, 3)]

    if color == 'red' and red_count < 4:
        red_count += 1

        return pygame.Color(color)
    elif color == 'red' and red_count == 4:
        return set_color()

    if color == 'blue' and blue_count < 4:
        blue_count += 1

        return pygame.Color(color)
    elif color == 'blue' and blue_count == 4:
        return set_color()

    if color == 'green' and green_count < 4:
        green_count += 1

        return pygame.Color(color)
    elif color == 'green' and green_count == 4:
        return set_color()

    if color == 'purple' and purple_count < 4:
        purple_count += 1

        return pygame.Color(color)
    elif color == 'purple' and purple_count == 4:
        return set_color()


class Cell:
    def __init__(self):
        self.captured = False
        self.value = 0
        self.color = set_color()


def classify_board(board, state):
    for i in range(4):
        for j in range(4):
            if state[i][j] == 1:
                board[i][j].value = 1
                board[i][j].captured = True
            if state[i][j] == -1:
                board[i][j].value = -1
                board[i][j].captured = True


grid_size = 4
board = [[Cell() for _ in range(grid_size)] for _ in range(grid_size)]
classify_board(board, state)
pygame.init()

window = pygame.display.set_mode((900, 700))
clock = pygame.time.Clock()


def move(player, color, i, j, effectGame, state):
    global game_turn
    if effectGame:
        if player == 1:
            for x in range(4):
                for y in range(4):
                    if state[x][y] == 1:
                        board[x][y].color = pygame.Color(color)
        elif player == -1:
            for x in range(4):
                for y in range(4):
                    if state[x][y] == -1:
                        board[x][y].color = pygame.Color(color)
        if i + 1 < 4 and board[i + 1][j].color == pygame.Color(color) and not board[i + 1][j].captured:
            board[i + 1][j].value = player
            state[i + 1][j] = player

            move(player, color, i + 1, j, True, state)
        if i - 1 >= 0 and board[i - 1][j].color == pygame.Color(color) and not board[i - 1][j].captured:
            board[i - 1][j].value = player
            board[i - 1][j].captured = True
            state[i - 1][j] = player

            move(player, color, i - 1, j, True, state)
        if j + 1 < 4 and board[i][j + 1].color == pygame.Color(color) and not board[i][j + 1].captured:
            board[i][j + 1].value = player
            state[i][j + 1] = player

            move(player, color, i, j + 1, True, state)
        if j - 1 >= 0 and board[i][j - 1].color == pygame.Color(color) and not board[i][j - 1].captured:
            board[i][j - 1].value = player
            board[i][j - 1].captured = True
            state[i][j - 1] = player

            move(player, color, i, j - 1, True, state)
    else:
        new_state = None
        return new_state
    return None
def reset():
    global game_turn, red_count, purple_count, green_count, blue_count, board, state, game_over
    game_turn = 0
    red_count = 0
    purple_count = 0
    green_count = 0
    blue_count = 0
    game_over = False
    board = [[Cell() for _ in range(grid_size)] for _ in range(grid_size)]
    classify_board(board, state)

    for i in range(4):
        for j in range(4):
            if i == 3 and j == 0:
                state[i][j] = 1
            elif i == 0 and j == 3:
                state[i][j] = -1
            else:
                state[i][j] = 0
    disable()


def disable():
    global green_active, red_active, blue_active, purple_active, state, board
    red_c = 0
    blue_c = 0
    green_c = 0
    purple_c = 0

    for col in range(4):
        for row in range(4):
            if state[col][row] == 1 or state[col][row] == -1:
                if board[col][row].color == pygame.Color('red'):
                    red_active = False
                    red_c += 1
                if board[col][row].color == pygame.Color('green'):
                    green_active = False
                    green_c += 1
                if board[col][row].color == pygame.Color('purple'):
                    purple_active = False
                    purple_c += 1
                if board[col][row].color == pygame.Color('blue'):
                    blue_active = False
                    blue_c += 1

    if red_c == 0:
        red_active = True
    if green_c == 0:
        green_active = True
    if blue_c == 0:
        blue_active = True
    if purple_c == 0:
        purple_active = True


def win(state):
    global game_over
    player1_count = 0
    player2_count = 0
    count = 0
    for i in range(4):
        for j in range(4):
            if state[i][j] == 1:
                count += 1
                player1_count += 1
            if state[i][j] == -1:
                count += 1
                player2_count += 1
    if count == 16:
        if player1_count > player2_count:
            game_over = True
            return 1
        elif player1_count < player2_count:
            game_over = True
            return -1
        else:
            game_over = True
            return 0


def ai_move(color):
    print(color)


def play_postion(color, state, player):
    new_state = None
    for i in range(4):
        for j in range(4):
            new_state = move(player, color, i, j, False, state)



def minimax(state, depth, player):
    global game_over, HUMAN, COMP, purple_active, red_active, green_active, blue_active
    moves = ['purple', 'red', 'green', 'blue']
    if depth == 0 or game_over:
        return evaluate(state)

    if player == True:
        maxEval = -infinity
        for move in moves:
            if move == 'purple' and purple_active:
                move = play_postion('purple')
                eval = minimax(move, depth - 1, False)
                maxEval = max(maxEval, eval)
            if move == 'red' and red_active:
                move = play_postion('red')
                eval = minimax(move, depth - 1, False)
                maxEval = max(maxEval, eval)
            if move == 'green' and green_active:
                move = play_postion('green')
                eval = minimax(move, depth - 1, False)
                maxEval = max(maxEval, eval)
            if move == 'blue' and blue_active:
                move = play_postion('blue')
                eval = minimax(move, depth - 1, False)
                maxEval = max(maxEval, eval)
        return maxEval
    else:
        minEval = +infinity
        for move in moves:
            if move == 'red' and red_active:
                move = play_postion('red')
                eval = minimax(move, depth - 1, True)
                minEval = min(minEval, eval)
            if move == 'purple' and purple_active:
                move = play_postion('purple')
                eval = minimax(move, depth - 1, True)
                minEval = min(minEval, eval)
            if move == 'blue' and blue_active:
                move = play_postion('blue')
                eval = minimax(move, depth - 1, True)
                minEval = min(minEval, eval)
            if move == 'green' and green_active:
                move = play_postion('green')
                eval = minimax(move, depth - 1, True)
                minEval = min(minEval, eval)


def evaluate(state):
    p1_score = 0
    p2_score = 0
    total = 0

    for i in range(4):
        for j in range(4):
            if state[i][j] == 1:
                p1_score += 1
                total += 1
            elif state[i][j] == -1:
                p2_score += 1
                total += 1

    if total == 16:
        if p1_score > p2_score:
            return 1
        elif p1_score < p2_score:
            return -1
        else:
            return 0
    else:
        if p1_score > p2_score:
            return (p1_score - p2_score) / 10
        elif p1_score < p2_score:
            return -(p2_score - p1_score) / 10
        else:
            return 0


def main():
    global game_turn
    disable()
    legal_move = False
    run = True

    while run:
        clock.tick(100)

        if game_turn % 2 == 0 and not game_over:
            pygame.display.set_caption('Player 1 turn')
        elif game_turn % 2 == 1 and not game_over:
            pygame.display.set_caption('Player 2 turn')

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    reset()
                    reset()
            if event.type == pygame.MOUSEBUTTONDOWN and game_over == False:
                for i in range(4):
                    for j in range(4):
                        piece = board[i][j]
                        if red.collidepoint(event.pos) and red_active:
                            if game_turn % 2 == 0:
                                if piece.captured and piece.value == 1:
                                    piece.color = pygame.Color('red')
                                    piece.value = 1
                                    move(1, 'red', i, j, True, state)
                                    legal_move = True

                            else:
                                if piece.captured and piece.value == -1:
                                    piece.color = pygame.Color('red')
                                    piece.value = -1
                                    move(-1, 'red', i, j, True, state)
                                    legal_move = True

                        if blue.collidepoint(event.pos) and blue_active:
                            if game_turn % 2 == 0:
                                if piece.captured and piece.value == 1:
                                    piece.color = pygame.Color('blue')
                                    piece.value = 1
                                    move(1, 'blue', i, j, True, state)
                                    legal_move = True

                            else:
                                if piece.captured and piece.value == -1:
                                    piece.color = pygame.Color('blue')
                                    piece.value = -1
                                    move(-1, 'blue', i, j, True, state)
                                    legal_move = True

                        if green.collidepoint(event.pos) and green_active:
                            if game_turn % 2 == 0:
                                if piece.captured and piece.value == 1:
                                    piece.color = pygame.Color('green')
                                    piece.value = 1
                                    move(1, 'green', i, j, True, state)
                                    legal_move = True

                            else:
                                if piece.captured and piece.value == -1:
                                    piece.color = pygame.Color('green')
                                    piece.value = -1
                                    move(-1, 'green', i, j, True, state)
                                    legal_move = True

                        if purple.collidepoint(event.pos) and purple_active:
                            if game_turn % 2 == 0:
                                if piece.captured and piece.value == 1:
                                    piece.color = pygame.Color('purple')
                                    piece.value = 1
                                    move(1, 'purple', i, j, True, state)
                                    legal_move = True

                            else:
                                if piece.captured and piece.value == -1:
                                    piece.color = pygame.Color('purple')
                                    piece.value = -1
                                    move(-1, 'purple', i, j, True, state)
                                    legal_move = True

                if legal_move:
                    game_turn += 1
                    disable()
                    legal_move = False
                    win(state)
                    #minimax(state, 3, True)
                    print(evaluate(state))
                    if game_over:
                        if win(state) == 1:
                            pygame.display.set_caption("Player 1 Wins")
                        elif win(state) == -1:
                            pygame.display.set_caption("Player 2 Wins")
                        else:
                            pygame.display.set_caption("Draw")

        window.fill(pygame.Color(40, 40, 40))
        for iy, rowOfCells in enumerate(board):
            for ix, cell in enumerate(rowOfCells):
                if cell.captured:
                    pygame.draw.rect(window, cell.color, (ix * 150 + 150, iy * 150 + 1, 148, 148))

                else:
                    pygame.draw.rect(window, cell.color, (ix * 150 + 150, iy * 150 + 1, 148, 148))
                if state[iy][ix] == 1:
                    pygame.draw.rect(window, pygame.Color("white"), pygame.Rect(ix * 150 + 150, iy * 150 + 1, 148, 148),
                                     10)
                if state[iy][ix] == -1:
                    pygame.draw.rect(window, pygame.Color("grey"), pygame.Rect(ix * 150 + 150, iy * 150 + 1, 148, 148),
                                     10)

        pygame.draw.rect(window, [255, 0, 0], red)
        pygame.draw.rect(window, [0, 0, 255], blue)
        pygame.draw.rect(window, [0, 255, 0], green)
        pygame.draw.rect(window, [155, 0, 255], purple)

        if not red_active:
            pygame.draw.rect(window, pygame.Color('black'), red, 3)
        if not blue_active:
            pygame.draw.rect(window, pygame.Color('black'), blue, 3)
        if not green_active:
            pygame.draw.rect(window, pygame.Color('black'), green, 3)
        if not purple_active:
            pygame.draw.rect(window, pygame.Color('black'), purple, 3)

        pygame.display.flip()


if __name__ == '__main__':
    main()

pygame.quit()
exit()
