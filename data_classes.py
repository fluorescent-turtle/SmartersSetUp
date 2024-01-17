import json
from dataclasses import dataclass


@dataclass
class Environment:
    name_field: str
    length_field: int
    width_field: int
    num_blocked_areas: int
    min_area_blocked: int
    max_area_blocked: int
    num_circle_blocked: int


@dataclass
class Robot:
    type: str
    speed: int
    cutting_diameter: int
    autonomy: int
    cutting_mode: str
    bounce_mode: str

