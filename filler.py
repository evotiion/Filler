import pygame
import random
from math import inf as infinity

pygame.init()

whiteText = (255, 255, 255)
greenText = (0, 255, 0)
blueText = (0, 0, 128)

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

playerOneScore = 1
playerTwoScore = 1

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


# creates the board
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


def move(player, color, i, j):
    global game_turn
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

        move(player, color, i + 1, j)
    if i - 1 >= 0 and board[i - 1][j].color == pygame.Color(color) and not board[i - 1][j].captured:
        board[i - 1][j].value = player
        board[i - 1][j].captured = True
        state[i - 1][j] = player

        move(player, color, i - 1, j)
    if j + 1 < 4 and board[i][j + 1].color == pygame.Color(color) and not board[i][j + 1].captured:
        board[i][j + 1].value = player
        state[i][j + 1] = player

        move(player, color, i, j + 1)
    if j - 1 >= 0 and board[i][j - 1].color == pygame.Color(color) and not board[i][j - 1].captured:
        board[i][j - 1].value = player
        board[i][j - 1].captured = True
        state[i][j - 1] = player

        move(player, color, i, j - 1)


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
    global game_over, playerTwoScore, playerOneScore
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
    else:
        playerOneScore = player1_count
        playerTwoScore = player2_count


text_font = pygame.font.SysFont("Comic Sans MS", 30)


def evaluate(state):
    """
    Function to heuristic evaluation of state.
    :param state: the state of the current board
    :return: +1 if the computer wins; -1 if the human wins; 0 draw
    """
    if wins(state) == 1:
        score = +1
    elif wins(state) == -1:
        score = -1
    else:
        score = 0
    #    print("in evaluate = " + str(score))
    return score


def wins(state):
    humanScore = 0
    computerScore = 0
    for i in range(4):
        for j in range(4):
            if state[i][j] == 1:
                computerScore += 1
            if state[i][j] == -1:
                humanScore += 1
    print("the humanScore is: " + str(humanScore))
    print("the computerScore is: " + str(computerScore))

    if computerScore > humanScore:
        return +1
    elif computerScore < humanScore:
        return -1
    else:
        return 0


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    window.blit(img, (x, y))

depth = 0

def getInfo(state, player):
    global depth
    depth = 0
    for i in range(4):
        for j in range(4):
            if state[i][j] == 0:
                depth += 1

    print("depth: " + str(depth))

    minimax(state, depth, player)  # calls the minimax algorithm


tries = 0


def minimax(state, depth, player):
    if player == COMP:
        best = [-1, -1, -infinity]  # [row, col, value]
    else:
        best = [-1, -1, +infinity]  # [row, col, value]

    if depth == 0 or game_over:
        score = evaluate(state)
        return [-1, -1, score]

    for i in range(4):
        for j in range(4):
            if state[i][j] == 0:
                state[i][j] = player
                score = minimax(state, depth - 1, -player)
                state[i][j] = 0
                score[0], score[1] = i, j

                if player == COMP:
                    if score[2] > best[2]:
                        best = score  # Max value
                else:
                    if score[2] < best[2]:
                        best = score  # Min value
    print("best: " + str(best))
    return best



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
                #Human player's move handling (as in your existing code)

        # Computer's turn
        if game_turn % 2 == 1 and not game_over:
            # Call minimax to determine the best move for the computer
            best_move = minimax(state, depth, COMP)
            # Update the game state with the best move
            i, j = best_move[0], best_move[1]
            move(COMP, color_arr[game_turn % 4], i, j)
            game_turn += 1
            disable()
            win(state)
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
                                     4)
                if state[iy][ix] == -1:
                    pygame.draw.rect(window, pygame.Color("grey"), pygame.Rect(ix * 150 + 150, iy * 150 + 1, 148, 148),
                                     4)

        pygame.draw.rect(window, [255, 0, 0], red)
        pygame.draw.rect(window, [0, 0, 255], blue)
        pygame.draw.rect(window, [0, 255, 0], green)
        pygame.draw.rect(window, [155, 0, 255], purple)

        if not red_active:
            pygame.draw.rect(window, pygame.Color('black'), red, 1)
        if not blue_active:
            pygame.draw.rect(window, pygame.Color('black'), blue, 1)
        if not green_active:
            pygame.draw.rect(window, pygame.Color('black'), green, 1)
        if not purple_active:
            pygame.draw.rect(window, pygame.Color('black'), purple, 1)

        draw_text("Player One Score:" + str(playerOneScore), text_font, pygame.Color("white"), 25, 650)
        draw_text("Player Two Score:" + str(playerTwoScore), text_font, pygame.Color("grey"), 600, 650)
        pygame.display.flip()


if __name__ == '__main__':
    main()

pygame.quit()
exit()
