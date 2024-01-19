from pydantic import BaseModel


class Environment(BaseModel):
    name_field: str = 'Null name'
    num_blocked_areas: int = 0
    num_circle_blocked: int = 0
    length_field: float = 0.0
    width_field: float = 0.0
    min_area_blocked: float = 0.0
    max_area_blocked: float = 0.0


class Robot(BaseModel):
    type: str = 'Null type'
    cutting_mode: str = 'Null cutting mode'
    bounce_mode: str = 'Null bounce mode'
    speed: float = 0.0
    cutting_diameter: float = 0.0
    autonomy: int = 0
    environment_name: str = 'Null environment name'
