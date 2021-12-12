class MapElement:
    def __init__(self,geometry):
        self.geometry = geometry
        self.layer = None

        self.line_color = '#696969'
        self.line_style = None
        self.line_width = 0.5

        self.face_color = '#FFFFFF'

        self.opacity = 1
        self.zorder = 1
