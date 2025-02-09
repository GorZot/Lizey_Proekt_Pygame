import pygame
from sys import exit
import math
from settings import *
import time
import sqlite3
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QFileDialog
from PyQt6 import QtGui


pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bogatyr-1")
clock = pygame.time.Clock()

shoot_sound = pygame.mixer.Sound('sounds/bullet.ogg')
shoot_sound.set_volume(0.3)
button_sound = pygame.mixer.Sound('sounds/button_sound.ogg')
damage_igrok_sound = pygame.mixer.Sound('sounds/sound_damage_igrok.ogg')
score = 0
count = 10

background = pygame.image.load("images/bg2.png").convert()
WIDTH_BG, HEIGHT_BG = background.get_rect().size
start = time.time()


def print_text(message, x, y, font_color=(99, 219, 215), font_type='FlaviusUniversal.ttf', font_size=30):
    font_type = pygame.font.Font(font_type, font_size)
    text = font_type.render(message, True, font_color)
    screen.blit(text, (x, y))


def helth_check(enemy, health_en):
    if health_en <= 0:
        dead(enemy)
    if count <= 0:
        pobeda()

def dead(enemy):
    global count, score
    enemy.kill()
    score += 1000
    count -= 1


def pobeda():
    finish = time.time()
    menu_back = pygame.image.load('images/bg2.png')
    global score, start
    final_score = score - int((finish - start) * 50)
    gg = True
    while gg:
        screen.blit(menu_back, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        print_text('             ПОЗДРАВЛЯЕМ! ВЫ СПРАВИЛИСЬ С ПОСТАВЛЕННОЙ ЗАДАЧЕЙ!', 70, 270)
        print_text('   Вы очистили данные территории от Опустошителей. Нажми Esc чтобы сохранить свой результат и выйти', 70, 310)
        print_text(f'                                                      Вы набрали {final_score} очков', 140, 350)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            name = 'GorZot'
            con = sqlite3.connect('abstract.db')
            c = con.cursor()
            c.execute('INSERT INTO Users (name, score) VALUES (?, ?)', (name, final_score))

            c.execute("SELECT * FROM Users")
            con.commit()
            con.close()
            pygame.quit()
            quit()

        pygame.display.update()
        clock.tick(15)

def start_game():
    pygame.mixer.music.load('sounds/fonovay.mp3')
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(loops=-1)
    global score, count
    health = 100
    health2 = 150
    health3 = 120
    health4 = 110
    health5 = 130
    health6 = 150
    health7 = 130
    health8 = 110
    health9 = 130
    health10 = 160

    while True:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        screen.blit(background, (0, 0))
        screen.fill('black')

        if health > 0:
            for i in bullet_group:
                if pygame.sprite.collide_rect(i, vrag):
                    health -= 1
                    helth_check(vrag, health)
                    break

        if health2 > 0:
            for i in bullet_group:
                if pygame.sprite.collide_rect(i, vrag2):
                    health2 -= 1
                    helth_check(vrag2, health2)
                    break

        if health3 > 0:
            for i in bullet_group:
                if pygame.sprite.collide_rect(i, vrag3):
                    health3 -= 1
                    helth_check(vrag3, health3)
                    break

        if health4 > 0:
            for i in bullet_group:
                if pygame.sprite.collide_rect(i, vrag4):
                    health4 -= 1
                    helth_check(vrag4, health4)
                    break

        if health5 > 0:
            for i in bullet_group:
                if pygame.sprite.collide_rect(i, vrag5):
                    health5 -= 1
                    helth_check(vrag5, health5)
                    break

        if health6 > 0:
            for i in bullet_group:
                if pygame.sprite.collide_rect(i, vrag6):
                    health6 -= 1
                    helth_check(vrag6, health6)
                    break

        if health7 > 0:
            for i in bullet_group:
                if pygame.sprite.collide_rect(i, vrag7):
                    health7 -= 1
                    helth_check(vrag7, health7)
                    break

        if health8 > 0:
            for i in bullet_group:
                if pygame.sprite.collide_rect(i, vrag8):
                    health8 -= 1
                    helth_check(vrag8, health8)
                    break

        if health9 > 0:
            for i in bullet_group:
                if pygame.sprite.collide_rect(i, vrag9):
                    health9 -= 1
                    helth_check(vrag9, health9)
                    break

        if health10 > 0:
            for i in bullet_group:
                if pygame.sprite.collide_rect(i, vrag10):
                    health10 -= 1
                    helth_check(vrag10, health10)
                    break

        camera.custom_draw()
        all_sprites_group.update()
        # pygame.draw.rect(screen, "red", player.hitbox_rect, width=2)
        # pygame.draw.rect(screen, "yellow", player.rect, width=2)

        pygame.display.update()
        clock.tick(FPS)

class Player(pygame.sprite.Sprite):
    global count
    def __init__(self):
        super().__init__()
        self.pos = pygame.math.Vector2(PLAYER_START_X, PLAYER_START_Y)
        self.image = pygame.transform.rotozoom(pygame.image.load("images/gg.png").convert_alpha(), 0, PLAYER_SIZE)
        self.base_player_image = self.image
        self.hitbox_rect = self.base_player_image.get_rect(center=self.pos)
        self.rect = self.hitbox_rect.copy()
        self.speed = PLAYER_SPEED
        self.shoot = False
        self.shoot_cooldown = 0
        self.gun_barrel_offset = pygame.math.Vector2(GUN_OFFSET_X, GUN_OFFSET_Y)
        self.player_health = PLAYER_HEALTH
        self.damage_cooldown = 0

    def player_rotation(self):
        self.mouse_coords = pygame.mouse.get_pos()
        self.x_change_mouse_player = (self.mouse_coords[0] - WIDTH // 2)
        self.y_change_mouse_player = (self.mouse_coords[1] - HEIGHT // 2)
        self.angle = math.degrees(math.atan2(self.y_change_mouse_player, self.x_change_mouse_player))
        self.image = pygame.transform.rotate(self.base_player_image, -self.angle - 90)
        self.rect = self.image.get_rect(center=self.hitbox_rect.center)

    def user_input(self):
        self.velocity_x = 0
        self.velocity_y = 0

        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.velocity_y = -self.speed
        if keys[pygame.K_s]:
            self.velocity_y = self.speed
        if keys[pygame.K_d]:
            self.velocity_x = self.speed
        if keys[pygame.K_a]:
            self.velocity_x = -self.speed

        if self.velocity_x != 0 and self.velocity_y != 0:
            self.velocity_x /= math.sqrt(2)
            self.velocity_y /= math.sqrt(2)

        if pygame.mouse.get_pressed() == (1, 0, 0) or keys[pygame.K_SPACE]:
            self.shoot = True
            self.is_shooting()
        else:
            self.shoot = False

    def is_shooting(self):
        if self.shoot_cooldown == 0:
            self.shoot_cooldown = SHOOT_COOLDOWN
            spawn_bullet_pos = self.pos + self.gun_barrel_offset.rotate(self.angle)
            self.bullet = Bullet(spawn_bullet_pos[0], spawn_bullet_pos[1], self.angle)
            bullet_group.add(self.bullet)
            all_sprites_group.add(self.bullet)

    def move(self):
        self.pos_x, self.pos_y = self.pos
        if 0 < self.pos[0] < WIDTH_BG and 0 < self.pos[1] < HEIGHT_BG:
            self.pos += pygame.math.Vector2(self.velocity_x, self.velocity_y)
            self.hitbox_rect.center = self.pos
            self.rect.center = self.hitbox_rect.center
        elif self.pos[0] <= 0:
            self.pos = (WIDTH_BG - 5, self.pos_y)
            self.hitbox_rect.center = self.pos
            self.rect.center = self.hitbox_rect.center
        elif self.pos[0] >= WIDTH_BG:
            self.pos = (0 + 5, self.pos_y)
            self.hitbox_rect.center = self.pos
            self.rect.center = self.hitbox_rect.center
        elif self.pos[1] <= 0:
            self.pos = (self.pos_x, HEIGHT_BG - 5)
            self.hitbox_rect.center = self.pos
            self.rect.center = self.hitbox_rect.center
        elif self.pos[1] >= HEIGHT_BG:
            self.pos = (self.pos_x, 0 + 5)
            self.hitbox_rect.center = self.pos
            self.rect.center = self.hitbox_rect.center


    def update(self):
        self.user_input()
        self.move()
        self.player_rotation()
        print_text(f'Количество жизней: {self.player_health}%', 40, 20)
        print_text(f'Врагов осталось: {count}', 40, 50)

        for i in enemy_group:
            if pygame.sprite.collide_rect(i, player):
                if self.damage_cooldown == 0:
                    self.damage_cooldown = DAMAGE_COOLDOWN
                    self.player_health -= 1
                    damage_igrok_sound.play()
                    print(self.player_health)
                    break
        if self.player_health == 0:
            self.died()

        if self.damage_cooldown > 0:
            self.damage_cooldown -= 1

        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    def died(self):
        game_over()

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle):
        super().__init__()
        self.image = pygame.image.load("images/bullet.png").convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, BULLET_SCALE)
        self.rect = self.image.get_rect()
        self.rect.center = (x - 50, y - 50)
        self.x = x - 50
        self.y = y - 50
        self.angle = angle
        self.speed = BULLET_SPEED
        self.x_vel = math.cos(self.angle * (2 * math.pi / 360)) * self.speed
        self.y_vel = math.sin(self.angle * (2 * math.pi / 360)) * self.speed
        self.bullet_lifetime = BULLET_LIFETIME
        self.spawn_time = pygame.time.get_ticks()

    def bullet_movement(self):
        self.x += self.x_vel
        self.y += self.y_vel

        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

        if pygame.time.get_ticks() - self.spawn_time > self.bullet_lifetime:
            self.kill()

    def update(self):
        self.bullet_movement()
        shoot_sound.play()


class Enemy(pygame.sprite.Sprite):
    def __init__(self, position, file):
        super().__init__(enemy_group, all_sprites_group)
        self.image = pygame.image.load(f"images/images_enemy/{file}").convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, 2)

        self.rect = self.image.get_rect()
        self.rect.center = position

        self.direction = pygame.math.Vector2()
        self.velocity = pygame.math.Vector2()
        self.speed = ENEMY_SPEED
        self.angle = 1

        self.position = pygame.math.Vector2(position)

    def hunt_player(self):
        player_vector = pygame.math.Vector2(player.hitbox_rect.center)
        enemy_vector = pygame.math.Vector2(self.rect.center)
        distance = self.get_vector_distance(player_vector, enemy_vector)

        if distance > 0:
            self.direction = (player_vector - enemy_vector).normalize()
        else:
            self.direction = pygame.math.Vector2()

        self.velocity = self.direction * self.speed
        self.position += self.velocity

        self.rect.centerx = self.position.x
        self.rect.centery = self.position.y

    def get_vector_distance(self, vector_1, vector_2):
        return (vector_1 - vector_2).magnitude()

    def update(self):
        self.hunt_player()


