import pygame
import random

pygame.init()

LARGEUR, HAUTEUR = 400, 600
ecran = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Challenge of Vicentia - Course")

BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
ROUGE = (220, 50, 50)
BLEU = (50, 100, 220)
GRIS = (90, 90, 90)
VERT = (60, 140, 60)
VITRE = (180, 220, 255)
JAUNE = (230, 200, 60)
VIOLET = (150, 70, 180)
MARRON = (140, 90, 60)
TOIT = (170, 60, 50)
VERT_FEU = (60, 200, 60)
ROUGE_FEU = (200, 40, 40)
JAUNE_FEU = (220, 200, 50)

horloge = pygame.time.Clock()
police = pygame.font.SysFont(None, 36)
police_petite = pygame.font.SysFont(None, 28)

ROUTE_MARGE = 20

voiture_largeur, voiture_hauteur = 50, 90
voiture_x = LARGEUR // 2 - voiture_largeur // 2
voiture_y = HAUTEUR - 120
vitesse_voiture = 8

obstacle_largeur, obstacle_hauteur = 50, 90
obstacles = []
couleurs_obstacles = [ROUGE, JAUNE, VIOLET]
vitesse_obstacles = 6
timer_spawn = 0

maisons = []
timer_maison = 0

score = 0
jeu_actif = True
en_cours = True

decalage_ligne = 0
timer_feu = 0
etat_feu = 0  # 0=rouge, 1=jaune, 2=vert


def dessiner_voiture(x, y, couleur):
    pygame.draw.rect(ecran, couleur, (x, y, voiture_largeur, voiture_hauteur), border_radius=10)
    pygame.draw.rect(ecran, VITRE, (x + 8, y + 10, voiture_largeur - 16, 20), border_radius=5)
    pygame.draw.rect(ecran, NOIR, (x - 4, y + 10, 8, 20))
    pygame.draw.rect(ecran, NOIR, (x + voiture_largeur - 4, y + 10, 8, 20))
    pygame.draw.rect(ecran, NOIR, (x - 4, y + voiture_hauteur - 30, 8, 20))
    pygame.draw.rect(ecran, NOIR, (x + voiture_largeur - 4, y + voiture_hauteur - 30, 8, 20))


def dessiner_maison(x, y, cote):
    largeur_maison, hauteur_maison = 45, 45
    pygame.draw.rect(ecran, MARRON, (x, y, largeur_maison, hauteur_maison))
    pygame.draw.polygon(ecran, TOIT, [
        (x - 5, y),
        (x + largeur_maison // 2, y - 20),
        (x + largeur_maison + 5, y)
    ])
    pygame.draw.rect(ecran, VITRE, (x + 8, y + 10, 10, 10))
    pygame.draw.rect(ecran, VITRE, (x + largeur_maison - 18, y + 10, 10, 10))
    pygame.draw.rect(ecran, (100, 60, 30), (x + largeur_maison // 2 - 6, y + 20, 12, 25))


def dessiner_route():
    ecran.fill(VERT)
    pygame.draw.rect(ecran, GRIS, (ROUTE_MARGE, 0, LARGEUR - ROUTE_MARGE * 2, HAUTEUR))

    for y in range(-40, HAUTEUR, 40):
        pygame.draw.line(ecran, BLANC, (LARGEUR // 2, y + decalage_ligne), (LARGEUR // 2, y + 20 + decalage_ligne), 4)

    pygame.draw.line(ecran, JAUNE, (ROUTE_MARGE, 0), (ROUTE_MARGE, HAUTEUR), 3)
    pygame.draw.line(ecran, JAUNE, (LARGEUR - ROUTE_MARGE, 0), (LARGEUR - ROUTE_MARGE, HAUTEUR), 3)


def dessiner_feu():
    x, y = LARGEUR // 2 - 15, 5
    pygame.draw.rect(ecran, NOIR, (x, y, 30, 70), border_radius=6)
    couleurs = [ROUGE_FEU, JAUNE_FEU, VERT_FEU]
    for i in range(3):
        couleur = couleurs[i] if i == etat_feu else (60, 60, 60)
        pygame.draw.circle(ecran, couleur, (x + 15, y + 12 + i * 22), 8)


while en_cours:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            en_cours = False

    touches = pygame.key.get_pressed()
    boutons_souris = pygame.mouse.get_pressed()
    pos_souris = pygame.mouse.get_pos()

    if jeu_actif:
        va_gauche = touches[pygame.K_LEFT]
        va_droite = touches[pygame.K_RIGHT]

        if boutons_souris[0]:
            if pos_souris[0] < LARGEUR // 2:
                va_droite = True
            else:
                va_gauche = True

        if va_gauche and voiture_x > ROUTE_MARGE:
            voiture_x -= vitesse_voiture
        if va_droite and voiture_x < LARGEUR - ROUTE_MARGE - voiture_largeur:
            voiture_x += vitesse_voiture

        decalage_ligne = (decalage_ligne + vitesse_obstacles) % 40

        timer_feu += 1
        if timer_feu > 90:
            timer_feu = 0
            etat_feu = (etat_feu + 1) % 3

        timer_spawn += 1
        if timer_spawn > 40:
            timer_spawn = 0
            x_obstacle = random.randint(ROUTE_MARGE, LARGEUR - ROUTE_MARGE - obstacle_largeur)
            couleur = random.choice(couleurs_obstacles)
            rect = pygame.Rect(x_obstacle, -obstacle_hauteur, obstacle_largeur, obstacle_hauteur)
            obstacles.append([rect, couleur])

        for item in obstacles[:]:
            item[0].y += vitesse_obstacles
            if item[0].y > HAUTEUR:
                obstacles.remove(item)
                score += 1
                if score % 5 == 0:
                    vitesse_obstacles += 1

        timer_maison += 1
        if timer_maison > 70:
            timer_maison = 0
            maisons.append([5, -50, "gauche"])
            maisons.append([LARGEUR - 50, -50, "droite"])

        for maison in maisons[:]:
            maison[1] += vitesse_obstacles
            if maison[1] > HAUTEUR:
                maisons.remove(maison)

        voiture_rect = pygame.Rect(voiture_x, voiture_y, voiture_largeur, voiture_hauteur)
        for item in obstacles:
            if voiture_rect.colliderect(item[0]):
                jeu_actif = False

    dessiner_route()

    for maison in maisons:
        dessiner_maison(maison[0], maison[1], maison[2])

    dessiner_feu()

    dessiner_voiture(voiture_x, voiture_y, BLEU)

    for item in obstacles:
        dessiner_voiture(item[0].x, item[0].y, item[1])

    texte_score = police.render(f"Score : {score}", True, NOIR)
    ecran.blit(texte_score, (ROUTE_MARGE + 10, 90))

    texte_gauche = police_petite.render("< Gauche", True, BLANC)
    texte_droite = police_petite.render("Droite >", True, BLANC)
    ecran.blit(texte_gauche, (ROUTE_MARGE + 5, HAUTEUR - 30))
    ecran.blit(texte_droite, (LARGEUR - ROUTE_MARGE - 105, HAUTEUR - 30))

    if not jeu_actif:
        texte_gameover = police.render("GAME OVER", True, ROUGE)
        ecran.blit(texte_gameover, (LARGEUR // 2 - 90, HAUTEUR // 2))

    pygame.display.flip()
    horloge.tick(60)

pygame.quit()

with open("scores.txt", "a") as f:
    f.write(f"Course : {score} points\n")
