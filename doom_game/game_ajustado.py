"""
MECHAARENA DOOM - First Person Shooter con Raycasting
Estilo clásico de DOOM usando Python + Pygame
Controles:
  W/S       - Mover adelante/atrás
  A/D       - Rotar izquierda/derecha
  MOUSE     - Apuntar
  CLICK IZQ - Disparar
  ESC       - Salir / Volver al Menú
"""

import pygame
import math
import sys
import random
import os

# ─────────────────────────────────────────────
#  CONSTANTES
# ─────────────────────────────────────────────
WIDTH, HEIGHT = 1024, 768
HALF_HEIGHT   = HEIGHT // 2
FPS           = 60

# Raycasting
FOV         = math.pi / 3          # 60°
HALF_FOV    = FOV / 2
NUM_RAYS    = WIDTH // 2           # un rayo por 2 px
DEPTH       = 20                   # distancia máxima de visión
DELTA_ANGLE = FOV / NUM_RAYS
SCALE       = WIDTH // NUM_RAYS    # ancho de cada franja

# Velocidades
<<<<<<< Updated upstream
# Movimiento ajustado para que la partida sea más controlable.
# Las velocidades están expresadas en unidades por segundo.
PLAYER_SPEED  = 3.40       # antes dependía de milisegundos y era inconsistente
PLAYER_ROT    = 0.0018     # sensibilidad del ratón
KEY_ROT_SPEED = 2.10       # radianes/segundo con A/D
SHOOT_COOLDOWN = 350       # ms entre disparos
=======
PLAYER_SPEED   = 3.40       
PLAYER_ROT     = 0.0018     
KEY_ROT_SPEED  = 2.10       
SHOOT_COOLDOWN = 350       
>>>>>>> Stashed changes

# Colores temáticos Doom
BLACK    = (0, 0, 0)
WHITE    = (255, 255, 255)
RED      = (200, 30, 30)
DARK_RED = (130, 0, 0)
ORANGE   = (220, 100, 0)
YELLOW   = (230, 200, 0)
GRAY     = (80, 80, 80)
DARK_GRAY= (40, 40, 40)
GREEN    = (0, 180, 0)
BLOOD    = (160, 0, 0)

# Paleta de paredes (por tipo de tile)
WALL_COLORS = {
<<<<<<< Updated upstream
    1: [(100, 60, 20), (140, 80, 30)],    # piedra marrón
    2: [(60, 60, 80), (90, 90, 120)],     # metal gris-azul
    3: [(150, 30, 30),(200, 50, 50)],     # pared roja infernal
    4: [(20, 60, 20), (30, 90, 30)],      # metal verde
=======
    1: [(110, 120, 130), (140, 150, 160)],  # Metal industrial
    2: [(20, 40, 90), (40, 70, 140)],       # Paneles azul neón
    3: [(80, 20, 120), (120, 40, 170)],     # Instalaciones púrpuras
    4: [(20, 80, 50), (40, 120, 80)],       # Servidores verdes
>>>>>>> Stashed changes
}

# ─────────────────────────────────────────────
#  BASE DE DATOS DE MAPAS
# ─────────────────────────────────────────────
MAPS_DATA = {
    "SECTOR CIBERNÉTICO": {
        "layout": [
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,2,2,0,0,0,0,0,0,3,0,0,0,0,0,0,1],
            [1,0,0,0,2,0,0,0,0,0,0,0,3,3,3,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,3,0,0,0,0,1],
            [1,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,4,4,0,1],
            [1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,4,0,0,1],
            [1,0,1,1,0,0,0,0,0,0,2,2,2,0,0,0,0,0,0,1],
            [1,0,1,0,0,0,0,0,0,0,2,0,2,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,2,0,2,0,0,0,0,3,0,1],
            [1,0,0,0,0,3,3,0,0,0,0,0,0,0,0,0,0,3,0,1],
            [1,0,0,0,0,3,0,0,0,0,0,0,0,0,4,4,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,1],
            [1,0,0,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,2,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        ],
        "spawns": [
            (3.5, 5.5),(10.5, 3.5),(15.5, 2.5),(6.5,12.5),
            (14.5,8.5),(10.5,10.5),(4.5,14.5),(17.5,6.5),
            (8.5,16.5),(12.5,15.5),(3.5,10.5),(18.5,12.5)
        ]
    },
    "LABERINTO DE NEÓN": {
        "layout": [
            [3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3],
            [3,0,0,0,3,0,0,0,0,0,0,0,0,0,3,0,0,0,0,3],
            [3,0,3,0,3,0,3,3,3,3,3,3,3,0,3,0,3,3,0,3],
            [3,0,3,0,0,0,3,0,0,0,0,0,3,0,3,0,0,3,0,3],
            [3,0,3,3,3,0,3,0,3,3,3,0,3,0,3,3,0,3,0,3],
            [3,0,0,0,3,0,0,0,3,0,0,0,3,0,0,0,0,3,0,3],
            [3,3,3,0,3,3,3,0,3,0,3,3,3,3,3,3,0,3,0,3],
            [3,0,0,0,0,0,3,0,3,0,0,0,0,0,0,3,0,3,0,3],
            [3,0,3,3,3,0,3,0,3,3,3,3,3,3,0,3,0,3,0,3],
            [3,0,3,0,0,0,0,0,0,0,0,0,0,3,0,3,0,0,0,3],
            [3,0,3,0,3,3,3,3,3,3,3,3,0,3,0,3,3,3,0,3],
            [3,0,3,0,3,0,0,0,0,0,0,3,0,3,0,0,0,3,0,3],
            [3,0,3,0,3,0,3,3,3,3,0,3,0,3,3,3,0,3,0,3],
            [3,0,0,0,3,0,3,0,0,3,0,3,0,0,0,3,0,3,0,3],
            [3,3,3,0,3,0,3,0,0,3,0,3,3,3,0,3,0,3,0,3],
            [3,0,0,0,3,0,0,0,0,3,0,0,0,3,0,3,0,0,0,3],
            [3,0,3,3,3,3,3,3,0,3,3,3,0,3,0,3,3,3,0,3],
            [3,0,0,0,0,0,0,3,0,0,0,3,0,0,0,0,0,3,0,3],
            [3,0,3,3,3,3,0,0,0,3,0,0,0,3,3,3,0,0,0,3],
            [3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3],
        ],
        "spawns": [
            (1.5, 5.5),(5.5, 1.5),(11.5, 3.5),(18.5, 1.5),
            (7.5, 7.5),(13.5, 7.5),(1.5, 13.5),(9.5, 13.5),
            (18.5, 9.5),(14.5, 15.5),(6.5, 17.5),(18.5, 17.5)
        ]
    },
    "NÚCLEO CENTRAL": {
        "layout": [
            [4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4],
            [4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4],
            [4,0,4,4,0,0,0,0,0,0,0,0,0,0,0,0,4,4,0,4],
            [4,0,4,4,0,0,0,0,0,0,0,0,0,0,0,0,4,4,0,4],
            [4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4],
            [4,0,0,0,0,2,2,2,2,2,2,2,2,2,2,0,0,0,0,4],
            [4,0,0,0,0,2,0,0,0,0,0,0,0,0,2,0,0,0,0,4],
            [4,0,0,0,0,2,0,0,0,0,0,0,0,0,2,0,0,0,0,4],
            [4,0,0,0,0,2,0,0,0,0,0,0,0,0,2,0,0,0,0,4],
            [4,0,0,0,0,2,0,0,0,0,0,0,0,0,2,0,0,0,0,4],
            [4,0,0,0,0,2,0,0,0,0,0,0,0,0,2,0,0,0,0,4],
            [4,0,0,0,0,2,0,0,0,0,0,0,0,0,2,0,0,0,0,4],
            [4,0,0,0,0,2,0,0,0,0,0,0,0,0,2,0,0,0,0,4],
            [4,0,0,0,0,2,2,2,2,2,2,2,2,2,2,0,0,0,0,4],
            [4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4],
            [4,0,4,4,0,0,0,0,0,0,0,0,0,0,0,0,4,4,0,4],
            [4,0,4,4,0,0,0,0,0,0,0,0,0,0,0,0,4,4,0,4],
            [4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4],
            [4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4],
            [4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4],
        ],
        "spawns": [
            (9.5, 7.5),(10.5, 7.5),(9.5, 11.5),(10.5, 11.5),
            (2.5, 2.5),(17.5, 2.5),(2.5, 17.5),(17.5, 17.5),
            (2.5, 9.5),(17.5, 9.5),(9.5, 2.5),(10.5, 17.5)
        ]
    }
}

