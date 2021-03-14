# write your code here
def print_board(symbols):
    print('---------\n|', end='')
    for i in range(len(symbols)):
        if(i == 2 or i == 5):
            print(' ' + symbols[i] + ' |\n|', end='')
        elif(i == 8):
            print(' ' + symbols[i] + ' |')
        else:
            print(' ' + symbols[i], end='')
    print('---------')

def has_won(symbol, symbols):
    #first row
    if symbols[0] == symbol and symbols[1] == symbol and symbols[2] == symbol: return True
    #second row
    if symbols[3] == symbol and symbols[4] == symbol and symbols[5] == symbol: return True
    #third row
    if symbols[6] == symbol and symbols[7] == symbol and symbols[8] == symbol: return True
    #first column
    if symbols[0] == symbol and symbols[3] == symbol and symbols[6] == symbol: return True
    #second column
    if symbols[1] == symbol and symbols[4] == symbol and symbols[7] == symbol: return True
    #third column
    if symbols[2] == symbol and symbols[5] == symbol and symbols[8] == symbol: return True
    #first diagonal
    if symbols[0] == symbol and symbols[4] == symbol and symbols[8] == symbol: return True
    #second diagonal
    if symbols[2] == symbol and symbols[4] == symbol and symbols[6] == symbol: return True
    return False
def count(symbol, symbols):
    numOf = 0
    for i in range(len(symbols)):
        if symbols[i] == symbol:
            numOf += 1
    return numOf
def valid_coordinate(coordinate):
    valid_row = coordinate[0] >= 1 and coordinate[0] <= 3
    valid_col = coordinate[1] >= 1 and coordinate[1] <= 3
    return valid_col and valid_row
def convert_to_index(coordinate):
    index = 0
    if(coordinate[0] == 1 and coordinate[1] == 2):   index = 1
    elif(coordinate[0] == 1 and coordinate[1] == 3): index = 2
    elif(coordinate[0] == 2 and coordinate[1] == 1): index = 3
    elif(coordinate[0] == 2 and coordinate[1] == 2): index = 4
    elif(coordinate[0] == 2 and coordinate[1] == 3): index = 5
    elif(coordinate[0] == 3 and coordinate[1] == 1): index = 6
    elif(coordinate[0] == 3 and coordinate[1] == 2): index = 7
    elif(coordinate[0] == 3 and coordinate[1] == 3): index = 8
    return index
def coordinate_taken(symbols, coordinate):
    index = convert_to_index(coordinate)
    return symbols[index] != ' '
def draw_exists(symbols):
    draw = False
    #check game not finished or draw
    if(not(has_won('X', symbols)) and not(has_won('O', symbols))):
        if ' ' not in symbols:
            draw = True
    return draw
def game_finished(symbols):
    print_board(symbols)
    finished = False
    if draw_exists(symbols):
        print('Draw')
        finished = True
    #check to see if there's already a winner
    elif has_won('X', symbols):
        print('X wins')
        finished = True
    elif has_won('O', symbols):
        print('O wins')
        finished = True
    return finished
def get_next_move(symbol, symbols):
    finished = False
    while not finished:
        entered_coordinate = input('Enter the coordinates:').split()
        #check to see if numbers
        if not(entered_coordinate[0].isdigit() and entered_coordinate[1].isdigit()):
            print('You should enter numbers!')
            continue
        #if numbers, convert to int and
        #check to see if they're in range
        for i in range(len(entered_coordinate)):
            entered_coordinate[i] = int(entered_coordinate[i])
        if(not(valid_coordinate(entered_coordinate))):
            print('Coordinates should be from 1 to 3!')
            continue
        #if valid coordinate check to see if coordinate
        #is already taken
        if(coordinate_taken(symbols, entered_coordinate)):
            print('This cell is occupied! Choose another one!')
            continue

        #update board
        symbols[convert_to_index(entered_coordinate)] = symbol
        finished = True
    return symbols
#----------------------------------------------start of program
#start with empty board
symbols = [' ',' ',' ',
           ' ',' ',' ',
           ' ',' ',' ',]
curr_symbol = 'X'
while(not(game_finished(symbols))):
    symbols = get_next_move(curr_symbol, symbols)
    if curr_symbol == 'X':
        curr_symbol = 'O'
    else:
        curr_symbol = 'X'
#check impossibles
#if has_won('X', symbols) and has_won('O', symbols):
#    print('Impossible')
#    exit()
#numXs = count('X', symbols)
#numOs = count('O', symbols)
#if((numXs > numOs + 1) or (numOs > numXs + 1)):
#    print('Impossible')
#    exit()


#handle the next move
    
    
    




    
