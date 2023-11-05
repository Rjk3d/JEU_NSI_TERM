import pyautogui
import pygame
import pygame.freetype
import ast

def menu_mini_jeu(user="User1",deb=False):

    if deb:
        pygame.mixer.music.unload()
        pygame.mixer.quit()

        pygame.init()
        logo_jeu = pygame.image.load("visual/logo_jeu2.png")
        pygame.display.set_icon(logo_jeu)

        pygame.mixer.init()
        pygame.mixer.music.load("sound/musique_menu_comp.mp3")
        pygame.mixer.music.set_volume(0.7)
        pygame.mixer.music.play(-1)  # faire tourner en boucle
    screen = pygame.display.set_mode((1280, 720))
    GAME_FONT = pygame.freetype.Font("for_construction/font.ttf", 24)

    bg = pygame.image.load("visual/menu_background2.jpg")
    bg = pygame.transform.scale(bg, (1280, 720))

    ar_menu=pygame.image.load("visual/ar_menu.png") #585*427
    ar_menu.set_colorkey([255,255,255])

    trs_btn = pygame.image.load("visual/personnalisation_btn.png")
    trs_btn = pygame.transform.scale(trs_btn, (60, 60))

    gemme=pygame.image.load("visual/gem.png")
    gemme = pygame.transform.scale(gemme,(30,30))

    switch = pygame.image.load("visual/switch.png")
    switch = pygame.transform.scale(switch, (41, 41))

    img_mj1=pygame.image.load("visual/ic_mj1.png")
    img_mj1 = pygame.transform.scale(img_mj1, (60, 60))

    txt_mode_mini_jeu, rect = GAME_FONT.render("MINI JEUX (Gagnez un max de gemmes!)", (255, 255, 255))

    pygame.display.set_caption("Menu Mini Jeux")

    with open("sauvegarde.txt", "r") as fichier:
        for elem in fichier:
            dict = ast.literal_eval(elem)
            solde = dict[user]["Solde"]

    text_solde, rect = GAME_FONT.render(solde,(255,255,255))

    run=True
    while run:
        clock = pygame.time.Clock()

        screen.blit(bg,(0,0))
        screen.blit(ar_menu, ((1280 - 585) / 2, (720 - 427) / 2))
        screen.blit(trs_btn, (0, 0))

        screen.blit(txt_mode_mini_jeu, ((1280 - list(txt_mode_mini_jeu.get_rect())[-2])/2, 10))
        screen.blit(text_solde, (1250-list(text_solde.get_rect())[-2], 10))
        screen.blit(gemme, (1250, 5))
        screen.blit(switch, (7, 60))
        screen.blit(img_mj1, (410, 200))

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 0<=event.pos[0]<=60 and 0<=event.pos[1]<=60:
                    import get_user
                    get_user.get_user("mj")
                if 410<=event.pos[0]<=470 and 200<=event.pos[1]<=260:
                    pyautogui.alert("Il parait que des gemmes apparaissent dans l'espace toutes les 30 secondes...Mais attention aux météorites!")
                    import mini_jeu1
                    mj1 = mini_jeu1.mini_jeu1()
                    mj1.run()
                if 7<=event.pos[0]<=48 and 60<=event.pos[1]<=101:
                    import main
                    main.main_menu(deb=False)

            clock.tick(60)

            if event.type==pygame.QUIT:
                run=False
                pygame.quit()

        pygame.display.update()

    pygame.quit()

if __name__=='__main__':
    menu_mini_jeu()