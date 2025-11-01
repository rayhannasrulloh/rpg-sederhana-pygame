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
RED = (255, 0, 0) # ### BARU ### Warna untuk musuh

pygame.display.set_caption("RPG Sederhana - Hindari Musuh!")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# --- 3. Class-Class Sprite ---

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([30, 30])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH // 2
        self.rect.y = SCREEN_HEIGHT // 2
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
        self.image = pygame.Surface([15, 15])
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# --- ### BARU ### Class Enemy ---
class Enemy(pygame.sprite.Sprite):
    """
    Class ini merepresentasikan musuh yang bergerak memantul.
    """
    def __init__(self):
        super().__init__()
        # Membuat gambar Musuh (kotak merah 40x40)
        self.image = pygame.Surface([40, 40])
        self.image.fill(RED)
        self.rect = self.image.get_rect()

        # Posisi awal acak
        self.rect.x = random.randint(0, SCREEN_WIDTH - 40)
        self.rect.y = random.randint(0, SCREEN_HEIGHT - 40)
        
        # Kecepatan acak (antara -4 dan 4, tapi bukan 0)
        self.speed_x = random.choice([-4, -3, 3, 4])
        self.speed_y = random.choice([-4, -3, 3, 4])

    def update(self, *args):
        """
        Kita tambahkan *args agar fungsi ini bisa menerima argumen 'keys'
        dari all_sprites.update(keys) tanpa error, meskipun tidak menggunakannya.
        """
        # Logika gerak
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        
        # Logika memantul di dinding
        if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            self.speed_x *= -1 # Balik arah horizontal
        if self.rect.top < 0 or self.rect.bottom > SCREEN_HEIGHT:
            self.speed_y *= -1 # Balik arah vertikal

# --- 4. Inisialisasi Game ---

all_sprites = pygame.sprite.Group()
coins_group = pygame.sprite.Group()
enemies_group = pygame.sprite.Group() # ### BARU ### Grup untuk musuh

player = Player()
all_sprites.add(player)

score = 0
font = pygame.font.SysFont(None, 36)
# ### BARU ### Font besar untuk "Game Over"
game_over_font = pygame.font.SysFont(None, 72)

def spawn_coin():
    rand_x = random.randint(0, SCREEN_WIDTH - 15)
    rand_y = random.randint(0, SCREEN_HEIGHT - 15)
    new_coin = Coin(rand_x, rand_y)
    all_sprites.add(new_coin)
    coins_group.add(new_coin)

spawn_coin()

# ### BARU ### Membuat satu musuh
enemy1 = Enemy()
all_sprites.add(enemy1)
enemies_group.add(enemy1)

# --- 5. Game Loop Utama ---
running = True
game_over = False # ### BARU ### Game state kita

while running:
    clock.tick(60)

    # --- (Bagian 1: Event Handling) ---
    # Kita tetap perlu cek event QUIT kapan saja
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()

    # --- (Bagian 2: Logika Update Game) ---
    # ### BARU ### Seluruh logika game hanya berjalan jika game_over == False
    if not game_over:
        # --- (Input Keyboard) ---
        keys = pygame.key.get_pressed()

        # --- (Update) ---
        # Memanggil .update() pada Player (pakai keys) dan Enemy (abaikan keys)
        all_sprites.update(keys)

        # --- (Deteksi Tabrakan Koin) ---
        collided_coins = pygame.sprite.spritecollide(player, coins_group, True)
        if collided_coins:
            for coin in collided_coins:
                score += 1
                spawn_coin()
        
        # --- (Deteksi Tabrakan Musuh) ---
        # Parameter 'False' berarti musuh TIDAK dihapus saat tabrakan
        collided_enemies = pygame.sprite.spritecollide(player, enemies_group, False)
        if collided_enemies:
            print("GAME OVER!")
            game_over = True # ### BARU ### Ubah game state!

    # --- (Bagian 3: Draw / Render) ---
    # Menggambar selalu dilakukan, baik game over maupun tidak
    
    screen.fill(BLACK)
    all_sprites.draw(screen)

    # Tampilkan Skor
    score_text = f"Skor: {score}"
    text_surface = font.render(score_text, True, WHITE)
    screen.blit(text_surface, (10, 10))

    # ### BARU ### Tampilkan layar Game Over jika game_over == True
    if game_over:
        # Buat teks "GAME OVER"
        go_text_surface = game_over_font.render("GAME OVER", True, WHITE)
        # Dapatkan 'rect' dari teks agar bisa diposisikan di tengah
        go_text_rect = go_text_surface.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        )
        # Gambar teks "GAME OVER" ke layar
        screen.blit(go_text_surface, go_text_rect)

    # Memperbarui tampilan layar
    pygame.display.flip()