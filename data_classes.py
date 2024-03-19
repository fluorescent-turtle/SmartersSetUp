from pydantic import BaseModel


class Environment(BaseModel):
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


class Robot(BaseModel):
    type: str
    cutting_mode: str
    speed: float
    cutting_diameter: float
    autonomy: int
    guide_lines: int = 2
    shear_load: int
    algo: str


class Simulator(BaseModel):
    dim_tassel: float
    repetitions: int
    cycle: int
