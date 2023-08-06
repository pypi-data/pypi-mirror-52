from marshmallow_dataclass import dataclass, class_schema


@dataclass
class ExportAvatarParams:
    def __init__(self, body_sizes: dict, work_path: str):
        self.body_sizes = body_sizes
        self.work_path = work_path

    body_sizes: dict
    work_path: str
