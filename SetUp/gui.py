
""" Copyright 2024 SetUpSmarters

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

     https://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License."""

import json
import math
import os
import subprocess
import sys
import tkinter as tk
from tkinter import Tk, ttk
from tkinter import simpledialog, filedialog, colorchooser
from tkinter.ttk import Button

import numpy as np
from future.moves.tkinter import simpledialog, colorchooser
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from SetUp.data_classes import RobotConfig, EnvConfig, SimulatorConfig, ConfigEncoder

# Global objects
python_objects = []
objects_data = {
    "length": 100.0,
    "width": 100.0,
    "circles": [],
    "squares": [],
    "isolated_area": [],
    "opening": [],
}


def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.abspath("."))
    return os.path.join(base_path, relative_path)


def produce_json(data):
    data_config = {"robot": data[0], "env": data[2], "simulator": data[1]}
    with open("data_file", "w") as data_file:
        json.dump(data_config, data_file, cls=ConfigEncoder, indent=2)


def from_dialogs():
    """Open the environment creation window using dialogs."""
    EnvironmentWindow()


def add_isolated_area():
    shape = simpledialog.askstring("Input", "Enter the isolated area shape:")
    d_tassel = python_objects[1].dim_tassel

    if shape == "Square":
        x, y = get_coordinates("bottom-left corner")
        width, height = get_dimensions()
        opening_x, opening_y = get_coordinates("openings' bottom-left corner")
        opening_width, opening_height = get_dimensions("opening")

        draw_rectangle(x, y, width, height, "black")
        draw_rectangle(opening_x, opening_y, opening_width, opening_height, "yellow")

        update_area_coordinates(x, y, width, height, d_tassel, "isolated_area")
    else:
        x_center, y_center, radius = get_circle_data()
        opening_x, opening_y = get_coordinates("openings' bottom-left corner")
        opening_width, opening_height = get_dimensions("opening")

        color = colorchooser.askcolor()[1]
        label = simpledialog.askstring("Input", "Enter the label:")

        draw_circle(x_center, y_center, radius, color, label)
        draw_rectangle(opening_x, opening_y, opening_width, opening_height, "yellow")

        update_area_coordinates_for_circle(x_center, y_center, radius, d_tassel, "is_area")

    update_area_coordinates(opening_x, opening_y, opening_width, opening_height, d_tassel, "opening")


def add_square():
    x, y = get_coordinates("bottom-left corner")
    width, height = get_dimensions()
    color = colorchooser.askcolor()[1]
    label = simpledialog.askstring("Input", "Enter the label:")

    draw_rectangle(x, y, width, height, color, label)
    update_area_coordinates(x, y, width, height, python_objects[1].dim_tassel, "squares")


def add_circle():
    x_center, y_center, radius = get_circle_data()
    color = colorchooser.askcolor()[1]
    label = simpledialog.askstring("Input", "Enter the label:")

    draw_circle(x_center, y_center, radius, color, label)
    update_area_coordinates_for_circle(x_center, y_center, radius, python_objects[1].dim_tassel, "circles")


def draw_map():
    ax.clear()
    width, length = objects_data["width"], objects_data["length"]
    tile_size = python_objects[1].dim_tassel
    x_positions = np.arange(0, width, tile_size)
    y_positions = np.arange(0, length, tile_size)

    for x in x_positions:
        for y in y_positions:
            ax.add_patch(plt.Rectangle((x, y), tile_size, tile_size, fill=None, edgecolor='black'))

    ax.set_xlim(0, width)
    ax.set_ylim(0, length)
    ax.set_aspect('equal')
    canv.draw()


def get_grid_dimensions():
    """Ask for grid dimensions using a simple dialog."""
    root = tk.Tk()
    root.withdraw()
    objects_data["length"] = simpledialog.askfloat("Grid Size", "Enter the length of the grid:", initialvalue=100.0)
    objects_data["width"] = simpledialog.askfloat("Grid Size", "Enter the width of the grid:", initialvalue=100.0)
    root.destroy()


class HandFreeWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        get_grid_dimensions()
        self.setup_map_editor()

    def setup_map_editor(self):
        """Setup the map editor window."""
        global ax, canv
        self.title("Map Editor")
        fig, ax = plt.subplots(figsize=(10, 10))

        top_frame, bottom_frame = tk.Frame(self), tk.Frame(self)
        top_frame.pack(side=tk.TOP, fill=tk.X)
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)

        canv = FigureCanvasTkAgg(fig, master=self)
        canv.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.create_buttons(top_frame, bottom_frame)
        draw_map()

    def create_buttons(self, top_frame, bottom_frame):
        """Create all the buttons for the map editor."""
        buttons = [
            ("Add Circle", add_circle),
            ("Add Square", add_square),
            ("Add Isolated Area", add_isolated_area),
            ("Back", self.click_back),
            ("Done", self.click_next),
        ]
        for name, command in buttons[:3]:
            tk.Button(top_frame, text=name, command=command).pack(side=tk.LEFT)
        for name, command in buttons[3:]:
            tk.Button(bottom_frame, text=name, command=command).pack(side=tk.RIGHT)

    def click_back(self):
        """Handle the click event for the "Back" button."""
        self.destroy()
        ChooseWindow()

    def click_next(self):
        """Handle the click event for the "Next" button."""
        python_objects.append(objects_data)
        produce_json(python_objects)
        self.destroy()


def get_coordinates(label="point"):
    """Get coordinates through dialogs."""
    x = simpledialog.askfloat("Input", f"Enter the x coordinate of the {label}:")
    y = simpledialog.askfloat("Input", f"Enter the y coordinate of the {label}:")
    return x, y


def get_dimensions(label="area"):
    """Get width and height through dialogs."""
    width = simpledialog.askfloat("Input", f"Enter the width of the {label}:")
    height = simpledialog.askfloat("Input", f"Enter the height of the {label}:")
    return width, height


def get_circle_data():
    """Get the center coordinates and radius for a circle."""
    x_center = simpledialog.askfloat("Input", "Enter the x coordinate of the center:")
    y_center = simpledialog.askfloat("Input", "Enter the y coordinate of the center:")
    radius = simpledialog.askfloat("Input", "Enter the radius:")
    return x_center, y_center, radius


def draw_rectangle(x, y, width, height, color, label=None):
    """Draw a rectangle on the map."""
    ax.add_patch(plt.Rectangle((x, y), width, height, color=color, alpha=0.5, label=label))
    plt.draw()


def draw_circle(x_center, y_center, radius, color, label=None):
    """Draw a circle on the map."""
    ax.add_patch(plt.Circle((x_center, y_center), radius, color=color, alpha=0.5, label=label))
    plt.draw()


def update_area_coordinates(x, y, width, height, d_tassel, area_type):
    """Update the coordinates for a rectangular area."""
    x, y = round(x / d_tassel), round(y / d_tassel)
    end_x, end_y = x + round(width / d_tassel), y + round(height / d_tassel)
    for i in range(x, end_x):
        for j in range(y, end_y):
            objects_data[area_type].append((i, j))


def update_area_coordinates_for_circle(x_center, y_center, radius, d_tassel, area_type):
    """Update the coordinates for a circular area."""
    x_center, y_center = math.floor(x_center / d_tassel), math.floor(y_center / d_tassel)
    radius = round(radius / d_tassel)

    for i in range(int(objects_data["length"] / d_tassel)):
        for j in range(int(objects_data["width"] / d_tassel)):
            dist = math.hypot(i - x_center, j - y_center)
            if dist <= radius:
                objects_data[area_type].append((i, j))



def from_handfree():
    """
    Open the HandFreeWindow.

    """
    HandFreeWindow()


