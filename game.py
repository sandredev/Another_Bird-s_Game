import pygame as pg
import bird 
import towers

def start():
    pg.init()

    # Objects and window setup
    width = 800
    height = 600
    bird_object = bird.Bird((width/2, 0), 70, 50)
    window = pg.display.set_mode((width, height))
    pg.display.set_caption("Another Bird's Game")
    clock = pg.time.Clock()
    run = True
    dt = 0
    is_jumping = False

    jump_cooldown_clock = pg.time.Clock()
    jump_cooldown_time = 0
    JUMP_COOLDOWN_LIMIT = 0.1

    towers_generator_cooldown_clock = pg.time.Clock()
    towers_generator_cooldown_time = 0
    TOWERS_GENERATOR_COOLDOWN_LIMIT = 1.6
    towers_generator = []

    background_img = pg.image.load("img/background.gif")
    background_img = pg.transform.scale(background_img, (width, height))

    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE or event.key == pg.K_UP:
                    is_jumping = True
            if event.type == pg.KEYUP:
                if event.key == pg.K_SPACE or event.key == pg.K_UP:
                    is_jumping = False
       
        # Game mechanics
        if is_jumping and jump_cooldown_time >= JUMP_COOLDOWN_LIMIT:
            bird_object.jump()
            jump_cooldown_time = 0
        bird_object.fall(dt)

        # Boundary conditions
        if bird_object.y_position - bird_object.height/2 < 0:
            bird_object.y_position = bird_object.height/2
            bird_object.update_position()
            bird_object.reset_init_y_speed()
        elif bird_object.y_position + bird_object.height/2 >= window.get_height():
            bird_object.y_position = window.get_height() - bird_object.height/2
            bird_object.update_position()
            bird_object.reset_init_y_speed()

        # Towers generation
        if towers_generator_cooldown_time >= TOWERS_GENERATOR_COOLDOWN_LIMIT:
            towers_generator.append(towers.Towers(window.get_width()))
            towers_generator_cooldown_time = 0
        
        # Drawing
        window.blit(background_img, (0,0))
        bird_object.draw_as_sprite(window)
        
        # Draw and move towers
        for towers_object in towers_generator:
            towers_object.draw_as_sprite(window)
            towers_object.move()
        # Cleanup off-screen towers
        towers_generator = [t for t in towers_generator if t.x_position + t.width_towers/2 >= 0]
        
        pg.display.flip()

        # Timing
        dt = clock.tick(60) / 1000 
        jump_cooldown_time += jump_cooldown_clock.tick() / 1000
        towers_generator_cooldown_time += towers_generator_cooldown_clock.tick() / 1000

    pg.quit()