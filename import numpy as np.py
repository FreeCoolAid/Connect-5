import numpy as np
import pygame
import math
import sys

ROW_COUNT = 6
COLUMN_COUNT = 7

BLUE = (0,0,255) #RGB
BLACK = (0,0,0) #RGB
YELLOW = (255,255,0) #RGB
GREEN= (30, 130, 75) #RGB
RED = (255,0,0) #RGB

def create_board():
    board = np.zeros((ROW_COUNT,COLUMN_COUNT)) #6 by 7 board written in 0's
    return board

def drop_piece(board, row, col, piece): 
    board[row][col] = piece  # Assigns a piece at the row/col

def valid_location_check(board, col):
    return board[ROW_COUNT-1][col] == 0   #Check if fifth row is clear (empty slot)

def get_next_open_row(board, col): #checks if the row is empty
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r
        
def print_board(board): #Changes numpy orientation (for the orientation of the board)
    print(np.flip(board, 0))


def winning_move(board, piece):
    #Check Horizontal Wins
    for c in range (COLUMN_COUNT-3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece: 
                return True
    #Check Vertical Wins        
    for c in range (COLUMN_COUNT):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True
            
    #Check Positve Slope Diaganol Wins
    for c in range (COLUMN_COUNT-3):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True 

    #Check Negative Slope Diaganol Wins
    for c in range (COLUMN_COUNT-3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True 


def draw_board(board): #Designing the board 
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, GREEN, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE + SQUARESIZE+SQUARESIZE/2)), RADIUS)
    
    for c in range(COLUMN_COUNT): #Colors the black circles with the players placement
        for r in range(ROW_COUNT): 
            if board [r][c] == 1: #player 1 places
                pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE + SQUARESIZE/2)), RADIUS)
            elif board [r][c] == 2: # player 2 places
                pygame.draw.circle(screen, BLUE, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE + SQUARESIZE/2)), RADIUS)

    pygame.display.update()

board = create_board() #Initialize Board
print_board(board)
game_over = False #Begins false to start the game
turn = 0 

pygame.init()
SQUARESIZE = 100    #100 pixels
 
width = COLUMN_COUNT * SQUARESIZE   #width of screen
height = (ROW_COUNT+1) * SQUARESIZE # height of screen

size = (width, height)

RADIUS = int(SQUARESIZE/2 - 5)

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

myfont = pygame.font.SysFont("monospace", 75)

while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0,0,width,SQUARESIZE))
            posx = event.pos[0]
            if turn == 0:
                pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
            else:
                pygame.draw.circle(screen, BLUE, (posx, int(SQUARESIZE/2)), RADIUS)
        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            #Player 1 Input
            pygame.draw.rect(screen, BLACK, (0,0,width,SQUARESIZE))

            if turn == 0:
                posx = event.pos[0]
                col = int(math.floor(posx/SQUARESIZE))
                
                if valid_location_check(board,col):
                    row = get_next_open_row(board,col)
                    drop_piece(board,row,col,1)
                    turn += 1
                    turn = turn %2

                    if winning_move(board, 1):  #Player 1 has the winning move end game
                        label = myfont.render("Player 1 Wins!!", 1, RED)
                        screen.blit(label, (40,10)) #Displays the winning label
                        game_over = True    #Ends the game

            else:
            #Player 2 Input
                posx = event.pos[0]
                col = int(math.floor(posx/SQUARESIZE))

                if valid_location_check(board,col):
                    row = get_next_open_row(board,col)
                    drop_piece(board,row,col,2)
                    turn += 1
                    turn = turn %2

                    if winning_move(board, 2):  #Player 2 has the winning move end game
                        label = myfont.render("Player 2 Wins!!", 1, BLUE)
                        screen.blit(label, (40,10)) #Displays the winning label
                        game_over = True #Ends the game

            print_board(board)
            draw_board(board)


            if game_over: 
                pygame.time.wait(3000) #Pause for 3 seconds before closing the application