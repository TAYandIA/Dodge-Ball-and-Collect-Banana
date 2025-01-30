#  un jeu de ballon , didactitiel video

import pygame
import random
import math

pygame.init()
hauteur_ecran = 800
largeur_ecran = 500


surface=pygame.display.set_mode((largeur_ecran,hauteur_ecran))

pygame.display.set_caption("link vs donkey kong")
horloge=pygame.time.Clock()

animlink = False
animDk = True

flip = False
vitesse = 5

plan = pygame.image.load("RessourcesJeux/background.jpg")

singe = pygame.image.load('RessourcesJeux/Dk anim/Idle/anim (1).gif')
singe_collision = 150
singeX,singeY = 400, 700

link = pygame.image.load('RessourcesJeux/link up/anim (1).gif')
link_collision = 30
linkX,linkY = 10, 30

def detect_collision(x1, y1, r1, x2, y2, r2):
    distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return distance <= (r1 + r2)

def list_pour_frame(path,nb_frame):
    pos_anim_link = []
    for i in range(nb_frame):
        pos_anim_link.append(path+'/'+'anim ('+str(i+1)+').gif')
    return pos_anim_link


def animer(chrono,truc_a_anime,event,animation,anim_actuelle):
    if anim_actuelle >= len(animation):
        anim_actuelle = -1
    if event.type == chrono:
        anim_actuelle += 1
        return [pygame.image.load(animation[anim_actuelle-1]),anim_actuelle]
    else :
        return [truc_a_anime,anim_actuelle]


def blit_link():
    global surface
    global flip
    global link,link_collision

    if flip == True:
        surface.blit(pygame.transform.flip(link, True, False),(linkX,linkY))
    else :
        surface.blit(link,(linkX,linkY))

def move_link():
    global linkX,linkY
    global animlink
    global vitesse
    global pos_anim_link
    global flip
    pressed_keys = pygame.key.get_pressed()

    if pressed_keys[pygame.K_LEFT]:
        if linkX > -1:
            linkX -= vitesse
        animlink = True
        pos_anim_link = list_pour_frame('RessourcesJeux/link side',2)
        flip = False

    elif pressed_keys[pygame.K_RIGHT]:
        if linkX < largeur_ecran - link_collision*2:
            linkX += vitesse
        flip = True
        pos_anim_link = list_pour_frame('RessourcesJeux/link side',2)
        animlink = True

    if pressed_keys[pygame.K_UP]:
        if linkY > -1:
            linkY -= vitesse
        flip = False
        pos_anim_link = list_pour_frame('RessourcesJeux/link up',2)
        animlink = True

    if pressed_keys[pygame.K_DOWN]:
        if linkY < hauteur_ecran - link_collision*2:
            linkY += vitesse
        flip = False
        pos_anim_link = list_pour_frame('RessourcesJeux/link down',2)
        animlink = True

    if pressed_keys[pygame.K_RIGHT] + pressed_keys[pygame.K_DOWN] + pressed_keys[pygame.K_UP] +  pressed_keys[pygame.K_LEFT] == 0:
        animlink = False


chrono_eventlink = pygame.USEREVENT+1
pygame.time.set_timer(chrono_eventlink, 50)
anim_actuelle_link = -1
def animer_link(event):
    global chrono_eventlink
    global anim_actuelle_link
    global link
    global animlink
    global pos_anim_link

    if animlink == True:
        donnee_anim_link = animer(chrono_eventlink,link,event,pos_anim_link,anim_actuelle_link)
        link = donnee_anim_link[0]
        anim_actuelle_link = donnee_anim_link[1]

chrono_banane = pygame.USEREVENT+2
pygame.time.set_timer(chrono_banane, 50)
anim_actuelle_banana = -1
def animer_banane(event,bananes):
    global anim_actuelle_banana
    global chrono_banane

    pos_anim_link = list_pour_frame('RessourcesJeux/banana',12)
    list_animation = []
    for banane in bananes:
        donne_anim_banane = animer(chrono_banane,banane,event,pos_anim_link,anim_actuelle_banana)
        banane = donne_anim_banane[0]
        anim_actuelle_banana = donne_anim_banane[1]
        list_animation.append(banane)

    return list_animation



chrono_not_happy = pygame.USEREVENT+3
pygame.time.set_timer(chrono_not_happy, 100)
chrono_happy = pygame.USEREVENT+4
pygame.time.set_timer(chrono_happy, 60)

anim_actuelle_singe_not_happy = -1
anim_actuelle_singe_happy = -1
happy = False
def animer_dk(event):
    global anim_actuelle_singe_not_happy,anim_actuelle_singe_happy
    global singe,singeX,singeY
    global animDk
    global happy
    global chrono_time_happy
    pos_anim_link_not_happy = list_pour_frame('RessourcesJeux/Dk anim/Idle',10)
    pos_anim_link_happy = list_pour_frame("RessourcesJeux/Dk anim/happy",13)
    if not happy:
        singeX,singeY = 300, 600
        donne_anim_singe = animer(chrono_not_happy,singe,event,pos_anim_link_not_happy,anim_actuelle_singe_not_happy)
        singe = donne_anim_singe[0]
        anim_actuelle_singe_not_happy = donne_anim_singe[1]
    if happy:
        singeX,singeY = 250, 550
        donne_anim_singe = animer(chrono_happy,singe,event,pos_anim_link_happy,anim_actuelle_singe_happy)
        singe = donne_anim_singe[0]
        anim_actuelle_singe_happy = donne_anim_singe[1]
    if anim_actuelle_singe_happy == 13:
        happy = False

