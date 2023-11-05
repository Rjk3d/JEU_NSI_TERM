import pygame
import ast
from pygame.locals import *
import pygame.freetype
import pytmx
import pyscroll
import pyautogui
import player

pygame.init()

#PROJECT_ROOT = pathlib.Path(__file__).parent
#SCREEN = pygame.display.set_mode((1280, 720))
GAME_FONT = pygame.freetype.Font("for_construction/font.ttf", 24)

class Game:
    def __init__(self,niv=1,nbr_alert=0, monde=1,user="User1",skin="visual/perso_mec/mec3.png"):
        assert monde==1 or monde==2,"monde ne peut être que 1 ou 2"
        pygame.mixer.music.unload()
        pygame.mixer.quit()
        pygame.mixer.init()
        if monde==1:
            pygame.mixer.music.load("sound/creepy-devil.mp3")
        elif monde==2:
            pygame.mixer.music.load("sound/monde2musique.mp3")
        pygame.mixer.music.set_volume(0.7)
        pygame.mixer.music.play(-1)

        self.user=user
        self.monde="Monde"+str(monde)
        self.screen = pygame.display.set_mode((1280, 720))
        self.img_menu = pygame.image.load("visual/img_menu.png")
        self.img_menu = pygame.transform.scale(self.img_menu, (60, 60))


        pygame.display.set_caption('The impossible (casse pas ton écran)')
        if monde==1:
            tmx_carte1 = pytmx.util_pygame.load_pygame('cartes/carte 1.tmx')
            if niv>=3:
                tmx_carte1 = pytmx.util_pygame.load_pygame('cartes/carte 1 piege.tmx') #ajout de murs piégés
        if monde==2:
            tmx_carte1 = pytmx.util_pygame.load_pygame('cartes/carte 2.tmx')
            if niv>=3:
                tmx_carte1 = pytmx.util_pygame.load_pygame('cartes/carte 2 piege.tmx')
        self.statue_trouve_int = 0
        self.statue_trouve = str(self.statue_trouve_int)
        data_carte1 = pyscroll.data.TiledMapData(tmx_carte1) #récupère la map depuis tiled
        carte1_layer = pyscroll.orthographic.BufferedRenderer(data_carte1, self.screen.get_size())
        carte1_layer.zoom = 4
        if niv>=5:
            carte1_layer.zoom = 10 #le niveau doit être très zoomé
        self.level = 1
        self.niv = niv
        self.lst_time_init=[]
        self.nbr_alert=nbr_alert

        with open("sauvegarde.txt", "r") as fichier:
            for elem in fichier:
                dict = ast.literal_eval(elem)
                self.solde = int(dict[self.user]["Solde"]) # quantité de gemmes
                self.niv_taille = int(dict[self.user]["niv_taille"]) # taille du perso

        player_position = tmx_carte1.get_object_by_name("point d'apparition")

        tailles_possibles=[1,0.90625,0.8125,0.75,0.625]

        taille=tailles_possibles[self.niv_taille]
        self.player = player.Player(player_position.x, player_position.y,skin=skin,taille=taille)

        self.statue_sound = pygame.mixer.Sound("sound/short-success-sound.mp3")
        self.victory_sound = pygame.mixer.Sound("sound/success-sound.mp3")

        self.walls = []
        self.walls_piege = []
        self.invisible_walls = []
        self.statue = []
        self.statue1 = []
        self.statue2 = []
        self.statue3 = []
        self.statue4 = []
        self.statue5 = []
        self.table = []



        for obj in tmx_carte1.objects:
            if obj.type == "collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            elif obj.type == "mur_piege": # mur_piege ou poison selon le monde 1 ou 2
                self.walls_piege.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            elif obj.type == "poison":
                self.walls_piege.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            elif obj.type == "invisible":
                self.invisible_walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        for statue in tmx_carte1.objects:
            if statue.type == "statue":
                self.statue.append(pygame.Rect(statue.x, statue.y, statue.width, statue.height))

        for statue1 in tmx_carte1.objects:
            if statue1.name == "statue1":
                statue1.visible=0
                self.statue1.append(pygame.Rect(statue1.x, statue1.y, statue1.width, statue1.height))
        for statue2 in tmx_carte1.objects:
            if statue2.name == "statue2":
                self.statue2.append(pygame.Rect(statue2.x, statue2.y, statue2.width, statue2.height))
        for statue3 in tmx_carte1.objects:
            if statue3.name == "statue3":
                self.statue3.append(pygame.Rect(statue3.x, statue3.y, statue3.width, statue3.height))
        for statue4 in tmx_carte1.objects:
            if statue4.name == "statue4":
                self.statue4.append(pygame.Rect(statue4.x, statue4.y, statue4.width, statue4.height))
        for statue5 in tmx_carte1.objects:
            if statue5.name == "statue5":
                self.statue5.append(pygame.Rect(statue5.x, statue5.y, statue5.width, statue5.height))
        for table in tmx_carte1.objects:
            if table.name == "table":
                self.table.append(pygame.Rect(table.x, table.y, table.width, table.height))

        self.group = pyscroll.PyscrollGroup(map_layer=carte1_layer, default_layer=2)
        self.group.add(self.player)

    def handle_input(self):
        """
        gère les mouvements en appelant les fonctions de player si l'on appuie sur les bonnes touches, et gère l'inversion des touches pour le monde 6
        """
        pressed = pygame.key.get_pressed()
        if self.niv<6:
            if pressed[K_UP] or pressed[K_z]: #la touche qui sert à aller vers le haut
                self.player.move_up()
                self.player.change_animation('up')
            elif pressed[K_DOWN] or pressed[K_s]: #la touche qui sert à aller vers le bas
                self.player.move_down()
                self.player.change_animation('down')
            elif pressed[K_LEFT] or pressed[K_q]: #la touche qui sert à aller vers la gauche
                self.player.move_left()
                self.player.change_animation('left')
            elif pressed[K_RIGHT] or pressed[K_d]: #la touche qui sert à aller vers la droite
                self.player.move_right()
                self.player.change_animation('right')
        else:  # Dans le niveau 6, les touches sont inversées
            if pressed[K_UP] or pressed[K_z]:
                self.player.move_down()
                self.player.change_animation('down')
            elif pressed[K_DOWN] or pressed[K_s]:
                self.player.move_up()
                self.player.change_animation('up')
            elif pressed[K_LEFT] or pressed[K_q]:
                self.player.move_right()
                self.player.change_animation('right')
            elif pressed[K_RIGHT] or pressed[K_d]:
                self.player.move_left()
                self.player.change_animation('left')


    def update(self):
        """
        s'occupe de toutes les actions et affichages à faire constamment comme les collisions, les statues pour le score, la réussite des niveaux...
        """
        self.group.update()

        for sprite in self.group.sprites(): #traite les avatars
            if sprite.feet.collidelist(self.walls) > -1:
                sprite.move_back()
            elif sprite.feet.collidelist(self.invisible_walls) > -1 and self.niv>=4:
                sprite.move_back()
            elif sprite.feet.collidelist(self.walls_piege) > -1:
                mort = pygame.mixer.Sound("sound/death-sound.mp3")
                mort.play()
                pygame.mixer.music.stop()
                import main
                main.main_menu(user=self.user)


            elif sprite.feet.collidelist(self.statue) > -1:

                if sprite.feet.collidelist(self.statue1) > -1:
                    self.statue_sound.play()
                    self.statue_trouve_int += 1
                    self.statue_trouve = str(self.statue_trouve_int)
                    self.statue1 = []
                elif sprite.feet.collidelist(self.statue2) > -1:
                    self.statue_sound.play()
                    self.statue_trouve_int += 1
                    self.statue_trouve = str(self.statue_trouve_int)
                    self.statue2 = []
                elif sprite.feet.collidelist(self.statue3) > -1:
                    self.statue_sound.play()
                    self.statue_trouve_int += 1
                    self.statue_trouve = str(self.statue_trouve_int)
                    self.statue3 = []
                elif sprite.feet.collidelist(self.statue4) > -1:
                    self.statue_sound.play()
                    self.statue_trouve_int += 1
                    self.statue_trouve = str(self.statue_trouve_int)
                    self.statue4 = []
                elif sprite.feet.collidelist(self.statue5) > -1:
                    self.statue_sound.play()
                    self.statue_trouve_int += 1
                    self.statue_trouve = str(self.statue_trouve_int)
                    self.statue5 = []
            elif sprite.feet.collidelist(self.table) > -1 and self.statue_trouve_int == 5 and self.niv==1:
                with open("sauvegarde.txt", "r") as fichier:
                    for elem in fichier:
                        dict = ast.literal_eval(elem)
                        niv_reussi = int(dict[self.user][self.monde])

                        if int(niv_reussi) <= 1:
                            dict[self.user][self.monde] = "1"

                self.solde += 1
                pyautogui.alert("En passant le portail vous avez trouvé une gemme !")
                dict[self.user]["Solde"] = str(self.solde)
                a = str(dict)
                with open("sauvegarde.txt", "w") as fichier:
                    fichier.write(a)
                pygame.mixer.music.stop()
                self.victory_sound.play()
                import main
                main.main_menu(user=self.user)

            elif sprite.feet.collidelist(self.table) > -1 and self.statue_trouve_int == 5 and self.niv==2:
                with open("sauvegarde.txt", "r") as fichier:
                    for elem in fichier:
                        dict = ast.literal_eval(elem)
                        niv_reussi = int(dict[self.user][self.monde])
                        if int(niv_reussi) <= 2:
                            dict[self.user][self.monde] = "2"
                            dict[self.user]["Solde"] = self.solde
                self.solde += 2
                pyautogui.alert("Vous avez trouvé 2 nouvelles gemmes !")
                dict[self.user]["Solde"] = str(self.solde)
                a=str(dict)
                with open("sauvegarde.txt", "w") as fichier:
                    fichier.write(a)
                pygame.mixer.music.stop()
                self.victory_sound.play()
                import main
                main.main_menu(user=self.user)
            elif sprite.feet.collidelist(self.table) > -1 and self.statue_trouve_int == 5 and self.niv==3:
                with open("sauvegarde.txt", "r") as fichier:
                    for elem in fichier:
                        dict = ast.literal_eval(elem)
                        niv_reussi = int(dict[self.user][self.monde])
                        if int(niv_reussi) <= 3:
                            dict[self.user][self.monde] = "3"
                self.solde += 3
                pyautogui.alert("Vous avez trouvé 3 nouvelles gemmes !")
                dict[self.user]["Solde"] = str(self.solde)
                a = str(dict)
                with open("sauvegarde.txt", "w") as fichier:
                    fichier.write(a)
                pygame.mixer.music.stop()
                self.victory_sound.play()
                import main
                main.main_menu(user=self.user)
            elif sprite.feet.collidelist(self.table) > -1 and self.statue_trouve_int == 5 and self.niv==4:
                with open("sauvegarde.txt", "r") as fichier:
                    for elem in fichier:
                        dict = ast.literal_eval(elem)
                        niv_reussi = int(dict[self.user][self.monde])
                        if int(niv_reussi) <= 4:
                            dict[self.user][self.monde] = "4"
                self.solde += 4
                pyautogui.alert("Vous avez trouvé 4 nouvelles gemmes !")
                dict[self.user]["Solde"] = str(self.solde)
                a = str(dict)
                with open("sauvegarde.txt", "w") as fichier:
                    fichier.write(a)
                pygame.mixer.music.stop()
                self.victory_sound.play()
                import main
                main.main_menu(user=self.user)
            elif sprite.feet.collidelist(self.table) > -1 and self.statue_trouve_int == 5 and self.niv==5:
                with open("sauvegarde.txt", "r") as fichier:
                    for elem in fichier:
                        dict = ast.literal_eval(elem)
                        niv_reussi = int(dict[self.user][self.monde])
                        if int(niv_reussi) <= 5:
                            dict[self.user][self.monde] = "5"

                self.solde += 5
                pyautogui.alert("Vous avez trouvé 5 nouvelles gemmes !")
                dict[self.user]["Solde"] = str(self.solde)
                a = str(dict)
                with open("sauvegarde.txt", "w") as fichier:
                    fichier.write(a)
                pygame.mixer.music.stop()
                self.victory_sound.play()
                import main
                main.main_menu(user=self.user)
            elif sprite.feet.collidelist(self.table) > -1 and self.statue_trouve_int == 5 and self.niv==6:
                with open("sauvegarde.txt", "r") as fichier:
                    for elem in fichier:
                        dict = ast.literal_eval(elem)
                        niv_reussi = int(dict[self.user][self.monde])
                        if int(niv_reussi) <= 6:
                            dict[self.user][self.monde] = "6"

                self.solde += 6
                pyautogui.alert("Vous avez trouvé 6 nouvelles gemmes !")
                dict[self.user]["Solde"] = str(self.solde)
                a = str(dict)
                with open("sauvegarde.txt", "w") as fichier:
                    fichier.write(a)
                pygame.mixer.music.stop()
                self.victory_sound.play()
                import main
                main.main_menu(user=self.user)


    def temps(self,temps_max_sec):
        """
        Crée et affiche le décompte du temps restant pour finir le niveau. Renvoi au menu si le temps est à 0.

        :param temps_max_sec: le temps maximum pour réaliser le niveau
        """
        assert temps_max_sec>0,"Le temps doit être supérieur à 0"
        if len(self.lst_time_init)==0:
            self.lst_time_init.append(int(pygame.time.get_ticks()/1000))

        temps_max = temps_max_sec
        temps_restant = temps_max - int(int(pygame.time.get_ticks()/1000)-self.lst_time_init[0])
        text_temps, rect = GAME_FONT.render(str(temps_restant),(255,163,26))
        self.screen.blit(text_temps, (70, 15))
        if temps_restant == 0:
            ouch = pygame.mixer.Sound("sound/death-sound.mp3")
            ouch.play()
            pygame.mixer.music.stop()
            import main
            main.main_menu(user=self.user)


    def run(self):
        """
        La fonction principale du mode histoire
        """
        clock = pygame.time.Clock()
        pygame.mixer.music.play(-1) #pour le passer en boucle

        run = True
        while run:
            self.player.save_location()
            self.handle_input()
            self.update()
            self.group.center(self.player.rect.center)
            self.group.draw(self.screen)

            text_statue, rect = GAME_FONT.render(self.statue_trouve + "/5", (255,163,26))
            self.screen.blit(text_statue, (1150, 15))

            self.screen.blit(self.img_menu, (1, 1))

            if self.niv==1:
                if self.nbr_alert==0:
                    pyautogui.alert("5 totems ont été éparpillés dans le labyrinthe ! retrouve les tous pour activer le portail de sortie et sortir de cet étrange labyrinthe ")
                    self.nbr_alert+=1
            if self.niv>=2:
                if self.nbr_alert==1:
                    pyautogui.alert("ATTENTION ! Une limite de temps a été ajoutée, qui sait ce qui pourrait arriver si le temps venait à s'écouler... ")
                    self.nbr_alert+=1
                Game.temps(self,140)
            if self.niv==3:
                if self.nbr_alert==2:
                    pyautogui.alert(" D'étranges murs sont apparus ! Ils ne m'inspirent pas confiance... Evite de les toucher !")
                    self.nbr_alert += 1
            if self.niv==4:
                if self.nbr_alert==3:
                    pyautogui.alert(" Etrange... Il semblerait que des murs invisibles empêchent de passer sur certaines cases...")
                    self.nbr_alert += 1
            if self.niv==5:
                if self.nbr_alert==4:
                    pyautogui.alert(" On n'y voit vraiment rien décidément. Garde les yeux grands ouverts ! ")
                    self.nbr_alert += 1
            if self.niv==6:
                if self.nbr_alert==5:
                    pyautogui.alert("L'air paraît bizarre... Tout semble inversé ! ")
                    self.nbr_alert += 1

            if self.niv==1:
                if self.nbr_alert == 6:
                    pyautogui.alert("GLAGLAGLA il fait froid ! Dépêche-toi de trouver tous les totems pour sortir de cet endroit glacial")
                    self.nbr_alert += 1
            if self.niv == 2:
                if self.nbr_alert == 7:
                    pyautogui.alert("Fais vite, si tu mets trop de temps, les engelures auront raison de toi !")
                    self.nbr_alert += 1
            if self.niv == 3:
                if self.nbr_alert == 8:
                    pyautogui.alert("Attention, la glace a laissé place à du poison sur certaines zones, à ne pas toucher!")
                    self.nbr_alert += 1

            if self.niv == 4:
                if self.nbr_alert == 9:
                    pyautogui.alert("La glace semble avoir rendu impossible le passage sur certaines cases...")
                    self.nbr_alert += 1

            if self.niv == 5:
                if self.nbr_alert == 10:
                    pyautogui.alert("* Le froid mordant t'empêche d'ouvrir pleinement les yeux *")
                    self.nbr_alert += 1

            if self.niv == 6:
                if self.nbr_alert == 11:
                    pyautogui.alert("La glace a rendu le sol glissant, attention à tes déplacement!")
                    self.nbr_alert += 1




            pygame.display.flip()


            for event in pygame.event.get():

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if 1 <= event.pos[0] <= 60 and 1 <= event.pos[1] <= 60: #correspond au bouton HOME
                        pygame.mixer.music.stop()
                        import main
                        main.main_menu(user=self.user)

                if event.type == pygame.QUIT: # appui de la croix rouge en haut à droite de la fenêtre
                    run = False
                    pygame.quit()
                    quit()

            clock.tick(60)

#game1=Game(niv=6,nbr_alert=5)
#game1.run()