def run_second_program(path_smarters):
    """
    Run the second program using subprocess.

    :param path_smarters: The path to the second program to run.
    :type path_smarters: str
    :raises FileNotFoundError: If the file at path_smarters does not exist.
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

        # Create frame for parameters entry
        frame = ttk.Frame(self)
        frame.place(anchor="center")

        # Frame label
        frame_label = ttk.Label(
            self, text="How do you want to create the environment?", font=("Arial", 18)
        )
        frame_label.grid(row=1, column=0, columnspan=3, padx=20, pady=20)

        # Create buttons for choosing environment creation method
        buttons = [
            ("By drawings", self.click_handfree),
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
        self.clear_and_destroy(SimulatorWindow)

    def click_handfree(self):
        """
        Handle the click event for the "By drawings" button.
        """
        self.clear_and_destroy(from_handfree)

    def clear_and_destroy(self, callback):
        """
        Clear the window widgets and destroy the window, then call the specified callback.

        :param callback: The callback function to be called after destroying the window.
        :type callback: callable
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

        # Window title
        self.dialog_opened = False
        self.title("SetUpSmarters")

        window_width = 600
        window_height = 600

        # Get the screen dimensions and calculate center position
        screen_width, screen_height = (
            self.winfo_screenwidth(),
            self.winfo_screenheight(),
        )
        center_x, center_y = (
            screen_width // 2 - window_width // 2,
            screen_height // 2 - window_height // 2,
        )

        # Set window position to the center of the screen
        self.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")

        # Create frame for parameters entry
        frame = ttk.Frame(self)
        frame.place(anchor="center")

        # Define field options
        options = {"padx": 8, "pady": 8}

        # Add frame label
        ttk.Label(self, text="Robot features", font=("Arial", 25)).grid(
            row=1, column=0, columnspan=3, **options
        )

        # Add robot type dropdown menu
        ttk.Label(frame, text="Robot type: ").grid(
            column=0, row=2, sticky="W", **options
        )
        OptionList = ["", "450X", "430X", "405X", "415X"]
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
        ]

        self.speed, self.cutting_diameter, self.autonomy = [var for _, var in fields]

        for i, (label_text, var) in enumerate(fields, start=4):
            ttk.Label(frame, text=label_text).grid(
                column=0, row=i, sticky="W", **options
            )
            entry = ttk.Entry(frame, textvariable=var)
            entry.grid(column=1, row=i, **options)
            entry.focus()

        # Divider
        divider = ttk.Separator(frame, orient="horizontal")
        divider.grid(column=0, row=7, columnspan=2, sticky="ew", pady=(10, 0))

        # Add cutting mode dropdown menu
        ttk.Label(frame, text="Cutting mode - bounce mode: ").grid(
            column=0, row=8, sticky="W", **options
        )
        self.cutting_mode = tk.StringVar()
        self.cutting_mode.set("")
        self.OptionCuttingList = [
            "",
            "random - ping-pong",
            "random - random",
            "systematic - ping-pong",
            "systematic - random",
            "Load your JSON file",
        ]
        self.cutting_mode_entry = tk.OptionMenu(
            frame,
            self.cutting_mode,
            *self.OptionCuttingList,
            command=lambda x: self.open_file_dialog()
            if self.cutting_mode.get() == "Load your JSON file"
            else None,
        )
        self.cutting_mode_entry.config(width=30, font=("Helvetica", 12))
        self.cutting_mode_entry.grid(column=1, row=8, **options)

        # Add Next button
        Button(self, text="Next", command=self.click_next).place(x=450, y=500)

        # Add padding to the frame and display it
        frame.grid(padx=20, pady=20)

    def open_file_dialog(self):
        """
        Open a file dialog to select a JSON file for cutting mode.
        """
        if not getattr(self, "dialog_opened", False):
            self.dialog_opened = True
            file_path = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
            if file_path:
                print("Selected file:", file_path)
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
        cutting_mo = self.cutting_mode.get()

        if cutting_mo == "Load your JSON file":
            algo = os.path.abspath(cutting_mo)
            cutting_mo = ""
        elif cutting_mo in [
            "random - ping-pong",
            "random - random",
            "systematic - ping-pong",
            "systematic - random",
        ]:
            algo = ""
        else:
            algo = os.path.abspath(cutting_mo)
            cutting_mo = ""

        if not robot_type:
            robot = RobotConfig(
                type="",
                cutting_mode=cutting_mo,
                speed=float(self.speed.get()),
                cutting_diameter=float(self.cutting_diameter.get()),
                autonomy=int(self.autonomy.get()),
                guide_lines=2,
                algo=algo,
            )
        else:
            with open(resource_path("robots.json"), "r") as robots_file:
                robots = json.load(robots_file)

            robot_index = {"450X": 0, "430X": 1}.get(robot_type, 2)
            robot_info = robots["robots"]["robot"][robot_index]

            robot = RobotConfig(
                type=robot_type,
                cutting_mode=cutting_mo,
                speed=float(robot_info["speed"]),
                cutting_diameter=float(robot_info["cut diameter"]),
                autonomy=int(robot_info["autonomy"]),
                guide_lines=2,
                algo=algo,
            )

        python_objects.append(robot)

        for widget in self.winfo_children():
            widget.destroy()
        self.destroy()
        SimulatorWindow()


