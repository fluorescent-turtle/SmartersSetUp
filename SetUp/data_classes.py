""" Copyright 2024 Sara Grecu

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
from dataclasses import dataclass

@dataclass
class RobotConfig:
    """
    Configuration for the lawnmower robot.
    """
    type: str
    cutting_mode: str
    speed: float
    cutting_diameter: float
    autonomy: int
    guide_lines: int
    algo: str


@dataclass
class EnvConfig:
    """
    Configuration for the environment.
    """
    length: float
    width: float
    num_blocked_squares: int
    min_width_square: float
    max_width_square: float
    min_height_square: float
    max_height_square: float
    num_blocked_circles: int
    min_ray: float
    max_ray: float
    isolated_area_min_length: float
    isolated_area_max_length: float
    min_radius: float
    max_radius: float
    isolated_area_min_width: float
    isolated_area_max_width: float
    isolated_area_shape: str


@dataclass
class SimulatorConfig:
    """
    Configuration for the simulator.
    """
    dim_tassel: float
    num_maps: int
    repetitions: int
    cycle: int


class ConfigEncoder(json.JSONEncoder):
    """
    Custom JSON encoder for config objects.
    """
    def default(self, obj):
        if hasattr(obj, "__dict__"):
            return obj.__dict__
        elif hasattr(obj, "_asdict"):
            return obj._asdict()
        return json.JSONEncoder.default(self, obj)
