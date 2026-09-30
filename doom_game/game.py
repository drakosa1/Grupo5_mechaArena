"""
MECHAARENA DOOM - First Person Shooter con Raycasting
Estilo clásico de DOOM usando Python + Pygame
Controles:
  W/S       - Mover adelante/atrás
  A/D       - Rotar izquierda/derecha
  MOUSE     - Apuntar
  CLICK IZQ - Disparar
  ESC       - Salir
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
FOV        = math.pi / 3          # 60°
HALF_FOV   = FOV / 2
NUM_RAYS   = WIDTH // 2           # un rayo por 2 px
DEPTH      = 20                   # distancia máxima de visión
DELTA_ANGLE = FOV / NUM_RAYS
SCALE       = WIDTH // NUM_RAYS    # ancho de cada franja

# Velocidades
PLAYER_SPEED  = 0.04
PLAYER_ROT    = 0.002

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
    1: [(100, 60, 20), (140, 80, 30)],    # piedra marrón
    2: [(60, 60, 80), (90, 90, 120)],     # metal gris-azul
    3: [(150, 30, 30),(200, 50, 50)],     # pared roja infernal
    4: [(20, 60, 20), (30, 90, 30)],      # metal verde
}

# ─────────────────────────────────────────────
#  MAPA  (0=libre, 1-4=pared)
# ─────────────────────────────────────────────
MAP = [
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
]
MAP_W = len(MAP[0])
MAP_H = len(MAP)

def wall_at(x, y):
    xi, yi = int(x), int(y)
    if 0 <= xi < MAP_W and 0 <= yi < MAP_H:
        return MAP[yi][xi]
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
        speed = PLAYER_SPEED * dt

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            dx += math.cos(self.angle) * speed
            dy += math.sin(self.angle) * speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dx -= math.cos(self.angle) * speed
            dy -= math.sin(self.angle) * speed

        nx, ny = self.x + dx, self.y + dy
        if wall_at(nx, self.y) == 0: self.x = nx
        if wall_at(self.x, ny) == 0: self.y = ny

        if keys[pygame.K_a]: self.angle -= 0.03
        if keys[pygame.K_d]: self.angle += 0.03

        if self.shoot_cooldown > 0: self.shoot_cooldown -= dt
        if self.pain_flash > 0:     self.pain_flash -= dt

    def rotate_mouse(self, dx):
        self.angle += dx * PLAYER_ROT

    def shoot(self, enemies):
        if self.shoot_cooldown > 0 or self.ammo <= 0:
            return False
        self.ammo -= 1
        self.shoot_cooldown = 15
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
        self.speed   = 0.008
        self.attack_cd = 0
        self.anim_t    = random.random() * 6.28   # fase de animación

    def take_damage(self, dmg):
        self.health -= dmg
        if self.health <= 0:
            self.alive = False

    def update(self, player, dt):
        if not self.alive: return
        self.anim_t += 0.05
        dx = player.x - self.x
        dy = player.y - self.y
        dist = math.hypot(dx, dy)

        # movimiento hacia el jugador
        if dist > 0.6:
            nx = self.x + (dx/dist) * self.speed * dt
            ny = self.y + (dy/dist) * self.speed * dt
            if wall_at(nx, self.y) == 0: self.x = nx
            if wall_at(self.x, ny) == 0: self.y = ny

        # ataque cuerpo a cuerpo
        if dist < 0.9:
            self.attack_cd -= dt
            if self.attack_cd <= 0:
                player.take_damage(8)
                self.attack_cd = 60

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
    # cielo degradado infernal (negro → rojo oscuro)
    for y in range(HALF_HEIGHT):
        t = y / HALF_HEIGHT
        r = int(10 + 80 * t)
        g = int(t * 5)
        b = 0
        pygame.draw.line(surface, (r, g, b), (0, y), (WIDTH, y))
    # suelo degradado oscuro
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

        # animación: oscilación vertical
        bob = int(math.sin(e.anim_t * 3) * 4)
        top += bob

        # dibujar sprite demonio (rectángulos de colores)
        if dist < z_buffer[max(0, min(sx, WIDTH-1))]:
            draw_demon_sprite(surface, left, top, sprite_w, sprite_h, e, dist)

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
    hud_surf.fill((0, 0, 0, 180))
    surface.blit(hud_surf, (0, HEIGHT - hud_h))

    # ── SALUD ──
    pygame.draw.rect(surface, (100,0,0), (20, HEIGHT-70, 200, 24))
    hp_w = int(200 * max(0, player.health) / 100)
    hp_col = (0,200,0) if player.health > 50 else (220,180,0) if player.health > 25 else (220,30,30)
    pygame.draw.rect(surface, hp_col, (20, HEIGHT-70, hp_w, 24))
    pygame.draw.rect(surface, WHITE,  (20, HEIGHT-70, 200, 24), 2)
    hp_txt = font_small.render(f"♥ {player.health}", True, WHITE)
    surface.blit(hp_txt, (28, HEIGHT-68))

    # ── MUNICIÓN ──
    ammo_txt = font_big.render(f"⚡{player.ammo}", True, YELLOW)
    surface.blit(ammo_txt, (WIDTH//2 - 40, HEIGHT-72))

    # ── SCORE ──
    score_txt = font_small.render(f"KILLS: {player.score//10}", True, WHITE)
    surface.blit(score_txt, (WIDTH - 160, HEIGHT-70))

    # ── PISTOLA ──
    draw_gun(surface, shoot_flash)

    # ── MIRA ──
    cx, cy = WIDTH // 2, HEIGHT // 2
    pygame.draw.line(surface, WHITE, (cx-12, cy), (cx+12, cy), 2)
    pygame.draw.line(surface, WHITE, (cx, cy-12), (cx, cy+12), 2)
    pygame.draw.circle(surface, WHITE, (cx, cy), 5, 1)

    # ── FLASH DE DOLOR ──
    if player.pain_flash > 0:
        alpha = int(min(180, player.pain_flash * 9))
        pain_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        pain_surf.fill((200, 0, 0, alpha))
        surface.blit(pain_surf, (0, 0))

    # ── MENSAJE DE KILL ──
    if kill_msg > 0:
        msg = font_big.render("DEMON SLAIN!", True, YELLOW)
        surface.blit(msg, (WIDTH//2 - msg.get_width()//2, HEIGHT//2 - 80))

def draw_gun(surface, shoot_flash):
    """Dibuja la pistola en la parte inferior central."""
    gx = WIDTH // 2
    gy = HEIGHT - 10
    kick = -20 if shoot_flash > 0 else 0

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
    if shoot_flash > 0:
        for _ in range(8):
            angle = random.uniform(0, 2*math.pi)
            r = random.randint(5, 20)
            fx = gx + int(math.cos(angle) * r)
            fy = gy - 85 + kick + int(math.sin(angle) * r // 2)
            pygame.draw.circle(surface, YELLOW, (fx, fy), random.randint(3,8))
        pygame.draw.circle(surface, WHITE, (gx, gy-85+kick), 6)

# ─────────────────────────────────────────────
#  PANTALLAS
# ─────────────────────────────────────────────
def draw_title_screen(surface, font_title, font_big, font_small):
    surface.fill((10,0,0))
    # efecto de fondo
    for i in range(0, WIDTH, 40):
        for j in range(0, HEIGHT, 40):
            if random.random() < 0.02:
                pygame.draw.rect(surface,(40,0,0),(i,j,40,40))

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
#  MINIMAP
# ─────────────────────────────────────────────
def draw_minimap(surface, player, enemies):
    cell = 8
    ox, oy = 10, 10
    for row in range(MAP_H):
        for col in range(MAP_W):
            v = MAP[row][col]
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
#  SPAWN INICIAL DE ENEMIGOS
# ─────────────────────────────────────────────
ENEMY_SPAWNS = [
    (3.5, 5.5),(10.5, 3.5),(15.5, 2.5),(6.5,12.5),
    (14.5,8.5),(10.5,10.5),(4.5,14.5),(17.5,6.5),
    (8.5,16.5),(12.5,15.5),(3.5,10.5),(18.5,12.5),
]

def make_enemies():
    return [Enemy(x, y) for x, y in ENEMY_SPAWNS]

# ─────────────────────────────────────────────
#  MAIN LOOP
# ─────────────────────────────────────────────
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("MechaArena Inferno")
    clock  = pygame.time.Clock()
    pygame.mouse.set_visible(False)
    pygame.event.set_grab(True)

    # Fuentes
    try:
        font_title = pygame.font.SysFont("impact", 80)
        font_big   = pygame.font.SysFont("impact", 36)
        font_small = pygame.font.SysFont("consolas", 22)
    except Exception:
        font_title = pygame.font.Font(None, 80)
        font_big   = pygame.font.Font(None, 36)
        font_small = pygame.font.Font(None, 22)

    # Estado del juego
    STATE_TITLE  = 0
    STATE_PLAY   = 1
    STATE_OVER   = 2
    STATE_WIN    = 3
    state = STATE_TITLE

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

    while True:
        dt = clock.tick(FPS)
        mx, my = pygame.mouse.get_rel()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if state == STATE_PLAY:
                        pygame.event.set_grab(False)
                        pygame.mouse.set_visible(True)
                        pygame.quit(); sys.exit()
                    else:
                        pygame.quit(); sys.exit()

                if state == STATE_TITLE and event.key == pygame.K_RETURN:
                    state = STATE_PLAY

                if state in (STATE_OVER, STATE_WIN) and event.key == pygame.K_r:
                    reset_game()
                    state = STATE_PLAY

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if state == STATE_PLAY:
                    hit = player.shoot(enemies)
                    if hit:
                        shoot_flash = 8
                        if any(not e.alive for e in enemies):
                            kill_msg = 45

        # ── TÍTULO ──
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

        # ── JUGANDO ──
        keys = pygame.key.get_pressed()
        player.move(keys, dt)
        player.rotate_mouse(mx)

        for e in enemies:
            e.update(player, dt)

        # comprobar condiciones
        if player.health <= 0:
            state = STATE_OVER
        if all(not e.alive for e in enemies):
            state = STATE_WIN

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
