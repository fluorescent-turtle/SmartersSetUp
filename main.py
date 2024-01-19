from gui import RobotWindow


def from_dialogs():
    RobotWindow().mainloop()


def from_handfree():
    pass


# The function collects all the data from the user
def get_data(mode):
    match mode:
        case 'handfree':
            from_handfree()
            pass
        case 'draw':
            from_dialogs()
            pass
        case _:
            raise Exception('You have to choose either "handfree" or "draw')


if __name__ == '__main__':
    get_data('draw')  # todo:da dove prendo il mode per data?
