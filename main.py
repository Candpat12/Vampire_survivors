import pygame
from os import path
from random import randint,choice
from math import sqrt

pygame.init()
length = 1024       # length correspond à la longueur de l'écran, qui est carré
FPS = 60            # FPS correspond aux nombres de frames par secondes

screen = pygame.display.set_mode((length,length))       # on définit l'écran
pygame.display.set_caption("Vampire survivors")                   

game_folder = path.dirname(__file__)
sprite_folder = path.join(game_folder,'sprites')
hero_folder = path.join(sprite_folder,'hero')           # on se place dans les différents dossiers dont on va avoir besoin
enemy_folder = path.join(sprite_folder,'enemy')

bg = pygame.image.load(path.join(sprite_folder, "bg.png")).convert()        # on importe le sprite du fond d'écran
bgs_coords = [[-length,-length],[-length,0],[-length,length],[0,-length],[0,0]\
              ,[0,length],[length,-length],[length,0],[length,length]]      # il va y avoir 9 "fonds d'écrans, on définit leurs coordonnées
heros = []
for file in [path.join(hero_folder,'right'),path.join(hero_folder,'left')] :
    l = []
    for i in range(1,5) :
        a = pygame.image.load(path.join(file,"hero_"+str(i)+'.png'))        # heros est une liste de 2 listes de 4 frames : la première
        a = pygame.transform.scale2x(a)                                     # correspond à lorsque l'on est orienté à droite
        l.append(a)                                                         # et l'autre lorsque regarde à gauche
    heros.append(l)
    
enemies = []
for file in [path.join(enemy_folder,'right'),path.join(enemy_folder,'left')] :
    l = []
    for i in range(1,4) :
        a = pygame.image.load(path.join(file,"enemy_"+str(i)+'.png'))       # pareil que pour "héros", mais avec enemy
        a = pygame.transform.scale2x(a)
        l.append(a)
    enemies.append(l)

clock = pygame.time.Clock()         # on définit l'horloge interne

game_on = True
cpt_mouv = 0                # cpt_mouv compte le temps qui s'écoule entre 2 mouvements, pour que le sprite ne change pas trop vite
cpt_spawn = 0
all_enemy = pygame.sprite.Group()
nb_enemy = 0                # nb_enemy compte le nombre d'ennemis
max_enemy = 10              # max_enemy correspond au nombre maximum d'ennemis
cpt_enemy = 0               # cpt_enemy compte le temps écoulé entre 2 apparitions d'ennemis
delay_enemy = FPS           # delay_enemy définis le temps qu'il faut attendre entre 2 apparitions d'ennemis
hero_speed = 5              # hero_speed et enemy_speed correspondent à la vitesse du héro et des enemy
enemy_speed = 3