CURRENT_MAP_NAME = "SECTOR CIBERNÉTICO"
CURRENT_MAP = MAPS_DATA[CURRENT_MAP_NAME]["layout"]
MAP_W = len(CURRENT_MAP[0])
MAP_H = len(CURRENT_MAP)

def set_active_map(map_name):
    global CURRENT_MAP_NAME, CURRENT_MAP, MAP_W, MAP_H
    CURRENT_MAP_NAME = map_name
    CURRENT_MAP = MAPS_DATA[map_name]["layout"]
    MAP_W = len(CURRENT_MAP[0])
    MAP_H = len(CURRENT_MAP)

def wall_at(x, y):
    xi, yi = int(x), int(y)
    if 0 <= xi < MAP_W and 0 <= yi < MAP_H:
        return CURRENT_MAP[yi][xi]
    return 1

# ─────────────────────────────────────────────
#  JUGADOR
# ─────────────────────────────────────────────
class Player:
    def __init__(self):
        self.x      = 1.5
        self.y      = 1.5
        self.angle  = 0.0
        self.health = 100
        self.ammo   = 50
        self.score  = 0
        self.shoot_cooldown = 0
        self.pain_flash     = 0   # frames de flash rojo al recibir daño

    def move(self, keys, dt):
        dx = dy = 0
        dt_sec = dt / 1000.0
        speed = PLAYER_SPEED * dt_sec

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            dx += math.cos(self.angle) * speed
            dy += math.sin(self.angle) * speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dx -= math.cos(self.angle) * speed
            dy -= math.sin(self.angle) * speed

        nx, ny = self.x + dx, self.y + dy
        if wall_at(nx, self.y) == 0: self.x = nx
        if wall_at(self.x, ny) == 0: self.y = ny

        if keys[pygame.K_a]: self.angle -= KEY_ROT_SPEED * dt_sec
        if keys[pygame.K_d]: self.angle += KEY_ROT_SPEED * dt_sec

        if self.shoot_cooldown > 0: self.shoot_cooldown -= dt
        if self.pain_flash > 0:     self.pain_flash -= dt

    def rotate_mouse(self, dx):
        self.angle += dx * PLAYER_ROT

    def shoot(self, enemies):
        if self.shoot_cooldown > 0 or self.ammo <= 0:
            return False
        self.ammo -= 1
        self.shoot_cooldown = SHOOT_COOLDOWN
        # detectar impacto en el rayo central
        for e in enemies:
            if e.alive and self._can_hit(e):
                e.take_damage(25)
                self.score += 10
                return True
        return True

    def _can_hit(self, enemy):
        dx = enemy.x - self.x
        dy = enemy.y - self.y
        dist = math.hypot(dx, dy)
        if dist > 12: return False
        angle_to = math.atan2(dy, dx)
        diff = (angle_to - self.angle + math.pi) % (2*math.pi) - math.pi
        return abs(diff) < 0.18

    def take_damage(self, dmg):
        self.health = max(0, self.health - dmg)
        self.pain_flash = 20

