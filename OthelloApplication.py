# Kelly Pham 25384246. Project 5

import tkinter

import OthelloControl as OC

import OthelloLogic
game = OthelloLogic.Othello()

DEFAULT_FONT = ("helvetica", 20)

class OthelloApp:
    def __init__(self, game_state, game_col, game_row, method):
        self._state = game_state
        self._col = game_col
        self._row = game_row
        self._score = game_state['score']
        self._method = method

        self._root_window = tkinter.Tk()
        self._root_window.wm_title("Othello!")

        self._canvas = tkinter.Canvas(master=self._root_window, width=500, height=500, background="salmon")
        self._canvas.grid(row=1, column=0, sticky=tkinter.N + tkinter.E + tkinter.S + tkinter.W)

        self._turn_in_text = tkinter.StringVar()
        self._turn_in_text.set(self._determine_turn())
        self._turn_display = tkinter.Label(master=self._root_window, font=DEFAULT_FONT,
                                           textvariable=self._turn_in_text)  # DON'T FORGET THAT THIS IS TOO SPECIFIC
        self._turn_display.grid(row=2, column=0, sticky=tkinter.N + tkinter.E + tkinter.S + tkinter.W)

        self._score_display = tkinter.Label(master=self._root_window, font=DEFAULT_FONT,
                                            text='BLACK: {} WHITE: {}'.format(self._score[0], self._score[1]))
        self._score_display.grid(row=0, column=0, sticky=tkinter.N + tkinter.E + tkinter.S + tkinter.W)

        self._canvas.bind("<Configure>", self._on_canvas_resize)
        self._canvas.bind("<ButtonRelease>", self._on_canvas_clicked)

        self._root_window.rowconfigure(0, weight=1)
        self._root_window.rowconfigure(1, weight=1)
        self._root_window.rowconfigure(2, weight=1)
        self._root_window.columnconfigure(0, weight=1)

    def _determine_turn(self):
        if self._state['turn'] == 1:
            return "TURN: BLACK"
        else:
            return "TURN: WHITE"

    def start(self):
        OC.OthelloControl(self._canvas, self._col, self._row, self._method).draw_game_state(self._state)
        self._root_window.grab_set()
        self._root_window.wait_window()

    def _turn_in_text(self):
        if self._state['turn'] == 1:
            return "BLACK"
        else:
            return "WHITE"

    def _on_canvas_resize(self, event: tkinter.Event):
        # self._redraw_game_state()
        OC.OthelloControl(self._canvas, self._col, self._row, self._method).redraw_game_state(self._state)

    def _on_canvas_clicked(self, event: tkinter.Event):
        canvas_width = self._canvas.winfo_width()
        canvas_height = self._canvas.winfo_height()

        point_clicked = tuple(OC.from_pixel(event.x, event.y, canvas_width, canvas_height))
        before_truncate = (str(point_clicked[0] * self._col + 1), str(point_clicked[1] * self._row + 1))
        dot_at = (before_truncate[0].index("."), before_truncate[1].index("."))
        move = (int(before_truncate[0][0:dot_at[0]]) , int(before_truncate[1][0:dot_at[1]]))

        OC.OthelloControl(self._canvas,self._col, self._row, self._method).place_move(
            self._state, move, self._score_display, self._turn_display)




