import pygame as pg
import game_parameters as gp
from PIL import Image


class Resources:
    def __init__(self):
        self.current_frame = 0
        self.frame_time = 0
        self.frame_speed = 0.03  

    def convertToGif(self, gif, frames, width, height):
        for frame in range(gif.n_frames):
            gif.seek(frame)
            frame_image = gif.copy().convert("RGBA")
            mode = gif.mode
            size = gif.size
            data = frame_image.tobytes()

            pygame_image = pg.image.fromstring(data, size, "RGBA")
            pygame_image = pg.transform.scale(pygame_image, (width, height))

            frames.append(pygame_image)

    def boostSpeed(self, boost):
        self.frame_speed = max(0.02, self.frame_speed + boost)

        
    def calculateCurrentFrame(self, frames, dt):
        self.frame_time += dt
        if self.frame_time >= self.frame_speed:
            self.frame_time = 0
            self.current_frame = (self.current_frame + 1) % len(frames)
        return self.current_frame  

    def centerX(self, n):
        #n is the amout of pixels of the object  
        return (gp.WIDTH_SCREEN - n)/2 #return the x center as 2x + n = total amout of pixels (window)
