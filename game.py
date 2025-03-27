import pygame
import sys
import math
import random

# Initialisation de Pygame
pygame.init()

# Dimensions de la fenêtre
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("FPS Game")

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Créer une image de personnage en pixel art
player_image = pygame.Surface((50, 50))
player_image.fill(BLUE)
pygame.draw.rect(player_image, WHITE, (15, 10, 20, 30))  # Corps
pygame.draw.rect(player_image, WHITE, (20, 5, 10, 10))   # Tête

# Créer une image d'arme en pixel art
weapon_image = pygame.Surface((20, 10))
weapon_image.fill(RED)

# Créer une image de cible en pixel art
target_image = pygame.Surface((30, 30))
target_image.fill(GREEN)

# Classe Joueur
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_image
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.speed = 5

    def update(self, keys):
        if keys[pygame.K_w]:
            self.rect.y -= self.speed
        if keys[pygame.K_s]:
            self.rect.y += self.speed
        if keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_d]:
            self.rect.x += self.speed

# Classe Projectile
class Projectile(pygame.sprite.Sprite):
    def __init__(self, pos, angle):
        super().__init__()
        self.image = weapon_image
        self.rect = self.image.get_rect(center=pos)
        self.angle = angle
        self.speed = 10

    def update(self):
        self.rect.x += self.speed * math.cos(self.angle)
        self.rect.y += self.speed * math.sin(self.angle)
        if self.rect.right < 0 or self.rect.left > WIDTH or self.rect.bottom < 0 or self.rect.top > HEIGHT:
            self.kill()

# Classe Cible
class Target(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = target_image
        self.rect = self.image.get_rect(center=pos)

# Groupes de sprites
player = Player()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
projectiles = pygame.sprite.Group()
targets = pygame.sprite.Group()

# Ajouter des cibles à des positions aléatoires
for _ in range(10):
    target = Target((random.randint(50, WIDTH-50), random.randint(50, HEIGHT-50)))
    all_sprites.add(target)
    targets.add(target)

# Boucle principale
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Clic gauche
                mouse_x, mouse_y = pygame.mouse.get_pos()
                angle = math.atan2(mouse_y - player.rect.centery, mouse_x - player.rect.centerx)
                projectile = Projectile(player.rect.center, angle)
                all_sprites.add(projectile)
                projectiles.add(projectile)

    keys = pygame.key.get_pressed()
    player.update(keys)
    projectiles.update()

    # Vérifier les collisions entre projectiles et cibles
    for projectile in projectiles:
        hit_targets = pygame.sprite.spritecollide(projectile, targets, True)
        if hit_targets:
            projectile.kill()

    screen.fill(BLACK)
    all_sprites.draw(screen)
    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
sys.exit() 