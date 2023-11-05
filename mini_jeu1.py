import pygame
import random
import ast
from pygame.locals import *
import pygame.freetype
from player import Player

pygame.init()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
GAME_FONT = pygame.freetype.Font("for_construction/font.ttf", 24)
pygame.display.set_caption("Jeu de météores")

class Meteor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.original_image = pygame.image.load("visual/projectile.png")
        self.original_image = pygame.transform.scale(self.original_image,(30,30))
        self.image=self.original_image
        self.rect = self.image.get_rect()
        self.gauche_ou_haut = random.randint(0, 1)
        if self.gauche_ou_haut==1:
            self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
            self.rect.y = random.randint(-100, -40)
            self.speedy = random.randint(5, 7)
        else:
            self.rect.x = random.randint(-100, -40)
            self.rect.y = random.randint(0, SCREEN_HEIGHT - self.rect.height)
            self.speedy = random.randint(5, 7)
        self.rotation_angle = 0

    def update(self):
        if self.gauche_ou_haut==1:
            self.rect.y += self.speedy
            if self.rect.top > SCREEN_HEIGHT:
                self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
                self.rect.y = random.randint(-100, -40)
                self.speedy = random.randint(3, 10)
        else:
            self.rect.x += self.speedy
            if self.rect.left > SCREEN_WIDTH:
                self.rect.x = 10
                self.rect.y = random.randint(0, SCREEN_HEIGHT - self.rect.height)
                self.speedy = random.randint(3, 10)
        self.rotation_angle = (self.rotation_angle + 5) % 360
        self.image = pygame.transform.rotate(self.original_image, self.rotation_angle)


class mini_jeu1:
    def __init__(self,user="User1"):
        pygame.mixer.music.unload()
        pygame.mixer.quit()
        pygame.mixer.init()
        pygame.mixer.music.load("sound/mj1.mp3")
        pygame.mixer.music.set_volume(0.7)
        pygame.mixer.music.play(-1)

        self.user=user
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Mini jeu 1")
        self.all_sprites = pygame.sprite.Group()
        self.meteors = pygame.sprite.Group()
        with open("skin.txt", "r") as f:
            for l in f:
                skin = l

        self.player = Player(600,500,taille=2.5,speed=6,skin=skin)
        self.all_sprites.add(self.player)
        self.lst_time_init = []

        self.img_menu = pygame.image.load("visual/img_menu.png")
        self.img_menu = pygame.transform.scale(self.img_menu, (60, 60))
        self.img_fond = pygame.image.load("visual/fond_mini_jeu.jpeg")
        self.img_fond = pygame.transform.scale(self.img_fond, (1280, 720))

        self.meteor_add = False

        with open("sauvegarde.txt", "r") as fichier:
            for elem in fichier:
                dict = ast.literal_eval(elem)
                self.solde = int(dict[self.user]["Solde"])
                self.niv_taille = int(dict[self.user]["niv_taille"])

        self.text_solde, rect = GAME_FONT.render(str(self.solde), (255, 255, 255))
        gemme = pygame.image.load("visual/gem.png")
        self.gemme = pygame.transform.scale(gemme, (30, 30))

        self.nbr_meteor=3

        for _ in range(self.nbr_meteor):
            meteor = Meteor()
            self.all_sprites.add(meteor)
            self.meteors.add(meteor)
        pygame.init()

    def handle_input(self):
        """
        gère les mouvements en appelant les fonctions de player si l'on appuie sur les bonnes touches, et gère l'inversion des touches pour le monde 6
        """
        pressed = pygame.key.get_pressed()

        if pressed[K_UP] and self.player.get_pos()[1] > 0 or pressed[K_z] and self.player.get_pos()[1] > 0:
            self.player.move_up()
            self.player.change_animation('up')
        elif pressed[K_DOWN] and self.player.get_pos()[1] < 660 or pressed[K_s] and self.player.get_pos()[1] < 660:
                self.player.move_down()
                self.player.change_animation('down')
        elif pressed[K_LEFT] and self.player.get_pos()[0]>0 or pressed[K_q] and self.player.get_pos()[0]>0:
            self.player.move_left()
            self.player.change_animation('left')
        elif pressed[K_RIGHT] and self.player.get_pos()[0] < 1245 or pressed[K_d] and self.player.get_pos()[0] < 1245:
            self.player.move_right()
            self.player.change_animation('right')

    def add_solde(self,a_ajoute):
        """
        Ajoute la quantité a_ajoute à la valeur de la clé solde dans le dictionnaire du fichier sauvegarde
        :param a_ajoute: la quantité à ajouter au solde
        """
        with open("sauvegarde.txt", "r") as fichier:
            for elem in fichier:
                dict = ast.literal_eval(elem)
                self.solde += a_ajoute
                dict[self.user]["Solde"] = self.solde

        dict[self.user]["Solde"] = str(self.solde)
        a = str(dict)
        with open("sauvegarde.txt", "w") as fichier:
            fichier.write(a)
        self.solde = int(dict[self.user]["Solde"])
        self.text_solde, rect = GAME_FONT.render(str(self.solde), (255, 255, 255))
        self.a_ete_ajoute=True#permet de l'ajouter qu'une seule fois

    def temps(self):
        """
        crée et affiche le chrono, et ajoute 1 gemme au solde toutes les 20 secondes
        """
        if len(self.lst_time_init)==0:
            self.lst_time_init.append(int(pygame.time.get_ticks()/1000))
        temps = 0
        temps = temps + int(int(pygame.time.get_ticks()/1000)-self.lst_time_init[0])
        text_temps, rect = GAME_FONT.render(str(temps),(255,163,26))
        self.screen.blit(text_temps, (70, 15))
        if temps%30==0 and temps>0 and self.a_ete_ajoute==False:
            self.add_solde(int(temps/30))
        if temps % 31 == 0:
            self.a_ete_ajoute=False
        if temps%7==0 and temps>0 and self.meteor_add==False:
            meteor = Meteor()
            self.nbr_meteor+=1
            self.all_sprites.add(meteor)
            self.meteors.add(meteor)
            self.meteor_add=True
        if temps % 8 == 0 and temps%56!=0:
            self.meteor_add=False

    def run(self):
        running = True
        clock = pygame.time.Clock()
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
            self.handle_input()

            self.all_sprites.update()
            self.screen.blit(self.img_fond, (0, 0))
            self.screen.blit(self.img_menu, (1, 1))
            self.screen.blit(self.text_solde, (1250 - list(self.text_solde.get_rect())[-2], 10))
            self.screen.blit(self.gemme, (1250, 5))

            hits = pygame.sprite.spritecollide(self.player, self.meteors, False)
            if hits:
                pygame.mixer.music.stop()
                import menu_mini_jeu as mmj
                mmj.menu_mini_jeu(deb=True)

            self.all_sprites.draw(self.screen)
            self.temps()
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if 1 <= event.pos[0] <= 60 and 1 <= event.pos[1] <= 60:
                        pygame.mixer.music.stop()
                        import main
                        main.main_menu(user=self.user)

                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    quit()

            clock.tick(60)


if __name__=='__main__':
    game1 = mini_jeu1()
    game1.run()