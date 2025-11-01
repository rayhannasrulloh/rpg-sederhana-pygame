import pygame
import sys
import random

# --- 1. Inisialisasi Pygame ---
pygame.init()

# --- 2. Pengaturan Layar dan Konstanta ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BLACK = (0, 0, 0)
# Kita tidak perlu lagi warna WHITE, YELLOW, RED, tapi biarkan saja
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

pygame.display.set_caption("RPG Sederhana - Dengan Sprite!")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# Memuat Font (Sama seperti sebelumnya)
font = pygame.font.SysFont(None, 36)
game_over_font = pygame.font.SysFont(None, 72)

# --- ### BARU ### Memuat Gambar Sprite ---
# Kita bungkus dengan try...except untuk menangani error jika file tidak ada
try:
    # 1. Memuat file gambar dari disk
    # .convert_alpha() sangat penting untuk performa gambar transparan
    player_img_original = pygame.image.load("player.png").convert_alpha()
    coin_img_original = pygame.image.load("coin.png").convert_alpha()
    enemy_img_original = pygame.image.load("enemy.png").convert_alpha()

    # 2. Mengubah ukuran gambar agar sesuai dengan hitbox game kita
    PLAYER_IMG = pygame.transform.scale(player_img_original, (30, 30))
    COIN_IMG = pygame.transform.scale(coin_img_original, (15, 15))
    ENEMY_IMG = pygame.transform.scale(enemy_img_original, (40, 40))

except pygame.error as e:
    print("--- ERROR: Tidak bisa memuat gambar sprite! ---")
    print("Pastikan file 'player.png', 'coin.png', dan 'enemy.png' ada")
    print(f"di folder yang sama dengan file .py kamu.")
    print(f"Detail error: {e}")
    pygame.quit()
    sys.exit()


# --- 3. Class-Class Sprite (DIMODIFIKASI) ---

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # ### BARU ### Menggunakan gambar yang sudah di-load
        self.image = PLAYER_IMG
        
        # Hapus/Komentari kode lama:
        # self.image = pygame.Surface([30, 30])
        # self.image.fill(WHITE)
        
        # Sisa kode __init__ sama persis
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH // 2
        self.rect.y = SCREEN_HEIGHT // 2
        self.speed = 5
        
    # Fungsi update() tidak berubah sama sekali
    def update(self, keys):
        if keys[pygame.K_LEFT]:  self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]: self.rect.x += self.speed
        if keys[pygame.K_UP]:    self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:  self.rect.y += self.speed
        # ... (logika batas layar) ...
        if self.rect.left < 0:   self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:  self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0:    self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT: self.rect.bottom = SCREEN_HEIGHT


class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # ### BARU ### Menggunakan gambar yang sudah di-load
        self.image = COIN_IMG
        
        # Hapus/Komentari kode lama:
        # self.image = pygame.Surface([15, 15])
        # self.image.fill(YELLOW)
        
        # Sisa kode __init__ sama persis
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # ### BARU ### Menggunakan gambar yang sudah di-load
        self.image = ENEMY_IMG
        
        # Hapus/Komentari kode lama:
        # self.image = pygame.Surface([40, 40])
        # self.image.fill(RED)
        
        # Sisa kode __init__ sama persis
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - 40)
        self.rect.y = random.randint(0, SCREEN_HEIGHT - 40)
        self.speed_x = random.choice([-4, -3, 3, 4])
        self.speed_y = random.choice([-4, -3, 3, 4])

    # Fungsi update() tidak berubah sama sekali
    def update(self, *args):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            self.speed_x *= -1
        if self.rect.top < 0 or self.rect.bottom > SCREEN_HEIGHT:
            self.speed_y *= -1

# --- 4. Fungsi Game Loop Utama ---
# !!! TIDAK ADA PERUBAHAN SAMA SEKALI DI FUNGSI INI !!!
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

            collided_coins = pygame.sprite.spritecollide(player, coins_group, True)
            if collided_coins:
                for coin in collided_coins:
                    score += 1
                    spawn_coin()
            
            collided_enemies = pygame.sprite.spritecollide(player, enemies_group, False)
            if collided_enemies:
                game_over = True

        screen.fill(BLACK)
        all_sprites.draw(screen)

        score_text = f"Skor: {score}"
        text_surface = font.render(score_text, True, WHITE)
        screen.blit(text_surface, (10, 10))

        if game_over:
            go_text_surface = game_over_font.render("GAME OVER", True, WHITE)
            go_text_rect = go_text_surface.get_rect(
                center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            )
            screen.blit(go_text_surface, go_text_rect)
            
            restart_text = "Tekan 'R' untuk Restart"
            restart_surface = font.render(restart_text, True, WHITE)
            restart_rect = restart_surface.get_rect(
                center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
            )
            screen.blit(restart_surface, restart_rect)

        pygame.display.flip()

# --- 5. Loop Master (Pemicu Game) ---
# !!! TIDAK ADA PERUBAHAN SAMA SEKALI DI BAGIAN INI !!!
while True:
    game_loop()