GRAVITATION = 1


class Character:
    def __init__(self):
        self.x = 100
        self.y = 100
        self.vert_velocity = 0
        self.hor_velocity = 0
        self.acceleration = GRAVITATION

    def collision(self):
        pass

    def death(self):
        pass