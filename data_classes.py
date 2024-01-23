from pydantic import BaseModel


class Environment(BaseModel):
    num_blocked_areas: int
    num_blocked_circles: int
    num_blocked_squares: int
    length_field: float
    width_field: float
    min_area_blocked: float
    max_area_blocked: float
    isolated_area_length: float
    isolated_area_width: float
    isolated_area_shape: str


class Robot(BaseModel):
    type: str
    cutting_mode: str
    bounce_mode: str
    speed: float
    cutting_diameter: float
    autonomy: int
    guide_lines: int = 2
    shear_load: int
