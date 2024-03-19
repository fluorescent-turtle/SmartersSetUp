"""
Main functions and classes for environment setup using dialogs.

This module provides functionality to create and configure environments,
robots, and simulators using dialog windows in a Tkinter-based GUI.

Functions:
    from_dialogs: Open the environment creation window using dialogs.
    from_handfree: Placeholder function for future implementation of hand free environment creation.
    produce_simulator_json: Produce a JSON file from the data provided by a simulator object.
    produce_environment_json: Produce a JSON file from the data provided by an environment object.
    produce_robot_json: Produce a JSON file from the data provided by a robot object.
    run_second_program: Run the second program using subprocess.

Classes:
    ChooseWindow: Main window for choosing how to create the environment.
    RobotWindow: Window for configuring robot features.
    EnvironmentWindow: Window for configuring environment features.
    SimulatorWindow: Main window for the simulator application.
"""

import json
import os
import subprocess
import tkinter as tk
from tkinter import Tk, ttk, filedialog
from tkinter.ttk import Button

from data_classes import Robot, Environment, Simulator


def produce_environment_json(environment):
    """
    Produce a JSON file from the data provided by an environment object.

    :param environment: The environment object containing data to be dumped into JSON.
    """
    with open("environment_file", "w") as environment_file:
        json.dump(environment.model_dump(), environment_file, indent=2)


def produce_robot_json(robot):
    """
    Produce a JSON file from the data provided by a robot object.

    :param robot: The robot object containing data to be dumped into JSON.
    """
    with open("robot_file", "w") as robot_file:
        json.dump(robot.model_dump(), robot_file, indent=2)


def produce_simulator_json(simulator):
    """
    Produce a JSON file from the data provided by a simulator object.

    :param simulator: The simulator object containing data to be dumped into JSON.
    """
    with open("simulator_file", "w") as simulation_file:
        json.dump(simulator.model_dump(), simulation_file, indent=2)


def from_dialogs():
    """
    Open the environment creation window using dialogs.
    """
    EnvironmentWindow()


def from_handfree():
    """
    Placeholder function for future implementation of hand free environment creation.
    """
    pass


def run_second_program(path_smarters):
    """
    Run the second program using subprocess.

    :param path_smarters: The path to the second program.
    """
    # Check if the file exists
    if not os.path.exists(path_smarters):
        raise FileNotFoundError(f"The file '{path_smarters}' does not exist.")

    # Run the second program
    subprocess.Popen(["python", path_smarters])


class ChooseWindow(Tk):
    """
    Main window for choosing how to create the environment.
    """

    def __init__(self):
        """
        Initialize the ChooseWindow.
        """
        super().__init__()

        # Set window title and dimensions
        self.title("SetUpSmarters")
        window_width = 560
        window_height = 280

        # Calculate window position
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        center_x = (screen_width - window_width) // 2
        center_y = (screen_height - window_height) // 2

        # Set window geometry
        self.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")

        # Parameters entry
        frame = ttk.Frame(self)
        frame.place(anchor="center")

        # Frame label
        frame_label = ttk.Label(
            self, text="How do you want to create the environment?", font=("Arial", 18)
        )
        frame_label.grid(row=1, column=0, columnspan=3, padx=20, pady=20)

        # Buttons
        buttons = [
            ("By hand drawing", self.click_handfree),
            ("By entries", self.click_entry),
        ]
        for i, (text, command) in enumerate(buttons, start=2):
            button = Button(self, text=text, command=command)
            button.grid(row=i, column=0, columnspan=3, padx=20, pady=10)

        # Back button
        back_button = Button(self, text="Back", command=self.click_back)
        back_button.place(x=80, y=200)

    def click_entry(self):
        """
        Handle the click event for the "By entries" button.
        """
        self.clear_and_destroy(from_dialogs)

    def click_back(self):
        """
        Handle the click event for the "Back" button.
        """
        self.clear_and_destroy(RobotWindow)

    def click_handfree(self):
        """
        Handle the click event for the "By hand drawing" button.
        """
        self.clear_and_destroy(from_handfree)

    def clear_and_destroy(self, callback):
        """
        Clear the window widgets and destroy the window, then call the specified callback.

        :param callback: The callback function to be called after destroying the window.
        """
        for widget in self.winfo_children():
            widget.destroy()
        self.destroy()
        callback()


