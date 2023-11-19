#________________________________IMPORTS________________________________
import numpy as np
import pygame
import math
import sys
import button
import random

pygame.init()

#________________________________CONSTANTS________________________________
ROW_COUNT = 7
COLUMN_COUNT = 8

BLUE = (0,0,255) #RGB
BLACK = (0,0,0) #RGB
YELLOW = (255,255,0) #RGB
GREEN= (30, 130, 75) #RGB
FULL_GREEN = (0, 220, 30) #RGB
RED = (255,0,0) #RGB

turn = 0 
game_on = False #Begins false so the game doesn't being yet
computer_game_on = False
initialize = True #Initialiaze stage (press the buttons to pick)



#________________________________Images________________________________
#Button image load
start_button = pygame.image.load('chip_player_start_button.png')
player_computer_button = pygame.image.load('chip_computer_start_button.png') 
exit_button = pygame.image.load('chip_quit_button.png')


#Button instance
player_computer_button = button.Button(120,580, player_computer_button, 0.35)
start_button = button.Button(310,580,start_button, 0.35) 
exit_button = button.Button(500,580, exit_button, 0.35)


#________________________________FUNCTIONS________________________________
def home_page(): #Loads everything for the home page initiliazation
    Game_BG=pygame.image.load('ConnectFiveEdit.png')
    Game_BG=pygame.transform.scale(Game_BG,(width,height))
    screen.blit(Game_BG, (0,0)) #Displays the home page
    start_button.draw(screen)
    player_computer_button.draw(screen)
    exit_button.draw(screen)
    pygame.display.update()

def create_board(): #Rows and columns for board
    board = np.zeros((ROW_COUNT,COLUMN_COUNT)) #7 by 8 board written in 0's
    return board

def drop_piece(board, row, col, piece): #Assigns a piece at the row/column 
    board[row][col] = piece  # Assigns a piece at the row/col

def valid_location_check(board, col): #Check if the piece can be placed in the column
    return board[ROW_COUNT-1][col] == 0   #Check if sixth row is clear (empty slot)

def get_next_open_row(board, col): #checks if the row is empty
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r
        
def print_board(board): #Changes numpy orientation (for the orientation of the board)
    print(np.flip(board, 0))

def winning_move(board, piece): #Checks all four win types (vert, horiz, diag up, and diag down)
    #Check Horizontal Wins
    for c in range (COLUMN_COUNT-4):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece and board[r][c+4] == piece: 
                return True
    #Check Vertical Wins        
    for c in range (COLUMN_COUNT):
        for r in range(ROW_COUNT-4):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece and board[r+4][c] == piece:
                return True
            
    #Check Positve Slope Diaganol Wins
    for c in range (COLUMN_COUNT-4):
        for r in range(ROW_COUNT-4):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece and board[r+4][c+4] == piece:
                return True 

    #Check Negative Slope Diaganol Wins
    for c in range (COLUMN_COUNT-4):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece and board[r-4][c+4] == piece:
                return True 

def draw_board(board): #Designing the board (colors and circles) 
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, FULL_GREEN, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE + SQUARESIZE+SQUARESIZE/2)), RADIUS)
    
    for c in range(COLUMN_COUNT): #Colors the black circles with the players placement
        for r in range(ROW_COUNT): 
            if board [r][c] == 1: #player 1 places
                pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE + SQUARESIZE/2)), RADIUS)
            elif board [r][c] == 2: # player 2 places
                pygame.draw.circle(screen, BLUE, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE + SQUARESIZE/2)), RADIUS)

    pygame.display.update()

def game_play(): #Connect 5 Game
    global turn
    global game_on
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
                        game_on = False    #Ends the game


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
                        game_on = False #Ends the game

            print_board(board)
            draw_board(board)
                
            if not game_on: 
                pygame.time.wait(3000) #Pause for 3 seconds before closing the application

def computer_game_play(): #Connect 5 against computer
    global turn
    global computer_game_on
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0,0,width,SQUARESIZE))
            posx = event.pos[0]
            if turn == 0:
                pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)

        pygame.display.update()

        if turn == 0:
            if event.type == pygame.MOUSEBUTTONDOWN:
                #Player 1 Input
                pygame.draw.rect(screen, BLACK, (0,0,width,SQUARESIZE))

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
                        computer_game_on = False    #Ends the game

        else:
        #Computer Input (Player 2)
            posx = random.randint(0,(8*SQUARESIZE))
            col = int(math.floor(posx/SQUARESIZE))

            
            if valid_location_check(board,col):
                row = get_next_open_row(board,col)
                drop_piece(board,row,col,2)
                pygame.time.wait(600)
                turn += 1
                turn = turn %2

                if winning_move(board, 2):  #Player 2 has the winning move end game
                    label = myfont.render("Player 2 Wins!!", 1, BLUE)
                    screen.blit(label, (40,10)) #Displays the winning label
                    computer_game_on = False #Ends the game

        print_board(board)
        draw_board(board)
                
        if not computer_game_on: 
            pygame.time.wait(3000) #Pause for 3 seconds before closing the application

def quit(): #Quits the system
    sys.exit()

#________________________________DISPLAY________________________________
SQUARESIZE = 90  #90 pixels
width = COLUMN_COUNT * SQUARESIZE   #width of screen
height = (ROW_COUNT+1) * SQUARESIZE # height of screen
size = (width, height) 
RADIUS = int(SQUARESIZE/2 - 5) 


screen = pygame.display.set_mode(size)
myfont = pygame.font.SysFont("monospace", 75)


board = create_board() #Initialize Board
print_board(board)
home_page()

#________________________________GAMEPLAY________________________________
while initialize:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:#If x in top right corner is pressed
            quit()
        if start_button.draw(screen): #If start button pressed
            draw_board(board)
            screen.fill("black")
            initialize = False
            game_on = True
        if player_computer_button.draw(screen):
            draw_board(board)
            screen.fill("black")
            initialize = False
            computer_game_on = True
        if exit_button.draw(screen): #if exit button pressed
            initialize = False
            game_on = False
            quit()

draw_board(board)
while game_on:
    pygame.display.update()
    game_play() #Events

while computer_game_on:
    pygame.display.update()
    computer_game_play() #Events
