# Kelly Pham 25384246. Project 5

import tkinter

import OthelloApplication

import OthelloLogic
game = OthelloLogic.Othello()

DEFAULT_FONT = ("helvetica", 20)


class Welcome:
    def __init__(self):
        self._root_window = tkinter.Tk()
        self._root_window.wm_title("Welcome to Othello!")

        greeting_label = tkinter.Label(master=self._root_window, text="Welcome to Othello, Kel's version!",
                                       font=DEFAULT_FONT)
        greeting_label.grid(row=0, columnspan=2, padx=20, sticky=tkinter.S)

        self._row_label = tkinter.Label(master=self._root_window, text="How many rows?\n# 4 to 16", font=DEFAULT_FONT)
        self._row_label.grid(row=1, column=0, padx=10, sticky=tkinter.W + tkinter.N + tkinter.S)

        self._column_label = tkinter.Label(master=self._root_window, text="How many columns?\n# 4 to 16",
                                           font=DEFAULT_FONT)
        self._column_label.grid(row=2, column=0, padx=10, sticky=tkinter.W + tkinter.N + tkinter.S)

        self._player_label = tkinter.Label(master=self._root_window, text="Who goes first?\nType B or W",
                                           font=DEFAULT_FONT)
        self._player_label.grid(row=3, column=0, padx=10, sticky=tkinter.W + tkinter.N + tkinter.S)

        self._arrangement_label = tkinter.Label(master=self._root_window, text="How to arrange?\nType B or W",
                                                font=DEFAULT_FONT)
        self._arrangement_label.grid(row=4, column=0, padx=10, sticky=tkinter.W + tkinter.N + tkinter.S)

        self._win_method_label = tkinter.Label(master=self._root_window, text="How to win?\nType > or <",
                                               font=DEFAULT_FONT)
        self._win_method_label.grid(row=5, column=0, padx=10, sticky=tkinter.W + tkinter.N + tkinter.S)

        self._row_entry = tkinter.Entry(master=self._root_window, width=10, font=DEFAULT_FONT)
        self._row_entry.grid(row=1, column=1, sticky=tkinter.W + tkinter.E + tkinter.N + tkinter.S)

        self._column_entry = tkinter.Entry(master=self._root_window, width=10, font=DEFAULT_FONT)
        self._column_entry.grid(row=2, column=1, sticky=tkinter.W + tkinter.E + tkinter.N + tkinter.S)

        self._player_entry = tkinter.Entry(master=self._root_window, width=10, font=DEFAULT_FONT)
        self._player_entry.grid(row=3, column=1, sticky=tkinter.W + tkinter.E + tkinter.N + tkinter.S)

        self._arrange_entry = tkinter.Entry(master=self._root_window, width=10, font=DEFAULT_FONT)
        self._arrange_entry.grid(row=4, column=1, sticky=tkinter.W + tkinter.E + tkinter.N + tkinter.S)

        self._method_entry = tkinter.Entry(master=self._root_window, width=10, font=DEFAULT_FONT)
        self._method_entry.grid(row=5, column=1, sticky=tkinter.W + tkinter.E + tkinter.N + tkinter.S)

        self._root_window.rowconfigure(1, weight=1)
        self._root_window.rowconfigure(2, weight=1)
        self._root_window.rowconfigure(3, weight=1)
        self._root_window.rowconfigure(4, weight=1)
        self._root_window.rowconfigure(5, weight=1)
        self._root_window.columnconfigure(1, weight=1)

        start_button = tkinter.Button(master=self._root_window, text="Start!", font=DEFAULT_FONT,
                                      command=self._on_start_clicked)
        start_button.grid(row=6, column=1, padx=10, sticky=tkinter.W + tkinter.E + tkinter.N + tkinter.S)

    def _on_start_clicked(self):
        self._row = self._row_entry.get()
        self._column = self._column_entry.get()
        self._player = self._player_entry.get()
        self._arrange = self._arrange_entry.get()
        self._method = self._method_entry.get()

        try:
            self._row = int(self._row)
            self._column = int(self._column)
            if self._player.upper() in ['B', 'W'] and self._arrange.upper() in ['B', 'W'] and self._method in ['<', '>']:
                original_board = game.create_table(self._player.upper(), self._arrange.upper(), self._column, self._row)
                self._root_window.destroy()
                OthelloApplication.OthelloApp(original_board, self._column, self._row, self._method).start()
        except ValueError:
            self._error_print = tkinter.Label(master=self._root_window,
                                              text="One or more of the above field is invalid", font=DEFAULT_FONT)
            self._error_print.grid(row=6, column=0, padx=10, sticky=tkinter.W + tkinter.E + tkinter.N + tkinter.S)

    def greet(self):
        self._root_window.mainloop()

if __name__ == "__main__":
    Welcome().greet()





