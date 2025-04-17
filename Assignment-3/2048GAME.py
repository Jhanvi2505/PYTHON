import tkinter as tk
import random

GRID_SIZE = 4
CELL_SIZE = 100
FONT = ("Helvetica", 24, "bold")
COLORS = {
    0: ("#CDC1B4", ""),
    2: ("#EEE4DA", "#776E65"),
    4: ("#EDE0C8", "#776E65"),
    8: ("#F2B179", "#F9F6F2"),
    16: ("#F59563", "#F9F6F2"),
    32: ("#F67C5F", "#F9F6F2"),
    64: ("#F65E3B", "#F9F6F2"),
    128: ("#EDCF72", "#F9F6F2"),
    256: ("#EDCC61", "#F9F6F2"),
    512: ("#EDC850", "#F9F6F2"),
    1024: ("#EDC53F", "#F9F6F2"),
    2048: ("#EDC22E", "#F9F6F2"),
}


class Game2048:
    def __init__(self, master):
        self.master = master
        self.master.title("2048")
        self.score = 0
        self.game_over = False
        self.won = False

        # Score display
        self.score_label = tk.Label(master, text="Score: 0", font=("Helvetica", 16))
        self.score_label.pack()

        # Restart button
        self.restart_button = tk.Button(master, text="Restart", font=("Helvetica", 12), command=self.restart_game)
        self.restart_button.pack(pady=5)

        # Canvas setup
        self.canvas = tk.Canvas(master, width=GRID_SIZE * CELL_SIZE, height=GRID_SIZE * CELL_SIZE, bg="#BBADA0")
        self.canvas.pack()

        # Key binding
        self.master.bind("<Key>", self.key_handler)

        # Game board init
        self.board = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
        self.spawn_tile()
        self.spawn_tile()
        self.draw_board()

    def restart_game(self):
        self.board = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
        self.score = 0
        self.game_over = False
        self.won = False
        self.score_label.config(text="Score: 0")
        self.spawn_tile()
        self.spawn_tile()
        self.draw_board()

    def spawn_tile(self):
        empty = [(r, c) for r in range(GRID_SIZE) for c in range(GRID_SIZE) if self.board[r][c] == 0]
        if empty:
            r, c = random.choice(empty)
            self.board[r][c] = random.choice([2] * 9 + [4])

    def compress(self, row):
        new_row = [num for num in row if num != 0]
        new_row += [0] * (GRID_SIZE - len(new_row))
        return new_row

    def merge(self, row):
        for i in range(GRID_SIZE - 1):
            if row[i] != 0 and row[i] == row[i + 1]:
                row[i] *= 2
                self.score += row[i]
                row[i + 1] = 0
        return row

    def move_left(self):
        moved = False
        for i in range(GRID_SIZE):
            original = list(self.board[i])
            new_row = self.compress(original)
            new_row = self.merge(new_row)
            new_row = self.compress(new_row)
            self.board[i] = new_row
            if new_row != original:
                moved = True
        return moved

    def move_right(self):
        moved = False
        for i in range(GRID_SIZE):
            original = list(self.board[i])
            row = original[::-1]
            new_row = self.compress(row)
            new_row = self.merge(new_row)
            new_row = self.compress(new_row)
            new_row = new_row[::-1]
            self.board[i] = new_row
            if new_row != original:
                moved = True
        return moved

    def move_up(self):
        moved = False
        for c in range(GRID_SIZE):
            col = [self.board[r][c] for r in range(GRID_SIZE)]
            original = list(col)
            new_col = self.compress(col)
            new_col = self.merge(new_col)
            new_col = self.compress(new_col)
            for r in range(GRID_SIZE):
                self.board[r][c] = new_col[r]
            if new_col != original:
                moved = True
        return moved

    def move_down(self):
        moved = False
        for c in range(GRID_SIZE):
            col = [self.board[r][c] for r in range(GRID_SIZE)][::-1]
            original = [self.board[r][c] for r in range(GRID_SIZE)]
            new_col = self.compress(col)
            new_col = self.merge(new_col)
            new_col = self.compress(new_col)
            new_col = new_col[::-1]
            for r in range(GRID_SIZE):
                self.board[r][c] = new_col[r]
            if new_col != original:
                moved = True
        return moved

    def key_handler(self, event):
        if self.game_over:
            return

        moved = False
        if event.keysym == 'Left':
            moved = self.move_left()
        elif event.keysym == 'Right':
            moved = self.move_right()
        elif event.keysym == 'Up':
            moved = self.move_up()
        elif event.keysym == 'Down':
            moved = self.move_down()

        if moved:
            self.spawn_tile()
            self.draw_board()
            self.score_label.config(text=f"Score: {self.score}")

            if not self.won and any(2048 in row for row in self.board):
                self.won = True
                self.canvas.create_text(
                    CELL_SIZE * GRID_SIZE // 2,
                    CELL_SIZE * GRID_SIZE // 2,
                    text="You Win!",
                    fill="green",
                    font=("Helvetica", 32, "bold")
                )

            if self.check_game_over():
                self.game_over = True
                self.canvas.create_text(
                    CELL_SIZE * GRID_SIZE // 2,
                    CELL_SIZE * GRID_SIZE // 2,
                    text="Game Over!",
                    fill="red",
                    font=("Helvetica", 32, "bold")
                )

    def draw_board(self):
        self.canvas.delete("all")
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                value = self.board[r][c]
                bg, fg = COLORS.get(value, ("#3C3A32", "#F9F6F2"))
                x1, y1 = c * CELL_SIZE, r * CELL_SIZE
                x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=bg, outline="white")
                if value:
                    self.canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2, text=str(value), fill=fg, font=FONT)

    def check_game_over(self):
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                if self.board[r][c] == 0:
                    return False
                if c < GRID_SIZE - 1 and self.board[r][c] == self.board[r][c + 1]:
                    return False
                if r < GRID_SIZE - 1 and self.board[r][c] == self.board[r + 1][c]:
                    return False
        return True


if __name__ == "__main__":
    root = tk.Tk()
    game = Game2048(root)
    root.mainloop()
