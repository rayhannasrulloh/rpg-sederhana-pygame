import pygame
import sys
import random

# --- 1. Inisialisasi Pygame ---
pygame.init()
pygame.mixer.init() # ### BARU ### Inisialisasi modul audio

# --- 2. Pengaturan Layar dan Konstanta ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
# ... (warna lain bisa dihapus jika mau) ...

pygame.display.set_caption("RPG Sederhana - Dengan Suara!")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# Memuat Font
font = pygame.font.SysFont(None, 36)
game_over_font = pygame.font.SysFont(None, 72)

# Memuat Gambar Sprite (Blok ini sama seperti sebelumnya)
try:
    player_img_original = pygame.image.load("player.png").convert_alpha()
    coin_img_original = pygame.image.load("coin.png").convert_alpha()
    enemy_img_original = pygame.image.load("enemy.png").convert_alpha()

    PLAYER_IMG = pygame.transform.scale(player_img_original, (30, 30))
    COIN_IMG = pygame.transform.scale(coin_img_original, (15, 15))
    ENEMY_IMG = pygame.transform.scale(enemy_img_original, (40, 40))

except pygame.error as e:
    print(f"--- ERROR: Gagal memuat gambar: {e} ---")
    pygame.quit()
    sys.exit()

# --- ### BARU ### Memuat Aset Audio ---
try:
    # Memuat musik latar
    # pygame.mixer.music.load("music.mp3") # Ganti ke .ogg jika kamu pakai .ogg
    # # Mengatur volume (0.0 - 1.0). 0.5 = 50% volume
    # pygame.mixer.music.set_volume(0.5)
    # # Memutar musik, -1 berarti loop selamanya
    # pygame.mixer.music.play(-1)
    
    # Memuat efek suara koin
    COIN_SOUND = pygame.mixer.Sound("coin.mp3")
    COIN_SOUND.set_volume(0.8) # Atur volume efek suara juga

except pygame.error as e:
    print("--- PERINGATAN: Tidak bisa memuat file audio! ---")
    print(f"Game akan berjalan tanpa suara.")
    print(f"Detail error: {e}")
    COIN_SOUND = None # Set ke None agar game tidak crash saat memainkannya


# --- 3. Class-Class Sprite (Tidak ada perubahan) ---
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = PLAYER_IMG
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
        self.image = COIN_IMG
        self.rect = self.image.get_rect()
        self.rect.x = x; self.rect.y = y

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = ENEMY_IMG
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

# --- 4. Fungsi Game Loop Utama ---
# Perubahan kecil ada di dalam 'if collided_coins'
def game_loop():
    all_sprites = pygame.sprite.Group()
    coins_group = pygame.sprite.Group()
    enemies_group = pygame.sprite.Group()

    player = Player()
    all_sprites.add(player)
    score = 0

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

    game_over = False
    running = True
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if game_over and event.key == pygame.K_r:
                    return

        if not game_over:
            keys = pygame.key.get_pressed()
            all_sprites.update(keys)

            # Tabrakan Koin
            collided_coins = pygame.sprite.spritecollide(player, coins_group, True)
            if collided_coins:
                for coin in collided_coins:
                    score += 1
                    spawn_coin()
                    
                    # --- ### BARU ### ---
                    # Mainkan suara koin (jika berhasil di-load)
                    if COIN_SOUND:
                        COIN_SOUND.play()
            
            # Tabrakan Musuh
            collided_enemies = pygame.sprite.spritecollide(player, enemies_group, False)
            if collided_enemies:
                # ### BARU (Opsional tapi bagus) ###
                # Hentikan musik saat game over
                pygame.mixer.music.stop()
                game_over = True

        # --- (Bagian Render tidak berubah) ---
        screen.fill(BLACK)
        all_sprites.draw(screen)
        
        score_text = f"Skor: {score}"
        text_surface = font.render(score_text, True, WHITE)
        screen.blit(text_surface, (10, 10))

        if game_over:
            go_text_surface = game_over_font.render("GAME OVER", True, WHITE)
            go_text_rect = go_text_surface.get_rect(
                center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(go_text_surface, go_text_rect)
            
            restart_text = "Tekan 'R' untuk Restart"
            restart_surface = font.render(restart_text, True, WHITE)
            restart_rect = restart_surface.get_rect(
                center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
            screen.blit(restart_surface, restart_rect)

        pygame.display.flip()

# --- 5. Loop Master (Pemicu Game) ---
# ### BARU ### Modifikasi kecil di sini
while True:
    game_loop() # Mulai/Restart game
    
    # ### BARU ### Setelah game_loop() selesai (karena restart)
    # Kita perlu memutar musik lagi, karena kita menghentikannya
    # saat game over.
    # try:
    #     # Coba putar lagi, siapa tahu file-nya ada
    #     pygame.mixer.music.play(-1)
    # except pygame.error:
    #     # Biarkan saja jika gagal
    #     pass