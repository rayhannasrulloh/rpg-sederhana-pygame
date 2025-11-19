import pygame
import sys
import random
import os

# --- 1. Inisialisasi Pygame ---
pygame.init()
pygame.mixer.init()

# --- 2. Pengaturan Layar dan Konstanta ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)

pygame.display.set_caption("RPG Sederhana - Ultimate Edition")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# Memuat Font
font = pygame.font.SysFont(None, 36)
game_over_font = pygame.font.SysFont(None, 72)
title_font = pygame.font.SysFont(None, 80)

# File Highscore
HIGHSCORE_FILE = "highscore.txt"

# Memuat Gambar Sprite
try:
    player_img_original = pygame.image.load("player.png").convert_alpha()
    coin_img_original = pygame.image.load("coin.png").convert_alpha()
    enemy_img_original = pygame.image.load("enemy.png").convert_alpha()
    
    # Try loading powerup, else fallback
    if os.path.exists("powerup.png"):
        powerup_img_original = pygame.image.load("powerup.png").convert_alpha()
    else:
        # Fallback if image missing
        powerup_img_original = pygame.Surface((20, 20))
        powerup_img_original.fill(YELLOW)

    PLAYER_IMG = pygame.transform.scale(player_img_original, (30, 30))
    COIN_IMG = pygame.transform.scale(coin_img_original, (15, 15))
    ENEMY_IMG = pygame.transform.scale(enemy_img_original, (40, 40))
    POWERUP_IMG = pygame.transform.scale(powerup_img_original, (25, 25))

except pygame.error as e:
    print(f"--- ERROR: Gagal memuat gambar: {e} ---")
    pygame.quit()
    sys.exit()

# Memuat Audio
try:
    COIN_SOUND = pygame.mixer.Sound("coin.mp3")
    COIN_SOUND.set_volume(0.8)
except pygame.error:
    COIN_SOUND = None

# --- Fungsi Helper ---
def load_high_score():
    if os.path.exists(HIGHSCORE_FILE):
        try:
            with open(HIGHSCORE_FILE, "r") as f:
                return int(f.read())
        except:
            return 0
    return 0

def save_high_score(score):
    with open(HIGHSCORE_FILE, "w") as f:
        f.write(str(score))

def draw_text_centered(text, font, color, y_offset):
    surface = font.render(text, True, color)
    rect = surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + y_offset))
    screen.blit(surface, rect)

# --- 3. Class-Class Sprite ---
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = PLAYER_IMG
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.speed = 5
        self.invincible = False
        self.invincible_start_time = 0
        self.invincible_duration = 5000 # ms
        self.transparent_image = pygame.Surface(self.rect.size, pygame.SRCALPHA)

    def update(self, keys):
        if keys[pygame.K_LEFT]:  self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]: self.rect.x += self.speed
        if keys[pygame.K_UP]:    self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:  self.rect.y += self.speed
        
        # Clamp to screen
        self.rect.clamp_ip(screen.get_rect())

        # Handle invincibility
        if self.invincible:
            current_time = pygame.time.get_ticks()
            if current_time - self.invincible_start_time > self.invincible_duration:
                self.invincible = False
                self.image = PLAYER_IMG # Reset appearance
            else:
                # Flicker effect
                if (current_time // 100) % 2 == 0:
                    self.image = self.transparent_image
                else:
                    self.image = PLAYER_IMG
        else:
            self.image = PLAYER_IMG

    def activate_powerup(self):
        self.invincible = True
        self.invincible_start_time = pygame.time.get_ticks()

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = COIN_IMG
        self.rect = self.image.get_rect()
        self.rect.x = x; self.rect.y = y

class Enemy(pygame.sprite.Sprite):
    def __init__(self, speed_bonus=0):
        super().__init__()
        self.image = ENEMY_IMG
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - 40)
        self.rect.y = random.randint(0, SCREEN_HEIGHT - 40)
        
        base_speed = 3 + speed_bonus
        # Ensure speed is at least 1
        speed_val = max(1, int(base_speed))
        
        self.speed_x = random.choice([-speed_val, speed_val])
        self.speed_y = random.choice([-speed_val, speed_val])

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        
        if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            self.speed_x *= -1
        if self.rect.top < 0 or self.rect.bottom > SCREEN_HEIGHT:
            self.speed_y *= -1

