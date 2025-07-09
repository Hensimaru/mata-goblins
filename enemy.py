import random
from pgzero.actor import Actor

class Enemy:
    def __init__(self, image_path, pos, bounds, speed=2):
        self.images = ["enemy", "enemy_attack"]  # Lista de sprites
        self.current_image_index = 0
        self.actor = Actor(self.images[self.current_image_index], pos=pos)
        self.bounds = bounds
        self.speed = speed
        self.frame_timer = 0

    def update(self):
        # Movimento aleatório
        dx = random.choice([-1, 0, 1])
        dy = random.choice([-1, 0, 1])
        self.actor.x += dx * self.speed
        self.actor.y += dy * self.speed

        # Limites da tela
        self.actor.x = max(0, min(self.bounds[0], self.actor.x))
        self.actor.y = max(0, min(self.bounds[1], self.actor.y))

        # Alterna entre imagens para simular animação
        self.frame_timer += 1
        if self.frame_timer >= 15:
            self.current_image_index = (self.current_image_index + 1) % len(self.images)
            self.actor.image = self.images[self.current_image_index]
            self.frame_timer = 0

    def draw(self):
        self.actor.draw()

    def collides_with(self, other_actor):
        return self.actor.colliderect(other_actor)

