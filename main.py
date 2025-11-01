import pygame
import sys

# --- 1. Inisialisasi Pygame ---
pygame.init()

# --- 2. Pengaturan Layar dan Konstanta ---

# Ukuran layar
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
# Warna (format RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
# Judul Jendela
pygame.display.set_caption("RPG Sederhana")

# Membuat layar
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Clock untuk mengatur FPS (Frames Per Second)
clock = pygame.time.Clock()

# --- 3. Class Player (Inti RPG kita) ---
class Player(pygame.sprite.Sprite):
    """
    Class ini merepresentasikan Player yang dikontrol oleh pemain.
    """
    def __init__(self):
        # Memanggil konstruktor dari class Sprite
        super().__init__()

        # Membuat gambar Player (kotak putih 30x30 piksel)
        self.image = pygame.Surface([30, 30])
        self.image.fill(WHITE)

        # Mengambil 'rect' (rectangle/persegi) dari gambar
        # 'rect' ini sangat penting untuk mengatur posisi dan deteksi tabrakan
        self.rect = self.image.get_rect()

        # Mengatur posisi awal Player (di tengah layar)
        self.rect.x = SCREEN_WIDTH // 2
        self.rect.y = SCREEN_HEIGHT // 2

        # Kecepatan gerak Player
        self.speed = 5

    def update(self, keys):
        """
        Fungsi ini dipanggil di setiap frame untuk memperbarui posisi Player
        berdasarkan input keyboard (keys).
        """
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

        # Logika batas layar (agar Player tidak keluar layar)
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

# --- 4. Inisialisasi Game ---

# Membuat grup untuk menampung semua sprite (objek game)
# Ini membantu kita meng-update dan menggambar semua objek sekaligus
all_sprites = pygame.sprite.Group()

# Membuat objek Player dari class Player
player = Player()
# Menambahkan Player ke grup sprite
all_sprites.add(player)


# --- 5. Game Loop Utama ---
running = True
while running:
    # Mengatur game agar berjalan pada 60 FPS
    clock.tick(60)

    # --- (Bagian 1: Event Handling) ---
    # Memeriksa semua event (input) yang terjadi
    for event in pygame.event.get():
        # Jika event-nya adalah menutup jendela (klik tombol X)
        if event.type == pygame.QUIT:
            running = False # Hentikan loop
            pygame.quit() # Tutup Pygame
            sys.exit()    # Keluar dari program

    # --- (Bagian 2: Input Keyboard) ---
    # Mendapatkan status semua tombol keyboard yang sedang ditekan
    keys = pygame.key.get_pressed()

    # --- (Bagian 3: Update) ---
    # Memanggil fungsi .update() pada semua sprite di dalam grup 'all_sprites'
    # (Dalam kasus ini, hanya akan memanggil player.update())
    all_sprites.update(keys)

    # --- (Bagian 4: Draw / Render) ---
    # Mengisi layar dengan warna latar belakang (hitam)
    screen.fill(222222)

    # Menggambar semua sprite di dalam grup 'all_sprites' ke layar
    all_sprites.draw(screen)

    # Memperbarui tampilan layar (menampilkan apa yang sudah kita gambar)
    pygame.display.flip()