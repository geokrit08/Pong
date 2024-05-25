import pygame
from pygame import *

# Constants
WIN_WIDTH = 700
WIN_HEIGHT = 500
FPS = 165

# GameSprite class
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, width, height):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (width, height))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

# Player class
class Player(GameSprite):
    def update_r(self):
        keys = key.get_pressed()
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < WIN_HEIGHT - 80:
            self.rect.y += self.speed
    
    def update_l(self):
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < WIN_HEIGHT - 80:
            self.rect.y += self.speed

# Initialize game
pygame.init()
window = display.set_mode((WIN_WIDTH, WIN_HEIGHT))

# Load background image
background = transform.scale(image.load('pong_background.png'), (WIN_WIDTH, WIN_HEIGHT))
mixer.init()
collision_sound = mixer.Sound('collision.mp3')
countdown_sound = mixer.Sound('countdown.mp3')

# Flags and clock
game = True
finish = False
clock = time.Clock()

# Create ball and paddles
racket1 = Player('racket.png', 30, 200, 4, 25, 75)
racket2 = Player('racket.png', 620, 200, 4, 25, 75)
ball = GameSprite('tenis_ball.png', 325, 200, 4, 25, 25)

# Font setup
font.init()
score_font = font.Font(None, 100)  # Increased font size for scores
win_font = font.Font(None, 35)
win1_text = win_font.render('PLAYER 1 WINS THIS ROUND!', True, (50, 205, 50))
win2_text = win_font.render('PLAYER 2 WINS THIS ROUND!', True, (50, 205, 50))

# Score counters
score1 = 0
score2 = 0

# Ball speed
speed_x = 3
speed_y = 3

def display_scores():
    score_display = score_font.render(f'{score1}  {score2}', True, (255, 255, 255))
    window.blit(score_display, (WIN_WIDTH // 2 - score_display.get_width() // 2, 20))  # Center the score display horizontally

# Main game loop
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
    
    if not finish:
        # Draw the background image
        window.blit(background, (0, 0))

        racket1.update_l()
        racket2.update_r()
        ball.rect.x += speed_x
        ball.rect.y += speed_y

        if sprite.collide_rect(racket1, ball) or sprite.collide_rect(racket2, ball):
            speed_x *= -1
            collision_sound.play()
        
        if ball.rect.y > WIN_HEIGHT - ball.rect.height or ball.rect.y < 0:
            speed_y *= -1

        if ball.rect.x < 0:
            score2 += 1
            finish = True
            window.blit(win2_text, (200, 200))

        if ball.rect.x > WIN_WIDTH:
            score1 += 1
            finish = True
            window.blit(win1_text, (200, 200))

        racket1.reset()
        racket2.reset()
        ball.reset()
        display_scores()

        # Check for best of three
        if score1 == 3:
            window.blit(win_font.render('PLAYER 1 WINS THE MATCH!', True, (50, 205, 50)), (200, 250))
            display.update()
            time.delay(3000)
            game = False
        elif score2 == 3:
            window.blit(win_font.render('PLAYER 2 WINS THE MATCH!', True, (50, 205, 50)), (200, 250))
            display.update()
            time.delay(3000)
            game = False
    
    else:
        time.delay(1500)
        countdown_sound.play()
        time.delay(3000)
        finish = False
        ball.rect.x, ball.rect.y = 325, 200
        racket1.rect.x, racket1.rect.y = 30, 200
        racket2.rect.x, racket2.rect.y = 620, 200
        speed_x, speed_y = 3, 3

    display.update()
    clock.tick(FPS)
