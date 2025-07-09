from pgzero.actor import Actor
from pgzero.keyboard import keyboard

class Hero:
    def __init__(self, pos, bounds, resource_path):
        self.pos = list(pos)
        self.bounds = bounds
        self.speed = 3
        self.direction = [0, 0]
        self.frame = 0
        self.frame_timer = 0
        self.resource_path = resource_path
        self.images_idle = ["hero_idle"]
        self.images_walk = ["hero_walk1", "hero_walk2"]
        self.images_attack = ["hero_attack"]
        self.current_image = self.images_idle[0]
        self.actor = Actor(self.current_image, pos=self.pos)
        self.attacking = False
        self.attack_timer = 0

    def update(self):
        self.handle_input()
        self.move()
        self.animate()

        if self.attacking:
            self.attack_timer -= 1
            if self.attack_timer <= 0:
                self.attacking = False

    def handle_input(self):
        self.direction = [0, 0]
        if keyboard.left or keyboard.a:
            self.direction[0] = -1
        if keyboard.right or keyboard.d:
            self.direction[0] = 1
        if keyboard.up or keyboard.w:
            self.direction[1] = -1
        if keyboard.down or keyboard.s:
            self.direction[1] = 1

    def move(self):
        self.pos[0] += self.direction[0] * self.speed
        self.pos[1] += self.direction[1] * self.speed

        self.pos[0] = max(0, min(self.bounds[0], self.pos[0]))
        self.pos[1] = max(0, min(self.bounds[1], self.pos[1]))

        self.actor.pos = self.pos

    def animate(self):
        if self.attacking:
            self.current_image = self.images_attack[0]
        elif self.direction != [0, 0]:
            self.frame_timer += 1
            if self.frame_timer >= 10:
                self.frame = (self.frame + 1) % len(self.images_walk)
                self.frame_timer = 0
            self.current_image = self.images_walk[self.frame]
        else:
            self.current_image = self.images_idle[0]
        self.actor.image = self.current_image

    def attack(self, enemies, score):
        self.attacking = True
        self.attack_timer = 10
        attack_range = 50
        for enemy in enemies[:]:
            dx = abs(self.actor.x - enemy.actor.x)
            dy = abs(self.actor.y - enemy.actor.y)
            if dx < attack_range and dy < attack_range:
                enemies.remove(enemy)
                score += 1
                if sounds.hit:
                    sounds.hit.play()
        return score

    def draw(self):
        self.actor.draw()


