import pygame
import random
from pygame.locals import *
from pygame import mixer
import sys
import random

# Inisialisasi class HoppingBun
class HoppingBunGame:
    def __init__(self):
        #ukuran layar
        self.screen = pygame.display.set_mode((800, 600))
        
        #Background
        self.background =  pygame.image.load('assets/bg.png')
        
        #Background music
        pygame.mixer.init()
        #bgm main game
        self.bgm = pygame.mixer.music.load("assets/bgm.mp3")
        #bgm dimulai
        pygame.mixer.music.play(-1)
        #SFX game over
        self.game_over_sfx = pygame.mixer.Sound("assets/game over_bgm.mp3")
        
        #font
        pygame.font.init()
        #font untuk high score dan score
        self.font = pygame.font.Font("assets/font.ttf", 25)
        #font untuk Game over
        self.font_game_over = pygame.font.Font("assets/font.ttf", 80)
        #font untuk tulisan restart, menu dan score high score di pae game over
        self.font_restart_menu = pygame.font.Font("assets/font.ttf", 30)
        #memanggil assets platform
        self.blog = pygame.image.load("assets/blog.png").convert_alpha()
        #platform bergerak
        self.blogmove = pygame.image.load("assets/blogmove.png").convert_alpha()
        #platform retak
        self.blogbreak = pygame.image.load("assets/blogbreak.png").convert_alpha()
        #platform retak patah
        self.blogbreak_1 = pygame.image.load("assets/blogbreak_1.png").convert_alpha()
        
        #panggil assets bunny kanan
        self.playerRight = pygame.image.load("assets/bunright.png").convert_alpha()
        #panggil assets bunny kanan lompat
        self.playerRight_1 = pygame.image.load("assets/bunright_1.png").convert_alpha()

        #panggil assets bunny kiri
        self.playerLeft = pygame.image.load("assets/bunleft.png").convert_alpha()
        #panggil assets bunny kiri lompat
        self.playerLeft_1 = pygame.image.load("assets/bunleft_1.png").convert_alpha()
        #panggil assets spring
        self.spring = pygame.image.load("assets/roket.png").convert_alpha()
        self.spring_1 = pygame.image.load("assets/roket.png").convert_alpha()
        
        #variabel game
        self.scroll_y = 0
        self.score = 0
        self.previous_score = 0
        self.high_score = 0
        self.direction = 0
        self.playerx = 400
        self.playery = 400
        self.platforms = [[400, 500, 0, 0]]
        self.springs = []
        self.cameray = 0
        self.jump = 0
        self.gravity = 0
        self.xmovement = 0 

    #memperbarui posisi, kecepatan, dan animasi pemain
    def updatePlayer(self):
        #jka pemain tidak sedang melompat
        if not self.jump:  
            #pemain bergerak ke bawah karena pengaruh gravitasi      
            self.playery += self.gravity
            self.gravity += 1
        #jika pemain sedang melompat
        elif self.jump: 
            #pemain bergerak ke atas karena sedang melompat
            self.playery -= self.jump
            self.jump -= 1
        #jika pemain melewati bagian atas layar
        if self.playery - self.cameray >= 200:
            #kamera digeser ke bawah,latar belakang geser kebawah
            self.cameray += 1
            self.scroll_y += 1
        #jika pemain berada di bagian bawah layar
        if self.playery - self.cameray <= 400:
            #kamera digeser ke atas,latar belakang geser ke atas
            self.cameray -= 1
            self.scroll_y -= 1
        key = pygame.key.get_pressed()
        #key untuk bunny ke kanan
        if key[K_RIGHT]:
            if self.xmovement < 7:
                self.xmovement += 1
            self.direction = 0
        #key untuk bunny ke kiri
        elif key[K_LEFT]:
            if self.xmovement > -7:
                self.xmovement -= 1
            self.direction = 1
        #jika tidak ditekan maka tidak bergerak
        else:
            if self.xmovement > 0:
                self.xmovement -= 1
            elif self.xmovement < 0:
                self.xmovement += 1
        #loop layar horizontal
        if self.playerx > 850:
            self.playerx = -50
        elif self.playerx < -50:
            self.playerx = 850
        self.playerx += self.xmovement
        if self.playery - self.cameray <= 200:
            self.cameray -= 10
        #menggambar animasi pemain
        if not self.direction:
            if self.jump:
                self.screen.blit(self.playerRight_1, (self.playerx, self.playery - self.cameray))
            else:
                self.screen.blit(self.playerRight, (self.playerx, self.playery - self.cameray))
        else:
            if self.jump:
                self.screen.blit(self.playerLeft_1, (self.playerx, self.playery - self.cameray))
            else:
                self.screen.blit(self.playerLeft, (self.playerx, self.playery - self.cameray))
    
    #memperbarui posisi platform dan melakukan pengecekan tabrakan antara pemain dan platform
    def updatePlatforms(self):
        #iterasi melalui setiap platform
        for p in self.platforms:
            #buat objek pygame.Rect untuk area platform
            rect = pygame.Rect(p[0], p[1], self.blog.get_width() - 50, self.blog.get_height())
            #buat objek pygame.Rect untuk area pemain
            player = pygame.Rect(self.playerx, self.playery, self.playerRight.get_width() - 10, self.playerRight.get_height())
            #periksa adanya tabrakan antara pemain dan platform
            if rect.colliderect(player) and self.gravity and self.playery < (p[1] - self.cameray):
                #jika platform bukan tipe 2, atur lompatan dan nonaktifkan gravitasi
                if p[2] != 2:
                    #ketinggianloncatbunny
                    self.jump = 17
                    self.gravity = 0
                #jika platform adalah tipe 2, atur status platform menjadi 1
                else:
                    p[-1] = 1
                #perbarui posisi platform (jika tipe 1)   
            if p[2] == 1:
                if p[-1] == 1:
                    #jika status platform adalah 1, geser platform ke kanan
                    p[0] += 5
                    #jika posisi platform melebihi batas, ubah status menjadi 0
                    if p[0] > 750:
                        p[-1] = 0
                else:
                    # jika status platform adalah 0, geser platform ke kiri
                    p[0] -= 5
                    # jika posisi platform kurang dari atau sama dengan 0, ubah status menjadi 1
                    if p[0] <= 0:
                        p[-1] = 1

    #untuk menggambarkan platform, latar belakang dan springs
    def drawPlatforms(self):
         #menghitung pergeseran latar belakang yang akan digambar
        background_scroll = self.scroll_y % self.background.get_height()
        #menghitung berapa banyak latar belakang yang diperlukan untuk mengisi layar
        visible_backgrounds = int(self.screen.get_height() / self.background.get_height()) + 2
        #loop untuk menggambar latar belakang yang bergulir
        for i in range(-1, visible_backgrounds):
            bg_y = i * self.background.get_height() + background_scroll
            #memastikan agar latar belakang yang tergambar cukup untuk mengisi layar
            if bg_y < self.screen.get_height():
                self.screen.blit(self.background, (0, self.screen.get_height() - bg_y - self.background.get_height()))
        #loop untuk menggambar platform
        for p in self.platforms:
            #menghitung perbedaan tinggi antara platform tertentu dan pemain
            check = self.platforms[1][1] - self.cameray
            #jika pemain mendekati bagian bawah layar
            if check > 600:
                #membuat platform baru secara acak
                platform = random.randint(0, 1000)
                if platform < 800:
                    platform = 0
                elif platform < 900:
                    platform = 1
                else:
                    platform = 2
                #menambahkan platform baru ke daftar
                self.platforms.append([random.randint(0, 700), self.platforms[-1][1] - 50, platform, 0])
                coords = self.platforms[-1]
                #menambahkan spring jika kondisi tertentu terpenuhi
                check = random.randint(0, 1000)
                if check > 900 and platform == 0:
                    self.springs.append([coords[0], coords[1] - 25, 0])
                #menghapus platform paling awal
                self.platforms.pop(0)
                #menambahkan skor dan memperbarui skor tertinggi
                self.score += 1
                if self.score > self.high_score:
                    self.high_score = self.score

            #menggambar platform berdasarkan jenisnya
            if p[2] == 0:
                self.screen.blit(self.blog, (p[0], p[1] - self.cameray))
            elif p[2] == 1:
                self.screen.blit(self.blogmove, (p[0], p[1] - self.cameray))
            elif p[2] == 2:
                if not p[3]:
                    self.screen.blit(self.blogbreak, (p[0], p[1] - self.cameray))
                else:
                    self.screen.blit(self.blogbreak_1, (p[0], p[1] - self.cameray))

        #loop untuk menggambar spring
        for spring in self.springs:
            if spring[-1]:
                self.screen.blit(self.spring_1, (spring[0], spring[1] - self.cameray))
            else:
                self.screen.blit(self.spring, (spring[0], spring[1] - self.cameray))
            #deteksi tabrakan antara pemain dan spring
            if pygame.Rect(spring[0], spring[1], self.spring.get_width(), self.spring.get_height()).colliderect(pygame.Rect(self.playerx, self.playery, self.playerRight.get_width(), self.playerRight.get_height())):
                #ketinggian spring
                self.jump = 30
                self.gravity -= 1

    def generatePlatforms(self):
        #inisialisasi posisi platform di atas layar
        on = 600
        while on > -100:
            #posisi horizontal platform dipilih secara acak
            x = random.randint(0,700)
            #jenis platform dipilih secara acak
            platform = random.randint(0, 1000)
            if platform < 800:
                platform = 0
            elif platform < 900:
                platform = 1
            else:
                platform = 2
            #menambahkan platform ke daftar dengan jenis, posisi, dan status tertentu
            self.platforms.append([x, on, platform, 0])
            #menurunkan posisi platform selanjutnya
            on -= 50
   
    def resetGame(self):
        #mereset kondisi permainan ke awal
        self.cameray = 0
        self.score = 0
        self.springs = []
        #menetapkan satu platform awal di tengah layar
        self.platforms = [[400, 500, 0, 0]]
        #menghasilkan platform-platform tambahan secara acak
        self.generatePlatforms()
        #menetapkan posisi awal pemain
        self.playerx = 400
        self.playery = 400
        #mengatur ketinggian lompatan dan scroll ke nol
        self.jump = 0
        self.scroll_y = 0
        #menetapkan status game over ke False dan menyimpan high score
        self.game_over = False
        self.save_high_score()

    def display_game_over(self, last_score,high_score):
        #menampilkan layar game over dengan skor terakhir dan high score
        game_over_bg = pygame.image.load("assets/game over.png").convert_alpha()
        self.screen.blit(game_over_bg, (0, 0))
        #menampilkan kata game over
        game_over_text = self.font_game_over.render("Game Over!", True, (255, 0, 0))
        self.screen.blit(game_over_text, (200, 170))
        #menampilkan kata score terakhir        
        score_text = self.font_restart_menu.render(f"Your Score^^: {last_score}", True, (255, 255, 255))
        self.screen.blit(score_text, (300, 300))
        #menampilkan kata high score
        high_score_text = self.font_restart_menu.render(f"High Score: {high_score}", True, (255, 255, 255))
        self.screen.blit(high_score_text, (300, 260))
        #menampilkan kata petunjuk tekan space untuk mulai ulang game
        restart_text = self.font_restart_menu.render("Press SPACE to Restart", True, (255, 255, 255))
        self.screen.blit(restart_text, (230, 340))
        #menampilkan kata petunjuk tekan M untuk kembali ke main menu
        main_menu_text = self.font_restart_menu.render("Press M to Go Back to Main Menu", True, (255, 255, 255))
        self.screen.blit(main_menu_text, (150, 380))

        #memberhentikan BGM game play
        pygame.mixer.music.stop()
        #memainkan SFX game over
        self.game_over_sfx.play()
        pygame.display.flip()

        while True:
            #jika click quit button maka ditutup
            for event in pygame.event.get():
                if event.type == QUIT:
                    #BGM game dimatikan
                    pygame.mixer.music.stop()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    #jika menekan space maka game akan dimulai kembali
                    if event.key == pygame.K_SPACE:
                        #musik game dimulai kembali
                        pygame.mixer.music.play(-1)
                        self.resetGame()
                        #Sfx game over stop
                        self.game_over_sfx.stop()
                        return
                    #jika menekan M maka akan kembali ke main menu
                    elif event.key == pygame.K_m:
                        main_menu()
                        
    def load_high_score(self):
        try:
            #membaca high score dari file teks
            with open("assets/high_score.txt", "r") as file:
                self.high_score = int(file.read())
        except FileNotFoundError:
            #jika file tidak ditemukan, tetapkan high score ke 0
            self.high_score = 0

    def save_high_score(self):
        #menyimpan high score ke dalam file teks
        with open("assets/high_score.txt", "w") as file:
            file.write(str(self.high_score))

    def run(self):
        clock = pygame.time.Clock()
        #memuat high score sebelum memulai permainan
        self.load_high_score()
        #menghasilkan platform-platform awal secara acak
        self.generatePlatforms()
        while True:
            self.screen.fill((255,255,255))
            clock.tick(45)
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.mixer.music.stop()
                    sys.exit()
            #menjalankan logika permainan, menggambar elemen-elemen, dan memperbarui layar
            if self.playery - self.cameray > 700:
                self.game_over = True
                self.display_game_over(self.score, self.high_score)
            background_scroll = self.scroll_y % self.background.get_height()
            self.screen.blit(self.background, (0, -background_scroll,))
            self.drawPlatforms()
            self.updatePlayer()
            self.updatePlatforms()
            #membuat teks high score dan score
            self.screen.blit(self.font.render("Score: " + str(self.score), -1, (255, 255, 255)), (25, 55))
            self.screen.blit(self.font.render("High Score: " + str(self.high_score), -1, (255, 255, 255)), (25, 25))
            
            pygame.display.flip() 

