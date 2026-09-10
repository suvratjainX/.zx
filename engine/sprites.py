from engine.assets import image

class Sprite:

    def __init__(
        self,
        file,
        x=0,
        y=0
    ):

        self.image = image(file)

        self.x = x
        self.y = y

    def move(self,dx,dy):

        self.x += dx
        self.y += dy

    def draw(self,screen):

        screen.blit(
            self.image,
            (self.x,self.y)
        )