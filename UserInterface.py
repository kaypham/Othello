# Kelly Pham 25384246. Lab 2. Project 4

import OthelloLogic as OL

game = OL.Othello()


def print_board(game_state: dict):
    board = game_state['board']
    print("B: {}  W: {}".format(game_state['score'][0], game_state['score'][1]))
    for col in range(len(board[0])):
        for row in range(len(board)):
            if board[row][col] == 0:
                space = "."
            elif board[row][col] == 1:
                space = "B"
            else:
                space = "W"
            print(space, " ", end="")
        print()
    return


def handle_inputs(game_col, game_row) -> 'move_tuple':
    input_move = input()
    satisfied = False
    while not satisfied:
        try:
            move_list = input_move.split()
            move_tuple = (int(move_list[1]), int(move_list[0]))

            while move_tuple[1] not in range(1, game_row + 1) or move_tuple[0] not in range(1, game_col + 1):
                input_move = input("There is no row {} column {}. "
                                   "Please enter a row number from 1 to {} and column number from 1 to {}, "
                                   "separated by a space ".format(move_tuple[1], move_tuple[0], game_row, game_col))
                move_list2 = input_move.split()
                try:
                    move_tuple = (int(move_list2[1]), int(move_list2[0]))
                    return move_tuple
                except (ValueError, IndexError):
                    move_tuple = (int(move_list[1]), (int(move_list[0])))

            satisfied = True
            return move_tuple
        except (ValueError, IndexError):
            input_move = input("Sorry. Column and row must be numbers. "
                               "Please enter a row number from 1 to {} and column number from 1 to {}, "
                               "separated by a space ".format(game_row, game_col))


def handle_game_process(game_state, move_tuple, game_col, game_row, method):
    found_winner = False
    while not found_winner:
        try:
            new_game_state = game.place_move(game_state, move_tuple, game_col, game_row)
            if not new_game_state:  # this is when move is invalid but there are options
                print("INVALID")
            else:
                print("VALID")
                print_board(new_game_state)
                game.game_over(new_game_state, game_col, game_row)
            if game_state['turn'] == 1:
                print("TURN: B")
            else:
                print("TURN: W")
            move_tuple = handle_inputs(game_col, game_row)
        except OL.GameOverError:
            found_winner = True
            print(game.winner(game_state, method))
        except OL.InvalidMoveError:
            print("The tile of ({}, {}) is not an empty tile. Please try again. ".format(move_tuple[1], move_tuple[0]))
            move_tuple = handle_inputs(game_col, game_row)

if __name__ == "__main__":
    row = int(input())
    column = int(input())
    player = input()
    arrangement = input()
    win_condition = input()
    try:
        game_state = game.create_table(player, arrangement, column, row)
        print_board(game_state)
        if player == "B":
            print("TURN: B")
        else:
            print("TURN: W")
        move_tuple = handle_inputs(column, row)
        handle_game_process(game_state, move_tuple, column, row, win_condition)
        print("THANKS FOR PLAYING! :)")
    except OL.OthelloBoardError:
        print("Sorry. The board cannot be smaller than size 4x4 or greater than size 16x16.")





