from pygame import image

from assets.settings import windows_width

class GameObject:
    def __init__(self, imageName, pos = (0, 0), speed = 5):
        self.speed = speed
        self.image = image.load(imageName).convert()
        self.pos = self.image.get_rect().move(pos)
    
    def move(self):
        self.pos = self.pos.move(self.speed, 0)
        if self.pos.right > windows_width:
            self.pos.left = 0
