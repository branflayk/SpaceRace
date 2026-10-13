#!/usr/bin/env python3
# === SPACE RACE
# === Brian Turner 2020-04-14
# === based on https://codeheir.com/2019/02/10/how-to-code-space-race-1973-2/
# === game class based on http://programarcadegames.com/python_examples/show_file.php?file=game_class_example.py

import pygame as pg
import random

BLACK = pg.Color('black') #(0,0,0)
WHITE = pg.Color('white') #(255,255,255)
WIDTH = 400
HEIGHT = 400
FPS = 60

class Ship(pg.sprite.Sprite):
    def __init__(self,x):
        pg.sprite.Sprite.__init__(self)
        self.x = x
        self.score = 0
        self.image = pg.image.load('spaceship2.png').convert_alpha()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.respawn()
        
    def respawn(self):
        self.y = HEIGHT - 20
        self.is_up = False
        self.is_down = False
        self.rect.center = (self.x,self.y)
        
    def move_up(self):
        self.y -= 1
        
    def move_down(self):
        self.y += 1
        
    def update(self):
        if self.is_up and self.y > 0:
            self.move_up()
        elif self.is_down and self.y < HEIGHT - 20:
            self.move_down()
            
        if self.y <= 0:
            self.score += 1
            self.respawn()
        self.rect.center = (self.x,self.y)
            
class Debris(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.r = 5
        self.image = pg.Surface([self.r*2,self.r*2])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
        pg.draw.ellipse(self.image,WHITE,[0,0,self.r*2,self.r*2])
        self.rect = self.image.get_rect()
        self.reset()
        
    def reset(self):
        self.y = random.randint(0,HEIGHT-70)
        self.spawn_left = random.random() < 0.5
        if self.spawn_left:
            self.x = random.randint(-WIDTH,0)
            self.moving_left = False
        else:
            self.x = random.randint(WIDTH,WIDTH*2)
            self.moving_left = True
            
    def update(self):
        if self.moving_left:
            self.x -= 1
        else:
            self.x += 1
        if self.off_screen():
            self.reset()
        self.rect.center = (self.x,self.y)
        
    def off_screen(self):
        if self.moving_left and self.x < -5:
            return True
        elif not self.moving_left and self.x > WIDTH+5:
            return True
        return False

class Timer:
    def __init__(self,size):
        self.x = WIDTH/2
        self.y = size #HEIGHT/2
        
    def update(self):
        self.y += 0.1

class Game:
    def __init__(self):
        self.title_screen = pg.image.load('race_title.png').convert()
        self.score_font = pg.font.Font(None,50)
        self.all_sprites = pg.sprite.Group()
        self.rock_sprites = pg.sprite.Group()
        self.left_ship = Ship(int(WIDTH * 0.33))
        self.right_ship = Ship(int(WIDTH * 0.66))
        self.all_sprites.add(self.left_ship)
        self.all_sprites.add(self.right_ship)
        self.done = False
        self.num_debris = 30
        self.timer = Timer(HEIGHT*0.5)
        for i in range(self.num_debris):
            d = Debris()
            self.all_sprites.add(d)
            self.rock_sprites.add(d)
        self.mode = 'title'
        
    def process_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return True
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    return True
                if self.mode == 'title':
                    self.mode = 'play'
                elif self.mode == 'play':
                    if event.key == pg.K_q:
                        self.left_ship.is_up = True
                        self.left_ship.is_down = False
                    if event.key == pg.K_a:
                        self.left_ship.is_up = False
                        self.left_ship.is_down = True
                        self.left_ship.move_down()
                    if event.key == pg.K_UP:
                        self.right_ship.is_up = True
                        self.right_ship.is_down = False
                    if event.key == pg.K_DOWN:
                        self.right_ship.is_up = False
                        self.right_ship.is_down = True
                elif self.mode == 'over':
                    self.__init__()
        return False
            
    def run_logic(self):
        if self.mode == 'play':
            self.all_sprites.update()
            self.timer.update()
            if pg.sprite.spritecollide(self.left_ship,self.rock_sprites,False):
                self.left_ship.respawn()
            if pg.sprite.spritecollide(self.right_ship,self.rock_sprites,False):
                self.right_ship.respawn()
            if self.timer.y > HEIGHT:
                self.mode = 'over'
    
    def draw_screen(self,screen):
        if self.mode == 'title':
            screen.blit(self.title_screen,(0,0))
        elif self.mode == 'play':
            screen.fill(BLACK)
            self.all_sprites.draw(screen)
            left_txt = self.score_font.render(str(self.left_ship.score),True,WHITE)
            right_txt = self.score_font.render(str(self.right_ship.score),True,WHITE)
            screen.blit(left_txt,[50,HEIGHT-40])
            screen.blit(right_txt,[350,HEIGHT-40])
            pg.draw.rect(screen,WHITE,(self.timer.x,self.timer.y,5,HEIGHT),0)
        elif self.mode == 'over':
            screen.fill(BLACK)
            txt1 = self.score_font.render('GAME',True,WHITE)
            txt2 = self.score_font.render('OVER',True,WHITE)
            txt1_rect = txt1.get_rect(center=(WIDTH/2, 100))
            txt2_rect = txt2.get_rect(center=(WIDTH/2, 200))
            screen.blit(txt1,txt1_rect)
            screen.blit(txt2,txt2_rect)
        pg.display.flip()
    
def main():
    pg.init()
    screen = pg.display.set_mode([WIDTH,HEIGHT])
    pg.display.set_caption('Space Race')
    clock = pg.time.Clock()
    pg.mouse.set_visible(False)
    game = Game()
    done = False
    while not done:
        done = game.process_events()
        game.run_logic()
        game.draw_screen(screen)
        clock.tick(FPS)
        #game_over = game.done
    pg.quit()
    
if __name__ == '__main__':
    main()