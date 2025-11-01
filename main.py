import pygame
import sys
import random # Sekarang kita benar-benar gunakan ini!

# --- 1. Inisialisasi Pygame ---
pygame.init()

# --- 2. Pengaturan Layar dan Konstanta ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
pygame.display.set_caption("RPG Sederhana - Kumpulkan Koin!")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# --- 3. Class Player & Coin (Tidak ada perubahan) ---
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

# --- 4. Inisialisasi Game ---

all_sprites = pygame.sprite.Group()
coins_group = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

# ### BARU ### Pengaturan Skor dan Font
score = 0
# Menggunakan font sistem default, ukuran 36
font = pygame.font.SysFont(None, 36)

# ### BARU ### Fungsi untuk memunculkan koin baru secara acak
def spawn_coin():
    """Membuat koin baru di posisi acak."""
    # -15 adalah agar koin (lebar 15px) tidak spawn di luar batas kanan/bawah
    rand_x = random.randint(0, SCREEN_WIDTH - 15)
    rand_y = random.randint(0, SCREEN_HEIGHT - 15)
    
    new_coin = Coin(rand_x, rand_y)
    all_sprites.add(new_coin)
    coins_group.add(new_coin)

# ### BARU ### Hapus 'coin1' yang lama dan panggil fungsi spawn
# Kode lama (dihapus):
# coin1 = Coin(100, 150)
# all_sprites.add(coin1)
# coins_group.add(coin1)

# Kode baru:
spawn_coin() # Memunculkan koin pertama

# --- 5. Game Loop Utama ---
running = True
while running:
    clock.tick(60)

    # --- (Bagian 1: Event Handling) ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()

    # --- (Bagian 2: Input Keyboard) ---
    keys = pygame.key.get_pressed()

    # --- (Bagian 3: Update) ---
    all_sprites.update(keys)

    # --- (Bagian 4: Deteksi Tabrakan) ---
    
    # Periksa tabrakan
    collided_coins = pygame.sprite.spritecollide(player, coins_group, True)

    # ### BARU ### Logika setelah tabrakan
    if collided_coins:
        # Kita pakai 'for' untuk berjaga-jaga jika 1 frame menabrak >1 koin
        for coin in collided_coins:
            print("Koin didapat! Skor +1")
            score += 1     # Tambah skor
            spawn_coin()   # Buat koin baru di tempat acak

    # --- (Bagian 5: Draw / Render) ---
    screen.fill(BLACK)
    all_sprites.draw(screen)

    # --- ### BARU ### Tampilkan Skor ---
    # 1. Buat string teks-nya (misal: "Skor: 5")
    score_text = f"Skor: {score}"
    
    # 2. Render teks: font.render(teks, anti-alias, warna)
    # Ini membuat "Surface" baru yang berisi gambar teks
    text_surface = font.render(score_text, True, WHITE)
    
    # 3. Blit (gambar) Surface teks ke layar utama
    # Kita taruh di posisi (10, 10) -> 10px dari kiri, 10px dari atas
    screen.blit(text_surface, (10, 10))

    # Memperbarui tampilan layar
    pygame.display.flip()