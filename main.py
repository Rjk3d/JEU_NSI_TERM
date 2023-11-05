import pyautogui
import pygame
import pygame.freetype
import game
import ast
import menu_mini_jeu as mmj

def main_menu(user="User1", deb=True):
    skin="visual/perso_mec/mec1.png"
    with open("skin.txt","r") as f:
        for l in f:
            skin=l
    if deb:
        pygame.mixer.music.unload()
        pygame.mixer.quit()

        pygame.init()
        logo_jeu=pygame.image.load("visual/logo_jeu2.png")
        pygame.display.set_icon(logo_jeu)

        pygame.mixer.init()
        pygame.mixer.music.load("sound/musique_menu_comp.mp3")
        pygame.mixer.music.set_volume(0.7)
        pygame.mixer.music.play(-1) #faire tourner en boucle


    screen = pygame.display.set_mode((1280, 720))
    GAME_FONT = pygame.freetype.Font("for_construction/font.ttf", 24)


    bg = pygame.image.load("visual/menu_background2.jpg")
    bg = pygame.transform.scale(bg, (1280, 720))


    ar_menu=pygame.image.load("visual/ar_menu.png") #585*427
    ar_menu.set_colorkey([255,255,255])

    trs_btn = pygame.image.load("visual/personnalisation_btn.png")
    trs_btn = pygame.transform.scale(trs_btn, (60, 60))

    ar_niv=pygame.image.load("visual/ar_niv.png")#134 × 137
    ar_niv_reussi=pygame.image.load("visual/ar_niv_reussi.png")#129 × 139

    gemme=pygame.image.load("visual/gem.png")
    gemme = pygame.transform.scale(gemme,(30,30))

    switch = pygame.image.load("visual/switch.png")
    switch = pygame.transform.scale(switch, (41, 41))

    barres_tailles=[]
    for i in range(1,6):
        barres_tailles.append(f"barre{i}.png")
    barre1=pygame.image.load("visual/barre_taille/"+barres_tailles[0])
    barre1=pygame.transform.scale(barre1,(350,35))
    barre2=pygame.image.load("visual/barre_taille/"+barres_tailles[1])
    barre2=pygame.transform.scale(barre2,(350,35))
    barre3=pygame.image.load("visual/barre_taille/"+barres_tailles[2])
    barre3 = pygame.transform.scale(barre3, (350, 35))
    barre4=pygame.image.load("visual/barre_taille/"+barres_tailles[3])
    barre4 = pygame.transform.scale(barre4, (350, 35))
    barre5=pygame.image.load("visual/barre_taille/"+barres_tailles[4])
    barre5 = pygame.transform.scale(barre5, (350, 35))

    btn_aug=pygame.image.load("visual/barre_taille/btn_aug.png")
    btn_aug = pygame.transform.scale(btn_aug,(40,40))
    btn_rap=pygame.image.load("visual/barre_taille/btn_rap.png")
    btn_rap = pygame.transform.scale(btn_rap,(40,40))


    ar_niv = pygame.transform.scale(ar_niv, (60, 60))
    ar_niv_reussi = pygame.transform.scale(ar_niv_reussi, (60, 60))

    txt_niv, rect = GAME_FONT.render("Monde 1", (255, 255, 255))
    txt_niv2, rect = GAME_FONT.render("Monde 2", (255, 255, 255))

    txt_mode_h, rect = GAME_FONT.render("MODE HISTOIRE", (255, 255, 255))


    pygame.display.set_caption("Menu")



    run=True
    while run:
        clock = pygame.time.Clock()

        with open("sauvegarde.txt", "r") as fichier:
            for elem in fichier:
                dict = ast.literal_eval(elem)
                nbr_niv_reussi = int(dict[user]["Monde1"])
                nbr_niv_reussi2 = int(dict[user]["Monde2"])
                solde = dict[user]["Solde"]

        text_solde, rect = GAME_FONT.render(solde, (255, 255, 255))




        screen.blit(bg,(0,0))
        screen.blit(ar_menu, ((1280 - 585) / 2, (720 - 427) / 2))
        screen.blit(trs_btn, (0, 0))
        screen.blit(txt_niv,(560,220))
        screen.blit(txt_niv2, (560, 350))
        screen.blit(txt_mode_h, ((1280 - list(txt_mode_h.get_rect())[-2])/2, 10))
        screen.blit(text_solde, (1250-list(text_solde.get_rect())[-2], 10))
        screen.blit(gemme, (1250, 5))
        screen.blit(switch, (7, 60))

        with open("sauvegarde.txt", "r") as fichier:
            for elem in fichier:
                dict = ast.literal_eval(elem)
        niv_taille = int(dict[user]["niv_taille"])

        if niv_taille==0:
            screen.blit(barre1,(465,480))
        elif niv_taille==1:
            screen.blit(barre2, (465,480))
        elif niv_taille==2:
            screen.blit(barre3, (465,480))
        elif niv_taille==3:
            screen.blit(barre4, (465,480))
        elif niv_taille==4:
            screen.blit(barre5, (465,480))

        screen.blit(btn_rap, (410, 477))
        screen.blit(btn_aug,(830,477))

        for i in range(1,7):
            if nbr_niv_reussi>=i:
                screen.blit(ar_niv_reussi, (330+i*80, 270))
            else:
                screen.blit(ar_niv, (330+i*80, 270))

        for i in range(1,7):
            if nbr_niv_reussi2>=i:
                screen.blit(ar_niv_reussi, (330+i*80, 400))
            else:
                screen.blit(ar_niv, (330+i*80, 400))


        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 0<=event.pos[0]<=60 and 0<=event.pos[1]<=60:
                    import get_user
                    get_user.get_user()
                if 7<=event.pos[0]<=48 and 60<=event.pos[1]<=101:
                    mmj.menu_mini_jeu()

                if 410<=event.pos[0]<=450 and 477<=event.pos[1]<=517:#(410, 477)
                    with open("sauvegarde.txt", "r") as fichier:
                        for elem in fichier:
                            dict = ast.literal_eval(elem)

                    taille_debloque = dict[user]["niv_taille_deb"]
                    if dict[user]["niv_taille"]>=1:
                        dict[user]["niv_taille"]-=1
                    a = str(dict)
                    with open("sauvegarde.txt", "w") as fichier:
                        fichier.write(a)
                #(830,477)
                if 830<=event.pos[0]<=870 and 477<=event.pos[1]<=517:#(410, 477)
                    with open("sauvegarde.txt", "r") as fichier:
                        for elem in fichier:
                            dict = ast.literal_eval(elem)

                    taille = dict[user]["niv_taille"]
                    taille_debloque = dict[user]["niv_taille_deb"]
                    if taille < 4 and taille==taille_debloque:
                        a = pyautogui.confirm(
                            "Pour rétrécir davantage, voulez vous acheter l'amélioration pour 15 gemmes?",
                            buttons=["Oui", "Non"],timeout=10000)
                        if a == "Oui":
                            if int(dict[user]["Solde"])>=15:
                                dict[user]["niv_taille_deb"] += 1
                                dict[user]["Solde"] = str(int(dict[user]["Solde"]) - 15)
                            else:
                                pyautogui.alert("Vous n'avez pas assez de gemmes")
                    if taille<4 and taille<taille_debloque:
                        dict[user]["niv_taille"] += 1

                    a = str(dict)
                    with open("sauvegarde.txt", "w") as fichier:
                        fichier.write(a)
                        fichier.close()

                if 410<=event.pos[0]<=470 and 270<=event.pos[1]<=330:
                    game1 = game.Game(user=user,skin=skin)
                    pygame.mixer.music.stop()
                    game1.run()
                if 490<=event.pos[0]<=550 and 270<=event.pos[1]<=330:
                    if nbr_niv_reussi>=1:
                        game2 = game.Game(niv=2,nbr_alert=1,user=user,skin=skin)
                        pygame.mixer.music.stop()
                        game2.run()
                    if nbr_niv_reussi<1:
                        pyautogui.alert("Vous devez d'abord réussir le niveau précédant")

                if 570<=event.pos[0]<=630 and 270<=event.pos[1]<=330:
                    if nbr_niv_reussi >= 2:
                        game2 = game.Game(niv=3, nbr_alert=2,user=user,skin=skin)
                        pygame.mixer.music.stop()
                        game2.run()
                    if nbr_niv_reussi < 2:
                        pyautogui.alert("Vous devez d'abord réussir le niveau précédant")

                if 650<=event.pos[0]<=710 and 270<=event.pos[1]<=330:
                    if nbr_niv_reussi >= 3:
                        game2 = game.Game(niv=4, nbr_alert=3,user=user,skin=skin)
                        pygame.mixer.music.stop()
                        game2.run()
                    if nbr_niv_reussi < 3:
                        pyautogui.alert("Vous devez d'abord réussir le niveau précédant")

                if 730<=event.pos[0]<=790 and 270<=event.pos[1]<=330:
                    if nbr_niv_reussi >= 4:
                        game2 = game.Game(niv=5, nbr_alert=4,user=user,skin=skin)
                        pygame.mixer.music.stop()
                        game2.run()
                    if nbr_niv_reussi < 4:
                        pyautogui.alert("Vous devez d'abord réussir le niveau précédant")

                if 810<=event.pos[0]<=870 and 270<=event.pos[1]<=330:
                    if nbr_niv_reussi >= 5:
                        game2 = game.Game(niv=6, nbr_alert=5,user=user,skin=skin)
                        pygame.mixer.music.stop()
                        game2.run()
                    if nbr_niv_reussi < 5:
                        pyautogui.alert("Vous devez d'abord réussir le niveau précédant")

                if 410<=event.pos[0]<=470 and 400<=event.pos[1]<=460:
                    game1 = game.Game(monde=2, nbr_alert=6,user=user,skin=skin)
                    pygame.mixer.music.stop()
                    game1.run()
                if 490<=event.pos[0]<=550 and 400<=event.pos[1]<=460:
                    if nbr_niv_reussi2>=1:
                        game2 = game.Game(niv=2,monde=2,user=user,skin=skin, nbr_alert=7)
                        pygame.mixer.music.stop()
                        game2.run()
                    if nbr_niv_reussi2<1:
                        pyautogui.alert("Vous devez d'abord réussir le niveau précédant")

                if 570<=event.pos[0]<=630 and 400<=event.pos[1]<=460:
                    if nbr_niv_reussi2 >= 2:
                        game2 = game.Game(niv=3, monde=2,user=user,skin=skin,nbr_alert=8)
                        pygame.mixer.music.stop()
                        game2.run()
                    if nbr_niv_reussi2 < 2:
                        pyautogui.alert("Vous devez d'abord réussir le niveau précédant")

                if 650<=event.pos[0]<=710 and 400<=event.pos[1]<=460:
                    if nbr_niv_reussi2 >= 3:
                        game2 = game.Game(niv=4, monde=2,user=user,skin=skin,nbr_alert=9)
                        pygame.mixer.music.stop()
                        game2.run()
                    if nbr_niv_reussi2 < 3:
                        pyautogui.alert("Vous devez d'abord réussir le niveau précédant")

                if 730<=event.pos[0]<=790 and 400<=event.pos[1]<=460:
                    if nbr_niv_reussi2 >= 4:
                        game2 = game.Game(niv=5, monde=2,user=user,skin=skin,nbr_alert=10)
                        pygame.mixer.music.stop()
                        game2.run()
                    if nbr_niv_reussi2 < 4:
                        pyautogui.alert("Vous devez d'abord réussir le niveau précédant")

                if 810<=event.pos[0]<=870 and 400<=event.pos[1]<=460:
                    if nbr_niv_reussi2 >= 5:
                        game2 = game.Game(niv=6, monde=2,user=user,skin=skin,nbr_alert=11)
                        pygame.mixer.music.stop()
                        game2.run()
                    if nbr_niv_reussi2 < 5:
                        pyautogui.alert("Vous devez d'abord réussir le niveau précédant")

            clock.tick(60)

            if event.type==pygame.QUIT:
                run=False
                pygame.quit()


        pygame.display.update()

    pygame.quit()

if __name__=='__main__':
    main_menu()