def collision_banane(event,bananes_donnee):
    global link_collision
    global singe_collision
    for bananes_donnee in bananes_donnee:
        if detect_collision(linkX+link_collision,linkY+link_collision,link_collision,bananes_donnee[0],bananes_donnee[1]+bananes_donnee[2],bananes_donnee[2]+bananes_donnee[2]):
            bananes_donnee[0] = random.randint(0,450)
            bananes_donnee[1] = random.randint(0,750)
            recuperer_banane(event)

        if detect_collision(singeX+singe_collision,singeY+singe_collision,singe_collision,bananes_donnee[0]+bananes_donnee[2],bananes_donnee[1]+bananes_donnee[2],bananes_donnee[2]):
            bananes_donnee[0] = random.randint(0,450)
            bananes_donnee[1] = random.randint(0,750)

score = 0
music_deja_joue = True
def recuperer_banane(event):
    global score
    global happy
    global music_deja_joue
    global vx, vy
    happy = True
    bande_son = pygame.mixer.music.load("RessourcesJeux/oh banana.mp3")
    pygame.mixer.music.play()
    score += 1

chrono_time_left = pygame.USEREVENT+5
pygame.time.set_timer(chrono_time_left, 1000)

time_left = 60
def chrono(event):
    global chrono_time_left
    global time_left
    global vx,vy

    if event.type == chrono_time_left:
        vx *= 1.01
        vy *= 1.01
        time_left -= 1

ball = pygame.image.load("RessourcesJeux/ball.png")
ball_collision = 95
ballX,ballY = 200,300
vx, vy = 1.3, 1.3
collision_avec_ballon = False
def move_balle():
    global vx,vy,largeur_ecran,hauteur_ecran,ballY,ballX,ball_collision,collision_avec_ballon
    ballX -= vx
    ballY -= vy
    rayon = ball_collision
    if ballX <= 0 or ballX > largeur_ecran - rayon*2:
        vx = -vx
    if ballY <= 0 or ballY > hauteur_ecran - rayon*2:
        vy = -vy

    if detect_collision(linkX+link_collision,linkY+link_collision,link_collision,ballX+ball_collision,ballY+ball_collision,ball_collision):
        collision_avec_ballon = True



play = True
score = 0
def principale():
    global singe
    global singe_collision
    global link
    global linkX,linkY,link_collision
    global play
    global score
    global time_left
    global vx, vy
    global ballX,ballY
    global collision_avec_ballon
    game_over=False

    font = pygame.font.Font("RessourcesJeux/police.ttf",22)

    text_perdu = font.render("Appuiyez sur Entrer",True,(0,255,0))
    background_text = pygame.image.load("RessourcesJeux/background text.png")

    banane1 = pygame.image.load('RessourcesJeux/banana/anim (1).gif')
    banane_donnee1 = [450, 500,20]

    banane2 = pygame.image.load('RessourcesJeux/banana/anim (1).gif')
    banane_donnee2 = [300, 500,20]

    while not game_over:
        keys=pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                game_over=True
            chrono(event)

            #dialogue(event)
            if play:
                animer_dk(event)
                animer_link(event)
                [banane1,banane2] = animer_banane(event,[banane1,banane2])

        if play:
            text_score = font.render("Score : "+str(score),True,(200,0,0))
            text_seconds = font.render("Temps Restants : "+str(time_left),True,(0,0,0))

            surface.blit(plan,(0,0))
            move_balle()
            move_link()
            collision_banane(event,[banane_donnee1,banane_donnee2])
            blit_link()

            surface.blit(singe, (singeX,singeY))
            surface.blit(banane1,(banane_donnee1[0],banane_donnee1[1]))
            surface.blit(banane2,(banane_donnee2[0],banane_donnee2[1]))
            surface.blit(ball,(ballX,ballY))
            surface.blit(text_score,(10,10))
            surface.blit(text_seconds,(180,10))

            if time_left <= 0 or collision_avec_ballon:
                link = pygame.image.load('RessourcesJeux/link up/anim (1).gif')
                play = False

        else:
            pressed_keys = pygame.key.get_pressed()
            surface.blit(background_text,(25,395))
            surface.blit(text_perdu,(50,420))
            surface.blit(text_score,(50,450))
            if pressed_keys[pygame.K_RETURN]:
                linkX,linkY = 50,50
                ballX,ballY = 200,400
                score = 0
                time_left = 60
                vx, vy = 1.3,1.3
                collision_avec_ballon = False
                play = True

        horloge.tick(60)
        pygame.display.update()

principale()
pygame.quit()
quit()