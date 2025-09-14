"""Estelle Doriot
Catch the snowflakes game
You control a polar bear to catch snowflakes and avoid lightning.
"""

from random import randint
import pygame

pygame.init()

HAUTEUR = 910
LARGEUR = 1215
fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Catch the snowflakes")
pygame.display.set_icon(pygame.image.load("snowflake.png"))

# horloge
horloge = pygame.time.Clock()

# arrière-plan
paysage = pygame.image.load("mountain.png")
paysage = pygame.transform.scale(paysage, (LARGEUR, HAUTEUR))
paysager = paysage.get_rect()

# ours
ours = pygame.image.load("polar-bear.png")
ours = pygame.transform.scale(ours, (324, 133))
oursr = ours.get_rect()

# eclair
eclair = pygame.image.load("lightning.png")
eclair = pygame.transform.scale(eclair, (13, 50))
eclairr = eclair.get_rect()
vitesse_eclair = 7

# flocon
flocon = pygame.image.load("snowflake.png")
flocon = pygame.transform.scale(flocon, (50, 50))
floconr = flocon.get_rect()
vitesse_flocon = 5

# écriture des vies
vies = 3
couleur_texte = (0, 0, 0)
police = pygame.font.Font("PermanentMarker-Regular.ttf", 30)
message_vie = police.render(f"Vies: {vies}", True, couleur_texte)
message_vier = message_vie.get_rect()
message_vier.x = 40
message_vier.y = 20

# écriture des points
points = 0
message_points = police.render(f"Points: {points}", True, couleur_texte)
message_pointsr = message_points.get_rect()
message_pointsr.x = LARGEUR - 200
message_pointsr.y = 20

# fond noir transparent
rectangle_noir = pygame.Surface((LARGEUR, HAUTEUR), pygame.SRCALPHA)
rectangle_noir.fill((0, 0, 0, 175))

# bouton restart
gris = (175, 175, 175)
restart = police.render("restart", True, gris)
restartr = restart.get_rect(center=(LARGEUR // 2, HAUTEUR // 2))


def nouveau_flocon():
    """déplace le flocon vers le haut de l'écran"""
    floconr.x = randint(0, LARGEUR - floconr.width)
    floconr.y = randint(-150, -100)


def nouvel_eclair():
    """déplace l'éclair vers le haut de l'écran"""
    eclairr.x = randint(0, LARGEUR - eclairr.width)
    eclairr.y = randint(-150, -100)


def setup_jeu():
    """initialisation des variables globales"""
    global vies, points, message_vie, message_points
    vies = 3
    message_vie = police.render(f"Vies: {vies}", True, couleur_texte)
    points = 0
    message_points = police.render(f"Points: {points}", True, couleur_texte)
    oursr.x = LARGEUR // 2
    oursr.y = HAUTEUR - oursr.height
    eclairr.x = randint(0, LARGEUR - eclairr.width)
    eclairr.y = randint(-200, -50)
    floconr.x = randint(0, LARGEUR - floconr.width)
    floconr.y = randint(-200, -50)


def affiche_jeu():
    """affiche les éléments du jeu"""
    fenetre.blit(paysage, paysager)
    fenetre.blit(ours, oursr)
    fenetre.blit(eclair, eclairr)
    fenetre.blit(flocon, floconr)
    fenetre.blit(message_vie, message_vier)
    fenetre.blit(message_points, message_pointsr)


def affiche_fin():
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
        if eclairr.y >= HAUTEUR:
            nouvel_eclair()

        # les flocons tombent
        floconr.y = floconr.y + vitesse_flocon
        if floconr.y >= HAUTEUR:
            nouveau_flocon()

        # collision avec le flocon
        if oursr.colliderect(floconr):
            points += 1
            message_points = police.render(f"Points: {points}", True, couleur_texte)
            nouveau_flocon()

        # collision avec l'éclair
        if oursr.colliderect(eclairr):
            vies -= 1
            message_vie = police.render(f"Vies: {vies}", True, couleur_texte)
            nouvel_eclair()

        # déplacement de l'ours
        if flèche_gauche and oursr.x > 0:
            oursr = oursr.move(-20, 0)
        if flèche_droite and oursr.x < LARGEUR - oursr.width:
            oursr = oursr.move(20, 0)

    # événements
    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            en_cours = False

        # on teste si on appuye sur une touche
        if evenement.type == pygame.KEYDOWN:
            if evenement.key == pygame.K_LEFT:  # flèche de gauche
                flèche_gauche = True
            if evenement.key == pygame.K_RIGHT:  # flèche de droite
                flèche_droite = True

        # on teste si on relache sur une touche
        if evenement.type == pygame.KEYUP:
            if evenement.key == pygame.K_LEFT:  # flèche de gauche
                flèche_gauche = False
            if evenement.key == pygame.K_RIGHT:  # flèche de droite
                flèche_droite = False

        # on teste si on a cliqué avec la souris
        if evenement.type == pygame.MOUSEBUTTONDOWN:
            xmouse, ymouse = pygame.mouse.get_pos()
            if restartr.collidepoint(xmouse, ymouse):
                setup_jeu()
                perdu = False

    if perdu:
        affiche_fin()
    else:
        affiche_jeu()

    pygame.display.update()
    horloge.tick(40)

pygame.quit()
