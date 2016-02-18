# Kelly Pham 25384246. Lab 2, project 5

import tkinter

import OthelloLogic
game = OthelloLogic.Othello()


def from_pixel(pixel_x, pixel_y, width, height):
        # to convert from where the user clicks (in pixels) to fractional coordinates
    return pixel_x/width, pixel_y/height


def to_pixel(frac_x1, frac_y1, frac_x2, frac_y2, width, height):
    return int(frac_x1 * width), int(frac_y1 * height), int(frac_x2 * width), int(frac_y2 * height)


class OthelloControl:
    def __init__(self, canvas, game_col, game_row, method):
        self._col = game_col
        self._row = game_row
        self._canvas = canvas
        self._board = []
        self._disc = {"BLACK": [], "WHITE": []}
        self._method = method

    def _convert_turn(self, game_state):
        if game_state['turn'] == 1:
            return 'BLACK'
        elif game_state['turn'] == 2:
            return "WHITE"
        else:
            return "NONE"

    def draw_game_state(self, game_state: "current game state of the game"):
        current_state = game_state['board']
        canvas_width = self._canvas.winfo_width()
        canvas_height = self._canvas.winfo_height()

        divided_width = canvas_width / self._col
        divided_height = canvas_height / self._row

        for col in range(len(current_state)):
            self._canvas.create_line(divided_width * col, 0, divided_width * col, canvas_height)
            self._board.append((divided_width * col/canvas_width, 0, divided_width * col/canvas_width, 1))
            for row in range(len(current_state[0])):
                if (0, divided_height * row, int(self._canvas['width']), divided_height * row) not in self._board:
                    self._board.append((0, divided_height * row/canvas_height, 1, divided_height * row/canvas_height))
                self._canvas.create_line((0, divided_height * row, canvas_width, divided_height * row))
                if current_state[col][row] == 1:
                    self._canvas.create_oval(divided_width * col, divided_height * row,
                                             divided_width * col + divided_width,
                                             divided_height * row + divided_height, fill='black')
                    self._disc['BLACK'].append((divided_width * col/canvas_width, divided_height * row/canvas_height,
                                                (divided_width * col + divided_width)/canvas_width,
                                                (divided_height * row + divided_height)/canvas_height))
                elif current_state[col][row] == 2:
                    self._canvas.create_oval(divided_width * col, divided_height * row,
                                             divided_width * col + divided_width,
                                             divided_height * row + divided_height, fill='white')
                    self._disc['WHITE'].append((divided_width * col/canvas_width, divided_height * row/canvas_height,
                                                (divided_width * col + divided_width)/canvas_width,
                                                (divided_height * row + divided_height)/canvas_height))

    def place_move(self, game_state, move: '(col, row)', score_display, turn_display):
        try:
            turn = tkinter.StringVar()
            new_game_state = game.place_move(game_state, move, self._col, self._row)
            if not new_game_state:
                pass
            else:
                self._canvas.delete(tkinter.ALL)
                self.draw_game_state(new_game_state)
                try:
                    score_display['text'] = 'BLACK: {} WHITE: {}'.format(new_game_state['score'][0],
                                                                         new_game_state['score'][1])
                    game.game_over(new_game_state, self._col, self._row)
                    turn.set('TURN: {}'.format(self._convert_turn(new_game_state)))
                    turn_display['textvariable'] = turn
                except:
                    turn.set(game.winner(new_game_state, self._method))
                    turn_display['textvariable'] = turn
                    turn_display['font'] = ('helvetica', 30)
        except:
            pass


    def redraw_game_state(self, game_state):
        self.draw_game_state(game_state)
        self._canvas.delete(tkinter.ALL)
        for point_x1, point_y1, point_x2, point_y2 in self._board:
            self._redraw_board(point_x1, point_y1, point_x2, point_y2)
        for black_disc in self._disc['BLACK']:
            black_x1, black_y1, black_x2, black_y2 = black_disc
            self._redraw_discs("black", black_x1, black_y1, black_x2, black_y2)
        for white_disc in self._disc['WHITE']:
            self._redraw_discs("white", white_disc[0], white_disc[1], white_disc[2], white_disc[3])

    def _redraw_board(self, frac_x1, frac_y1, frac_x2, frac_y2):
        canvas_width = self._canvas.winfo_width()
        canvas_height = self._canvas.winfo_height()

        pixel_x1, pixel_y1, pixel_x2, pixel_y2 = to_pixel(
            frac_x1, frac_y1, frac_x2, frac_y2, canvas_width, canvas_height)
        self._canvas.create_line(pixel_x1, pixel_y1, pixel_x2, pixel_y2)

    def _redraw_discs(self, color, disc_x1, disc_y1, disc_x2, disc_y2):
        canvas_width = self._canvas.winfo_width()
        canvas_height = self._canvas.winfo_height()

        pixel_x1, pixel_y1, pixel_x2, pixel_y2 = to_pixel(
            disc_x1, disc_y1, disc_x2, disc_y2, canvas_width, canvas_height)
        self._canvas.create_oval(pixel_x1, pixel_y1, pixel_x2, pixel_y2, fill=color)

