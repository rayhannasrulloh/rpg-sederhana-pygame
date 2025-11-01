import pygame
import sys
import random # ### BARU ### Kita akan butuh ini nanti, tapi kita impor saja dulu

# --- 1. Inisialisasi Pygame ---
pygame.init()

# --- 2. Pengaturan Layar dan Konstanta ---

# Ukuran layar
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
# Warna (format RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0) # ### BARU ### Warna untuk koin kita

# Judul Jendela
pygame.display.set_caption("RPG Sederhana - Kumpulkan Koin!")

# Membuat layar
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Clock untuk mengatur FPS (Frames Per Second)
clock = pygame.time.Clock()

# --- 3. Class Player (Tidak ada perubahan dari sebelumnya) ---
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
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

        # Logika batas layar
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

# --- ### BARU ### Class Coin ---
class Coin(pygame.sprite.Sprite):
    """
    Class ini merepresentasikan koin yang bisa dikumpulkan.
    """
    def __init__(self, x, y):
        # Memanggil konstruktor dari class Sprite
        super().__init__()

        # Membuat gambar Koin (kotak kuning 15x15 piksel)
        self.image = pygame.Surface([15, 15])
        self.image.fill(YELLOW)

        # Mengambil 'rect' (rectangle/persegi) dari gambar
        self.rect = self.image.get_rect()

        # Mengatur posisi koin berdasarkan parameter x dan y
        self.rect.x = x
        self.rect.y = y

# --- 4. Inisialisasi Game ---

# Membuat grup untuk menampung SEMUA sprite (untuk menggambar)
all_sprites = pygame.sprite.Group()

# ### BARU ### Membuat grup KHUSUS untuk koin (untuk deteksi tabrakan)
coins_group = pygame.sprite.Group()

# Membuat objek Player dari class Player
player = Player()
# Menambahkan Player ke grup 'all_sprites'
all_sprites.add(player)

# ### BARU ### Membuat koin pertama
# Kita tempatkan koin ini di posisi x=100, y=150
coin1 = Coin(100, 150)

# ### BARU ### Menambahkan koin ke KEDUA grup
all_sprites.add(coin1)    # Agar koin ikut tergambar
coins_group.add(coin1) # Agar koin bisa dideteksi tabrakannya

# --- 5. Game Loop Utama ---
running = True
while running:
    # Mengatur game agar berjalan pada 60 FPS
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
    # Memanggil fungsi .update() pada semua sprite di 'all_sprites'
    # (Player akan bergerak, Koin tidak punya .update() jadi akan diabaikan)
    all_sprites.update(keys)

    # --- (Bagian 4: ### BARU ### Deteksi Tabrakan) ---
    
    # Perintah ini memeriksa apakah 'player' bertabrakan dengan sprite APAPUN
    # di dalam 'coins_group'.
    # Parameter 'True' berarti: jika terjadi tabrakan, HAPUS sprite
    # dari 'coins_group' tersebut (koinnya jadi "terkumpul").
    collided_coins = pygame.sprite.spritecollide(player, coins_group, True)

    # 'collided_coins' adalah sebuah LIST berisi koin yang tertabrak.
    # Jika list ini tidak kosong (artinya ada tabrakan), kita cetak pesan.
    if collided_coins:
        # Kita bisa saja menabrak lebih dari 1 koin di 1 frame,
        # jadi kita pakai 'for'
        for coin in collided_coins:
            print("Koin didapat!")
            # Sprite koin akan otomatis terhapus dari SEMUA grup
            # karena kita pakai parameter 'True' di atas.

    # --- (Bagian 5: Draw / Render) ---
    # (Nama bagian di-update dari 4 menjadi 5)
    
    screen.fill(BLACK)

    # Menggambar semua sprite (Player dan Koin yang tersisa)
    all_sprites.draw(screen)

    pygame.display.flip()