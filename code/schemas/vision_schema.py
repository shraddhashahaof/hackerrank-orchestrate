from pydantic import BaseModel


class VisionInspection(BaseModel):

    object: str

    visible_damage: str

    affected_part: str

    image_quality: str

    damage_visible: bool