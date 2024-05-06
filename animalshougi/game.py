from animalshougi.board import Board
from animalshougi.piece import *
import curses

class Game:
    SELECT_PIECE = 0
    SELECT_DEST = 1

    def __init__(self):
        self.board = Board()
        self.mode = self.SELECT_PIECE
        self.init_curses()
        self.try_counts = [0, 0]

    def init_curses(self):
        self.strscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.strscr.keypad(True)

    def finish_curses(self):
        curses.nocbreak()
        self.strscr.keypad(False)
        curses.echo()
        curses.endwin()

    def display(self):
        scr = self.strscr
        scr.clear()
        scr.move(0, 0)
        scr.addstr(0, 0, self.board.view())
        (x, y) = self.view_pos(self.board.selected_piece_pos())  # カーソルの座標
        if self.mode == self.SELECT_PIECE:
            scr.addstr(7, 0, "[Space] Next piece. [Return] Select piece. [q] Quit.")
        else:
            (px, py) = self.view_pos(self.board.selected_piece_piece)
            scr.addstr(7, 0, "[Space] Next position. [Return] Select or cancel move position. [q] Quit.")
            scr.addch(py, px, self.board.get_piece(self.board.selected_piece_piece).serialize(), curses.A_REVERSE)
        scr.move(y, x)
        scr.refresh()

    def view_pos(self, pos):
        VIEW_Y = 5
        if isinstance(pos, int):
            offset = 0 if self.board.turn == 0 else 1
            return (pos, VIEW_Y + offset)
        else:
            return pos

    def judgement(self):
        turn = self.board.turn
        # ライオンが取られているか
        player = self.board.turn_player
        for piece in player.captured_piece:
            if isinstance(piece, Lion):
                if piece.owner == 0:
                    return "You Win.  Lion captured!"
                else:
                    return "You lose.  Lion captured!"
        # ライオンが相手陣地にいるか
        if self.try_counts[0]:
            return "You Win. Lion tried to escape!"
        elif self.try_counts[1]:
            return "You lose. Lion tried to escape!"

        for piece in self.board.board[turn * 3]:
            if isinstance(piece, Lion) and piece.owner == turn:
                self.try_counts[turn] += 1
        return 0




if __name__ == "__main__":
    game = Game()
    game.display()
    while True:
        key = game.strscr.getkey()
        if key == "q":
            break
        elif key == " ":
            if game.mode == game.SELECT_PIECE:
                game.board.select_next_piece()
            else:
                game.board.select_next_move_piece()
        elif key == "\n":
            if game.mode == game.SELECT_PIECE:
                game.mode = game.SELECT_DEST
            else:
                if game.board.is_original_pos():
                    game.mode = game.SELECT_PIECE
                    game.strscr.addstr(8, 0, "Move canceled.")
                else:
                    game.board.move_piece(game.board.selected_piece_piece, game.board.selected_move_piece)
                    result = game.judgement()
                    if result:
                        game.strscr.addstr(8, 0, f"{result}")
                        game.strscr.getkey()
                        break
                    else:
                        game.board.toggle_turn()
                        game.mode = game.SELECT_PIECE
        game.display()
    game.finish_curses()
