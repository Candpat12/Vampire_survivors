import pygame
from os import path

pygame.init()
length = 1024
FPS = 60

screen = pygame.display.set_mode((length,length))
pygame.display.set_caption("Mon jeu")

game_folder = path.dirname(__file__)
sprite_folder = path.join(game_folder,'sprites')
hero_folder = path.join(sprite_folder,'hero')
enemy_folder = path.join(sprite_folder,'enemy')

bg = pygame.image.load(path.join(sprite_folder, "bg.png")).convert()
bgs_coords = [[-length,-length],[-length,0],[-length,length],[0,-length],[0,0],[0,length],[length,-length],[length,0],[length,length]]
heros = []
for file in [path.join(hero_folder,'right'),path.join(hero_folder,'left')] :
    l = []
    for i in range(1,5) :
        a = pygame.image.load(path.join(file,"hero_"+str(i)+'.png'))
        a = pygame.transform.scale2x(a)
        l.append(a)
    heros.append(l)
    
enemies = []
for file in [path.join(enemy_folder,'right'),path.join(enemy_folder,'left')] :
    l = []
    for i in range(1,4) :
        a = pygame.image.load(path.join(file,"enemy_"+str(i)+'.png'))
        a = pygame.transform.scale2x(a)
        l.append(a)
    enemies.append(l)

clock = pygame.time.Clock()

class Hero(pygame.sprite.Sprite) :
    
    def __init__(self) :
        pygame.sprite.Sprite.__init__(self)
        self.cote = 0
        self.step = 0
        self.image = heros[self.cote][self.step]
        self.rect = self.image.get_rect()
        self.rect.center = (length// 2,length//2)
    
    def draw(self) :
        screen.blit(self.image,self.rect)
    
    def marcher(self) :
        self.step = (self.step + 1) % 4
        self.image = heros[self.cote][self.step]
        
class Enemy(pygame.sprite.Sprite) :
    
    def __init__(self) :
        pygame.sprite.Sprite.__init__(self)
        self.cote = 0
        self.step = 0
        self.image = enemies[self.cote][self.step]
        self.rect = self.image.get_rect()
        self.rect.center = (length-20,length//2)

hero = Hero()
enemy = Enemy()
game_on = True
cpt_mouv = 0

while game_on :
    
    cpt_mouv += 1
    
    clock.tick(FPS)
    bg_change_x = 0
    bg_change_y = 0

    for event in pygame.event.get() :
        if event.type == pygame.QUIT :
            game_on = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_z] :
        bg_change_y += 5
    if keys[pygame.K_q] :
        bg_change_x += 5
        if hero.cote == 0 :
            hero.cote = 1
    if keys[pygame.K_s] :
        bg_change_y -= 5
    if keys[pygame.K_d] :
        bg_change_x -= 5
        if hero.cote == 1 :
            hero.cote = 0

    if (bg_change_x != 0 or bg_change_y != 0):
        if cpt_mouv >= 10 :
            hero.marcher()
            cpt_mouv = 0
    elif hero.step % 2 == 1 :
        hero.step = 0
        hero.image = heros[hero.cote][hero.step]
        
    for i in range(len(bgs_coords)) :
        if bgs_coords[i][0] > length :
            bgs_coords[i][0] -= length*2
        elif bgs_coords[i][0] < -length:
            bgs_coords[i][0] += length*2
        if bgs_coords[i][1] > length :
            bgs_coords[i][1] -= length*2
        elif bgs_coords[i][1] < -length:
            bgs_coords[i][1] += length*2
        bgs_coords[i][0] += bg_change_x
        bgs_coords[i][1] += bg_change_y
        screen.blit(bg,bgs_coords[i])
    
    hero.draw()
    screen.blit(enemy.image,enemy.rect)


    pygame.display.flip()

pygame.quit()