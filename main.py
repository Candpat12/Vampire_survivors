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
bullet_folder = path.join(sprite_folder,'bullet')

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
    
bullets = []
for i in range(1,5) :
    bullets.append(pygame.image.load((path.join(bullet_folder,"bullet_"+str(i)+'.png'))))

clock = pygame.time.Clock()         # on définit l'horloge interne

game_on = True
cpt_mouv = 0                # cpt_mouv compte le temps qui s'écoule entre 2 mouvements, pour que le sprite ne change pas trop vite
cpt_spawn = 0
cpt_immunity = FPS*2
all_enemy = pygame.sprite.Group()
all_bullets = pygame.sprite.Group()
nb_enemy = 0                # nb_enemy compte le nombre d'ennemis
max_enemy = 100              # max_enemy correspond au nombre maximum d'ennemis
cpt_enemy = 0               # cpt_enemy compte le temps écoulé entre 2 apparitions d'ennemis
delay_enemy = FPS*0.5           # delay_enemy définis le temps qu'il faut attendre entre 2 apparitions d'ennemis
cpt_bullet = 0
delay_bullet = FPS // 2
hero_speed = 5              # hero_speed et enemy_speed correspondent à la vitesse du héro et des enemy
enemy_speed = 3
max_health = 100            # max_health et hp correspondent respectivement aux PV maximums et aux PV actuels
hp = 100

