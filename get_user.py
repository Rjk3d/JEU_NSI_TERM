import pyautogui
from main import main_menu
from menu_mini_jeu import menu_mini_jeu
import pygame
import pygame.freetype
import ast

def get_image(path):
    sprite_sheet = pygame.image.load(path)#"visual/perso_mec/mec1.png"
    image = pygame.Surface([32, 32])
    image.blit(sprite_sheet, (0, 0), (32, 0, 32, 32))
    image = pygame.transform.scale(image, (80, 80))
    image.set_colorkey([0, 0, 0])
    return image

def unlock(skin):
    with open("sauvegarde.txt", "r") as fichier:
        for elem in fichier:
            dict = ast.literal_eval(elem)
            dict["User1"]["skin"][skin]=True


    a = str(dict)
    with open("sauvegarde.txt", "w") as fichier:
        fichier.write(a)

def get_user(mode="h"):
    assert mode=="mj" or mode=="h" or mode==None,"mode doit être mj(mini jeu) ou h (histoire)"#sert à savoir d'où l'on vient pour retourner au même endroit après le choix
    pygame.init()

    with open("sauvegarde.txt", "r") as fichier:
        for elem in fichier:
            dict = ast.literal_eval(elem)
    dico_skin = dict["User1"]["skin"]

    screen = pygame.display.set_mode((1280, 720))
    GAME_FONT = pygame.freetype.Font("for_construction/font.ttf", 24)

    bg = pygame.image.load("visual/menu_background2.jpg")
    bg = pygame.transform.scale(bg, (1280, 720))

    cadena = pygame.image.load("visual/cadena.jpg")
    cadena = pygame.transform.scale(cadena,(50,50))
    cadena.set_colorkey([255,255,255])

    gemme = pygame.image.load("visual/gem.png")
    gemme = pygame.transform.scale(gemme, (30, 30))

    with open("sauvegarde.txt", "r") as fichier:
        for elem in fichier:
            dict = ast.literal_eval(elem)
            solde = int(dict["User1"]["Solde"])

    text_solde, rect = GAME_FONT.render(str(solde), (255, 255, 255))

    ar_menu=pygame.image.load("visual/ar_menu.png") #585*427
    ar_menu.set_colorkey([255,255,255])

    txt_skin_mec, rect = GAME_FONT.render("Garçons:", (255, 255, 255))
    txt_skin_meuf, rect = GAME_FONT.render("Filles:", (255, 255, 255))

    txt_menu_skin, rect = GAME_FONT.render("CHOISISSEZ UN SKIN (en cliquant dessus)", (255, 255, 255))

    images_mecs=[]
    for i in range(1,5):
        path=f"visual/perso_mec/mec{i}.png"
        images_mecs.append(get_image(path))

    images_meufs = []
    for i in range(1, 6):
        path = f"visual/perso_meuf/meuf{i}.png"
        images_meufs.append(get_image(path))

    pygame.display.set_caption("Choisissez un skin")

    run=True
    while run:
        screen.blit(bg, (0, 0))
        screen.blit(ar_menu, ((1280 - 585) / 2, (720 - 427) / 2))

        screen.blit(text_solde, (1250 - list(text_solde.get_rect())[-2], 10))
        screen.blit(gemme, (1250, 5))

        screen.blit(txt_menu_skin, ((1280 - list(txt_menu_skin.get_rect())[-2])/2, 10))


        screen.blit(txt_skin_mec,(560,190))
        screen.blit(txt_skin_meuf, (560, 360))

        for i in range(4):
            screen.blit(images_mecs[i],(420+i*120,240))
            if dico_skin[f"mec{i}"]==False:
                screen.blit(cadena,(435+i*120,255))

        for i in range(5):
            screen.blit(images_meufs[i],(400+i*100,440))
            if dico_skin[f"meuf{i}"]==False:
                screen.blit(cadena,(415+i*100,455))

        for event in pygame.event.get():

            if event.type == pygame.MOUSEBUTTONDOWN:
                if 420 <= event.pos[0] <= 500 and 240 <= event.pos[1] <= 320:
                    if dico_skin["mec0"]==True:
                        with open("skin.txt","w") as file:
                            file.write("visual/perso_mec/mec1.png")
                            file.close()
                            if mode=="h":
                                main_menu(deb=False)
                            elif mode=="mj":
                                menu_mini_jeu()
                    else:
                        pyautogui.alert("Vous ne l'avez pas débloqué")
                if 540 <= event.pos[0] <= 620 and 240 <= event.pos[1] <= 320:
                    if dico_skin["mec1"] == True:
                        with open("skin.txt","w") as file:
                            file.write("visual/perso_mec/mec2.png")
                            file.close()
                            if mode == "h":
                                main_menu(deb=False)
                            elif mode == "mj":
                                menu_mini_jeu()
                    else:
                        a = pyautogui.confirm("Vous ne l'avez pas débloqué, Voulez-vous l'acheter pour 10 gemmes?",buttons=["Oui","Non"])

                        if a=="Oui":
                            if int(solde)>=10:
                                with open("sauvegarde.txt", "r") as fichier:
                                    for elem in fichier:
                                        dict = ast.literal_eval(elem)
                                solde -= 10
                                dict["User1"]["Solde"] = str(solde)
                                a = str(dict)
                                with open("sauvegarde.txt", "w") as fichier:
                                    fichier.write(a)
                                unlock("mec1")
                                with open("skin.txt", "w") as file:
                                    file.write("visual/perso_mec/mec2.png")
                                    file.close()
                                    if mode == "h":
                                        main_menu(deb=False)
                                    elif mode == "mj":
                                        menu_mini_jeu()
                            else:
                                pyautogui.alert("Vous n'avez pas assez de gemmes")


                if 660 <= event.pos[0] <= 740 and 240 <= event.pos[1] <= 320:
                    if dico_skin["mec2"] == True:
                        with open("skin.txt", "w") as file:
                            file.write("visual/perso_mec/mec3.png")
                            file.close()
                            if mode == "h":
                                main_menu(deb=False)
                            elif mode == "mj":
                                menu_mini_jeu()
                    else:
                        a = pyautogui.confirm("Vous ne l'avez pas débloqué, Voulez-vous l'acheter pour 10 gemmes?", buttons=["Oui", "Non"])
                        if a == "Oui":
                            if int(solde) >= 10:
                                with open("sauvegarde.txt", "r") as fichier:
                                    for elem in fichier:
                                        dict = ast.literal_eval(elem)
                                solde -= 10
                                dict["User1"]["Solde"] = str(solde)
                                a = str(dict)
                                with open("sauvegarde.txt", "w") as fichier:
                                    fichier.write(a)
                                unlock("mec2")
                                with open("skin.txt", "w") as file:
                                    file.write("visual/perso_mec/mec3.png")
                                    file.close()
                                    if mode == "h":
                                        main_menu(deb=False)
                                    elif mode == "mj":
                                        menu_mini_jeu()
                            else:
                                pyautogui.alert("Vous n'avez pas assez de gemmes")

                if 780 <= event.pos[0] <= 860 and 240 <= event.pos[1] <= 320:
                    if dico_skin["mec3"] == True:
                        with open("skin.txt", "w") as file:
                            file.write("visual/perso_mec/mec4.png")
                            file.close()
                            if mode == "h":
                                main_menu(deb=False)
                            elif mode == "mj":
                                menu_mini_jeu()
                    else:
                        a = pyautogui.confirm("Vous ne l'avez pas débloqué, Voulez vous l'acheter pour 10 gemmes?",
                                              buttons=["Oui", "Non"])
                        if a == "Oui":
                            if int(solde) >= 10:
                                with open("sauvegarde.txt", "r") as fichier:
                                    for elem in fichier:
                                        dict = ast.literal_eval(elem)
                                solde -= 10
                                dict["User1"]["Solde"] = str(solde)
                                a = str(dict)
                                with open("sauvegarde.txt", "w") as fichier:
                                    fichier.write(a)
                                unlock("mec3")
                                with open("skin.txt", "w") as file:
                                    file.write("visual/perso_mec/mec4.png")
                                    file.close()
                                    if mode == "h":
                                        main_menu(deb=False)
                                    elif mode == "mj":
                                        menu_mini_jeu()
                            else:
                                pyautogui.alert("Vous n'avez pas assez de gemmes")


                if 400 <= event.pos[0] <= 480 and 440 <= event.pos[1] <= 520:
                    if dico_skin["meuf0"] == True:
                        with open("skin.txt", "w") as file:
                            file.write("visual/perso_meuf/meuf1.png")
                            file.close()
                            if mode == "h":
                                main_menu(deb=False)
                            elif mode == "mj":
                                menu_mini_jeu()
                    else:
                        a = pyautogui.confirm("Vous ne l'avez pas débloqué, Voulez vous l'acheter pour 10 gemmes?",
                                              buttons=["Oui", "Non"])
                        if a == "Oui":
                            if int(solde) >= 10:
                                with open("sauvegarde.txt", "r") as fichier:
                                    for elem in fichier:
                                        dict = ast.literal_eval(elem)
                                solde -= 10
                                dict["User1"]["Solde"] = str(solde)
                                a = str(dict)
                                with open("sauvegarde.txt", "w") as fichier:
                                    fichier.write(a)
                                unlock("meuf0")
                                with open("skin.txt", "w") as file:
                                    file.write("visual/perso_meuf/meuf1.png")
                                    file.close()
                                    if mode == "h":
                                        main_menu(deb=False)
                                    elif mode == "mj":
                                        menu_mini_jeu()
                            else:
                                pyautogui.alert("Vous n'avez pas assez de gemmes")


                if 500 <= event.pos[0] <= 580 and 440 <= event.pos[1] <= 520:
                    if dico_skin["meuf1"] == True:
                        with open("skin.txt", "w") as file:
                            file.write("visual/perso_meuf/meuf2.png")
                            file.close()
                            if mode == "h":
                                main_menu(deb=False)
                            elif mode == "mj":
                                menu_mini_jeu()
                    else:
                        a = pyautogui.confirm("Vous ne l'avez pas débloqué, Voulez vous l'acheter pour 10 gemmes?",
                                              buttons=["Oui", "Non"])
                        if a == "Oui":
                            if int(solde) >= 10:
                                with open("sauvegarde.txt", "r") as fichier:
                                    for elem in fichier:
                                        dict = ast.literal_eval(elem)
                                solde -= 10
                                dict["User1"]["Solde"] = str(solde)
                                a = str(dict)
                                with open("sauvegarde.txt", "w") as fichier:
                                    fichier.write(a)
                                unlock("meuf1")
                                with open("skin.txt", "w") as file:
                                    file.write("visual/perso_meuf/meuf2.png")
                                    file.close()
                                    if mode == "h":
                                        main_menu(deb=False)
                                    elif mode == "mj":
                                        menu_mini_jeu()
                            else:
                                pyautogui.alert("Vous n'avez pas assez de gemmes")



                if 600 <= event.pos[0] <= 680 and 440 <= event.pos[1] <= 520:
                    if dico_skin["meuf2"] == True:
                        with open("skin.txt", "w") as file:
                            file.write("visual/perso_meuf/meuf3.png")
                            file.close()
                            if mode == "h":
                                main_menu(deb=False)
                            elif mode == "mj":
                                menu_mini_jeu()
                    else:
                        a = pyautogui.confirm("Vous ne l'avez pas débloqué, Voulez vous l'acheter pour 10 gemmes?",
                                              buttons=["Oui", "Non"])
                        if a == "Oui":
                            if int(solde) >= 10:
                                with open("sauvegarde.txt", "r") as fichier:
                                    for elem in fichier:
                                        dict = ast.literal_eval(elem)
                                solde -= 10
                                dict["User1"]["Solde"] = str(solde)
                                a = str(dict)
                                with open("sauvegarde.txt", "w") as fichier:
                                    fichier.write(a)
                                unlock("meuf2")
                                with open("skin.txt", "w") as file:
                                    file.write("visual/perso_meuf/meuf3.png")
                                    file.close()
                                    if mode == "h":
                                        main_menu(deb=False)
                                    elif mode == "mj":
                                        menu_mini_jeu()
                            else:
                                pyautogui.alert("Vous n'avez pas assez de gemmes")


                if 700 <= event.pos[0] <= 780 and 440 <= event.pos[1] <= 520:
                    if dico_skin["meuf3"] == True:
                        with open("skin.txt", "w") as file:
                            file.write("visual/perso_meuf/meuf4.png")
                            file.close()
                            if mode == "h":
                                main_menu(deb=False)
                            elif mode == "mj":
                                menu_mini_jeu()
                    else:
                        a = pyautogui.confirm("Vous ne l'avez pas débloqué, Voulez vous l'acheter pour 10 gemmes?",
                                              buttons=["Oui", "Non"])
                        if a == "Oui":
                            if int(solde) >= 10:
                                with open("sauvegarde.txt", "r") as fichier:
                                    for elem in fichier:
                                        dict = ast.literal_eval(elem)
                                solde -= 10
                                dict["User1"]["Solde"] = str(solde)
                                a = str(dict)
                                with open("sauvegarde.txt", "w") as fichier:
                                    fichier.write(a)
                                unlock("meuf3")
                                with open("skin.txt", "w") as file:
                                    file.write("visual/perso_meuf/meuf4.png")
                                    file.close()
                                    if mode == "h":
                                        main_menu(deb=False)
                                    elif mode == "mj":
                                        menu_mini_jeu()
                            else:
                                pyautogui.alert("Vous n'avez pas assez de gemmes")


                if 800 <= event.pos[0] <= 880 and 440 <= event.pos[1] <= 520:
                    if dico_skin["meuf4"] == True:
                        with open("skin.txt", "w") as file:
                            file.write("visual/perso_meuf/meuf5.png")
                            file.close()
                            if mode == "h":
                                main_menu(deb=False)
                            elif mode == "mj":
                                menu_mini_jeu()
                    else:
                        a = pyautogui.confirm("Vous ne l'avez pas débloqué, Voulez vous l'acheter pour 10 gemmes?",
                                              buttons=["Oui", "Non"])
                        if a == "Oui":
                            if int(solde) >= 10:
                                with open("sauvegarde.txt", "r") as fichier:
                                    for elem in fichier:
                                        dict = ast.literal_eval(elem)
                                solde -= 10
                                dict["User1"]["Solde"] = str(solde)
                                a = str(dict)
                                with open("sauvegarde.txt", "w") as fichier:
                                    fichier.write(a)
                                unlock("meuf4")
                                with open("skin.txt", "w") as file:
                                    file.write("visual/perso_meuf/meuf5.png")
                                    file.close()
                                    if mode == "h":
                                        main_menu(deb=False)
                                    elif mode == "mj":
                                        menu_mini_jeu()
                            else:
                                pyautogui.alert("Vous n'avez pas assez de gemmes")

            if event.type == pygame.QUIT:
                run = False
                pygame.quit()


        pygame.display.update()

    pygame.quit()



if __name__=='__main__':
    get_user()