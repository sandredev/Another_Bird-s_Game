import pygame as pg
import towers
import game_parameters as gp
import math as ma
import time 
from PIL import Image
from debug import Debug
from resources import Resources
from bird import Bird
from main_title import Main_title
from sounds_loader import Sounds_loader

class Game:
    def __init__(self):
        pg.init()
        # Objects and window setup
        self.width = gp.WIDTH_SCREEN
        self.height = gp.HEIGHT_SCREEN
        self.bird_object = Bird((self.width/2, 0), 70, 50)
        self.window = pg.display.set_mode((self.width, self.height))
        pg.display.set_caption("Another Bird's Game")
        self.font = pg.font.SysFont('Comic Sans', 20)
        self.clock = pg.time.Clock()
        self.debugger = Debug()
        self.run = True
        self.dt = 0
        self.is_jumping = False
        self.already_jumped = False
        self.time_started = time.time() 
        self.resources = Resources()
         # Cooldowns setup
        self.jump_cooldown_clock = pg.time.Clock()
        self.jump_cooldown_time = 0
        self.JUMP_COOLDOWN_LIMIT = gp.JUMP_COOLDOWN_LIMIT

        # Towers generator setup
        self.towers_generator_cooldown_clock = pg.time.Clock()
        self.towers_generator_cooldown_time = 0
        self.TOWERS_GENERATOR_COOLDOWN_LIMIT = gp.TOWERS_GENERATOR_COOLDOWN_LIMIT
        self.towers_generator = []

        #main title setup 
        self.mTitle = Main_title()
        self.resources.frame_speed = 0.3
        self.sl = Sounds_loader().sounds
        # Background setup
        self.frames_background = []
        self.gif_background = Image.open("img/background.gif")
        self.resources.convertToGif(self.gif_background, self.frames_background, gp.WIDTH_SCREEN, gp.HEIGHT_SCREEN)
        self.life_count = gp.LIFE_COUNT
        self.score = 0
        self.menu = True 
        self.counter = 0


    def start(self):
        self.sl.play_music('main_menu')

        while self.run:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.run = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE or event.key == pg.K_UP:
                        self.is_jumping = True
                        if self.menu:
                            self.sl.stop_music('main_menu')
                        else:
                            self.sl.play_sfx('jump')
                    if event.key == pg.K_d and self.menu == False:
                        self.debugger.toggle()
                    if event.key == pg.K_x:
                        self.life_count += 1
                if event.type == pg.KEYUP:
                    if event.key == pg.K_SPACE or event.key == pg.K_UP:
                        self.is_jumping = False
                        self.already_jumped = False
            
            self.dt = self.clock.tick(gp.FPS) / 1000 
            self.jump_cooldown_time += self.jump_cooldown_clock.tick() / 1000
            self.towers_generator_cooldown_time += self.towers_generator_cooldown_clock.tick() / 1000


            #Info from debug mode
            self.debugger.add(f"x: {round(self.bird_object.x_position)}", 10, 150)    
            self.debugger.add(f"y: {round(self.bird_object.y_position)}", 10, 185)    
            self.debugger.add(f"tiempo desde el ultimo salto: {round(self.bird_object.t,1)} seg", 10, 220)     
            self.debugger.add(f"velocidad: {round(self.bird_object.y_speed)}", 10, 255)      
            self.debugger.add(f"gravedad: {gp.GRAVITY}", 10, 290)      
            self.debugger.add(f"ángulo: {round(self.bird_object.angle)}", 10, 330)    
            self.debugger.add(f"tiempo transcurrido: {round(time.time() - self.time_started)} seg", 10, 365)    
            self.debugger.add(f"{gp.FPS} FPS", 720, 15)

            if self.menu:
                self.window.blit(self.frames_background[self.resources.calculateCurrentFrame(self.frames_background,self.dt)], (0,0))
                self.mTitle.draw(self.window,self.dt)
                self.bird_object.draw_as_sprite(self.window)
                pg.display.flip()
                self.counter += self.dt*3
                self.bird_object.set_coordinates((self.width/2, self.height/2 + 100 * ma.sin(self.counter)),  -ma.cos(self.counter)*50, self.dt)
                if self.is_jumping:
                    self.menu = False  
            else:
                if self.is_jumping and self.jump_cooldown_time >= gp.JUMP_COOLDOWN_LIMIT and not self.already_jumped:
                    self.bird_object.jump()
                    self.jump_cooldown_time = 0
                    self.already_jumped = True
                self.bird_object.fall(self.dt)

                # Boundary conditions
                if self.bird_object.y_position - self.bird_object.height/2 < 0:
                    self.bird_object.y_position = self.bird_object.height/2
                    self.bird_object.update_position()
                    self.bird_object.reset_init_y_speed()
                elif self.bird_object.y_position + self.bird_object.height/2 >= self.window.get_height():
                    self.bird_object.y_position = self.window.get_height() - self.bird_object.height/2
                    self.bird_object.update_position()
                    self.bird_object.reset_init_y_speed()

                # Towers generation
                if self.towers_generator_cooldown_time >= gp.TOWERS_GENERATOR_COOLDOWN_LIMIT:
                    self.towers_generator.append(towers.Towers(self.window.get_width()))
                    self.towers_generator_cooldown_time = 0


                # Drawing
                self.window.blit(self.frames_background[self.resources.calculateCurrentFrame(self.frames_background,self.dt)], (0,0))
                self.bird_object.draw_as_sprite(self.window)

                self.resources.boostSpeed(-0.00007) # Boost the speed of the background gif
                # Towers drawing, movement and collision detection
                for self.towers_object in self.towers_generator:
                    self.towers_object.draw_as_sprite(self.window)
                    self.towers_object.move()
                    if self.towers_object.collides_with_bird(self.bird_object):
                        self.life_count -= 1
                        self.sl.play_sfx('hit')
                        self.towers_generator.remove(self.towers_object)
                        if self.life_count <= 0:
                            self.sl.play_sfx('game_over')
                            print("Game Over!")
                            self.menu = True
                            self.sl.play_music('main_menu')
                            self.restart()
                    # Scored
                    if self.towers_object.x_position + self.towers_object.width_towers/2 < self.bird_object.x_position and not hasattr(self.towers_object, 'scored'):
                        self.score += 1
                        self.sl.play_sfx('tube')
                        self.towers_object.scored = True
                        if gp.DISTANCE_BETWEEN_TOWERS > 120:
                            gp.DISTANCE_BETWEEN_TOWERS -= 1 # Increase difficulty over time
                        if gp.TOWERS_GENERATOR_COOLDOWN_LIMIT > 1.05 :
                            gp.TOWERS_GENERATOR_COOLDOWN_LIMIT -= self.score // 10 * 0.001  # Increase difficulty over time
                
            
                # Cleanup off-screen towers
                self.towers_generator = [t for t in self.towers_generator if t.x_position + t.width_towers/2 >= 0]
                
                # Debugger drawing
                self.debugger.draw(self.window, self.font,self.dt)
                # Lifes and score drawing
                self.lifes_view = self.font.render(f'{self.life_count} lives', True, (255, 255, 255))
                self.score_view = self.font.render(f'Score: {self.score}', True, (255, 255, 255))
                self.window.blit(self.lifes_view, (gp.WIDTH_SCREEN - 90, gp.HEIGHT_SCREEN - 50))
                self.window.blit(self.score_view, (10,0))
                pg.display.flip()
        pg.quit()

    def restart(self):
        self.towers_generator = []   
        self.life_count = gp.LIFE_COUNT
        self.score = 0
        self.bird_object.set_coordinates((self.width/2, self.height/2), 0, 0)
        self.bird_object.reset_init_y_speed()
        self.resources.frame_speed = 0.3
        gp.DISTANCE_BETWEEN_TOWERS = 200
        gp.TOWERS_GENERATOR_COOLDOWN_LIMIT = 2.0