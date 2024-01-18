from dataclasses import dataclass


@dataclass
class Environment:
    name_field: str
    length_field: float
    width_field: float
    num_blocked_areas: int
    min_area_blocked: float
    max_area_blocked: float
    num_circle_blocked: int


@dataclass
class Robot:
    name_env: str
    type: str
    speed: float
    cutting_diameter: float
    autonomy: int
    cutting_mode: str
    bounce_mode: str

