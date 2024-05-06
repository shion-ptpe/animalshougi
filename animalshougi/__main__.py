from animalshougi.game import Game


def main():
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


if __name__ == "__main__":
    main()