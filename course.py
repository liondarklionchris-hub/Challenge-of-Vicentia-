import pygame
import random
import os

pygame.init()

INVERSER_TACTILE = True

LARGEUR, HAUTEUR = 400, 600
ecran = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Road Rush - Challenge of Vicentia")

BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
ROUGE = (220, 50, 50)
VERT = (60, 140, 60)
VERT_FEU = (60, 200, 60)
ROUGE_FEU = (200, 40, 40)
JAUNE_FEU = (220, 200, 50)

horloge = pygame.time.Clock()
police = pygame.font.SysFont(None, 32)
police_petite = pygame.font.SysFont(None, 28)

DOSSIER = "assets/PNG"

voiture_largeur, voiture_hauteur = 50, 90


def charger_image(chemin, largeur, hauteur):
    img = pygame.image.load(chemin).convert_alpha()
    return pygame.transform.smoothscale(img, (largeur, hauteur))


img_joueur = charger_image(f"{DOSSIER}/Cars/car_blue_1.png", voiture_largeur, voiture_hauteur)

noms_ennemis = ["car_red_1.png", "car_black_1.png", "car_green_1.png"]
imgs_ennemis = [charger_image(f"{DOSSIER}/Cars/{nom}", voiture_largeur, voiture_hauteur) for nom in noms_ennemis]

img_route = charger_image(f"{DOSSIER}/Tiles/Asphalt road/road_asphalt01.png", 80, 80)
img_arbre = charger_image(f"{DOSSIER}/Objects/tree_large.png", 40, 55)

ROUTE_MARGE = 20

voiture_x = LARGEUR // 2 - voiture_largeur // 2
voiture_y = HAUTEUR - 120
vitesse_voiture = 8

obstacle_largeur, obstacle_hauteur = voiture_largeur, voiture_hauteur
obstacles = []
vitesse_obstacles = 6
timer_spawn = 0

arbres = []
timer_arbre = 0

score = 0
jeu_actif = True
en_cours = True

decalage_route = 0
timer_feu = 0
etat_feu = 0


def charger_meilleur_score():
    try:
        with open("meilleur_score.txt", "r") as f:
            return int(f.read())
    except:
        return 0


meilleur_score = charger_meilleur_score()


def dessiner_route():
    ecran.fill(VERT)
    pygame.draw.rect(ecran, (90, 90, 90), (ROUTE_MARGE, 0, LARGEUR - ROUTE_MARGE * 2, HAUTEUR))

    for y in range(-80, HAUTEUR, 80):
        ecran.blit(img_route, (ROUTE_MARGE, y + decalage_route))


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
            touche_gauche_ecran = pos_souris[0] < LARGEUR // 2
            if INVERSER_TACTILE:
                touche_gauche_ecran = not touche_gauche_ecran
            if touche_gauche_ecran:
                va_gauche = True
            else:
                va_droite = True

        if va_gauche and voiture_x > ROUTE_MARGE:
            voiture_x -= vitesse_voiture
        if va_droite and voiture_x < LARGEUR - ROUTE_MARGE - voiture_largeur:
            voiture_x += vitesse_voiture

        decalage_route = (decalage_route + vitesse_obstacles) % 80

        timer_feu += 1
        if timer_feu > 90:
            timer_feu = 0
            etat_feu = (etat_feu + 1) % 3

        timer_spawn += 1
        if timer_spawn > 40:
            timer_spawn = 0
            x_obstacle = random.randint(ROUTE_MARGE, LARGEUR - ROUTE_MARGE - obstacle_largeur)
            img_choisie = random.choice(imgs_ennemis)
            rect = pygame.Rect(x_obstacle, -obstacle_hauteur, obstacle_largeur, obstacle_hauteur)
            obstacles.append([rect, img_choisie])

        for item in obstacles[:]:
            item[0].y += vitesse_obstacles
            if item[0].y > HAUTEUR:
                obstacles.remove(item)
                score += 1
                if score % 5 == 0:
                    vitesse_obstacles += 1

        timer_arbre += 1
        if timer_arbre > 60:
            timer_arbre = 0
            arbres.append([2, -60])
            arbres.append([LARGEUR - 42, -60])

        for arbre in arbres[:]:
            arbre[1] += vitesse_obstacles
            if arbre[1] > HAUTEUR:
                arbres.remove(arbre)

        voiture_rect = pygame.Rect(voiture_x, voiture_y, voiture_largeur, voiture_hauteur)
        for item in obstacles:
            if voiture_rect.colliderect(item[0]):
                jeu_actif = False

    dessiner_route()

    for arbre in arbres:
        ecran.blit(img_arbre, (arbre[0], arbre[1]))

    dessiner_feu()

    ecran.blit(img_joueur, (voiture_x, voiture_y))

    for item in obstacles:
        ecran.blit(item[1], (item[0].x, item[0].y))

    texte_score = police.render(f"Score : {score}  |  Record : {max(score, meilleur_score)}", True, NOIR)
    ecran.blit(texte_score, (ROUTE_MARGE + 5, 90))

    texte_gauche = police_petite.render("< Gauche", True, BLANC)
    texte_droite = police_petite.render("Droite >", True, BLANC)
    ecran.blit(texte_gauche, (ROUTE_MARGE + 5, HAUTEUR - 30))
    ecran.blit(texte_droite, (LARGEUR - ROUTE_MARGE - 105, HAUTEUR - 30))

    if not jeu_actif:
        texte_gameover = police.render("GAME OVER", True, ROUGE)
        ecran.blit(texte_gameover, (LARGEUR // 2 - 80, HAUTEUR // 2))

    pygame.display.flip()
    horloge.tick(60)

pygame.quit()

if score > meilleur_score:
    with open("meilleur_score.txt", "w") as f:
        f.write(str(score))

with open("scores.txt", "a") as f:
    f.write(f"Course : {score} points\n")
