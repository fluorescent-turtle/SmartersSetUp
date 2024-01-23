import json
import tkinter as tk
from tkinter import Tk, ttk, StringVar
from tkinter.ttk import Button

from data_classes import Robot, Environment


def from_dialogs():
    EnvironmentWindow()


def from_handfree():
    pass


# The function produce a json file from the data coming from get_data()
def produce_environment_json(environment):
    with open("environment_file", "w") as environment_file:
        json.dump(environment.model_dump(), environment_file, indent=2)


def produce_robot_json(robot):
    with open("robot_file", "w") as robot_file:
        json.dump(robot.model_dump(), robot_file, indent=2)


class ChooseWindow(Tk):
    def __init__(self):
        super().__init__()

        # window title
        self.title("Smarters")

        window_width = 560
        window_height = 280

        # get the screen dimension
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # find the center point
        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2)

        # set the position of the window to the center of the screen
        self.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

        # parameters entry
        frame = ttk.Frame(self)
        frame.place(anchor='center')

        # field options
        options = {'padx': 20, 'pady': 20}

        # frame label
        frame_label = ttk.Label(self, text='How do you want to create the environment?', font=('Arial', 18))
        frame_label.grid(row=1, column=0, columnspan=3, **options)

        # Graphic drawing
        graphic_button = Button(self, text="By hand drawing", command=self.click_handfree)
        graphic_button.grid(row=2, column=0, columnspan=3)

        # Entries
        entry_button = Button(self, text="By entries", command=self.click_entry)
        entry_button.grid(row=5, column=0, columnspan=3)

        # Back button
        back_button = Button(self, text="Back", command=self.click_back)
        back_button.place(x=80, y=200)

        # add padding to the frame and show it
        frame.grid(padx=20, pady=20)

    def click_entry(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.destroy()
        from_dialogs()

    def click_back(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.destroy()
        RobotWindow()

    def click_handfree(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.destroy()
        from_handfree()


class RobotWindow(Tk):
    def __init__(self):
        super().__init__()

        # window title
        self.title("Smarters")

        window_width = 600
        window_height = 600

        # get the screen dimension
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # find the center point
        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2)

        # set the position of the window to the center of the screen
        self.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

        # parameters entry
        frame = ttk.Frame(self)
        frame.place(anchor='center')

        # field options
        options = {'padx': 8, 'pady': 8}

        # frame label
        frame_label = ttk.Label(self, text='Robot features', font=('Arial', 25))
        frame_label.grid(row=1, column=0, columnspan=3, **options)

        # robot type
        first_label = ttk.Label(frame, text='Robot type: ')
        first_label.grid(column=0, row=2, sticky='W', **options)

        OptionList = [
            "",
            "450X",
            #"405X",
            #"415X",
            "430X"]
        self.robot_type = tk.StringVar()
        self.robot_type.set(OptionList[0])
        robot_entry = tk.OptionMenu(frame, self.robot_type, *OptionList)
        robot_entry.config(width=20, font=("Helvetica", 12))
        robot_entry.grid(column=1, row=2, **options)
        robot_entry.focus()

        # label that guides the user
        frame_label2 = ttk.Label(frame, text='OR')
        frame_label2.grid(column=0, row=3, columnspan=3, **options)

        # speed
        fourth_label = ttk.Label(frame, text='Speed (m/h): ')
        fourth_label.grid(column=0, row=4, sticky='W', **options)

        self.speed = tk.StringVar()
        speed_entry = ttk.Entry(frame, textvariable=self.speed)
        speed_entry.grid(column=1, row=4, **options)
        speed_entry.focus()

        # cutting diameter
        fifth_label = ttk.Label(frame, text='Cutting diameter: ')
        fifth_label.grid(column=0, row=5, sticky='W', **options)

        self.cutting_diameter = tk.StringVar()
        cutting_diameter_entry = ttk.Entry(frame, textvariable=self.cutting_diameter)
        cutting_diameter_entry.grid(column=1, row=5, **options)
        cutting_diameter_entry.focus()

        # autonomy
        sixth_label = ttk.Label(frame, text='Autonomy (minutes): ')
        sixth_label.grid(column=0, row=6, sticky='W', **options)

        self.autonomy: StringVar = tk.StringVar()
        autonomy_entry = ttk.Entry(frame, textvariable=self.autonomy)
        autonomy_entry.grid(column=1, row=6, **options)
        autonomy_entry.focus()

        # guide lines
        #seventh_label = ttk.Label(frame, text='Guide lines (number): ')
        #seventh_label.grid(column=0, row=7, sticky='W', **options)

        #self.guide_lines = tk.IntVar()
        #guide_lines_entry = ttk.Entry(frame, textvariable=self.guide_lines)
        #guide_lines_entry.grid(column=1, row=7, **options)
        #guide_lines_entry.focus()

        # separator
        sep = ttk.Separator(frame, orient='horizontal')
        sep.grid(columnspan=3, row=7, column=0, sticky='ew', **options)

        # cutting mode
        second_label = ttk.Label(frame, text='Cutting mode: ')
        second_label.grid(column=0, row=8, sticky='W', **options)

        OptionList = ["random", "systematic"]
        self.cutting_mode = tk.StringVar()
        self.cutting_mode.set(OptionList[0])
        cutting_mode_entry = tk.OptionMenu(frame, self.cutting_mode, *OptionList)
        cutting_mode_entry.config(width=20, font=("Helvetica", 12))
        cutting_mode_entry.grid(column=1, row=8, **options)
        cutting_mode_entry.focus()

        # bounce mode
        third_label = ttk.Label(frame, text='Bounce mode: ')
        third_label.grid(column=0, row=9, sticky='W', **options)

        OptionList = ["ping-pong", "probability distribution", "random"]
        self.bounce_mode = tk.StringVar()
        self.bounce_mode.set(OptionList[0])
        bounce_mode_entry = tk.OptionMenu(frame, self.bounce_mode, *OptionList)
        bounce_mode_entry.config(width=20, font=("Helvetica", 12))
        bounce_mode_entry.grid(column=1, row=9, **options)
        bounce_mode_entry.focus()

        # shear load
        eighth_label = ttk.Label(frame, text='Shear load: ')
        eighth_label.grid(column=0, row=10, sticky='W', **options)

        self.shear_load = tk.IntVar()
        shear_load_entry = ttk.Entry(frame, textvariable=self.shear_load)
        shear_load_entry.grid(column=1, row=10, **options)
        shear_load_entry.focus()

        # Next button
        next_button = Button(self, text="Next", command=self.click_next)
        next_button.place(x=450, y=500)

        # add padding to the frame and show it
        frame.grid(padx=20, pady=20)

    def click_next(self):
        if self.robot_type.get() == "":
            produce_robot_json(
                Robot(type="", cutting_mode=self.cutting_mode.get(),
                      bounce_mode=self.bounce_mode.get(),
                      speed=float(self.speed.get()), cutting_diameter=float(self.cutting_diameter.get()),
                      autonomy=int(self.autonomy.get()), guide_lines=2, #guide_lines=int(self.guide_lines.get())
                      shear_load=int(self.shear_load.get())))
        else:
            # legge il file
            with open("robots.json", 'r') as robots_file:
                robots = json.load(robots_file)

            robot_mapping = {
                "450X": 0,
                #"405X": 1,
                #"415X": 2,
                "430X": 1
            }

            robot_index = robot_mapping.get(self.robot_type.get(), 2)
            robot_info = robots['robots']['robot'][robot_index]

            robot = Robot(
                type=self.robot_type.get(),
                cutting_mode=self.cutting_mode.get(),
                bounce_mode=self.bounce_mode.get(),
                speed=float(robot_info['speed']),
                cutting_diameter=float(robot_info['cut diameter']),
                autonomy=int(robot_info['autonomy']),
                #guide_lines=int(robot_info['guide lines']),
                shear_load=int(self.shear_load.get())
            )

            # crea il file json
            produce_robot_json(robot)

        for widget in self.winfo_children():
            widget.destroy()
        self.destroy()
        ChooseWindow()


class EnvironmentWindow(Tk):
    def __init__(self):
        super().__init__()

        # window title
        self.title("Smarters")

        window_width = 900
        window_height = 900

        # get the screen dimension
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # find the center point
        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2)

        # set the position of the window to the center of the screen
        self.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

        # parameters entry
        frame = ttk.Frame(self)

        # field options
        options = {'padx': 8, 'pady': 8}

        # frame label
        frame_label = ttk.Label(self, text='Environment features', font=('Arial', 25))
        frame_label.grid(row=1, column=0, **options)

        # length
        first_label = ttk.Label(frame, text='Length (environment): ')
        first_label.grid(column=0, row=0, sticky='W', **options)

        self.length = tk.IntVar()
        length_entry = ttk.Entry(frame, textvariable=self.length)
        length_entry.grid(column=1, row=0, **options)
        length_entry.focus()

        # width
        second_label = ttk.Label(frame, text='Width (environment): ')
        second_label.grid(column=0, row=1, sticky='W', **options)

        self.width = tk.IntVar()
        width_entry = ttk.Entry(frame, textvariable=self.width)
        width_entry.grid(column=1, row=1, **options)
        width_entry.focus()

        # number of blocked areas
        third_label = ttk.Label(frame, text='Blocked areas (number): ')
        third_label.grid(column=0, row=2, sticky='W', **options)

        self.num_blocked_areas = tk.IntVar()
        num_blocked_areas_entry = ttk.Entry(frame, textvariable=self.num_blocked_areas)
        num_blocked_areas_entry.grid(column=1, row=2, **options)
        num_blocked_areas_entry.focus()

        # minimum area of blocked areas
        fourth_label = ttk.Label(frame, text='Min area blocked areas: ')
        fourth_label.grid(column=0, row=3, sticky='W', **options)

        self.min_area = tk.StringVar()
        min_area_entry = ttk.Entry(frame, textvariable=self.min_area)
        min_area_entry.grid(column=1, row=3, **options)
        min_area_entry.focus()

        # maximum area of blocked areas
        fifth_label = ttk.Label(frame, text='Max area blocked areas: ')
        fifth_label.grid(column=0, row=4, sticky='W', **options)

        self.max_area = tk.StringVar()
        max_area_entry = ttk.Entry(frame, textvariable=self.max_area)
        max_area_entry.grid(column=1, row=4, **options)
        max_area_entry.focus()

        # number of circles in blocked areas
        sixth_label = ttk.Label(frame, text='Number of circles (blocked areas): ')
        sixth_label.grid(column=0, row=5, sticky='W', **options)

        self.circles = tk.StringVar()
        circles_entry = ttk.Entry(frame, textvariable=self.circles)
        circles_entry.grid(column=1, row=5, **options)
        circles_entry.focus()

        # number of squares in blocked areas
        seventh_label = ttk.Label(frame, text='Number of squares (blocked areas): ')
        seventh_label.grid(column=0, row=6, sticky='W', **options)

        self.squares = tk.StringVar()
        squares_entry = ttk.Entry(frame, textvariable=self.squares)
        squares_entry.grid(column=1, row=6, **options)
        squares_entry.focus()

        # Isolated area features
        eighth_label = ttk.Label(frame, text='Length (isolated area): ')
        eighth_label.grid(column=0, row=8, sticky='W', **options)

        self.isolated_area_len = tk.StringVar()
        isolated_area_len_entry = ttk.Entry(frame, textvariable=self.isolated_area_len)
        isolated_area_len_entry.grid(column=1, row=8, **options)
        isolated_area_len_entry.focus()

        ninth_label = ttk.Label(frame, text='Width (isolated area): ')
        ninth_label.grid(column=0, row=9, sticky='W', **options)

        self.isolated_area_wid = tk.StringVar()
        isolated_area_wid_entry = ttk.Entry(frame, textvariable=self.isolated_area_wid)
        isolated_area_wid_entry.grid(column=1, row=9, **options)
        isolated_area_wid_entry.focus()

        tenth_label = ttk.Label(frame, text='Shape (isolated area): ')
        tenth_label.grid(column=0, row=10, sticky='W', **options)

        OptionList = ["Square", "Circle"]
        self.shape = tk.StringVar()
        self.shape.set(OptionList[0])
        shape_entry = tk.OptionMenu(frame, self.shape, *OptionList)
        shape_entry.config(width=20, font=("Helvetica", 12))
        shape_entry.grid(column=1, row=10, **options)
        shape_entry.focus()

        # Done button
        done_button = Button(self, text="Done", command=self.click_done)
        done_button.place(x=800, y=820)

        # Back button
        back_button = Button(self, text="Back", command=self.click_back)
        back_button.place(x=50, y=820)

        # add padding to the frame and show it
        frame.grid(padx=20, pady=20)

    def click_done(self):
        produce_environment_json(
            Environment(num_blocked_areas=self.num_blocked_areas.get(), num_blocked_circles=self.circles.get(),
                        num_blocked_squares=self.squares.get(), length_field=float(self.length.get()),
                        width_field=float(self.width.get()), min_area_blocked=float(self.min_area.get()),
                        max_area_blocked=float(self.max_area.get()),
                        isolated_area_length=float(self.isolated_area_len.get()),
                        isolated_area_width=float(self.isolated_area_wid.get()), isolated_area_shape=self.shape.get()))
        exit()

    def click_back(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.destroy()
        ChooseWindow()