class PowerUp(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = POWERUP_IMG
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - 25)
        self.rect.y = random.randint(0, SCREEN_HEIGHT - 25)

# --- 4. Game Loop ---
def show_start_screen(high_score):
    screen.fill(BLACK)
    draw_text_centered("RPG ADVENTURE", title_font, YELLOW, -100)
    draw_text_centered(f"High Score: {high_score}", font, WHITE, -20)
    draw_text_centered("Tekan ENTER untuk Mulai", font, WHITE, 50)
    draw_text_centered("Kumpulkan Koin, Hindari Musuh!", font, BLUE, 100)
    pygame.display.flip()
    
    waiting = True
    while waiting:
        clock.tick(15)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting = False

def game_loop():
    all_sprites = pygame.sprite.Group()
    coins_group = pygame.sprite.Group()
    enemies_group = pygame.sprite.Group()
    powerups_group = pygame.sprite.Group()

    player = Player()
    all_sprites.add(player)
    
    score = 0
    high_score = load_high_score()
    
    # Initial Spawns
    for _ in range(3): # Start with 3 coins
        c = Coin(random.randint(0, SCREEN_WIDTH-15), random.randint(0, SCREEN_HEIGHT-15))
        all_sprites.add(c); coins_group.add(c)
        
    enemy = Enemy()
    all_sprites.add(enemy); enemies_group.add(enemy)

    running = True
    game_over = False
    
    while running:
        clock.tick(60)
        
        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if game_over and event.key == pygame.K_r:
                    return # Restart
                if game_over and event.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()

        if not game_over:
            keys = pygame.key.get_pressed()
            player.update(keys)
            enemies_group.update()
            
            # Difficulty Scaling
            # Every 5 points, add speed or new enemy
            difficulty_level = score // 5
            
            # Check Coin Collisions
            hits = pygame.sprite.spritecollide(player, coins_group, True)
            for hit in hits:
                score += 1
                if COIN_SOUND: COIN_SOUND.play()
                
                # Spawn new coin
                c = Coin(random.randint(0, SCREEN_WIDTH-15), random.randint(0, SCREEN_HEIGHT-15))
                all_sprites.add(c); coins_group.add(c)
                
                # Spawn Powerup chance (10%)
                if random.random() < 0.1:
                    p = PowerUp()
                    all_sprites.add(p); powerups_group.add(p)
                
                # Increase Difficulty
                if score % 5 == 0:
                    # Add a new enemy with increased speed
                    e = Enemy(speed_bonus=difficulty_level * 0.5)
                    all_sprites.add(e); enemies_group.add(e)

            # Check Powerup Collisions
            phits = pygame.sprite.spritecollide(player, powerups_group, True)
            for p in phits:
                player.activate_powerup()
            
            # Check Enemy Collisions
            if not player.invincible:
                if pygame.sprite.spritecollide(player, enemies_group, False):
                    game_over = True
                    if score > high_score:
                        save_high_score(score)
                        high_score = score

        # Draw
        screen.fill(BLACK)
        all_sprites.draw(screen)
        
        # UI
        score_text = font.render(f"Skor: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        
        hs_text = font.render(f"High Score: {high_score}", True, YELLOW)
        screen.blit(hs_text, (10, 40))
        
        if player.invincible:
            inv_text = font.render("INVINCIBLE!", True, RED)
            screen.blit(inv_text, (SCREEN_WIDTH//2 - 50, 10))

        if game_over:
            draw_text_centered("GAME OVER", game_over_font, RED, -50)
            draw_text_centered(f"Final Score: {score}", font, WHITE, 10)
            draw_text_centered("Tekan 'R' untuk Restart", font, WHITE, 60)
            draw_text_centered("Tekan 'ESC' untuk Keluar", font, WHITE, 100)

        pygame.display.flip()

# --- Main Execution ---
while True:
    current_hs = load_high_score()
    show_start_screen(current_hs)
    game_loop()