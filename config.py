class Config:
    def __init__(self, cfg):
        self.width = cfg["width"]
        self.height = cfg["height"]
        self.fps = cfg["target_fps"]
        self.cell_size = cfg["cell_size"]

