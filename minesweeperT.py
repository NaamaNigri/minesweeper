import tkinter as tk
import random


new_size = [[9, 9, 81, 10], [16, 16, 256, 40], [16, 30, 480, 99]]
size = new_size[0]

mine_grid = tk.Tk()

buttons = [[None] * size[1] for i in range(size[0])]


def grid_gen():
    grid = []
    for i in range(size[0]):
        line = []
        for j in range(size[1]):
            line.append(0)
        grid.append(line)

    return grid


def planting_mines(grid):
    mines = size[3]

    grid_size = [len(grid), len(grid[0])]

    while mines > 0:
        row = random.randint(0, grid_size[0] - 1)
        col = random.randint(0, grid_size[1] - 1)
        random_cell = grid[row][col]
        if random_cell == 0:
            grid[row][col] = 10
            mines -= 1


def update_if_valid_location(valid_rows_and_cols, row, col):
    valid_rows = valid_rows_and_cols[0]
    valid_cols = valid_rows_and_cols[1]
    if row in valid_rows and col in valid_cols:
        if grid[row][col] < 10:
            grid[row][col] += 1
        return True
    return False


def update_square_around(valid_rows_and_cols, i, j):
    for row_offset in range(-1, 2):
        for col_offset in range(-1, 2):
            update_if_valid_location(valid_rows_and_cols, i + row_offset, j + col_offset)


def hints():
    valid_rows_and_cols = [range(len(grid)), range(len(grid[0]))]
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] >= 10:
                update_square_around(valid_rows_and_cols, i, j)


def button_click(row, col):
    if grid[row][col] == 10:
        win_lose_pop_box(False)

    if grid[row][col] == 0:
        find_next_zero(grid, row, col)

    else:
        buttons[row][col].config(text=f"{grid[row][col]}", state=tk.DISABLED, bg="white")

    white = 0
    for i in range(size[0]):
        for j in range(size[1]):
            if buttons[i][j]["bg"] == "white":
                white += 1

    if size[2] - white == size[3]:
        win_lose_pop_box(True)


def right_click(row, col):
    if buttons[row][col]['text'] == 'F':
        buttons[row][col].config(text=f" ", state=tk.ACTIVE, bg="grey")
    else:
        buttons[row][col].config(text=f"F", state=tk.DISABLED, bg="red")


def game_button_grid(button_lst):
    for row in range(size[0]):
        for col in range(size[1]):
            button_lst[row][col] = tk.Button(mine_grid, text=" ", padx=15, pady=10, bg="grey", command=lambda r=row, c=col: button_click(r, c))
            button_lst[row][col].grid(row=row, column=col,  padx=5, pady=5, sticky='E')
            button_lst[row][col].bind("<Button-3>", lambda event, r=row, c=col: right_click(r, c))


def is_valid_location(valid_rows_and_cols, row, col):
    valid_rows = valid_rows_and_cols[0]
    valid_cols = valid_rows_and_cols[1]
    if row in valid_rows and col in valid_cols:
        return True
    return False


def find_next_zero(grid, i, j):
    valid_rows_and_cols = [range(len(grid)), range(len(grid[0]))]
    if grid[i][j] == 0:
        buttons[i][j].config(state=tk.DISABLED, bg="white")
        grid[i][j] = " "

        for index in range(-1, 2):
            for index2 in range(-1, 2):
                if is_valid_location(valid_rows_and_cols, i + index, j + index2):
                    find_next_zero(grid, i + index, j + index2)
    if not grid[i][j] == 10:
        buttons[i][j].config(text=f"{grid[i][j]}", state=tk.DISABLED, bg="white")


def win_lose_pop_box(boll):
    global win_window
    win_window = tk.Toplevel(mine_grid)
    text = "You win!"
    if not boll:
        text = "You lose!"

    label = tk.Label(win_window, text="Game Over", padx=20, pady=20)
    label.grid(row=0, column=0, sticky=tk.EW)
    label2 = tk.Label(win_window, text=text, padx=20, pady=20)
    label2.grid(row=0, column=1, sticky=tk.EW)
    exit_button = tk.Button(win_window, text="Exit Game", command=bye)
    exit_button.grid(row=1, column=1, padx=5, pady=5)
    play_again_button = tk.Button(win_window, text="Play again", command=restart_game)
    play_again_button.grid(row=1, column=0, padx=5, pady=5)


def restart_game():
    global win_window
    win_window.quit()
    win_window.destroy()
    mine()


def mine():

    global grid
    grid = grid_gen()
    planting_mines(grid)
    hints()

    #tk button grid
    game_button_grid(buttons)

    mine_grid.mainloop()


def bye():
    exit()


restart = tk.Button(mine_grid, text="Restart", command=mine, bg="grey")
restart.grid(row=size[0]+1, columnspan=size[1], sticky=tk.NSEW)

mine()
