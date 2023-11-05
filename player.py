import pygame
import animation
import random


class Player(animation.AnimateSprite):
    def __init__(self, x, y,skin="visual/perso_mec/mec3.png",taille=1,speed=2):
        super().__init__(skin=skin,taille=taille)#initialise la classe animation mis en entrée de cette classe
        self.image = self.get_image(0,0,taille=taille)
        self.image.set_colorkey([0,0,0]) #enlever  le noir
        self.rect = self.image.get_rect()
        self.position = [x,y]
        self.feet=pygame.Rect(0,0, self.rect.width*0.5, 12)
        self.old_position=self.position.copy()
        self.speed = speed

    def save_location(self):
        """
        permet de conserver une position afin d'y retourner lorsqu'on souhaite empecher un mouvement (colision mur)
        """
        self.old_position = self.position.copy()
    def move_right(self):
        """
        ajoute le nombre de pixels choisi via self.speed à la position x
        """
        self.position[0] += self.speed
    def move_left(self):
        """
        enleve le nombre de pixels choisi via self.speed à la position x
        """
        self.position[0] -= self.speed
    def move_down(self):
        """
        ajoute le nombre de pixels choisi via self.speed à la position y
        """
        self.position[1] += self.speed
    def move_up(self):
        """
        enleve le nombre de pixels choisi via self.speed à la position y
        """
        self.position[1] -= self.speed
    def update(self):
        """
        fait en sorte que le rect du personnage (par ses pieds) suit le mouvement
        """
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom
    def move_back(self):
        """
        empeche le personnage d'avancer en le renvoyant toujours à son ancienne position, tout en faisant un bruitage de douleur
        """
        self.position = self.old_position
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom
        ouch = pygame.mixer.Sound(f"sound/male_pain{random.randint(1,4)}.mp3")#permet de diversifier les bruits
        ouch.play()
    def get_pos(self):
        return self.position

