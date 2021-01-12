def entercells():
    move = input('Enter cells:').replace('_', ' ')
    grid = [[' ', ' ', ' '] for i in range(3)]
    for i in range(9):
        grid[i // 3][i % 3] = move[i]
    return grid


def printgrid(grid):
    print('---------')
    for i in range(3):
        print(f'| {grid[i][0]} {grid[i][1]} {grid[i][2]} |')
    print('---------')


def makemove(grid, x_turn):
    valid = False
    while not valid:
        coordinates = input('Enter the coordinates:').split()
        if coordinates[0].isdigit() and coordinates[1].isdigit():
            coordinates[0] = int(coordinates[0])
            coordinates[1] = int(coordinates[1])
            if 0 < coordinates[0] < 4 and 0 < coordinates[1] < 4:
                if grid[coordinates[0] - 1][coordinates[1] - 1] == ' ':
                    if x_turn:
                        grid[coordinates[0] - 1][coordinates[1] - 1] = 'X'
                        x_turn = False
                    else:
                        grid[coordinates[0] - 1][coordinates[1] - 1] = 'O'
                        x_turn = True
                    valid = True
                    printgrid(grid)
                else:
                    print('This cell is occupied! Choose another one!')
            else:
                print('Coordinates should be from 1 to 3!')
        else:
            print('You should enter numbers!')
    return x_turn

def gamestate(grid, state):
    x_count = 0
    o_count = 0
    empty_cells = False
    for i in range(3):
        for j in range(3):
            if grid[i][j] == 'X':
                x_count += 1
            elif grid[i][j] == 'O':
                o_count += 1
            if not empty_cells:
                empty_cells = grid[i][j] == ' '

    x_row = False
    o_row = False
    for i in range(3):
        if not x_row:
            x_row = all(elem == 'X' for elem in grid[i])
        if not o_row:
            o_row = all(elem == 'O' for elem in grid[i])

    if grid[0][0] == grid[1][0] == grid[2][0]:
        if grid[0][0] == 'X':
            x_row = True
        elif grid[0][0] == 'O':
            o_row = True

    if grid[0][1] == grid[1][1] == grid[2][1]:
        if grid[0][1] == 'X':
            x_row = True
        elif grid[0][1] == 'O':
            o_row = True

    if grid[0][2] == grid[1][2] == grid[2][2]:
        if grid[0][2] == 'X':
            x_row = True
        elif grid[0][2] == 'O':
            o_row = True


    if (grid[0][0] == grid[1][1] == grid[2][2]) or (grid[0][2] == grid[1][1] == grid[2][0]):
        if grid[1][1] == 'X':
            x_row = True
        elif grid[1][1] == 'O':
            o_row = True

    if not empty_cells and not x_row and not o_row:
        state = 'Draw'

    if (x_row and o_row) or abs(o_count - x_count) >= 2:
        state = 'Impossible'

    if x_row and not o_row:
        state = 'X wins'
    elif not x_row and o_row:
        state = 'O wins'
    return state

state = 'Game not finished'
grid = [[' ', ' ', ' '] for i in range(3)]
printgrid(grid)
x_turn = True

while state not in ['O wins', 'X wins', 'Draw']:
    x_turn = makemove(grid, x_turn)
    state = gamestate(grid, state)

print(f'{state}')