class EnvironmentWindow(Tk):
    """
    Window for configuring environment features.
    """

    def __init__(self):
        """
        Initialize the EnvironmentWindow.
        """
        super().__init__()

        # Set window title
        self.absolute_path = None
        self.title("SetUpSmarters")

        window_width = 1200
        window_height = 1200

        # Get the screen dimensions and calculate center position
        screen_width, screen_height = (
            self.winfo_screenwidth(),
            self.winfo_screenheight(),
        )
        center_x, center_y = (
            screen_width // 2 - window_width // 2,
            screen_height // 2 - window_height // 2,
        )

        # Set the position of the window to the center of the screen
        self.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")

        # Create a frame for parameters entry
        frame = ttk.Frame(self)

        # Define options for field spacing
        options = {"padx": 8, "pady": 8}

        # Add frame label for environment features
        ttk.Label(self, text="Environment features", font=("Arial", 25)).grid(
            row=0, column=0, columnspan=2, **options
        )

        # Define entries for environment parameters
        entries = [
            ("Length (environment): ", tk.StringVar()),
            ("Width (environment): ", tk.StringVar()),
            ("Number of squares (blocked areas): ", tk.IntVar()),
            ("Min width (blocked squares): ", tk.StringVar()),
            ("Max width (blocked squares): ", tk.StringVar()),
            ("Min height (blocked squares): ", tk.StringVar()),
            ("Max height (blocked squares): ", tk.StringVar()),
            ("Number of circles (blocked areas): ", tk.IntVar()),
            ("Min ray (blocked circles): ", tk.StringVar()),
            ("Max ray (blocked circles): ", tk.StringVar()),
            ("Min height (isolated area): ", tk.StringVar()),
            ("Max height (isolated area): ", tk.StringVar()),
            ("Min width (isolated area): ", tk.StringVar()),
            ("Max width (isolated area): ", tk.StringVar()),
            ("Min radius (isolated area): ", tk.StringVar()),
            ("Max radius (isolated area): ", tk.StringVar()),
        ]

        (
            self.length,
            self.width,
            self.blocked_squares,
            self.min_width,
            self.max_width,
            self.min_height,
            self.max_height,
            self.circles,
            self.min_ray,
            self.max_ray,
            self.isolated_min_length,
            self.isolated_max_length,
            self.isolated_min_width,
            self.isolated_max_width,
            self.min_radius,
            self.max_radius,
        ) = [var for _, var in entries]

        # Create and place entry widgets for each parameter
        for i, (label_text, var) in enumerate(entries, start=1):
            ttk.Label(frame, text=label_text).grid(
                row=i, column=0, sticky="W", **options
            )
            entry = ttk.Entry(frame, textvariable=var)
            entry.grid(row=i, column=1, **options)

        # Add isolated area shape option menu
        ttk.Label(frame, text="Shape (isolated area): ").grid(
            row=len(entries) + 1, column=0, sticky="W", **options
        )
        option_list = ["Square", "Circle"]
        shape_var = tk.StringVar()
        shape_var.set(option_list[0])
        option_menu = ttk.OptionMenu(frame, shape_var, *option_list)
        option_menu.config(width=20)
        option_menu.grid(row=len(entries) + 1, column=1, **options)

        # Add button to load extra data
        ttk.Label(frame, text="Load your data: ").grid(
            row=len(entries) + 2, column=0, sticky="W", **options
        )
        button = tk.Button(frame, text="Open", command=self.button_click)
        button.config(width=20)
        button.grid(row=len(entries) + 2, column=1, **options)

        # Add Done and Back buttons
        Button(self, text="Done", command=self.click_next, padding=5).place(
            x=600, y=790
        )
        Button(self, text="Back", command=self.click_back).place(x=10, y=790)

        # Add padding to the frame and display it
        frame.grid(padx=20, pady=20)

        self.entries = dict(entries)
        self.shape = shape_var
        self.button = button

    def button_click(self):
        """
        Open a file dialog to select a JSON file for extra data.

        :param self: The instance of the EnvironmentWindow class.
        """
        self.absolute_path = None
        file_path = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
        if file_path:
            self.absolute_path = os.path.abspath(file_path)
            print("File selected:", self.absolute_path)
            self.button.config(text=os.path.basename(self.absolute_path))

    def click_back(self):
        """
        Handle the click event for the "Back" button.

        :param self: The instance of the EnvironmentWindow class.
        """
        self.destroy()
        ChooseWindow()

    def click_next(self):
        """
        Handle the click event for the "Done" button.
        Save the user input from entries and proceed accordingly.

        :param self: The instance of the EnvironmentWindow class.
        """
        environment = EnvConfig(
            length=float(self.length.get()),
            width=float(self.width.get()),
            num_blocked_squares=self.blocked_squares.get(),
            min_width_square=float(self.min_width.get()),
            max_width_square=float(self.max_width.get()),
            min_height_square=float(self.min_height.get()),
            max_height_square=float(self.max_height.get()),
            num_blocked_circles=self.circles.get(),
            min_ray=float(self.min_ray.get()),
            max_ray=float(self.max_ray.get()),
            isolated_area_min_length=float(self.isolated_min_length.get()),
            isolated_area_max_length=float(self.isolated_max_length.get()),
            min_radius=float(self.min_radius.get()),
            max_radius=float(self.max_radius.get()),
            isolated_area_min_width=float(self.isolated_min_width.get()),
            isolated_area_max_width=float(self.isolated_max_width.get()),
            isolated_area_shape=self.shape.get(),
        )
        python_objects.append(environment)

        produce_json(python_objects)
        # run_second_program("smarters.py")  # todo: include the default plugin name here

        self.destroy()


