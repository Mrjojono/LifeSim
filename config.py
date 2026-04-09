# Taille par défaut au lancement (Taille moyenne)
DEFAULT_SCREEN_WIDTH = 1200
DEFAULT_SCREEN_HEIGHT = 800


GRID_WIDTH = 80
GRID_HEIGHT = 60

CLEANER_COUNT = 10

# Densité initiale
INITIAL_HEALTHY_DENSITY = 0.12
INITIAL_VIRUS_COUNT = 5

# Vitesse de simulation
FPS = 5

# Paramètres planner (optimisés pour fluidité)
PLANNER_LOCAL_RADIUS = 8
PLANNER_WAIT_TIME = 0.8
PLANNER_GLOBAL_WAIT_TIME = 6.0
PLANNER_MAX_WORKERS = 2




# Règles pour les cellules SAINES (Conway classique = 3 / 2-3)
BIRTH_THRESHOLD = 4      # Nombre de voisins pour naître (Augmente pour rendre la vie DUR)
SURVIVE_MIN = 2          # Voisins min pour survivre
SURVIVE_MAX = 3          # Voisins max pour survivre

# Règles pour les VIRUS
VIRUS_INFECTION_CHANCE = 0.4  # 40% de chance d'infecter un voisin sain
VIRUS_DIE_CHANCE = 0.1        # Chance de mourir naturellement (vieillesse)
VIRUS_CROWD_LIMIT = 5         # Si > 5 voisins virus, ils s'étouffent (compétition)

# Couleurs (Rappel)
COLOR_ALIVE = (0, 255, 0)      # Vert
COLOR_VIRUS = (255, 50, 50)    # Rouge
COLOR_CLEANER = (50, 150, 255) # Bleu
COLOR_DEAD = (20, 20, 30)      
COLOR_GRID = (40, 40, 50)
COLOR_BACKGROUND = (10, 10, 15)