class RobotWindow(Tk):
    """
    Window for configuring robot features.
    """

    def __init__(self):
        """
        Initialize the RobotWindow.
        """
        super().__init__()

        # window title
        self.dialog_opened = False
        self.title("SetUpSmarters")

        window_width = 600
        window_height = 600

        # get the screen dimension and find the center point
        screen_width, screen_height = self.winfo_screenwidth(), self.winfo_screenheight()
        center_x, center_y = screen_width // 2 - window_width // 2, screen_height // 2 - window_height // 2

        # set the position of the window to the center of the screen
        self.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")

        # parameters entry
        frame = ttk.Frame(self)
        frame.place(anchor="center")

        # field options
        options = {"padx": 8, "pady": 8}

        # Add frame label
        ttk.Label(self, text="Robot features", font=("Arial", 25)).grid(row=1, column=0, columnspan=3, **options)

        # Add robot type entry
        ttk.Label(frame, text="Robot type: ").grid(column=0, row=2, sticky="W", **options)
        OptionList = ["", "450X", "430X"]
        self.robot_type = tk.StringVar()
        self.robot_type.set(OptionList[0])
        robot_entry = tk.OptionMenu(frame, self.robot_type, *OptionList)
        robot_entry.config(width=20, font=("Helvetica", 12))
        robot_entry.grid(column=1, row=2, **options)
        robot_entry.focus()

        # Label that guides the user
        ttk.Label(frame, text="OR").grid(column=0, row=3, columnspan=3, **options)

        # Add fields for robot features
        fields = [
            ("Speed (m/h): ", tk.StringVar()),
            ("Cutting diameter: ", tk.StringVar()),
            ("Autonomy (minutes): ", tk.StringVar()),
            ("Shear load: ", tk.IntVar()),
        ]

        self.speed, self.cutting_diameter, self.autonomy, self.shear_load = [var for _, var in fields]

        for i, (label_text, var) in enumerate(fields, start=4):
            ttk.Label(frame, text=label_text).grid(column=0, row=i, sticky="W", **options)
            entry = ttk.Entry(frame, textvariable=var)
            entry.grid(column=1, row=i, **options)
            entry.focus()

        # Add cutting mode entry
        ttk.Label(frame, text="Cutting mode: ").grid(column=0, row=8, sticky="W", **options)
        self.cutting_mode = tk.StringVar()
        self.cutting_mode.set("")
        self.OptionCuttingList = [
            "",
            "random - ping-pong",
            "random - probability distribution",
            "random - random",
            "systematic - ping-pong",
            "systematic - probability distribution",
            "systematic - random",
            "Load your JSON file",
        ]
        self.cutting_mode_entry = tk.OptionMenu(
            frame,
            self.cutting_mode,
            *self.OptionCuttingList,
            command=lambda x: self.open_file_dialog() if self.cutting_mode.get() == "Load your JSON file" else None,
        )
        self.cutting_mode_entry.config(width=20, font=("Helvetica", 12))
        self.cutting_mode_entry.grid(column=1, row=8, **options)

        # Add Next button
        Button(self, text="Next", command=self.click_next).place(x=450, y=500)

        # add padding to the frame and show it
        frame.grid(padx=20, pady=20)

    def open_file_dialog(self):
        """
        Open a file dialog to select a JSON file for cutting mode.
        """
        if not getattr(self, "dialog_opened", False):
            self.dialog_opened = True
            file_path = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
            if file_path:
                print("File selezionato:", file_path)
                file_name = os.path.basename(file_path)
                load_json_index = self.OptionCuttingList.index("Load your JSON file")
                self.OptionCuttingList[load_json_index] = file_name
                self.update_cutting_mode_menu()
                if self.cutting_mode.get() == "Load your JSON file":
                    self.cutting_mode.set(file_name)
            self.dialog_opened = False

    def update_cutting_mode_menu(self):
        """
        Update the cutting mode menu with the loaded JSON file.
        """
        selected_option = self.cutting_mode.get()
        self.cutting_mode_entry["menu"].delete(0, "end")
        for option in self.OptionCuttingList:
            if option == "Load your JSON file":
                self.cutting_mode_entry["menu"].add_command(
                    label=option, command=self.open_file_dialog
                )
            else:
                self.cutting_mode_entry["menu"].add_command(
                    label=option,
                    command=lambda value=option: self.cutting_mode.set(value),
                )
        if selected_option in self.OptionCuttingList:
            self.cutting_mode.set(selected_option)

    def click_next(self):
        """
        Handle the click event for the "Next" button.
        """
        robot_type = self.robot_type.get()
        cutting_mode = self.cutting_mode.get()

        if cutting_mode == "Load your JSON file":
            algo = os.path.abspath(cutting_mode)
            cutting_mode = ""
        elif cutting_mode in [
            "random - ping-pong",
            "random - probability distribution",
            "random - random",
            "systematic - ping-pong",
            "systematic - probability distribution",
            "systematic - random",
        ]:
            algo = ""
        else:
            algo = os.path.abspath(cutting_mode)
            cutting_mode = ""

        if not robot_type:
            robot = Robot(
                type="",
                cutting_mode_bounce_mode=cutting_mode,
                speed=float(self.speed.get()),
                cutting_diameter=float(self.cutting_diameter.get()),
                autonomy=int(self.autonomy.get()),
                guide_lines=2,
                shear_load=int(self.shear_load.get()),
                algo=algo,
            )
        else:
            with open("robots.json", "r") as robots_file:
                robots = json.load(robots_file)

            robot_index = {"450X": 0, "430X": 1}.get(robot_type, 2)
            robot_info = robots["robots"]["robot"][robot_index]

            robot = Robot(
                type=robot_type,
                cutting_mode=cutting_mode,
                speed=float(robot_info["speed"]),
                cutting_diameter=float(robot_info["cut diameter"]),
                autonomy=int(robot_info["autonomy"]),
                shear_load=int(self.shear_load.get()),
                algo=algo,
            )

        produce_robot_json(robot)

        for widget in self.winfo_children():
            widget.destroy()
        self.destroy()
        ChooseWindow()


