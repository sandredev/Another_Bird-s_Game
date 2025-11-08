import pygame as pg
import physics_values as physics

class Bird:
    def __init__(self, init_position = (300, 0), width = 50, height = 50):
        self.current_position = init_position
        self.x_position, self.y_position = self.current_position
        self.init_y_position = self.y_position
        self.width = width
        self.height = height
        self.rectangle = pg.Rect(0, 0, width, height) # rectangle of the bird in the frame
        self.rectangle.center = self.current_position

        # Motion values
        self.init_y_speed = 0
        self.y_speed = self.init_y_speed
        self.t = 0 

        # Bird sprite
        self.sprite = pg.image.load("img/bird.png")
        self.sprite = pg.transform.scale(self.sprite, (width, height))

    def fall(self, dt):
        self.t += dt
        # formula: dy/dt = -t*g + v_0 but -t*g switched to t*g instead to
        # properly show the behavior in the screen
        self.y_speed = self.t*physics.GRAVITY + self.init_y_speed
        self.y_position += self.y_speed*dt # dy = f'(x)dx
        self.update_position()
    
    def jump(self):
        self.init_y_speed = -500 # jump speed
        self.t = 0        

    def update_position(self):
        self.current_position = (self.current_position[0], self.y_position)
        self.rectangle.center = (self.current_position[0], self.y_position)

    def reset_init_y_speed(self):
        self.init_y_speed = 0

    def draw_as_rectangle(self, window):
        pg.draw.rect(window, (0, 0, 255), self.rectangle)
    
    def draw_as_sprite(self, window):
        window.blit(self.sprite, self.rectangle)