class Hero(pygame.sprite.Sprite) :
    
    def __init__(self) :
        pygame.sprite.Sprite.__init__(self)
        self.cote = 0
        self.step = 0
        self.image = heros[self.cote][self.step]            # hero.cote correspond à la liste de heros que l'on va utiliser (gauche ou droite)
        self.rect = self.image.get_rect()                   # hero.step correspond à l'étape du cycle de marche du héro dans lequel on se trouve
        self.rect.center = (length// 2,length//2)
        self.immune = False
        
        
    
    def draw(self) :
        global cpt_immunity
        if cpt_immunity >= FPS*2 :
            self.immune = False
        elif cpt_immunity % 10 == 0 :
            self.immune = not self.immune
        if not self.immune :    
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
        b = choice([i for i in range(-length//2,1)]+[i for i in range(length,int(length*1.5))])
        self.knocked = False
        if choice([True,False]) :
            self.rect.center = (a,b)
        else :
            self.rect.center = (b,a)
    
    def update(self) :
        global cpt_immunity,hp
        if not self.knocked :
            liste_mouv = [0,0]
            if self.rect.x not in [(length//2)-40,(length//2)-15] and self.rect.y not in [(length//2)-40,(length//2)-15] :
                velocity = enemy_speed/sqrt(2)
            else :
                velocity = enemy_speed
            if self.rect.x >= (length//2) - 15 :
                self.rect.x -= velocity
                liste_mouv[0] = -velocity
            elif self.rect.x <= (length//2) - 40 :
                self.rect.x += velocity
                liste_mouv[0] = velocity
            if self.rect.y >= (length//2) - 15 :
                self.rect.y -= velocity
                liste_mouv[1] = -velocity
            elif self.rect.y <= (length//2) - 40 :
                self.rect.y += velocity
                liste_mouv[1] = velocity
            if pygame.sprite.collide_rect(self,hero) and cpt_immunity >= FPS*2 :
                cpt_immunity = 0
                self.knocked = True
                hp -= 5
            if liste_mouv != [0,0] :
                self.liste_mouv = liste_mouv
        else :
            self.rect.x -= self.liste_mouv[0]*2
            self.rect.y -= self.liste_mouv[1]*2
            if cpt_immunity > FPS*0.5 :
                self.knocked = False

class Bullet(pygame.sprite.Sprite) :
    
    def __init__(self,cote) :
        pygame.sprite.Sprite.__init__(self)
        self.image = bullets[0]
        self.status = 0
        self.rect = self.image.get_rect()
        self.rect.center = (length//2,length//2)
        self.cpt_rota = 0
        self.delay_rota = FPS//16
        if cote == 0 :
            self.mouv = 7
        else :
            self.mouv = -7
        
    def update(self) :
        global all_enemy
        self.rect.x += self.mouv
        self.cpt_rota += 1
        if self.cpt_rota >= self.delay_rota :
            self.status = (self.status+1) % 4
            self.image = bullets[self.status]
            self.cpt_rota = 0
            
            
    

hero = Hero()

#--------------------Programme principal--------------------

while game_on :
    
    if hp <= 0 :
        game_on = False
        
    cpt_mouv += 1           # on incrémente chaque compteur
    cpt_enemy += 1
    cpt_bullet += 1
    
    if cpt_immunity < FPS*2 :
        cpt_immunity += 1
        
    
    clock.tick(FPS)
    
    bg_change_x = 0         # quand le héro se "déplace", c'est le bg qui en réalité change. On définit bg_change x et y que
    bg_change_y = 0         # l'on va plus tard modifier, puis incrémenter aux coordonnés de chaque background


#--------------------Vérification des évènements--------------------


    for event in pygame.event.get() :
        if event.type == pygame.QUIT :      # on vérifie si le joueur essaie de quitter
            game_on = False

    keys = pygame.key.get_pressed()
    if int(keys[pygame.K_z]) + int(keys[pygame.K_s]) + int(keys[pygame.K_q]) + int(keys[pygame.K_d]) == 2 :
        velocity = hero_speed/sqrt(2)               # la vitesse change selon si l'on est en diagonale ou en ligne droite
    else :                                          # on se sert du théorème de pythagore pour que la vitesse reste la même
        velocity = hero_speed
    if keys[pygame.K_z] :
        bg_change_y += velocity
    if keys[pygame.K_q] :
        bg_change_x += velocity
        hero.cote = 1
    if keys[pygame.K_s] :                   # on regarde si le joueur appuie sur z,q,s ou d, puis on modifie bg_change
        bg_change_y -= velocity             # on change également le côté du sprite du joueur si besoin
    if keys[pygame.K_d] :
        bg_change_x -= velocity
        hero.cote = 0
    
    
#--------------------Déplacements/apparitions des ennemis--------------------
    
    
    for enemy in all_enemy.sprites() :
        enemy.rect.x += bg_change_x             # ici, on éloigne (ou rapproche) le joueur de l'ennemi selon son déplacement
        enemy.rect.y += bg_change_y
    
    for bullet in all_bullets.sprites() :
        bullet.rect.x += bg_change_x             # ici, on éloigne (ou rapproche) le joueur de l'ennemi selon son déplacement
        bullet.rect.y += bg_change_y

    if cpt_enemy >= delay_enemy and nb_enemy <= max_enemy :
        all_enemy.add(Enemy())
        cpt_enemy = 0                           # on définit les conditions qui font qu'un nouvel ennemi peut apparaître
        nb_enemy += 1
    
    if cpt_bullet >= delay_bullet :
        a = Bullet(hero.cote)
        all_bullets.add(a)
        cpt_bullet = 0
    
    all_enemy.update()                          # chaque ennemi se rapproche du joueur
    all_bullets.update()
    
    if (bg_change_x != 0 or bg_change_y != 0):
        if cpt_mouv >= 10 :
            hero.marcher()                  # s'il y a eu un déplacement et si le chrono le permet, on change le sprite
            cpt_mouv = 0
    elif hero.step % 2 == 1 :
        hero.step = 0                       # si le héro est sur un sprite où il est en train de marcher, on retourne au sprite de base
        hero.image = heros[hero.cote][hero.step]
            
    
#--------------------condition de mort des divers sprites--------------------
    for bullet in all_bullets.sprites() :
        if bullet.rect.x > length*2 or bullet.rect.x < -length or bullet.rect.y > length*2  or bullet.rect.y < -length :
            all_bullets.remove(bullet)
        for enemy in all_enemy.sprites() :
            if pygame.sprite.collide_rect(enemy,bullet) :
                all_bullets.remove(bullet)
                all_enemy.remove(enemy)




#--------------------affichage des sprites + modification du background--------------------
        

    for i in range(len(bgs_coords)) :
        if bgs_coords[i][0] > length :
            bgs_coords[i][0] -= length*2
        elif bgs_coords[i][0] < -length:
            bgs_coords[i][0] += length*2        # si un fond est hors-champ, on le fait réapparaitre de l'autre côté
        if bgs_coords[i][1] > length :          # c'est ce qui donne l'impression d'une map infinie
            bgs_coords[i][1] -= length*2
        elif bgs_coords[i][1] < -length:
            bgs_coords[i][1] += length*2
        bgs_coords[i][0] += bg_change_x         # chaque bg va changer de coordonnées selon le déplacement du joueur
        bgs_coords[i][1] += bg_change_y         
        screen.blit(bg,bgs_coords[i])           # on affiche les backgrounds
    
    
    hero.draw()                                 # on affiche le héro et les ennemis à l'écran
    all_enemy.draw(screen)
    all_bullets.draw(screen)
    pygame.draw.rect(screen,(255,0,0),(476,558,72,10))
    pygame.draw.rect(screen,(0,255,0),(476,558,72*(hp/max_health),10))
    pygame.display.flip()                       # on retourne l'écran pour afficher les changements

pygame.quit()