# ─────────────────────────────────────────────
#  ENEMIGO (Demonio)
# ─────────────────────────────────────────────
class Enemy:
    def __init__(self, x, y):
        self.x       = x
        self.y       = y
        self.alive   = True
        self.health  = 60
        self.speed   = 1.25   # unidades/segundo; da más tiempo para reaccionar
        self.attack_cd = 0
        self.anim_t    = random.random() * 6.28   # fase de animación

    def take_damage(self, dmg):
        self.health -= dmg
        if self.health <= 0:
            self.alive = False

    def update(self, player, dt):
        if not self.alive: return
        dt_sec = dt / 1000.0
        self.anim_t += 3.0 * dt_sec
        dx = player.x - self.x
        dy = player.y - self.y
        dist = math.hypot(dx, dy)

        # movimiento hacia el jugador
        if dist > 0.6:
            nx = self.x + (dx/dist) * self.speed * dt_sec
            ny = self.y + (dy/dist) * self.speed * dt_sec
            if wall_at(nx, self.y) == 0: self.x = nx
            if wall_at(self.x, ny) == 0: self.y = ny

        # ataque cuerpo a cuerpo
        if dist < 0.9:
            self.attack_cd -= dt
            if self.attack_cd <= 0:
                player.take_damage(8)
                self.attack_cd = 900  # ms entre ataques enemigos

    def screen_pos(self, player, proj_dist):
        dx = self.x - player.x
        dy = self.y - player.y
        dist = math.hypot(dx, dy)
        if dist < 0.1: return None, None, None

        angle = math.atan2(dy, dx) - player.angle
        angle = (angle + math.pi) % (2*math.pi) - math.pi

        if abs(angle) > HALF_FOV + 0.2:
            return None, None, None

        sx = int((angle + HALF_FOV) / FOV * WIDTH)
        h  = int(proj_dist / (dist + 0.001) * 0.9)
        return sx, h, dist

