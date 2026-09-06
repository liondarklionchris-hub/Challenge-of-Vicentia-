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
GRIS = (100, 100, 100)
VITRE = (180, 220, 255)

horloge = pygame.time.Clock()
police = pygame.font.SysFont(None, 36)

voiture_largeur, voiture_hauteur = 50, 90
voiture_x = LARGEUR // 2 - voiture_largeur // 2
voiture_y = HAUTEUR - 120
vitesse_voiture = 8

obstacle_largeur, obstacle_hauteur = 50, 90
obstacles = []
vitesse_obstacles = 6
timer_spawn = 0

score = 0
jeu_actif = True
en_cours = True


def dessiner_voiture(x, y):
    pygame.draw.rect(ecran, BLEU, (x, y, voiture_largeur, voiture_hauteur), border_radius=10)
    pygame.draw.rect(ecran, VITRE, (x + 8, y + 10, voiture_largeur - 16, 20), border_radius=5)
    pygame.draw.rect(ecran, NOIR, (x - 4, y + 10, 8, 20))
    pygame.draw.rect(ecran, NOIR, (x + voiture_largeur - 4, y + 10, 8, 20))
    pygame.draw.rect(ecran, NOIR, (x - 4, y + voiture_hauteur - 30, 8, 20))
    pygame.draw.rect(ecran, NOIR, (x + voiture_largeur - 4, y + voiture_hauteur - 30, 8, 20))


while en_cours:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            en_cours = False

    touches = pygame.key.get_pressed()

    if jeu_actif:
        if touches[pygame.K_LEFT] and voiture_x > 0:
            voiture_x -= vitesse_voiture
        if touches[pygame.K_RIGHT] and voiture_x < LARGEUR - voiture_largeur:
            voiture_x += vitesse_voiture

        timer_spawn += 1
        if timer_spawn > 40:
            timer_spawn = 0
            x_obstacle = random.randint(0, LARGEUR - obstacle_largeur)
            obstacles.append(pygame.Rect(x_obstacle, -obstacle_hauteur, obstacle_largeur, obstacle_hauteur))

        for obs in obstacles[:]:
            obs.y += vitesse_obstacles
            if obs.y > HAUTEUR:
                obstacles.remove(obs)
                score += 1
                if score % 5 == 0:
                    vitesse_obstacles += 1

        voiture_rect = pygame.Rect(voiture_x, voiture_y, voiture_largeur, voiture_hauteur)
        for obs in obstacles:
            if voiture_rect.colliderect(obs):
                jeu_actif = False

    ecran.fill(GRIS)
    pygame.draw.line(ecran, BLANC, (LARGEUR // 2, 0), (LARGEUR // 2, HAUTEUR), 4)

    dessiner_voiture(voiture_x, voiture_y)

    for obs in obstacles:
        pygame.draw.rect(ecran, ROUGE, obs, border_radius=6)

    texte_score = police.render(f"Score : {score}", True, NOIR)
    ecran.blit(texte_score, (10, 10))

    if not jeu_actif:
        texte_gameover = police.render("GAME OVER", True, ROUGE)
        ecran.blit(texte_gameover, (LARGEUR // 2 - 90, HAUTEUR // 2))

    pygame.display.flip()
    horloge.tick(60)

pygame.quit()

with open("scores.txt", "a") as f:
    f.write(f"Course : {score} points\n")
