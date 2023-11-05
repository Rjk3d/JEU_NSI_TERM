import pygame


class AnimateSprite(pygame.sprite.Sprite):
    def __init__(self,skin="visual/perso_mec/mec3.png",taille=1):
        assert taille==2.5 or taille==1 or taille==0.625 or taille==0.75 or taille==0.8125 or taille==0.90625#multiplicateurs de 32 pour rester en nombre entier
        super().__init__()
        self.sprite_sheet = pygame.image.load(skin)
        self.sprite_sheet = pygame.transform.scale(self.sprite_sheet,(self.sprite_sheet.get_size()[0]*taille,self.sprite_sheet.get_size()[1]*taille))
        self.animation_index = 0
        self.images = {
            'down': self.get_images(0,taille),
            'left': self.get_images(32*taille,taille),
            'right': self.get_images(64*taille,taille),
            'up': self.get_images(96*taille,taille)
        }

    def get_image(self, x, y,taille):
        """
        Récupère l'image souhaité depuis le sprite_sheet, en prenant en compte la taille si elle est réduite

        :param x: La coordonée en x de l'image que l'on veut récupérer
        :param y: La coordonée en y de l'image que l'on veut récupérer
        :param taille: La taille afin de conserver les bonnes images mais résuites
        :return: l'image souhaité
        """
        image=pygame.Surface([32*taille,32*taille])
        image.blit(self.sprite_sheet,(0, 0), (x, y, 32*taille, 32*taille))#dans sprite_sheet chaque partie qui représente un personnage fait initialement 32 pixels
        return image

    def change_animation(self, name):
        """
        Permet de faire l'animation de mouvement en alternant les trois images d'une même rangée
        :param name:
        :return:
        """
        self.image=self.images[name][self.animation_index]
        self.image.set_colorkey((0,0,0))
        self.animation_index += 1
        if self.animation_index >= len(self.images[name]):
            self.animation_index=0


    def get_images(self, y,taille):
        """
        Réupère la rangée de l'image souhaité

        :param y: coordonnée de la rangée souhaité
        :param taille:conserver les changements de taille
        :return: La rangée d'image d'une direction
        """
        images=[]
        for i in range (0,3):
            x = i*32*taille
            image=self.get_image(x,y,taille)
            images.append(image)
        return images