# ─────────────────────────────────────────────
#  RAYCASTER
# ─────────────────────────────────────────────
def cast_rays(surface, player):
    z_buffer = [float('inf')] * WIDTH
    proj_dist = (WIDTH // 2) / math.tan(HALF_FOV)

    for ray in range(NUM_RAYS):
        ray_angle = player.angle - HALF_FOV + ray * DELTA_ANGLE
        sin_a = math.sin(ray_angle)
        cos_a = math.cos(ray_angle)

        # DDA
        for depth in range(1, int(DEPTH * 20)):
            t = depth * 0.05
            tx = player.x + cos_a * t
            ty = player.y + sin_a * t
            tile = wall_at(tx, ty)
            if tile:
                # corrección de ojo de pez
                dist = t * math.cos(ray_angle - player.angle)
                proj_height = int(proj_dist / (dist + 0.001))

                # color de pared con gradiente de distancia
                colors = WALL_COLORS.get(tile, [(100,100,100),(150,150,150)])
                # alternar color claro/oscuro según si golpea cara N/S o E/W
                frac_x = tx - int(tx)
                frac_y = ty - int(ty)
                use_dark = (abs(frac_y) > abs(frac_x)) if abs(sin_a) > abs(cos_a) else False
                base_col = colors[1] if use_dark else colors[0]

                shade = max(0.15, 1.0 - dist / DEPTH)
                col   = tuple(int(c * shade) for c in base_col)

                x_screen = ray * SCALE
                wall_top    = HALF_HEIGHT - proj_height // 2
                wall_bottom = HALF_HEIGHT + proj_height // 2

                pygame.draw.rect(surface, col,
                                 (x_screen, wall_top, SCALE, wall_bottom - wall_top))

                # guardar z_buffer
                for i in range(SCALE):
                    if x_screen + i < WIDTH:
                        z_buffer[x_screen + i] = dist
                break

    return z_buffer, proj_dist

# ─────────────────────────────────────────────
#  DIBUJAR CIELO E SUELO
# ─────────────────────────────────────────────
def draw_background(surface):
<<<<<<< Updated upstream
    # cielo degradado infernal (negro → rojo oscuro)
=======
>>>>>>> Stashed changes
    for y in range(HALF_HEIGHT):
        t = y / HALF_HEIGHT
        r = int(10 + 80 * t)
        g = int(t * 5)
        b = 0
        pygame.draw.line(surface, (r, g, b), (0, y), (WIDTH, y))
<<<<<<< Updated upstream
    # suelo degradado oscuro
=======
    
>>>>>>> Stashed changes
    for y in range(HALF_HEIGHT, HEIGHT):
        t = (y - HALF_HEIGHT) / HALF_HEIGHT
        shade = int(25 + 15 * t)
        pygame.draw.line(surface, (shade, shade//2, shade//3),
                         (0, y), (WIDTH, y))

# ─────────────────────────────────────────────
#  SPRITES ENEMIGOS
# ─────────────────────────────────────────────
def draw_enemies(surface, enemies, player, z_buffer, proj_dist):
    # ordenar por distancia (más lejos primero)
    sorted_e = sorted(
        [e for e in enemies if e.alive],
        key=lambda e: -math.hypot(e.x - player.x, e.y - player.y)
    )

    for e in sorted_e:
        sx, sh, dist = e.screen_pos(player, proj_dist)
        if sx is None: continue

        sprite_w = max(4, sh)
        sprite_h = max(4, sh)
        left = sx - sprite_w // 2
        top  = HALF_HEIGHT - sprite_h // 2

<<<<<<< Updated upstream
        # animación: oscilación vertical
        bob = int(math.sin(e.anim_t * 3) * 4)
=======
        bob = int(math.sin(e.anim_t * 4) * 5)
>>>>>>> Stashed changes
        top += bob

        # dibujar sprite demonio (rectángulos de colores)
        if dist < z_buffer[max(0, min(sx, WIDTH-1))]:
            draw_demon_sprite(surface, left, top, sprite_w, sprite_h, e, dist)

<<<<<<< Updated upstream
def draw_demon_sprite(surface, x, y, w, h, enemy, dist):
    """Dibuja un demonio estilizado con primitivas."""
    shade = max(0.2, 1.0 - dist / DEPTH)
    def sc(r, g, b): return (int(r*shade), int(g*shade), int(b*shade))

    # cuerpo rojo
    body_rect = pygame.Rect(x + w//4, y + h//3, w//2, h//2)
    pygame.draw.rect(surface, sc(180, 30, 30), body_rect)

    # cabeza
    head_r = w // 3
    hx = x + w // 2
    hy = y + h // 4
    pygame.draw.circle(surface, sc(200, 60, 40), (hx, hy), head_r)

    # cuernos
    pygame.draw.polygon(surface, sc(220, 180, 50), [
        (hx - head_r, hy), (hx - head_r//2, hy - head_r),
        (hx - head_r*2//3, hy - head_r//2)
    ])
    pygame.draw.polygon(surface, sc(220, 180, 50), [
        (hx + head_r, hy), (hx + head_r//2, hy - head_r),
        (hx + head_r*2//3, hy - head_r//2)
    ])

    # ojos rojos brillantes
    eye_r = max(1, head_r // 4)
    pygame.draw.circle(surface, (255, 50, 50), (hx - head_r//3, hy - 2), eye_r)
    pygame.draw.circle(surface, (255, 50, 50), (hx + head_r//3, hy - 2), eye_r)

    # barra de salud
=======
def draw_mecha_sprite(surface, x, y, w, h, enemy, dist):
    shade = max(0.2, 1.0 - dist / DEPTH)
    def sc(r, g, b): return (int(r*shade), int(g*shade), int(b*shade))

    body_w = w // 2
    body_h = h // 2
    bx = x + w // 4
    by = y + h // 3
    pygame.draw.rect(surface, sc(120, 130, 140), (bx, by, body_w, body_h))
    pygame.draw.rect(surface, sc(60, 70, 80), (bx, by, body_w, body_h), max(1, w//30))

    shoulder_w = w // 5
    shoulder_h = h // 5
    pygame.draw.rect(surface, sc(160, 170, 180), (bx - shoulder_w//1.5, by, shoulder_w, shoulder_h))
    pygame.draw.rect(surface, sc(160, 170, 180), (bx + body_w - shoulder_w//3, by, shoulder_w, shoulder_h))

    head_w = int(w / 2.5)
    head_h = int(h / 3.5)
    hx = x + w // 2 - head_w // 2
    hy = y + h // 6
    pygame.draw.rect(surface, sc(50, 50, 60), (hx, hy, head_w, head_h))

    visor_w = head_w - max(4, w//15)
    visor_h = max(2, head_h // 3)
    vx = hx + (head_w - visor_w) // 2
    vy = hy + head_h // 4
    pygame.draw.rect(surface, CYAN, (vx, vy, visor_w, visor_h))

    pygame.draw.line(surface, sc(200, 200, 200), (hx + head_w//2, hy), (hx + head_w//2, hy - head_h//2), 2)
    pygame.draw.circle(surface, LASER_RED, (hx + head_w//2, hy - head_h//2), max(2, w//20))

>>>>>>> Stashed changes
    bar_w = w
    bar_h = 4
    bx, by = x, y - 8
    pygame.draw.rect(surface, (80, 0, 0), (bx, by, bar_w, bar_h))
    hp_ratio = enemy.health / 60
    pygame.draw.rect(surface, (220, 30, 30), (bx, by, int(bar_w * hp_ratio), bar_h))

# ─────────────────────────────────────────────
#  HUD
# ─────────────────────────────────────────────
def draw_hud(surface, player, font_big, font_small, shoot_flash, kill_msg):
    # barra inferior
    hud_h = 90
    hud_surf = pygame.Surface((WIDTH, hud_h), pygame.SRCALPHA)
<<<<<<< Updated upstream
    hud_surf.fill((0, 0, 0, 180))
    surface.blit(hud_surf, (0, HEIGHT - hud_h))

    # ── SALUD ──
    pygame.draw.rect(surface, (100,0,0), (20, HEIGHT-70, 200, 24))
=======
    hud_surf.fill((0, 15, 30, 180))
    surface.blit(hud_surf, (0, HEIGHT - hud_h))

    pygame.draw.rect(surface, (0,50,0), (20, HEIGHT-70, 200, 24))
>>>>>>> Stashed changes
    hp_w = int(200 * max(0, player.health) / 100)
    hp_col = (0,200,0) if player.health > 50 else (220,180,0) if player.health > 25 else (220,30,30)
    pygame.draw.rect(surface, hp_col, (20, HEIGHT-70, hp_w, 24))
    pygame.draw.rect(surface, WHITE,  (20, HEIGHT-70, 200, 24), 2)
    hp_txt = font_small.render(f"♥ {player.health}", True, WHITE)
    surface.blit(hp_txt, (28, HEIGHT-68))

<<<<<<< Updated upstream
    # ── MUNICIÓN ──
    ammo_txt = font_big.render(f"⚡{player.ammo}", True, YELLOW)
    surface.blit(ammo_txt, (WIDTH//2 - 40, HEIGHT-72))

    # ── SCORE ──
    score_txt = font_small.render(f"KILLS: {player.score//10}", True, WHITE)
    surface.blit(score_txt, (WIDTH - 160, HEIGHT-70))

    # ── PISTOLA ──
    draw_gun(surface, shoot_flash)

    # ── MIRA ──
=======
    ammo_txt = font_big.render(f"⚡{player.ammo}", True, CYAN)
    surface.blit(ammo_txt, (WIDTH//2 - 40, HEIGHT-72))

    score_txt = font_small.render(f"MECHAS: {player.score//10}", True, CYAN)
    surface.blit(score_txt, (WIDTH - 160, HEIGHT-70))

    map_info = font_small.render(f"MAPA: {CURRENT_MAP_NAME}", True, BLUE_NEON)
    surface.blit(map_info, (20, HEIGHT-30))

    draw_gun(surface, shoot_flash)

>>>>>>> Stashed changes
    cx, cy = WIDTH // 2, HEIGHT // 2
    pygame.draw.line(surface, WHITE, (cx-12, cy), (cx+12, cy), 2)
    pygame.draw.line(surface, WHITE, (cx, cy-12), (cx, cy+12), 2)
    pygame.draw.circle(surface, WHITE, (cx, cy), 5, 1)

<<<<<<< Updated upstream
    # ── FLASH DE DOLOR ──
=======
>>>>>>> Stashed changes
    if player.pain_flash > 0:
        alpha = int(min(180, player.pain_flash * 9))
        pain_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        pain_surf.fill((200, 0, 0, alpha))
        surface.blit(pain_surf, (0, 0))

    if kill_msg > 0:
        msg = font_big.render("DEMON SLAIN!", True, YELLOW)
        surface.blit(msg, (WIDTH//2 - msg.get_width()//2, HEIGHT//2 - 80))

def draw_gun(surface, shoot_flash):
    """Dibuja la pistola en la parte inferior central."""
    gx = WIDTH // 2
    gy = HEIGHT - 10
    kick = -20 if shoot_flash > 0 else 0

<<<<<<< Updated upstream
    # caño
    pygame.draw.rect(surface, (60,60,60), (gx-8, gy-80+kick, 16, 60))
    # cuerpo
    pygame.draw.rect(surface, (50,50,50), (gx-20, gy-50+kick, 40, 45))
    # agarre
    pygame.draw.polygon(surface, (40,40,40), [
        (gx-10, gy-10+kick), (gx+10, gy-10+kick),
        (gx+15, gy+kick),    (gx-5,  gy+kick)
    ])
    # muzzle flash
=======
    pygame.draw.rect(surface, (80,80,90), (gx-10, gy-80+kick, 20, 60))
    pygame.draw.rect(surface, CYAN, (gx-4, gy-75+kick, 8, 40))
    pygame.draw.rect(surface, (40,40,50), (gx-25, gy-50+kick, 50, 45))
    pygame.draw.polygon(surface, (20,20,30), [
        (gx-15, gy-10+kick), (gx+15, gy-10+kick),
        (gx+20, gy+kick),    (gx-10, gy+kick)
    ])
    
>>>>>>> Stashed changes
    if shoot_flash > 0:
        for _ in range(8):
            angle = random.uniform(0, 2*math.pi)
            r = random.randint(5, 20)
            fx = gx + int(math.cos(angle) * r)
            fy = gy - 85 + kick + int(math.sin(angle) * r // 2)
            pygame.draw.circle(surface, YELLOW, (fx, fy), random.randint(3,8))
        pygame.draw.circle(surface, WHITE, (gx, gy-85+kick), 6)

# ─────────────────────────────────────────────
#  PANTALLAS DEL JUEGO
# ─────────────────────────────────────────────
def draw_title_screen(surface, font_title, font_big, font_small):
<<<<<<< Updated upstream
    surface.fill((10,0,0))
    # efecto de fondo
=======
    surface.fill((5, 10, 20))
>>>>>>> Stashed changes
    for i in range(0, WIDTH, 40):
        for j in range(0, HEIGHT, 40):
            if random.random() < 0.02:
                pygame.draw.rect(surface,(40,0,0),(i,j,40,40))

<<<<<<< Updated upstream
    title = font_title.render("MECHAARENA", True, RED)
    sub   = font_title.render("INFERNO",     True, ORANGE)
    start = font_big.render("[ENTER] COMENZAR", True, YELLOW)
    info  = font_small.render("WASD=Mover  RATON=Apuntar  CLICK=Disparar  ESC=Salir", True, GRAY)

    surface.blit(title, (WIDTH//2 - title.get_width()//2, 160))
    surface.blit(sub,   (WIDTH//2 - sub.get_width()//2,   240))
    # línea roja decorativa
    pygame.draw.line(surface, RED, (WIDTH//4, 310), (3*WIDTH//4, 310), 3)
    surface.blit(start, (WIDTH//2 - start.get_width()//2, 370))
    surface.blit(info,  (WIDTH//2 - info.get_width()//2,  460))
=======
    title = font_title.render("MECHAARENA", True, WHITE)
    sub   = font_title.render("CYBERPUNK",     True, CYAN)
    map_t = font_small.render(f"MAPA ACTIVO: {CURRENT_MAP_NAME}", True, BLUE_NEON)
    start = font_big.render("[ENTER] INICIAR SISTEMA", True, GREEN)
    info  = font_small.render("WASD=Mover  RATON=Apuntar  CLICK=Disparar  ESC=Salir", True, GRAY)

    surface.blit(title, (WIDTH//2 - title.get_width()//2, 140))
    surface.blit(sub,   (WIDTH//2 - sub.get_width()//2,   220))
    surface.blit(map_t, (WIDTH//2 - map_t.get_width()//2, 290))
    pygame.draw.line(surface, BLUE_NEON, (WIDTH//4, 330), (3*WIDTH//4, 330), 4)
    surface.blit(start, (WIDTH//2 - start.get_width()//2, 380))
    surface.blit(info,  (WIDTH//2 - info.get_width()//2,  480))
>>>>>>> Stashed changes

def draw_game_over(surface, font_title, font_big, player):
    surface.fill((5,0,0))
    over  = font_title.render("GAME OVER",        True, RED)
    score = font_big.render(f"Demonios eliminados: {player.score//10}", True, YELLOW)
    retry = font_big.render("[R] Reintentar  [ESC] Salir", True, GRAY)
    surface.blit(over,  (WIDTH//2 - over.get_width()//2, 250))
    surface.blit(score, (WIDTH//2 - score.get_width()//2, 360))
    surface.blit(retry, (WIDTH//2 - retry.get_width()//2, 450))

def draw_win(surface, font_title, font_big, player):
    surface.fill((0,5,0))
    win   = font_title.render("VICTORIA!",        True, YELLOW)
    score = font_big.render(f"Demonios eliminados: {player.score//10}", True, GREEN)
    retry = font_big.render("[R] Jugar otra vez  [ESC] Salir", True, GRAY)
    surface.blit(win,   (WIDTH//2 - win.get_width()//2, 250))
    surface.blit(score, (WIDTH//2 - score.get_width()//2, 360))
    surface.blit(retry, (WIDTH//2 - retry.get_width()//2, 450))

# ─────────────────────────────────────────────
#  INTERFAZ DE MENÚ CIBERPUNK
# ─────────────────────────────────────────────
def draw_cyber_cursor(surface, x, y):
    pygame.draw.circle(surface, CYAN, (x, y), 8, 2)
    pygame.draw.circle(surface, LASER_RED, (x, y), 3)
    pygame.draw.line(surface, BLUE_NEON, (x - 14, y), (x - 6, y), 2)
    pygame.draw.line(surface, BLUE_NEON, (x + 6, y), (x + 14, y), 2)
    pygame.draw.line(surface, BLUE_NEON, (x, y - 14), (x, y - 6), 2)
    pygame.draw.line(surface, BLUE_NEON, (x, y + 6), (x, y + 14), 2)

def draw_cyber_menu(surface, menu_items, selected_idx, font_title, font_menu, font_small, subscreen="MAIN", map_selected_idx=0, diff_selected=1, confirm_quit=False):
    for y in range(HEIGHT):
        ratio = y / HEIGHT
        r = int(2 + 8 * ratio)
        g = int(5 + 20 * ratio)
        b = int(15 + 45 * ratio)
        pygame.draw.line(surface, (r, g, b), (0, y), (WIDTH, y))

    for i in range(0, WIDTH, 50):
        pygame.draw.line(surface, (0, 35, 75), (i, 0), (i, HEIGHT), 1)
    for j in range(0, HEIGHT, 50):
        pygame.draw.line(surface, (0, 35, 75), (0, j), (WIDTH, j), 1)

    t1 = font_title.render("MECHAARENA", True, BLUE_NEON)
    t1_glow = font_title.render("MECHAARENA", True, CYAN)
    t2 = font_title.render("CYBERPUNK ENGINE", True, WHITE)
    
    surface.blit(t1, (WIDTH//2 - t1.get_width()//2 + 3, 63))
    surface.blit(t1_glow, (WIDTH//2 - t1_glow.get_width()//2, 60))
    surface.blit(t2, (WIDTH//2 - t2.get_width()//2, 130))

    pygame.draw.rect(surface, BLUE_NEON, (WIDTH//2 - 300, 200, 600, 4), border_radius=2)
    pygame.draw.rect(surface, CYAN, (WIDTH//2 - 300, 201, 600, 2), border_radius=1)

    if subscreen == "MAIN":
        start_y = 240
        spacing = 50
        for idx, item in enumerate(menu_items):
            ey = start_y + idx * spacing
            is_sel = (idx == selected_idx)
            color = CYAN if is_sel else (120, 160, 200)
            
            txt = font_menu.render(item, True, color)
            tx = WIDTH//2 - txt.get_width()//2
            
            if is_sel:
                sel_bg = pygame.Surface((440, 38), pygame.SRCALPHA)
                sel_bg.fill((0, 150, 255, 40))
                surface.blit(sel_bg, (WIDTH//2 - 220, ey - 3))
                pygame.draw.rect(surface, CYAN, (WIDTH//2 - 220, ey - 3, 440, 38), 1)

                draw_cyber_cursor(surface, tx - 30, ey + 16)
                draw_cyber_cursor(surface, tx + txt.get_width() + 30, ey + 16)

            surface.blit(txt, (tx, ey))

    elif subscreen == "SELECT_MAP":
        st_txt = font_menu.render("SELECCIONAR SECTOR DE COMBATE", True, CYAN)
        surface.blit(st_txt, (WIDTH//2 - st_txt.get_width()//2, 230))
        
        map_list = list(MAPS_DATA.keys())
        for idx, m_name in enumerate(map_list):
            ey = 295 + idx * 55
            is_sel = (idx == map_selected_idx)
            is_active = (m_name == CURRENT_MAP_NAME)
            
            col = CYAN if is_sel else (150, 150, 160)
            prefix = "[ACTIVO] " if is_active else "         "
            txt = font_small.render(f"{prefix}{idx+1}. {m_name}", True, col)
            tx = WIDTH//2 - txt.get_width()//2
            
            if is_sel:
                sel_bg = pygame.Surface((460, 40), pygame.SRCALPHA)
                sel_bg.fill((0, 255, 255, 30))
                surface.blit(sel_bg, (WIDTH//2 - 230, ey - 5))
                pygame.draw.rect(surface, CYAN, (WIDTH//2 - 230, ey - 5, 460, 40), 1)
                draw_cyber_cursor(surface, tx - 25, ey + 10)

            surface.blit(txt, (tx, ey))

        hint = font_small.render("[ENTER] Cargar Mapa   [ESC] Volver", True, WHITE)
        surface.blit(hint, (WIDTH//2 - hint.get_width()//2, 530))

    elif subscreen == "DIFFICULTY":
        st_txt = font_menu.render("SELECCIONAR NIVEL DE AMENAZA", True, CYAN)
        surface.blit(st_txt, (WIDTH//2 - st_txt.get_width()//2, 230))
        
        diffs = [
            "1. RECLUTA (FACIL)",
            "2. CYBER SOLDADO (NORMAL)",
            "3. MECHA HUNTER (DIFICIL)",
            "4. PROTOCOLO OVERLORD (EXTREMO)"
        ]
        for idx, d_text in enumerate(diffs):
            ey = 300 + idx * 45
            is_sel = (idx == diff_selected)
            col = CYAN if is_sel else GRAY
            txt = font_small.render(d_text, True, col)
            tx = WIDTH//2 - txt.get_width()//2
            surface.blit(txt, (tx, ey))
            if is_sel:
                draw_cyber_cursor(surface, tx - 25, ey + 10)

        hint = font_small.render("[ENTER] Confirmar   [ESC] Volver", True, WHITE)
        surface.blit(hint, (WIDTH//2 - hint.get_width()//2, 530))

    elif subscreen == "OPTIONS":
        st_txt = font_menu.render("CONFIGURACION DE NUCLEO", True, CYAN)
        surface.blit(st_txt, (WIDTH//2 - st_txt.get_width()//2, 230))
        
        opts = [
            "AUDIO: INTERFAZ SINTETIZADA [OK]",
            "RESOLUCION: 1024x768 CIBERPUNK 60FPS",
            "MIRA NEON: SENSIBILIDAD DINAMICA",
            "MOTOR: RAYCASTING PROJECTION v2.6"
        ]
        for idx, o_text in enumerate(opts):
            ey = 300 + idx * 40
            txt = font_small.render(o_text, True, WHITE)
            surface.blit(txt, (WIDTH//2 - txt.get_width()//2, ey))

        hint = font_small.render("[ESC] Volver al Menú", True, BLUE_NEON)
        surface.blit(hint, (WIDTH//2 - hint.get_width()//2, 520))

    elif subscreen == "CREDITS":
        st_txt = font_menu.render("ARCHIVOS DE SISTEMA", True, GREEN)
        surface.blit(st_txt, (WIDTH//2 - st_txt.get_width()//2, 230))
        
        creds = [
            "MECHAARENA: CYBERPUNK FPS ENGINE",
            "Desarrollado en Python + Pygame",
            "Renderizado 3D Estilo Retro Raycasting",
            "Interfaz Ciberpunk Azul y Cian 2026"
        ]
        for idx, c_text in enumerate(creds):
            ey = 300 + idx * 40
            txt = font_small.render(c_text, True, CYAN if idx == 0 else WHITE)
            surface.blit(txt, (WIDTH//2 - txt.get_width()//2, ey))

        hint = font_small.render("[ESC] Volver al Menú", True, BLUE_NEON)
        surface.blit(hint, (WIDTH//2 - hint.get_width()//2, 520))

    if confirm_quit:
        pop_w, pop_h = 520, 160
        px, py = WIDTH//2 - pop_w//2, HEIGHT//2 - pop_h//2
        pop_surf = pygame.Surface((pop_w, pop_h), pygame.SRCALPHA)
        pop_surf.fill((5, 20, 40, 230))
        surface.blit(pop_surf, (px, py))
        pygame.draw.rect(surface, CYAN, (px, py, pop_w, pop_h), 2)
        
        q1 = font_small.render("¿DESCONECTAR SISTEMA Y SALIR?", True, WHITE)
        q2 = font_small.render("PRESIONA [S] PARA CONFIRMAR  O  [N] CANCELAR", True, CYAN)
        surface.blit(q1, (WIDTH//2 - q1.get_width()//2, py + 40))
        surface.blit(q2, (WIDTH//2 - q2.get_width()//2, py + 90))

    footer = font_small.render("TECLAS [W/S] NAVEGAR   [ENTER] SELECCIONAR   [ESC] ATRAS", True, (80, 120, 160))
    surface.blit(footer, (WIDTH//2 - footer.get_width()//2, HEIGHT - 35))

# ─────────────────────────────────────────────
#  MINIMAP
# ─────────────────────────────────────────────
def draw_minimap(surface, player, enemies):
    cell = 8
    ox, oy = 10, 10
    for row in range(MAP_H):
        for col in range(MAP_W):
            v = CURRENT_MAP[row][col]
            col_map = DARK_GRAY if v == 0 else WALL_COLORS.get(v, [[GRAY]])[0]
            pygame.draw.rect(surface, col_map, (ox + col*cell, oy + row*cell, cell-1, cell-1))
    # jugador
    px = int(ox + player.x * cell)
    py = int(oy + player.y * cell)
    pygame.draw.circle(surface, GREEN, (px, py), 3)
    ex = px + int(math.cos(player.angle) * 8)
    ey = py + int(math.sin(player.angle) * 8)
    pygame.draw.line(surface, YELLOW, (px,py), (ex,ey), 2)
    # enemigos
    for e in enemies:
        if e.alive:
            ex2 = int(ox + e.x * cell)
            ey2 = int(oy + e.y * cell)
            pygame.draw.circle(surface, RED, (ex2, ey2), 2)

# ─────────────────────────────────────────────
#  SPAWN DE ENEMIGOS SEGÚN EL MAPA
# ─────────────────────────────────────────────
def make_enemies():
    spawns = MAPS_DATA[CURRENT_MAP_NAME]["spawns"]
    return [Enemy(x, y) for x, y in spawns]

# ─────────────────────────────────────────────
#  MAIN LOOP
# ─────────────────────────────────────────────
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
<<<<<<< Updated upstream
    pygame.display.set_caption("MechaArena Inferno")
=======
    pygame.display.set_caption("MechaArena Cyberpunk Engine")
>>>>>>> Stashed changes
    clock  = pygame.time.Clock()

    # Fuentes
    try:
        font_title = pygame.font.SysFont("impact", 75)
        font_menu  = pygame.font.SysFont("impact", 36)
        font_big   = pygame.font.SysFont("impact", 36)
        font_small = pygame.font.SysFont("consolas", 20)
    except Exception:
        font_title = pygame.font.Font(None, 75)
        font_menu  = pygame.font.Font(None, 36)
        font_big   = pygame.font.Font(None, 36)
        font_small = pygame.font.Font(None, 20)

<<<<<<< Updated upstream
    # Estado del juego
    STATE_TITLE  = 0
    STATE_PLAY   = 1
    STATE_OVER   = 2
    STATE_WIN    = 3
    state = STATE_TITLE
=======
    STATE_MENU   = 0
    STATE_TITLE  = 1
    STATE_PLAY   = 2
    STATE_OVER   = 3
    STATE_WIN    = 4
    state = STATE_MENU

    # Opciones de Menú
    menu_items = [
        "NUEVA INCURSION", 
        "ESCOGER MAPA", 
        "SECTOR AMENAZA", 
        "CONFIGURACION", 
        "CREDITOS", 
        "DESCONECTAR"
    ]
    selected_menu = 0
    subscreen = "MAIN"
    map_selected_idx = 0
    diff_selected = 1
    confirm_quit = False
>>>>>>> Stashed changes

    player  = Player()
    enemies = make_enemies()
    shoot_flash = 0
    kill_msg    = 0

    def reset_game():
        nonlocal player, enemies, shoot_flash, kill_msg
        player  = Player()
        enemies = make_enemies()
        shoot_flash = 0
        kill_msg    = 0

    pygame.mouse.set_visible(True)
    pygame.event.set_grab(False)

    while True:
        dt = clock.tick(FPS)
        mx, my = pygame.mouse.get_rel() if state == STATE_PLAY else (0, 0)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            # ─────────────────────────────────────────────
            # CONTROLES Y NAVEGACIÓN DEL MENÚ
            # ─────────────────────────────────────────────
            if state == STATE_MENU:
                if confirm_quit:
                    if event.type == pygame.KEYDOWN:
                        if event.key in (pygame.K_s, pygame.K_y):
                            pygame.quit(); sys.exit()
                        elif event.key in (pygame.K_n, pygame.K_ESCAPE):
                            confirm_quit = False
                    continue

                if event.type == pygame.KEYDOWN:
                    if subscreen == "MAIN":
                        if event.key in (pygame.K_UP, pygame.K_w):
                            selected_menu = (selected_menu - 1) % len(menu_items)
                        elif event.key in (pygame.K_DOWN, pygame.K_s):
                            selected_menu = (selected_menu + 1) % len(menu_items)
                        elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                            if selected_menu == 0:     # NUEVA INCURSION
                                state = STATE_TITLE
                            elif selected_menu == 1:   # ESCOGER MAPA
                                subscreen = "SELECT_MAP"
                            elif selected_menu == 2:   # SECTOR AMENAZA
                                subscreen = "DIFFICULTY"
                            elif selected_menu == 3:   # CONFIGURACION
                                subscreen = "OPTIONS"
                            elif selected_menu == 4:   # CREDITOS
                                subscreen = "CREDITS"
                            elif selected_menu == 5:   # DESCONECTAR
                                confirm_quit = True
                        elif event.key == pygame.K_ESCAPE:
                            confirm_quit = True

                    elif subscreen == "SELECT_MAP":
                        map_names = list(MAPS_DATA.keys())
                        if event.key in (pygame.K_UP, pygame.K_w):
                            map_selected_idx = (map_selected_idx - 1) % len(map_names)
                        elif event.key in (pygame.K_DOWN, pygame.K_s):
                            map_selected_idx = (map_selected_idx + 1) % len(map_names)
                        elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                            set_active_map(map_names[map_selected_idx])
                            subscreen = "MAIN"
                        elif event.key == pygame.K_ESCAPE:
                            subscreen = "MAIN"

                    elif subscreen == "DIFFICULTY":
                        if event.key in (pygame.K_UP, pygame.K_w):
                            diff_selected = (diff_selected - 1) % 4
                        elif event.key in (pygame.K_DOWN, pygame.K_s):
                            diff_selected = (diff_selected + 1) % 4
                        elif event.key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_ESCAPE):
                            subscreen = "MAIN"

                    elif subscreen in ("OPTIONS", "CREDITS"):
                        if event.key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_ESCAPE):
                            subscreen = "MAIN"

            # ─────────────────────────────────────────────
            # CONTROLES GENERALES DEL JUEGO
            # ─────────────────────────────────────────────
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if state == STATE_PLAY:
                        state = STATE_MENU
                        pygame.event.set_grab(False)
                        pygame.mouse.set_visible(True)
                    else:
                        state = STATE_MENU

                if state == STATE_TITLE and event.key == pygame.K_RETURN:
                    reset_game()
                    state = STATE_PLAY
                    pygame.mouse.set_visible(False)
                    pygame.event.set_grab(True)

                if state in (STATE_OVER, STATE_WIN) and event.key == pygame.K_r:
                    reset_game()
                    state = STATE_PLAY
                    pygame.mouse.set_visible(False)
                    pygame.event.set_grab(True)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if state == STATE_PLAY:
                    alive_before = sum(e.alive for e in enemies)
                    fired = player.shoot(enemies)
                    if fired:
                        shoot_flash = 8
                        alive_after = sum(e.alive for e in enemies)
                        if alive_after < alive_before:
                            kill_msg = 45

<<<<<<< Updated upstream
        # ── TÍTULO ──
=======
        # Renderizado del Menú Principal
        if state == STATE_MENU:
            draw_cyber_menu(screen, menu_items, selected_menu, font_title, font_menu, font_small, subscreen, map_selected_idx, diff_selected, confirm_quit)
            pygame.display.flip()
            continue

>>>>>>> Stashed changes
        if state == STATE_TITLE:
            draw_title_screen(screen, font_title, font_big, font_small)
            pygame.display.flip()
            continue

        # ── GAME OVER / WIN ──
        if state == STATE_OVER:
            draw_game_over(screen, font_title, font_big, player)
            pygame.display.flip()
            continue
        if state == STATE_WIN:
            draw_win(screen, font_title, font_big, player)
            pygame.display.flip()
            continue

<<<<<<< Updated upstream
        # ── JUGANDO ──
=======
        # Actualización de Lógica de Juego
>>>>>>> Stashed changes
        keys = pygame.key.get_pressed()
        player.move(keys, dt)
        player.rotate_mouse(mx)

        for e in enemies:
            e.update(player, dt)

        # comprobar condiciones
        if player.health <= 0:
            state = STATE_OVER
            pygame.event.set_grab(False)
            pygame.mouse.set_visible(True)
        if all(not e.alive for e in enemies):
            state = STATE_WIN
            pygame.event.set_grab(False)
            pygame.mouse.set_visible(True)

        if shoot_flash > 0: shoot_flash -= 1
        if kill_msg    > 0: kill_msg    -= 1

        # ── RENDER ──
        draw_background(screen)
        z_buf, pdist = cast_rays(screen, player)
        draw_enemies(screen, enemies, player, z_buf, pdist)
        draw_hud(screen, player, font_big, font_small, shoot_flash, kill_msg)
        draw_minimap(screen, player, enemies)

        # FPS
        fps_txt = font_small.render(f"FPS:{int(clock.get_fps())}", True, GRAY)
        screen.blit(fps_txt, (WIDTH-80, 10))

        pygame.display.flip()

if __name__ == "__main__":
    main()
