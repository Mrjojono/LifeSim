from config import *
from cell import Cell
import random
import os 

class Grid:
    def __init__(self, width, height):
        self.grid = [[Cell(x, y) for x in range(width)] for y in range(height)]
        self.width = width
        self.height = height

    def count_neighbors(self, x, y):
        count = 0
        for nx in range(x-1, x+2):      
            for ny in range(y-1, y+2):  
                if nx < 0 or nx >= self.width or ny < 0 or ny >= self.height:
                    continue
                if nx == x and ny == y:
                    continue
                if self.grid[ny][nx].alive:
                    count += 1
        return count

    def has_neighbor_type(self, x, y, type_name):
        for nx in range(x-1, x+2):
            for ny in range(y-1, y+2):
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    if nx == x and ny == y: continue
                    if self.grid[ny][nx].type == type_name:
                        return True
        return False

    def step(self):
        new_grid = [[Cell(x, y) for x in range(self.width)] for y in range(self.height)]
        for y in range(self.height):
            for x in range(self.width):
                current_cell = self.grid[y][x]
                neighbors = self.count_neighbors(x, y)
                
                if current_cell.type == "EMPTY":
                    if neighbors == BIRTH_THRESHOLD: 
                        new_grid[y][x].set_type("HEALTHY")

                elif current_cell.type == "HEALTHY":
                    if self.has_neighbor_type(x, y, "VIRUS") and random.random() < VIRUS_INFECTION_CHANCE:
                        new_grid[y][x].set_type("VIRUS")
                    elif SURVIVE_MIN <= neighbors <= SURVIVE_MAX:
                        new_grid[y][x].set_type("HEALTHY")
                    else:
                        new_grid[y][x].set_type("EMPTY")
                elif current_cell.type == "VIRUS":
                    if self.has_neighbor_type(x, y, "HEALTHY"):
                        new_grid[y][x].set_type("VIRUS")
                    elif neighbors > VIRUS_CROWD_LIMIT:
                        new_grid[y][x].set_type("EMPTY")
                    elif random.random() < VIRUS_DIE_CHANCE:
                        new_grid[y][x].set_type("EMPTY")
                    else:
                        new_grid[y][x].set_type("VIRUS")
                elif current_cell.type == "CLEANER":
                    new_grid[y][x].set_type("CLEANER")
                    
        self.grid = new_grid

    def generate_pddl(self, agent_x, agent_y, radius=8, output_path="pddl/problem.pddl"):
    
        
        min_x, max_x = max(0, agent_x - radius), min(self.width, agent_x + radius)
        min_y, max_y = max(0, agent_y - radius), min(self.height, agent_y + radius)

        output_dir = os.path.dirname(output_path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)

        # On utilise "with" qui ferme le fichier automatiquement à la fin du bloc
        with open(output_path, "w") as f:
            f.write("(define (problem solve-virus)\n  (:domain ecosystem)\n")
            
            # OBJETS
            f.write("  (:objects ")
            for y in range(min_y, max_y):
                for x in range(min_x, max_x):
                    f.write(f"cell_{x}_{y} ")
            f.write("- cell)\n")

            # INITIALISATION
            f.write("  (:init\n")
            f.write(f"    (at cell_{agent_x}_{agent_y})\n")
            
            target_virus = None
            for y in range(min_y, max_y):
                for x in range(min_x, max_x):
                    c = f"cell_{x}_{y}"
                    if self.grid[y][x].type == "VIRUS":
                        f.write(f"    (is-virus {c})\n")
                        if target_virus is None: target_virus = c
                    else:
                        f.write(f"    (is-empty {c})\n")
                    
                    # Voisins (On simplifie pour réduire la taille du fichier)
                    if x + 1 < max_x:
                        f.write(f"    (neighbor {c} cell_{x+1}_{y}) (neighbor cell_{x+1}_{y} {c})\n")
                    if y + 1 < max_y:
                        f.write(f"    (neighbor {c} cell_{x}_{y+1}) (neighbor cell_{x}_{y+1} {c})\n")
            
            f.write("  )\n")

            # BUT
            if target_virus:
                f.write(f"  (:goal (not (is-virus {target_virus})))\n")
            else:
                f.write(f"  (:goal (at cell_{agent_x}_{agent_y}))\n")
            
            f.write(")\n")
            
            # --- FORCE L'ÉCRITURE SUR LE DISQUE ---
            f.flush()
            os.fsync(f.fileno()) 
        # Ici, le fichier est Garanti Fermé.

    def get_cell(self, x, y): return self.grid[y][x]
