from resources import Resources
from PIL import Image

class Debug:
    def __init__(self):
        self.active = False
        self.lines = []
        self.frames = []   
        gif = Image.open("img/debugTitle.gif") #Debug Mode title
        self.res = Resources()
        self.res.convertToGif(gif,self.frames, 250,110)
        
    def toggle(self):
        self.active = not self.active

    def add(self, text, x, y):
        self.lines.append((text, x, y))

    def draw(self, surface, font, dt):
        if not self.active: #Validate drawing when debug mode is off
            return
        
        # Drawing the debug's title gif
        index = self.res.calculateCurrentFrame(self.frames, dt)
        frame = self.frames[index]
        surface.blit(frame, (0, 10))

        # Drawing lines
        for text, x, y in self.lines:
            render = font.render(text, True, (255, 255, 255))
            surface.blit(render, (x, y))
        self.lines.clear()
