import json


# The function collects all the data from the user
def get_data(mode):
    match mode:
        case 'handfree':
            # allows the handfree drawning (shows the right screen)
            # collects the data from the drawning in two different classes (environment, robot)
            pass
        case 'draw':
            # allows the automatic drawning (shows the dialog fragments to the user)
            # collects the data from the dialogs
            pass
        case _:
            raise Exception('You have to choose either "handfree" or "draw')

    # lastly: creates a json file with the data collected
    produce_json()


# The function produce a json file from the data coming from get_data()
def produce_json():
    pass


if __name__ == '__main__':
    get_data()