class SimulatorWindow(Tk):
    """
    Main window for the simulator application.
    """

    def __init__(self):
        """
        Initialize the SimulatorWindow.
        """
        super().__init__()

        # Set window title
        self.title("SetUpSmarters")

        window_width = 500
        window_height = 500

        # Get the screen dimensions and calculate center position
        screen_width, screen_height = (
            self.winfo_screenwidth(),
            self.winfo_screenheight(),
        )
        center_x, center_y = (
            screen_width // 2 - window_width // 2,
            screen_height // 2 - window_height // 2,
        )

        # Set the position of the window to the center of the screen
        self.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")

        # Create a frame for parameters entry
        frame = ttk.Frame(self)
        frame.place(anchor="center")

        # Define options for field spacing
        options = {"padx": 20, "pady": 20}

        # Add frame label for simulator features
        ttk.Label(self, text="Simulator features", font=("Arial", 18)).grid(
            row=1, column=0, columnspan=3, **options
        )

        simulator_entries = []
        entries = [
            ("Dimension of the tassel (m):", tk.DoubleVar, 0.20),
            ("Number of maps:", tk.IntVar, 0),
            ("Repetition times: ", tk.IntVar, 0),
            ("Cutting mins:", tk.IntVar, 0),
        ]

        # Create and place entry widgets for each simulator parameter
        for i, (label_text, var_factory, default_value) in enumerate(entries):
            ttk.Label(frame, text=label_text).grid(
                column=0, row=i + 2, sticky="W", **options
            )
            var = var_factory()
            var.set(default_value)
            entry = ttk.Entry(frame, textvariable=var)
            entry.grid(column=1, row=i + 2, **options)
            entry.focus()
            simulator_entries.append((label_text, var))

        # Add Next and Back buttons
        tk.Button(self, text="Next", command=self.click_next).place(x=350, y=400)
        Button(self, text="Back", command=self.click_back).place(x=50, y=400)

        # Add padding to the frame and display it
        frame.grid(padx=20, pady=20)

        self.simulator_entries = simulator_entries

    def click_back(self):
        """
        Handle the click event for the "Back" button.

        :param self: The instance of the SimulatorWindow class.
        """
        self.destroy()
        RobotWindow()

    def click_next(self):
        """
        Handle the click event for the "Next" button.

        :param self: The instance of the SimulatorWindow class.
        """
        simulator_params = {}
        key_mapping = {
            "Dimension of the tassel (m):".strip(): "dim_tassel",
            "Number of maps:".strip(): "num_maps",
            "Repetition times: ".strip(): "repetitions",
            "Cutting mins:".strip(): "cycle",
        }

        for original_key, var in self.simulator_entries:
            mapped_key = key_mapping[original_key.strip()]
            simulator_params[mapped_key] = var.get()

        simulator = SimulatorConfig(**simulator_params)

        python_objects.append(simulator)

        for widget in self.winfo_children():
            widget.destroy()
        self.destroy()
        ChooseWindow()

