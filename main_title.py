from resources import Resources
from PIL import Image

class Main_title:
    def __init__(self):
        self.frames = []
        self.framesEnter = []

        gif = Image.open("img/main_title.gif")
        gif2 = Image.open("img/enter_line.gif")

        self.res_title = Resources()
        self.res_enter = Resources()
        self.res_title.frame_speed = 0.041
        self.res_enter.frame_speed = 0.07

        self.res_title.convertToGif(gif, self.frames, 400, 220)
        self.res_enter.convertToGif(gif2, self.framesEnter, 500, 160)

    def draw(self, surface, dt):
        # Title
        idx_title = self.res_title.calculateCurrentFrame(self.frames, dt)
        surface.blit(self.frames[idx_title], (self.res_title.centerX(400), 10))

        # Press ENTER text
        idx_enter = self.res_enter.calculateCurrentFrame(self.framesEnter, dt)
        surface.blit(self.framesEnter[idx_enter], (self.res_enter.centerX(500), 400))

