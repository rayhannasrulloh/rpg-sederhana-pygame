import pygame
import sys
import random

# --- 1. Inisialisasi Pygame ---
pygame.init()

# --- 2. Pengaturan Layar dan Konstanta ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

pygame.display.set_caption("RPG Sederhana - Tekan 'R' untuk Restart")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# ### BARU (DIPINDAHKAN DARI BAWAH) ###
# Kita definisikan Font di luar loop agar tidak perlu di-load ulang
font = pygame.font.SysFont(None, 36)
game_over_font = pygame.font.SysFont(None, 72)


# --- 3. Class-Class Sprite (Tidak ada perubahan) ---
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([30, 30]); self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH // 2; self.rect.y = SCREEN_HEIGHT // 2
        self.speed = 5
    def update(self, keys):
        if keys[pygame.K_LEFT]:  self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]: self.rect.x += self.speed
        if keys[pygame.K_UP]:    self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:  self.rect.y += self.speed
        if self.rect.left < 0:   self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:  self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0:    self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT: self.rect.bottom = SCREEN_HEIGHT

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([15, 15]); self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.x = x; self.rect.y = y

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([40, 40]); self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - 40)
        self.rect.y = random.randint(0, SCREEN_HEIGHT - 40)
        self.speed_x = random.choice([-4, -3, 3, 4])
        self.speed_y = random.choice([-4, -3, 3, 4])
    def update(self, *args):
        self.rect.x += self.speed_x; self.rect.y += self.speed_y
        if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            self.speed_x *= -1
        if self.rect.top < 0 or self.rect.bottom > SCREEN_HEIGHT:
            self.speed_y *= -1

# --- 4. ### BARU ### Fungsi Game Loop Utama ---
# Seluruh logika game kita sekarang ada di dalam fungsi ini
def game_loop():

    # --- (Bagian 4.1: Inisialisasi Game) ---
    # Kode ini sekarang berjalan SETIAP KALI game_loop() dipanggil
    
    all_sprites = pygame.sprite.Group()
    coins_group = pygame.sprite.Group()
    enemies_group = pygame.sprite.Group()

    player = Player()
    all_sprites.add(player)

    score = 0 # Skor di-reset ke 0

    def spawn_coin():
        rand_x = random.randint(0, SCREEN_WIDTH - 15)
        rand_y = random.randint(0, SCREEN_HEIGHT - 15)
        new_coin = Coin(rand_x, rand_y)
        all_sprites.add(new_coin)
        coins_group.add(new_coin)

    spawn_coin()

    enemy1 = Enemy()
    all_sprites.add(enemy1)
    enemies_group.add(enemy1)

    # --- (Bagian 4.2: Game Loop Internal) ---
    game_over = False # Game state di-reset ke False
    running = True
    while running:
        clock.tick(60)

        # --- (Event Handling) ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # ### BARU ### Jika quit, kita tutup semuanya
                pygame.quit()
                sys.exit()
            
            # ### BARU ### Logika untuk Restart
            if event.type == pygame.KEYDOWN:
                # Hanya jika game over DAN tombol 'R' ditekan
                if game_over and event.key == pygame.K_r:
                    return # Keluar dari fungsi game_loop()
                           # Ini akan menyebabkan loop master di luar
                           # memanggil game_loop() lagi (me-restart)

        # --- (Logika Update Game) ---
        if not game_over:
            keys = pygame.key.get_pressed()
            all_sprites.update(keys)

            # Tabrakan Koin
            collided_coins = pygame.sprite.spritecollide(player, coins_group, True)
            if collided_coins:
                for coin in collided_coins:
                    score += 1
                    spawn_coin()
            
            # Tabrakan Musuh
            collided_enemies = pygame.sprite.spritecollide(player, enemies_group, False)
            if collided_enemies:
                game_over = True

        # --- (Draw / Render) ---
        screen.fill(BLACK)
        all_sprites.draw(screen)

        # Tampilkan Skor
        score_text = f"Skor: {score}"
        text_surface = font.render(score_text, True, WHITE)
        screen.blit(text_surface, (10, 10))

        if game_over:
            # Tampilkan "GAME OVER"
            go_text_surface = game_over_font.render("GAME OVER", True, WHITE)
            go_text_rect = go_text_surface.get_rect(
                center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            )
            screen.blit(go_text_surface, go_text_rect)
            
            # ### BARU ### Tampilkan instruksi Restart
            restart_text = "Tekan 'R' untuk Restart"
            restart_surface = font.render(restart_text, True, WHITE)
            restart_rect = restart_surface.get_rect(
                center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
            )
            screen.blit(restart_surface, restart_rect)

        pygame.display.flip()

# --- 5. ### BARU ### Loop Master (Pemicu Game) ---
# Kode ini berada di luar fungsi game_loop()
# Tugasnya hanya memanggil game_loop() berulang kali.
while True:
    game_loop()