class Camera(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.offset = pygame.math.Vector2()
        self.floor_rect = background.get_rect(topleft=(0, 0))

    def custom_draw(self):
        self.offset.x = player.rect.centerx - WIDTH // 2
        self.offset.y = player.rect.centery - HEIGHT // 2

        floor_offset_pos = self.floor_rect.topleft - self.offset
        screen.blit(background, floor_offset_pos)

        for sprite in all_sprites_group:
            offset_pos = sprite.rect.topleft - self.offset
            screen.blit(sprite.image, offset_pos)


class Button:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.inactive_color = (15, 103, 133)
        self.active_color = (99, 219, 215)

    def draw(self, x, y, message, action=None, font_size=30):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if x < mouse[0] < x + self.width and y < mouse[1] < y + self.height:
            pygame.draw.rect(screen, self.active_color, (x, y, self.width, self.height))

            if click[0] == 1:
                pygame.mixer.Sound.play(button_sound)
                pygame.time.delay(300)
                if action is not None:
                    if action == quit:
                        pygame.quit()
                        quit()
                    else:
                        action()
        else:
            pygame.draw.rect(screen, self.inactive_color, (x, y, self.width, self.height))
        print_text(message=message, x=x+10, y=y+10, font_size=font_size)


all_sprites_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()

camera = Camera()
player = Player()
all_sprites_group.add(player)


def game_over():
    finish = time.time()
    menu_back = pygame.image.load('images/bg2.png')
    pygame.mixer.music.load('sounds/nach.mp3')
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(loops=-1)
    global score, start
    final_score = score - int((finish - start) * 50)
    gg = True
    while gg:
        screen.blit(menu_back, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        print_text('                                     Связь потеряна... Нажми Esc чтобы сдаться', 100, 260)
        print_text(f'                                                      Вы набрали {final_score} очков', 140, 350)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                name = 'GorZot'
                con = sqlite3.connect('abstract.db')
                c = con.cursor()
                c.execute('INSERT INTO Users (name, score) VALUES (?, ?)', (name, final_score))

                c.execute("SELECT * FROM Users")
                con.commit()
                con.close()
                pygame.quit()
                quit()

        pygame.display.update()
        clock.tick(15)


def menu():
    pygame.mixer.music.load('sounds/nach.mp3')
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(loops=-1)
    menu_back = pygame.image.load('images/bg2.png')
    show = True

    start = Button(500, 70)
    quit_btn = Button(500, 70)
    instruction = ['', '', '', '', '', '',  '', '      УПРАВЛЕНИЕ', '      WASD - полет', '      space или лкм - стрельба']
    history = ['Шел 2345 год. Наша планета была опустошена страшной войной с неожиданно появившимися инопланетными захватчиками ',
               '   названными - Опустошителями. Остатки человечества скрываются в глубоких подземных бункерах, каждый день борясь',
               '            за существование. Но надежда не умерла, с помощью технологий излеченных из остовов механизмов противника',
               '                           был построен прототип совершенной автономной саморазвивающейся боевой машины - "Bogatyr-1"',
               '                                                          ТАК ПУСТЬ ЖЕ НАЧНЕТСЯ БИТВА ЗА СУДЬБУ ЧЕЛОВЕЧЕСТВА!']

    while show:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        screen.blit(menu_back, (0, 0))
        font = pygame.font.Font('FlaviusUniversal.ttf', 30)
        text_coord = 300
        for line in instruction:
            string_rendered = font.render(line, 1, pygame.Color(99, 219, 215))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)
        font = pygame.font.Font('FlaviusUniversal.ttf', 23)
        text_coord = 20
        for line in history:
            string_rendered = font.render(line, 1, pygame.Color(99, 219, 215))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)
        start.draw(400, 250, 'В БОЙ!', start_game, 50)
        quit_btn.draw(400, 350, 'ВЫЙТИ', quit, 50)
        pygame.display.update()
        clock.tick(60)


vrag = Enemy((1000, 1000), 'enemy.png')
vrag2 = Enemy((600, 1200), 'enemy2.png')
vrag3 = Enemy((900, 1000), 'enemy3.png')
vrag4 = Enemy((1100, 1000), 'enemy4.png')
vrag5 = Enemy((800, 1500), 'enemy5.png')
vrag6 = Enemy((1000, 1100), 'enemy6.png')
vrag7 = Enemy((300, 1500), 'enemy7.png')
vrag8 = Enemy((400, 1100), 'enemy8.png')
vrag9 = Enemy((100, 1900), 'enemy9.png')
vrag10 = Enemy((700, 1300), 'enemy10.png')


menu()