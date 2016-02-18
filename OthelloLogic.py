# Kelly Pham 25384246. Lab 2. Project 5

class GameOverError(Exception):
    pass


class InvalidMoveError(Exception):
    pass


class OthelloBoardError(Exception):
    pass


NONE = 0
BLACK = 1
WHITE = 2


class Othello:
    def _arrange_board(self, col: int, row: int, board: [[int]], arrangement: str):
        if arrangement == "B":
            board[int(col/2)-1][int(row/2)-1] = BLACK
            board[int(col/2)][int(row/2)] = BLACK
            board[int(col/2-1)][int(row/2)] = WHITE
            board[int(col/2)][int(row/2-1)] = WHITE
        else:
            board[int(col/2)-1][int(row/2)-1] = WHITE
            board[int(col/2)][int(row/2)] = WHITE
            board[int(col/2-1)][int(row/2)] = BLACK
            board[int(col/2)][int(row/2-1)] = BLACK
        return board

    def _game_scores(self, board):
        black_score = 0
        white_score = 0
        for column in board:
            for row in column:
                if row == 1:
                    black_score += 1
                if row == 2:
                    white_score += 1
        return black_score, white_score

    def _opposite_turn(self, turn: int) -> 'other player':
        if turn == 1:
            return WHITE
        elif turn == 2:
            return BLACK

    def _valid_game_board(self, game_col, game_row):
        if game_col not in range(4, 17) or game_row not in range(4, 17):
            raise OthelloBoardError("Board cannot be less than size 4x4 and greater than 16x16. ")

    def _valid_col_input(self, input_col, game_col):
        # raise an exception if user inputs a column that is not on the board. Note that it checks on user's view NOT.
        if not type(input_col) != int and not 0 <= input_col < game_col:
            raise ValueError("Column number must be an integer between 0 and {} not {}".format(game_col, input_col))

    def _valid_row_input(self, input_row, game_row):
        # raise an exception if user inputs a row that is not on the board
        if not type(input_row) != int and not 0 <= input_row < game_row:
            raise ValueError("Row number must be an integer between 0 and {} not {}".format(game_row, input_row))

    def _no_valid_move_left(self, game_state, turn, game_col, game_row):
        # this function will check if there are any possible move left for the given turn
        # what if it is to check if all of the zeros left are "dead-zeros"?

        check_zeros = []
        count_turn = 0
        count_other = 0
        board = game_state['board']
        the_other = self._opposite_turn(turn)

        for col in range(game_col):
            for row in range(game_row):
                if board[col][row] == 0:
                    check_zeros.append([col + 1, row + 1])

        if len(check_zeros) != 0:
            for each in check_zeros:
                move_tuple = (each[0], each[1])
                try:
                    self._valid_input_move(game_state, turn, game_col, game_row, move_tuple)
                except InvalidMoveError:
                    count_turn += 1
                try:
                    self._valid_input_move(game_state, the_other, game_col, game_row, move_tuple)
                except InvalidMoveError:
                    count_other += 1
                    continue
        else:
            raise GameOverError("There are no tiles left")

        if count_turn == len(check_zeros) and count_other == len(check_zeros):
            raise GameOverError("There are no more valid move")

    def _valid_input_move(self, game_state, turn, game_col, game_row, move_tuple):
        # if the move is valid, it will return a list of tiles to be flipped.
        # if the move is invalid, the function will raise InvalidMoveError

        to_b_flipped = []

        board = game_state['board']
        the_other = self._opposite_turn(turn)

        check_col_next = move_tuple[0] - 1  # translate this move into zero-based
        check_row_next = move_tuple[1] - 1

        for testing in [[0, -1], [1, -1], [1, 0], [1, 1], [0, 1], [-1, 1], [-1, 0], [-1, -1]]:
            check_col_next += testing[0]
            check_row_next += testing[1]
            try:
                self._valid_col_input(check_col_next, game_col)
                self._valid_row_input(check_row_next, game_row)
            except ValueError:
                check_col_next = move_tuple[0] - 1
                check_row_next = move_tuple[1] - 1
                continue

            if board[check_col_next][check_row_next] == the_other:
                while board[check_col_next][check_row_next] == the_other:
                    check_col_next += testing[0]
                    check_row_next += testing[1]
                    try:
                        self._valid_col_input(check_col_next, game_col)
                        self._valid_row_input(check_row_next, game_row)
                    except ValueError:
                        check_col_next = move_tuple[0] - 1
                        check_row_next = move_tuple[1] - 1
                        continue
                if board[check_col_next][check_row_next] == game_state['turn']:
                    while board[check_col_next][check_row_next] != board[move_tuple[0] - 1][move_tuple[1] - 1]:
                        check_col_next -= testing[0]
                        check_row_next -= testing[1]
                        if board[check_col_next][check_row_next] != board[move_tuple[0] - 1][move_tuple[1] - 1]:
                            to_b_flipped.append([check_col_next, check_row_next])
                else:
                    check_col_next = move_tuple[0] - 1
                    check_row_next = move_tuple[1] - 1
                    continue
            else:
                check_col_next = move_tuple[0] - 1
                check_row_next = move_tuple[1] - 1
                continue
        if len(to_b_flipped) == 0:  # if there is nothing to be flipped
            raise InvalidMoveError("The move cannot flip any of the opponent's discs.")
        else:
            return to_b_flipped  # the list is in zero-based style

    def create_table(self, player: str, arrangement: str, col: int, row: int):

        self._valid_game_board(col, row)

        game_board = []
        for num_col in range(col):
            game_board.append([])
            for num_row in range(row):
                game_board[-1].append(NONE)

        game_board = self._arrange_board(col, row, game_board, arrangement)

        if player == "B":
            player = BLACK
        else:
            player = WHITE

        score = self._game_scores(game_board)

        game_state = {'board': game_board, 'turn': player, 'score': score}
        return game_state

    def place_move(self, game_state: dict, move_tuple: '(col, row)', game_col, game_row) -> 'game_state':
        # if move_tuple is a valid move (aka does have a to_b_flipped list), return an updated game_state
        # if move_tuple is invalid, but there are other moves that are valid, keep the current game_state
        #  -> check this by using the method of _no_more_valid_move. Catch exception, try above, except below
        # if move_tuple is invalid, n there are NO other moves that are valid, update the turn only!

        the_other = self._opposite_turn(game_state['turn'])

        # before placing any moves, check the validity, if any of the following is invalid, exception raised
        self._valid_col_input(move_tuple[0] - 1, game_col)
        self._valid_row_input(move_tuple[1] - 1, game_row)
        self._no_valid_move_left(game_state, game_state['turn'], game_col, game_row)
        if game_state['board'][move_tuple[0] - 1][move_tuple[1] - 1] != 0:
            raise InvalidMoveError("The tile ({}, {}) is not empty.".format(move_tuple[1], move_tuple[0]))

        try:
            to_b_flipped = self._valid_input_move(game_state, game_state['turn'], game_col, game_row, move_tuple)
            for each in to_b_flipped:
                game_state['board'][each[0]][each[1]] = game_state['turn']  # to flip the disc(s)
            game_state['board'][move_tuple[0] - 1][move_tuple[1] - 1] = game_state['turn']
            game_state['score'] = self._game_scores(game_state['board'])
            game_state['turn'] = self._opposite_turn(game_state['turn'])
            return game_state
        except InvalidMoveError:
            try:
                self._no_valid_move_left(game_state, game_state['turn'], game_col, game_row)
                return False
            except GameOverError:
                game_state['turn'] = the_other
                return game_state

    def game_over(self, game_state, game_col, game_row):
        self._no_valid_move_left(game_state, game_state['turn'], game_col, game_row)

    def winner(self, game_state, method):
        score = self._game_scores(game_state['board'])
        if method == ">":
            if score[0] > score[1]:
                return "WINNER: BLACK"
            elif score[1] > score[0]:
                return "WINNER: WHITE"
            else:
                return "WINNER: NONE"
        else:
            if score[0] < score[1]:
                return "WINNER: BLACK"
            elif score[1] < score[0]:
                return "WINNER: WHITE"
            else:
                return "WINNER: NONE"