class Hero(pygame.sprite.Sprite) :
    
    def __init__(self) :
        pygame.sprite.Sprite.__init__(self)
        self.cote = 0
        self.step = 0
        self.image = heros[self.cote][self.step]            # hero.cote correspond à la liste de heros que l'on va utiliser (gauche ou droite)
        self.rect = self.image.get_rect()                   # hero.step correspond à l'étape du cycle de marche du héro dans lequel on se trouve
        self.rect.center = (length// 2,length//2)
    
    def draw(self) :
        screen.blit(self.image,self.rect)                   # draw sert à dessiner sur l'écran le sprite
    
    def marcher(self) :
        self.step = (self.step + 1) % 4
        self.image = heros[self.cote][self.step]            # marcher permet d'avancer dans le cycle de marche du sprite
        
class Enemy(pygame.sprite.Sprite) :
    
    def __init__(self) :
        pygame.sprite.Sprite.__init__(self)
        self.cote = 0
        self.step = 0                                       # pareil que hero
        self.image = enemies[self.cote][self.step]
        self.rect = self.image.get_rect()
        a = randint(-length,length)
        b = choice([i for i in range(-length,1)]+[i for i in range(length,length*2+1)])
        if choice([True,False]) :
            self.rect.center = (a,b)
        else :
            self.rect.center = (b,a)
    
    def draw(self) :
        screen.blit(self.image,self.rect)                   # draw sert à dessiner sur l'écran le sprite
    
    def update(self) :
        if self.rect.x not in [(length//2)-40,(length//2)-15] and self.rect.y not in [(length//2)-40,(length//2)-15] :
            velocity = enemy_speed/sqrt(2)
        else :
            velocity = enemy_speed
        if self.rect.x >= (length//2) - 15 :
            self.rect.x -= velocity
        elif self.rect.x <= (length//2) - 40 :
            self.rect.x += velocity
        if self.rect.y >= (length//2) - 15 :
            self.rect.y -= velocity
        elif self.rect.y <= (length//2) - 40 :
            self.rect.y += velocity
        

hero = Hero()
enemy = Enemy()

while game_on :
    
    cpt_mouv += 1
    cpt_enemy += 1
    
    clock.tick(FPS)
    bg_change_x = 0         # quand le héro se "déplace", c'est le bg qui en réalité change. On définit bg_change x et y que
    bg_change_y = 0         # l'on va plus tard modifier, puis incrémenter aux coordonnés de chaque background

    for event in pygame.event.get() :
        if event.type == pygame.QUIT :      # on vérifie si le joueur essaie de quitter
            game_on = False

    keys = pygame.key.get_pressed()
    if (keys[pygame.K_z] or keys[pygame.K_s]) and (keys[pygame.K_q] or keys[pygame.K_d]) :
        velocity = hero_speed/sqrt(2)
    else :
        velocity = hero_speed
    if keys[pygame.K_z] :
        bg_change_y += velocity
    if keys[pygame.K_q] :
        bg_change_x += velocity
        if hero.cote == 0 :
            hero.cote = 1
    if keys[pygame.K_s] :                   # on regarde si le joueur appuie sur z,q,s ou d, puis on modifie bg_change
        bg_change_y -= velocity
    if keys[pygame.K_d] :
        bg_change_x -= velocity
        if hero.cote == 1 :
            hero.cote = 0
    
    for enemy in all_enemy.sprites() :
        enemy.rect.x += bg_change_x
        enemy.rect.y += bg_change_y

    if cpt_enemy >= delay_enemy and nb_enemy <= max_enemy :
        all_enemy.add(Enemy())
        cpt_enemy = 0
        nb_enemy += 1
    
    all_enemy.update()
    
    if (bg_change_x != 0 or bg_change_y != 0):
        if cpt_mouv >= 10 :
            hero.marcher()                  # s'il y a eu un déplacement et si le chrono le permet, on change le sprite
            cpt_mouv = 0
    elif hero.step % 2 == 1 :
        hero.step = 0                       # si le héro est sur un sprite où il est en train de marche, on retourne au sprite de base
        hero.image = heros[hero.cote][hero.step]
        
    for i in range(len(bgs_coords)) :
        if bgs_coords[i][0] > length :
            bgs_coords[i][0] -= length*2
        elif bgs_coords[i][0] < -length:
            bgs_coords[i][0] += length*2        # si un fond est hors-champ, on le fait réapparaitre de l'autre côté
        if bgs_coords[i][1] > length :          # c'est ce quidonne l'impression d'une map infinie
            bgs_coords[i][1] -= length*2
        elif bgs_coords[i][1] < -length:
            bgs_coords[i][1] += length*2
        bgs_coords[i][0] += bg_change_x         # chaque bg va changer de coordonnées selon le déplacement du joueur
        bgs_coords[i][1] += bg_change_y         
        screen.blit(bg,bgs_coords[i])           # on affiche les backgrounds
    
    hero.draw()                                 # on affiche le héro à l'écran
    all_enemy.draw(screen)
    
    pygame.display.flip()                       # on retourne l'écran pour afficher les changements

pygame.quit()