class EnvironmentWindow(Tk):
    """
    Window for configuring environment features.
    """

    def __init__(self):
        """
        Initialize the EnvironmentWindow.
        """
        super().__init__()

        # window title
        self.absolute_path = None
        self.title("SetUpSmarters")

        window_width = 900
        window_height = 900

        # get the screen dimension and find the center point
        screen_width, screen_height = self.winfo_screenwidth(), self.winfo_screenheight()
        center_x, center_y = screen_width // 2 - window_width // 2, screen_height // 2 - window_height // 2

        # set the position of the window to the center of the screen
        self.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")

        # parameters entry
        frame = ttk.Frame(self)

        # field options
        options = {"padx": 8, "pady": 8}

        # frame label
        ttk.Label(self, text="Environment features", font=("Arial", 25)).grid(row=1, column=0, **options)

        entries = [
            ("Length (environment): ", tk.StringVar()),
            ("Width (environment): ", tk.StringVar()),
            ("Number of squares (blocked areas): ", tk.IntVar()),
            ("Min width (blocked squares): ", tk.StringVar()),
            ("Max width (blocked squares): ", tk.StringVar()),
            ("Min height (blocked squares): ", tk.StringVar()),
            ("Max height (blocked squares): ", tk.StringVar()),
            ("Number of circles (blocked areas): ", tk.IntVar()),
            ("Ray (if circles): ", tk.StringVar()),
            ("Length (isolated area): ", tk.StringVar()),
            ("Width (isolated area): ", tk.StringVar()),
            ("Radius (isolated area): ", tk.StringVar()),
        ]

        for i, (label_text, var) in enumerate(entries):
            ttk.Label(frame, text=label_text).grid(row=i, column=0, sticky="W", **options)
            entry = ttk.Entry(frame, textvariable=var)
            entry.grid(row=i, column=1, **options)
            entry.focus()

        # Isolated area shape
        ttk.Label(frame, text="Shape (isolated area): ").grid(row=len(entries), column=0, sticky="W", **options)
        option_list = ["Square", "Circle"]
        shape_var = tk.StringVar()
        shape_var.set(option_list[0])
        option_menu = tk.OptionMenu(frame, shape_var, *option_list)
        option_menu.config(width=20, font=("Helvetica", 12))
        option_menu.grid(row=len(entries), column=1, **options)
        option_menu.focus()

        # Extra data
        ttk.Label(frame, text="Load your data: ").grid(row=len(entries) + 1, column=0, sticky="W", **options)
        button = tk.Button(frame, text="Open", command=self.button_click)
        button.config(width=20, font=("Helvetica", 12))
        button.grid(row=len(entries) + 1, column=1, **options)

        # Done button
        Button(self, text="Next", command=self.click_next).place(x=800, y=820)

        # Back button
        Button(self, text="Back", command=self.click_back).place(x=10, y=820)

        # add padding to the frame and show it
        frame.grid(padx=20, pady=20)

        self.entries = dict(entries)
        self.shape = shape_var
        self.button = button

    def button_click(self):
        """
        Open a file dialog to select a JSON file for extra data.
        """
        file_path = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
        if file_path:
            self.absolute_path = os.path.abspath(file_path)
            print("File selected:", self.absolute_path)
            self.button.config(text=os.path.basename(self.absolute_path))

    def click_back(self):
        """
        Handle the click event for the "Back" button.
        """
        self.destroy()
        RobotWindow()

    def click_next(self):
        """
        Handle the click event for the "Next" button.
        """
        environment_params = {key: value.get() for key, value in self.entries.items()}
        environment_params["ray"] = environment_params.get("ray") or None
        environment_params["isolated_area_radius"] = environment_params.get("isolated_area_radius") or None
        environment_params["isolated_area_shape"] = self.shape.get()
        environment_params["extra_data_path"] = self.absolute_path

        environment = Environment(**environment_params)
        produce_environment_json(environment)

        self.destroy()
        SimulatorWindow()


