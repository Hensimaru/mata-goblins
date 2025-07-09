import random
import os
from pygame import Rect
import pgzrun
from hero import Hero
from enemy import Enemy
from resource_utils import resource_path

WIDTH = 800
HEIGHT = 600

game_state = "menu"
sound_on = True
score = 0

HIGHSCORE_FILE = "highscore.txt"

def load_highscore():
    if os.path.exists(HIGHSCORE_FILE):
        with open(HIGHSCORE_FILE, "r") as f:
            try:
                return int(f.read().strip())
            except ValueError:
                return 0
    return 0

def save_highscore(score):
    with open(HIGHSCORE_FILE, "w") as f:
        f.write(str(score))

highscore = load_highscore()

start_button = Rect(300, 200, 200, 50)
sound_button = Rect(300, 270, 200, 50)
instructions_button = Rect(300, 340, 200, 50)
exit_button = Rect(300, 410, 200, 50)
restart_button = Rect(300, 400, 200, 50)

hero = Hero((WIDTH // 2, HEIGHT // 2), (WIDTH, HEIGHT), resource_path)
enemies = []

def spawn_enemies(n=5):
    global enemies
    enemies = []
    for _ in range(n):
        x = random.randint(50, WIDTH - 50)
        y = random.randint(50, HEIGHT - 50)
        enemy = Enemy("enemy", (x, y), (WIDTH, HEIGHT), speed=2)
        enemies.append(enemy)

def draw():
    screen.clear()
    if game_state == "menu":
        draw_menu()
    elif game_state == "playing":
        draw_game()
    elif game_state == "game_over":
        draw_game_over()
    elif game_state == "instructions":
        draw_instructions()

def draw_menu():
    screen.draw.text("Dungeon Escape", center=(WIDTH // 2, 100), fontsize=60, color="white")
    screen.draw.text(f"High Score: {highscore}", center=(WIDTH // 2, 160), fontsize=40, color="yellow")
    screen.draw.filled_rect(start_button, "green")
    screen.draw.text("Start Game", center=start_button.center, color="white")
    screen.draw.filled_rect(sound_button, "blue")
    screen.draw.text("Sound On" if sound_on else "Sound Off", center=sound_button.center, color="white")
    screen.draw.filled_rect(instructions_button, "orange")
    screen.draw.text("Como Jogar", center=instructions_button.center, color="white")
    screen.draw.filled_rect(exit_button, "red")
    screen.draw.text("Exit", center=exit_button.center, color="white")

def draw_game():
    screen.draw.text(f"Score: {score}", (10, 10), fontsize=40, color="white")
    hero.draw()
    for enemy in enemies:
        enemy.draw()

def draw_game_over():
    screen.draw.text("Game Over!", center=(WIDTH // 2, HEIGHT // 2 - 80), fontsize=60, color="red")
    screen.draw.text(f"Final Score: {score}", center=(WIDTH // 2, HEIGHT // 2), fontsize=40, color="white")
    screen.draw.text(f"High Score: {highscore}", center=(WIDTH // 2, HEIGHT // 2 + 40), fontsize=30, color="yellow")
    screen.draw.filled_rect(restart_button, "orange")
    screen.draw.text("Restart", center=restart_button.center, color="white")

def draw_instructions():
    screen.draw.text("Como Jogar", center=(WIDTH // 2, 100), fontsize=60, color="white")
    screen.draw.text("Use W, A, S, D ou setas para mover", center=(WIDTH // 2, 200), fontsize=40, color="lightblue")
    screen.draw.text("Pressione ESPAÇO para atacar", center=(WIDTH // 2, 250), fontsize=40, color="lightblue")
    screen.draw.text("Clique em qualquer lugar para voltar", center=(WIDTH // 2, 400), fontsize=30, color="gray")

def on_mouse_down(pos):
    global game_state, sound_on
    if game_state == "menu":
        if start_button.collidepoint(pos):
            game_state = "playing"
            hero.pos = [WIDTH // 2, HEIGHT // 2]
            spawn_enemies(5)
            if sound_on:
                music.play("bg_music")
                sounds.click.play()
        elif sound_button.collidepoint(pos):
            sound_on = not sound_on
            if not sound_on:
                music.stop()
        elif instructions_button.collidepoint(pos):
            game_state = "instructions"
        elif exit_button.collidepoint(pos):
            exit()
    elif game_state == "game_over":
        if restart_button.collidepoint(pos):
            game_state = "menu"
    elif game_state == "instructions":
        game_state = "menu"

def update():
    global game_state, score, highscore
    if game_state == "playing":
        hero.update()
        for enemy in enemies:
            enemy.update()
            if enemy.collides_with(hero.actor):
                if sound_on:
                    sounds.hit.play()
                if score > highscore:
                    save_highscore(score)
                    highscore = score
                game_state = "game_over"
                music.stop()

        if keyboard.space and not hero.attacking:
            score = hero.attack(enemies, score)

pgzrun.go()


