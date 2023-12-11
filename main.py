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

bg = pygame.image.load(path.join(sprite_folder, "bg.png")).convert()
bgs_coords = [[-length,-length],[-length,0],[-length,length],[0,-length],[0,0],[0,length],[length,-length],[length,0],[length,length]]
heros = []
for file in [path.join(hero_folder,'right'),path.join(hero_folder,'left')] :
    l = []
    for i in range(1,5) :
        l.append(pygame.image.load(path.join(file,"hero_"+str(i)+'.png')))
    heros.append(l)

clock = pygame.time.Clock()

class Hero(pygame.sprite.Sprite) :
    
    def __init__(self) :
        pygame.sprite.Sprite.__init__(self)
        self.images = heros
        self.image = heros[0][0]
        self.rect = self.image.get_rect
        self.rect.center = (length// 2,length//2)

hero = Hero()
game_on = True

while game_on :
    
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
    if keys[pygame.K_s] :
        bg_change_y -= 5
    if keys[pygame.K_d] :
        bg_change_x -= 5

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
    
    hero.draw(screen)

    pygame.display.update()

pygame.quit()