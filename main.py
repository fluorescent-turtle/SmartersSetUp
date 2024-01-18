import json

from data_classes import Environment, Robot
from gui import Window


#from ctypes import windll


def from_dialogs(environment, robot):
    pass


def from_handfree(environment, robot):
    pass


# The function collects all the data from the user
def get_data(mode):
    environment = Environment()
    robot = Robot()
    match mode:
        case 'handfree':
            from_handfree(environment, robot)
            pass
        case 'draw':
            from_dialogs(environment, robot)
            pass
        case _:
            raise Exception('You have to choose either "handfree" or "draw')

    # lastly: creates a json file with the data collected
    produce_json(robot)


# The function produce a json file from the data coming from get_data()
def produce_json(robot):
    with open("data_file", "w") as data_file:
        json.dump(robot.model_dump(), data_file, indent=2)


if __name__ == '__main__':
    Window().mainloop()
