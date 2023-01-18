from random import *
from pygame import *

init()

hauteur = 910
largeur = 1215
fenetre = display.set_mode((largeur, hauteur))
display.set_caption("Catch the snowflakes")
display.set_icon(image.load("snowflake.png"))

# horloge
horloge = time.Clock()

# arrière-plan
paysage = image.load("mountain.png")
paysage = transform.scale(paysage, (largeur, hauteur))
paysager = paysage.get_rect()

# ours
ours = image.load("polar-bear.png")
ours = transform.scale(ours, (324, 133))
oursr = ours.get_rect()

# eclair
eclair = image.load("lightning.png")
eclair = transform.scale(eclair, (13, 50))
eclairr = eclair.get_rect()
vitesse_eclair = 7

# flocon
flocon = image.load("snowflake.png")
flocon = transform.scale(flocon, (50, 50))
floconr = flocon.get_rect()
vitesse_flocon = 5

# écriture des vies
vies = 3
couleur_texte = (0, 0, 0)
police = font.Font("PermanentMarker-Regular.ttf", 30)
message_vie = police.render(f"Vies: {vies}", 1, couleur_texte)
message_vier = message_vie.get_rect()
message_vier.x = 40
message_vier.y = 20

# écriture des points
points = 0
message_points = police.render(f"Points: {points}", 1, couleur_texte)
message_pointsr = message_points.get_rect()
message_pointsr.x = largeur - 200
message_pointsr.y = 20

# fond noir transparent
rectangle_noir = Surface((largeur, hauteur), SRCALPHA)
rectangle_noir.fill((0, 0, 0, 175))

# bouton restart
gris = (175, 175, 175)
restart = police.render("restart", 1, gris)
restartr = restart.get_rect(center=(largeur//2, hauteur//2))

def nouveau_flocon():
    """déplace le flocon vers le haut de l'écran"""
    floconr.x = randint(0, largeur - floconr.width)
    floconr.y = randint(-150, -100)

def nouvel_eclair():
    """déplace l'éclair vers le haut de l'écran"""
    eclairr.x = randint(0, largeur - eclairr.width)
    eclairr.y = randint(-150, -100)

def setup_jeu():
    global vies, points, message_vie, message_points
    vies = 3
    message_vie = police.render(f"Vies: {vies}", 1, couleur_texte)
    points = 0
    message_points = police.render(f"Points: {points}", 1, couleur_texte)
    oursr.x = largeur / 2
    oursr.y = hauteur - oursr.height
    eclairr.x = randint(0, largeur - eclairr.width)
    eclairr.y = randint(-200, -50)
    floconr.x = randint(0, largeur - floconr.width)
    floconr.y = randint(-200, -50)

def affichejeu():
    """affiche les éléments du jeu"""
    fenetre.blit(paysage, paysager)
    fenetre.blit(ours,oursr)
    fenetre.blit(eclair, eclairr)
    fenetre.blit(flocon, floconr)
    fenetre.blit(message_vie, message_vier)
    fenetre.blit(message_points, message_pointsr)

def affichefin():
    """affiche les éléments de l'écran de fin de jeu"""
    fenetre.blit(paysage, paysager)
    fenetre.blit(rectangle_noir, (0, 0))
    fenetre.blit(restart, restartr)

en_cours = True
perdu = False
flèche_gauche = False
flèche_droite = False

setup_jeu()

while en_cours:
    if vies == 0:
        perdu = True
        
    if not perdu:
        # les éclairs tombent
        eclairr.y = eclairr.y + vitesse_eclair
        if eclairr.y >= hauteur:
            nouvel_eclair()

        # les flocons tombent
        floconr.y = floconr.y + vitesse_flocon
        if floconr.y >= hauteur:
            nouveau_flocon()

        # collision avec le flocon
        if oursr.colliderect(floconr):
            points += 1
            message_points = police.render(f"Points: {points}", 1, couleur_texte)
            nouveau_flocon()

        # collision avec l'éclair
        if oursr.colliderect(eclairr):
            vies -= 1
            message_vie = police.render(f"Vies: {vies}", 1, couleur_texte)
            nouvel_eclair()

        # déplacement de l'ours
        if flèche_gauche and oursr.x > 0:
            oursr = oursr.move(-20, 0)
        if flèche_droite and oursr.x < largeur - oursr.width:
            oursr = oursr.move(20, 0)

    # événements
    for evenement in event.get():
        if evenement.type == QUIT:
            en_cours = False

        # on teste si on appuye sur une touche
        if evenement.type == KEYDOWN:  
            if evenement.key == K_LEFT:  # flèche de gauche
                flèche_gauche = True
            if evenement.key == K_RIGHT:  # flèche de droite
                flèche_droite = True

        # on teste si on relache sur une touche
        if evenement.type == KEYUP:  
            if evenement.key == K_LEFT:  # flèche de gauche
                flèche_gauche = False
            if evenement.key == K_RIGHT:  # flèche de droite
                flèche_droite = False

        # on teste si on a cliqué avec la souris
        if evenement.type == MOUSEBUTTONDOWN:
            xmouse, ymouse = mouse.get_pos()
            if restartr.collidepoint(xmouse, ymouse):
                setup_jeu()
                perdu = False

    if perdu:
        affichefin()
    else:
        affichejeu()

    display.update()
    horloge.tick(40)

quit()
