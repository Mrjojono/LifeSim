import pygame
import sys
import random
import time
import os
from concurrent.futures import ThreadPoolExecutor
from config import *
from grid import Grid
from planner import solve_pddl

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PDDL_DIR = os.path.join(BASE_DIR, "pddl")

pygame.init()
grid = Grid(GRID_WIDTH, GRID_HEIGHT)

for y in range(GRID_HEIGHT):
    for x in range(GRID_WIDTH):
        if random.random() < INITIAL_HEALTHY_DENSITY:
            grid.get_cell(x, y).set_type("HEALTHY")

for _ in range(INITIAL_VIRUS_COUNT):
    vx, vy = random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1)
    grid.get_cell(vx, vy).set_type("VIRUS")

cleaner_count = max(1, int(CLEANER_COUNT))
cleaners = []
occupied_positions = set()

for cleaner_id in range(cleaner_count):
    if cleaner_id == 0:
        cx, cy = GRID_WIDTH // 2, GRID_HEIGHT // 2
    else:
        cx, cy = random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1)
        tries = 0
        while (cx, cy) in occupied_positions and tries < 100:
            cx, cy = random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1)
            tries += 1

    occupied_positions.add((cx, cy))
    grid.get_cell(cx, cy).set_type("CLEANER")
    cleaners.append({
        "id": cleaner_id,
        "pos": [cx, cy],
        "plan": [],
        "future": None,
        "pending_scope": None,
        "last_plan_time": 0.0,
        "last_global_plan_time": 0.0,
    })

screen = pygame.display.set_mode((DEFAULT_SCREEN_WIDTH, DEFAULT_SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Écosystème - Joan")
clock = pygame.time.Clock()

wait_time = PLANNER_WAIT_TIME
local_radius = PLANNER_LOCAL_RADIUS
global_wait_time = PLANNER_GLOBAL_WAIT_TIME
full_radius = max(GRID_WIDTH, GRID_HEIGHT)
domain_path = os.path.join(PDDL_DIR, "domain.pddl")
executor = ThreadPoolExecutor(max_workers=max(1, min(PLANNER_MAX_WORKERS, cleaner_count)))


def submit_plan(cleaner, radius, scope):
    problem_path = os.path.join(PDDL_DIR, f"problem_cleaner_{cleaner['id']}.pddl")
    grid.generate_pddl(cleaner["pos"][0], cleaner["pos"][1], radius=radius, output_path=problem_path)
    cleaner["future"] = executor.submit(solve_pddl, domain_path, problem_path)
    cleaner["pending_scope"] = scope


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    current_time = time.time()

    for cleaner in cleaners:
        future = cleaner["future"]
        if future and future.done():
            next_plan = future.result()

            planned_scope = cleaner["pending_scope"]
            cleaner["future"] = None
            cleaner["pending_scope"] = None

            if next_plan:
                cleaner["plan"] = next_plan
            elif planned_scope == "local" and (current_time - cleaner["last_global_plan_time"]) > global_wait_time:
                cleaner["last_global_plan_time"] = current_time
                submit_plan(cleaner, full_radius, "global")

    for cleaner in cleaners:
        if cleaner["plan"] or cleaner["future"]:
            continue
        if (current_time - cleaner["last_plan_time"]) > wait_time:
            cleaner["last_plan_time"] = current_time
            submit_plan(cleaner, local_radius, "local")

    for cleaner in cleaners:
        if not cleaner["plan"]:
            continue

        action = cleaner["plan"].pop(0)
        if action[0] == "move":
            target = action[2].split("_")
            nx, ny = int(target[1]), int(target[2])
            if grid.get_cell(nx, ny).type == "CLEANER":
                continue

            ox, oy = cleaner["pos"]
            grid.get_cell(ox, oy).set_type("EMPTY")
            cleaner["pos"] = [nx, ny]
            grid.get_cell(nx, ny).set_type("CLEANER")

        elif action[0] == "cure":
            target = action[2].split("_")
            tx, ty = int(target[1]), int(target[2])
            if grid.get_cell(tx, ty).type == "VIRUS":
                grid.get_cell(tx, ty).set_type("EMPTY")

    screen.fill(COLOR_BACKGROUND)
    win_w, win_h = screen.get_size()
    cell_w, cell_h = win_w / GRID_WIDTH, win_h / GRID_HEIGHT

    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            cell = grid.get_cell(x, y)
            rect = pygame.Rect(x * cell_w, y * cell_h, cell_w, cell_h)

            if cell.type == "HEALTHY":
                color = COLOR_ALIVE
            elif cell.type == "VIRUS":
                color = COLOR_VIRUS
            elif cell.type == "CLEANER":
                color = COLOR_CLEANER
            else:
                color = COLOR_DEAD

            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, COLOR_GRID, rect, 1)

    grid.step()

    pygame.display.flip()
    clock.tick(FPS)

executor.shutdown(wait=False, cancel_futures=True)
pygame.quit()
sys.exit()
