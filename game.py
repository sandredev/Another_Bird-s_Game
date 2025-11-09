import pygame as pg
import bird 
import towers
import game_parameters as gp

def start():
    pg.init()

    # Objects and window setup
    width = gp.WIDTH_SCREEN
    height = gp.HEIGHT_SCREEN
    bird_object = bird.Bird((width/2, 0), 70, 50)
    window = pg.display.set_mode((width, height))
    pg.display.set_caption("Another Bird's Game")
    clock = pg.time.Clock()
    run = True
    dt = 0
    is_jumping = False

    # Cooldowns setup
    jump_cooldown_clock = pg.time.Clock()
    jump_cooldown_time = 0
    JUMP_COOLDOWN_LIMIT = gp.JUMP_COOLDOWN_LIMIT

    # Towers generator setup
    towers_generator_cooldown_clock = pg.time.Clock()
    towers_generator_cooldown_time = 0
    TOWERS_GENERATOR_COOLDOWN_LIMIT = gp.TOWERS_GENERATOR_COOLDOWN_LIMIT
    towers_generator = []

    # Background setup
    background_img = pg.image.load("img/background.gif")
    background_img = pg.transform.scale(background_img, (width, height))

    life_count = gp.LIFE_COUNT
    score = 0

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
    
        # Towers drawing, movement and collision detection
        for towers_object in towers_generator:
            towers_object.draw_as_sprite(window)
            towers_object.move()
            if towers_object.collides_with_bird(bird_object):
                life_count -= 1
                print(f"Lives left: {life_count}")
                towers_generator.remove(towers_object)
                if life_count <= 0:
                    print("Game Over!")
                    run = False
            if towers_object.x_position + towers_object.width_towers/2 < bird_object.x_position and not hasattr(towers_object, 'scored'):
                score += 1
                print(f"Score: {score}")
                towers_object.scored = True
    

        # Cleanup off-screen towers
        towers_generator = [t for t in towers_generator if t.x_position + t.width_towers/2 >= 0]
        
        pg.display.flip()

        # Timing
        dt = clock.tick(gp.FPS) / 1000 
        jump_cooldown_time += jump_cooldown_clock.tick() / 1000
        towers_generator_cooldown_time += towers_generator_cooldown_clock.tick() / 1000

    pg.quit()