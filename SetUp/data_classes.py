import json
from dataclasses import dataclass


# Define data classes for Robot, Env, and Simulator configurations
@dataclass
class RobotConfig:
    type: str
    cutting_mode: str
    speed: float
    cutting_diameter: float
    autonomy: int
    guide_lines: int
    algo: str


@dataclass
class EnvConfig:
    length: float
    width: float
    num_blocked_squares: int
    min_width_square: float
    max_width_square: float
    min_height_square: float
    max_height_square: float
    num_blocked_circles: int
    ray: float
    isolated_area_length: float
    radius: float
    isolated_area_width: float
    isolated_area_shape: str


@dataclass
class SimulatorConfig:
    dim_tassel: float
    repetitions: int
    cycle: int


class ConfigEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, '__dict__'):
            return obj.__dict__
        elif hasattr(obj, '_asdict'):
            return obj._asdict()
        return json.JSONEncoder.default(self, obj)