#CODE UNTUK MAIN MENU

#ukuran layar main menu
SCREEN = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Hopping Bun")
#memanggil gambar background
BG = pygame.image.load("assets/main_bg.png")

class Button():
    def __init__(self, image, pos):
        #inisialisasi objek tombol dengan gambar dan posisi yang diberikan
        self.image = image #menyimpan gambar yang akan digunakan sebagai tombol
        self.x_pos = pos[0] #menyimpan koordinat x posisi tombol
        self.y_pos = pos[1] #menyimpan koordinat y posisi tombol
        #jika terdapat gambar, buat rect sesuai dengan gambar
        if self.image is not None:
            self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        #memperbarui tampilan layar dengan gambar tombol
        if self.image is not None:
            screen.blit(self.image, self.rect)

    def checkForInput(self, position):
        #memeriksa apakah posisi mouse berada dalam batas tombol
        if self.image is not None and position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            #jika iya, kembalikan True, menunjukkan bahwa tombol ditekan
            return True
        #jika tidak, kembalikan False
        return False

#UNTUK MEMAINKAN Hopping Bun
def play():
    hopping_bun_game = HoppingBunGame()
    while True:
        hopping_bun_game.run()

#UNTUK MENAMPILKAN MAINMENU
def main_menu():
    pygame.init()
    #Inisialisasi mixer
    pygame.mixer.init()
    #background music main menu
    pygame.mixer.music.load("assets/menu_bgm.mp3")
    #mainkan bgm
    pygame.mixer.music.play(-1)
    while True:
        #ukuran layar main menu
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()
        #memanggil assets button
        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(673, 450))
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(673, 535))
         
        for event in pygame.event.get():
            #jika click close maka ditutup
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                #jika clic kbutton play code game dimulai
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.mixer.music.stop()
                    play()
                #jika click quit butto nmaka ditutup
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.mixer.music.stop()
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
# Memanggil fungsi main_menu untuk memulai permainan
main_menu()
