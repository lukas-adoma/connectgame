# connectFour
import pygame
import sys
import numpy as np
import math
import random

BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

ROW_COUNT = 6
COLUMN_COUNT = 7
WIN_BY = 4

PLAYER = 0
AI = 1

PLAYER_PIECE = 1
AI_PIECE = 2

WINDOW_LENGTH = WIN_BY
EMPTY = 0


def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board


def drop_piece(board, row, col, piece):
    board[row][col] = piece


def is_valid_location(board, col):
    return board[0][col] == 0


def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        rowNum = ROW_COUNT - (r + 1)
        if board[rowNum][col] == 0:
            return rowNum


def winning_move(board, piece):
    # Check horizontal locations
    for c in range(COLUMN_COUNT - (WIN_BY - 1)):
        for r in range(ROW_COUNT):
            equalCounter = 0
            for nextile in range(WIN_BY - 1):
                nextile += 1
                if board[r][c + (nextile - 1)] == piece and board[r][c + nextile] == piece:
                    equalCounter = equalCounter + 1
                if (equalCounter == WIN_BY - 1):
                    return True
    # Check for vertical locations
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - (WIN_BY - 1)):
            equalCounter = 0
            for nextile in range(WIN_BY - 1):  # Logic for the if statements to win by WIN_BY
                nextile += 1
                if board[r + (nextile - 1)][c] == piece and board[r + nextile][c] == piece:
                    equalCounter = equalCounter + 1
                if (equalCounter == WIN_BY - 1):
                    return True
    # Check for postitve slope diaganol
    for c in range(COLUMN_COUNT - (WIN_BY - 1)):
        for r in range(ROW_COUNT - (WIN_BY - 1)):
            equalCounter = 0
            for nextile in range(WIN_BY - 1):
                nextile = nextile + 1
                if board[r + (nextile - 1)][c + (nextile - 1)] == piece and board[r + nextile][c + nextile] == piece:
                    equalCounter = equalCounter + 1
                if(equalCounter == WIN_BY - 1):
                    return True
    # Check for positive slop diaganol
    for c in range(COLUMN_COUNT - (WIN_BY - 1)):
        for r in range((WIN_BY - 1), ROW_COUNT):
            equalCounter = 0
            for nextile in range(WIN_BY - 1):
                nextile = nextile + 1
                if board[r - (nextile - 1)][c + (nextile - 1)] == piece and board[r - nextile][c + nextile] == piece:
                    equalCounter = equalCounter + 1
                if(equalCounter == WIN_BY - 1):
                    return True


def evaluate_window(window, piece):
    score = 0
    opp_piece = PLAYER_PIECE
    if piece == PLAYER_PIECE:
        opp_piece = AI_PIECE
    if window.count(piece) == WIN_BY:
        score += 100
    elif window.count(piece) == (WIN_BY - 1) and window.count(EMPTY) == 1:
        score += 10
    elif window.count(piece) == (WIN_BY - 2) and window.count(EMPTY) == 2:
        score += 5
    if window.count(opp_piece) == (WIN_BY - 1) and window.count(EMPTY) == 1:
        score -= 80

    return score


def score_position(board, piece):
    score = 0
    # Score Center Column
    center_array = [int(i) for i in list(board[:, COLUMN_COUNT // 2])]
    center_count = center_array.count(piece)
    score += center_count * 6
    # Score Horizontal
    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(COLUMN_COUNT - (WIN_BY - 1)):
            window = row_array[c:c + WINDOW_LENGTH]  # THIS NEEDS TO OPTIMIZED FOR WINDOW TO WIN BY?
            score += evaluate_window(window, piece)
    # Score vertical
    for c in range(COLUMN_COUNT):
        column_array = [int(i) for i in list(board[:, c])]
        for r in range(ROW_COUNT - (WIN_BY - 1)):
            window = column_array[r:r + WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    # Score Positive Slope
    for r in range(ROW_COUNT - (WIN_BY - 1)):
        for c in range(COLUMN_COUNT - (WIN_BY - 1)):
            window = [board[r + i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    # Score Negative Slope
    for r in range(ROW_COUNT - (WIN_BY - 1)):
        for c in range(COLUMN_COUNT - ((WIN_BY - 1))):
            window = [board[r + (WIN_BY - 1) - i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    return score


def pick_best_move(baord, piece):
    best_score = 0
    valid_locations = get_valid_locations(board)
    best_col = random.choice(valid_locations)
    for col in valid_locations:
        row = get_next_open_row(board, col)
        temp_board = board.copy()
        drop_piece(temp_board, row, col, piece)
        score = score_position(temp_board, piece)
        if score > best_score:
            best_score = score
            best_col = col
    return best_col


def get_valid_locations(board):
    valid_locations = []
    for col in range(COLUMN_COUNT):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations


def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            if board[r][c] == 0:
                pygame.draw.circle(screen, BLACK, (int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            elif board[r][c] == PLAYER_PIECE:
                pygame.draw.circle(screen, RED, (int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            elif board[r][c] == AI_PIECE:
                pygame.draw.circle(screen, YELLOW, (int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    pygame.display.update()


board = create_board()
print(board)
game_over = False
turn = 0

pygame.init()

SQUARESIZE = 50

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE / 2 - 5)

myFont = pygame.font.SysFont("monospace", 75)

turn = random.randint(PLAYER, AI)

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
            posx = event.pos[0]
            if turn == PLAYER:
                pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE / 2)), RADIUS)
        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
            # Ask for player 1 input
            if turn == PLAYER:
                posx = event.pos[0]
                col = int(math.floor(posx / SQUARESIZE))

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, PLAYER_PIECE)

                    if winning_move(board, PLAYER_PIECE):
                        label = myFont.render("Player 1 wins!", 1, RED)
                        screen.blit(label, (40, 10))
                        print(board)
                        draw_board(board)
                        game_over = True

                    turn += 1
                    turn = turn % 2
            # AI Input
        if turn == AI and not game_over:
            # col = random.randint(0, COLUMN_COUNT - 1)
            col = pick_best_move(board, AI_PIECE)
            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, AI_PIECE)

                if winning_move(board, AI_PIECE):
                    label = myFont.render("Player 2 wins!", 1, YELLOW)
                    screen.blit(label, (40, 10))
                    print(board)
                    draw_board(board)
                    game_over = True

                print(board)
                draw_board(board)
                turn += 1
                turn = turn % 2
