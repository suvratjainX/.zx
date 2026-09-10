class Camera:

    def __init__(self):

        self.x = 0
        self.y = 0

        self.target = None

    def follow(self,obj):

        self.target = obj

    def update(self):

        if self.target:

            self.x = (
                self.target.x - 640
            )

            self.y = (
                self.target.y - 360
            )

camera = Camera()