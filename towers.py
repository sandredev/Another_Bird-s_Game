import pygame as pg
import random
import game_parameters as gp

class Towers:
    def __init__(self, x_init_position):
        self.x_position = x_init_position
        self.speed_movement = -5
        self.width_towers = gp.WIDTH_TOWER
        self.distance_between_towers = gp.DISTANCE_BETWEEN_TOWERS
        self.height_lower_tower = self.height_upper_tower = 500
        self.y_position_lower_tower = random.randint(450,750)
        self.y_position_upper_tower = self.y_position_lower_tower - self.distance_between_towers - self.height_upper_tower
        self.lower_tower = pg.Rect(self.x_position, self.y_position_lower_tower, self.width_towers, self.height_lower_tower)
        self.upper_tower = pg.Rect(self.x_position, self.y_position_upper_tower, self.width_towers, self.height_upper_tower)
        self.tower_sprite = pg.image.load("img/tower.png")
        self.lower_tower_sprite = pg.transform.scale(self.tower_sprite, (self.width_towers, self.height_lower_tower))
        self.upper_tower_sprite = pg.transform.scale(self.tower_sprite, (self.width_towers, self.height_upper_tower))
        self.upper_tower_sprite = pg.transform.flip(self.upper_tower_sprite, False, True)

    def move(self):
        self.x_position += self.speed_movement
        self.upper_tower.center = (self.x_position, self.y_position_upper_tower)
        self.lower_tower.center = (self.x_position, self.y_position_lower_tower)

    def draw_as_rectangle(self, window):
        pg.draw.rect(window, (255, 255, 255), self.lower_tower)
        pg.draw.rect(window, (255, 255, 255), self.upper_tower)
        
    def draw_as_sprite(self, window):
        window.blit(self.lower_tower_sprite, self.lower_tower)
        window.blit(self.upper_tower_sprite, self.upper_tower)

    def collides_with_bird(self, bird_object):
        return self.lower_tower.colliderect(bird_object.rectangle) or self.upper_tower.colliderect(bird_object.rectangle)