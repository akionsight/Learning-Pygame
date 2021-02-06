import pygame
import os
pygame.font.init()
pygame.mixer.init()

WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
HEALTH_FONT = pygame.font.SysFont("comicsans", 40)
WINNER_FONT =  pygame.font.SysFont("comicsans", 100)
WIDTH = 900
HEIGHT = 500
FPS = 60
VEL = 5
BULLET_VEL = 7
BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Grenade+1.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Gun+Silencer.mp3'))
SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', "space.png")),(WIDTH, HEIGHT) )
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

MAX_BULLETS = 3 
BLACK = (0, 0, 0)
BORDER = pygame.Rect(WIDTH//2-5 , 0, 10, HEIGHT)
SPACESHIP_WIDTH = 55
SPACESHIP_HEIGHT = 40
YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join("Assets", "spaceship_yellow.png"))
RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join("Assets", "spaceship_red.png"))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)


WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("First game")

def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL

        if red.colliderect(bullet):
            yellow_bullets.remove(bullet)
            print("red is hit")
            BULLET_HIT_SOUND.play()
            pygame.event.post(pygame.event.Event(RED_HIT))
        
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)
            # BULLET_HIT_SOUND.play()


    for bullet in red_bullets:
        bullet.x -= BULLET_VEL

        if yellow.colliderect(bullet):
            red_bullets.remove(bullet)
            print('Yellow is Hit')
            BULLET_HIT_SOUND.play()
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
        elif bullet.x < 0:
            red_bullets.remove(bullet)
            


    pass


def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):

        # WIN.fill(WHITE)
        WIN.blit(SPACE, (0, 0))
        pygame.draw.rect(WIN, BLACK, BORDER)
        red_health_text = HEALTH_FONT.render(f"HEALTH: {str(red_health)}", 1, WHITE)
        yellow_health_text = HEALTH_FONT.render(f"HEALTH: {str(yellow_health)}", 1, WHITE)
        WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
        WIN.blit(yellow_health_text, (10, 10))
        WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
        WIN.blit(RED_SPACESHIP, (red.x, red.y))
        for bullets in red_bullets:
            pygame.draw.rect(WIN, RED, bullets)
        
        for bullets in yellow_bullets:
            pygame.draw.rect(WIN, YELLOW, bullets)



        pygame.display.update()

def key_handler_yellow(keys_pressed,yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0:  # LEFT
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x:  # RIGHT
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0:  # UP
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT - 15:  # DOWN
        yellow.y += VEL

def key_handler_red(keys_pressed,red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width:  # LEFT
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH:  # RIGHT
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0:  # UP
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT - 15:  # DOWN
        red.y += VEL

def draw_winner(text):
    print('draw winner triggerd')
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH/ 2 - draw_text.get_width()/ 2, HEIGHT/2 - draw_text.get_height()))
    pygame.display.update()
    pygame.time.delay(5000)

def main():
    clock = pygame.time.Clock()
    yellow_bullets = []
    red_bullets = []
    run = True
    RED_HEALTH = 10
    YELLOW_HEALTH = 10
    red = pygame.Rect(700,300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
                    pass

                elif event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.height//2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
                    pass
            
            if event.type == RED_HIT:
                RED_HEALTH -= 1
            if event.type == YELLOW_HIT:
                YELLOW_HEALTH -= 1
        Winner_Text = ''
        if RED_HEALTH <= 0:
            Winner_Text = "YELLOW WINS"
        if YELLOW_HEALTH <= 0:
            Winner_Text = "RED WINS"
        
        if Winner_Text != "":
            draw_winner(Winner_Text)
            break
            pass # someone won
            # elif pygame.event.post()
        
        handle_bullets(yellow_bullets, red_bullets, yellow, red)
        keys_pressed = pygame.key.get_pressed()
        key_handler_yellow(keys_pressed, yellow)
        key_handler_red(keys_pressed, red)



        draw_window(red, yellow, red_bullets, yellow_bullets, RED_HEALTH, YELLOW_HEALTH)
    main()

if __name__ == "__main__":
    main()