class SimulatorWindow(Tk):
    """
    Main window for the simulator application.
    """

    def __init__(self):
        """
        Initialize the SimulatorWindow.
        """
        super().__init__()

        # window title
        self.title("SetUpSmarters")

        window_width = 900
        window_height = 900

        # get the screen dimension and find the center point
        screen_width, screen_height = self.winfo_screenwidth(), self.winfo_screenheight()
        center_x, center_y = screen_width // 2 - window_width // 2, screen_height // 2 - window_height // 2

        # set the position of the window to the center of the screen
        self.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")

        # Create parameters entry frame
        frame = ttk.Frame(self)
        frame.place(anchor="center")

        # Define options for fields
        options = {"padx": 20, "pady": 20}

        # Add frame label
        ttk.Label(self, text="Simulator features", font=("Arial", 18)).grid(row=1, column=0, columnspan=3, **options)

        entries = [
            ("Dimension of the tassel (m): ", tk.StringVar(), "0.5"),
            ("Cutting cycle time (h): ", tk.IntVar()),
            ("Repetition times: ", tk.IntVar())
        ]

        for i, (label_text, var, default_value) in enumerate(entries):
            ttk.Label(frame, text=label_text).grid(column=0, row=i+2, sticky="W", **options)
            entry = ttk.Entry(frame, textvariable=var)
            entry.grid(column=1, row=i+2, **options)
            entry.insert(0, default_value)
            entry.focus()

        # Add Next button
        tk.Button(self, text="Done", command=self.click_done).place(x=350, y=400)

        # Add padding to the frame and show it
        frame.grid(padx=20, pady=20)

        self.entries = dict(entries)

    def click_done(self):
        """
        Handle the click event for the "Done" button.
        """
        simulator_params = {key: value.get() for key, value in self.entries.items()}
        simulator = Simulator(**simulator_params)

        produce_simulator_json(simulator)
        run_second_program("smarters.py") # todo: qui ci va il nome del plugin di default

        self.destroy()
