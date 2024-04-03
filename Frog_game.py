import random
import pygame
import sys
import csv
pygame.init()

width_screen = 800
height_screen = 600
screen = pygame.display.set_mode((width_screen, height_screen))
FPS = 60
clock=pygame.time.Clock()

main_font="Fonts/main_font.ttf"
head_font="Fonts/head_font.ttf"

font_main=pygame.font.Font(main_font, 60)
font_head=pygame.font.Font(head_font, 23)


game_over=False
retry_text=font_head.render('PRESS ANY KEY', True, (255,255,255))
retry_rect= retry_text.get_rect()
retry_rect.center=(width_screen//2, height_screen//2)

background_image = pygame.image.load("Images/background.png")


ground_image= pygame.image.load("Images/ground.png")
ground_image=pygame.transform.scale(ground_image, (804,50))
ground_high=ground_image.get_height()
ground_rect = pygame.Rect(0, height_screen - ground_high, width_screen, ground_high)

enemy_image= pygame.image.load("Images/enemy.png")
enemy_image=pygame.transform.scale(enemy_image, (50,50))

player_image= pygame.image.load("Images/player.png")
player_image=pygame.transform.scale(player_image, (80, 80))

stone_image=pygame.image.load("Images/stone.png")
stone_image = pygame.transform.scale(stone_image, (40,40))

main_sound = pygame.mixer.Sound("Sounds/Main_sound.mp3")
main_sound.set_volume(0.1)
game_over_sound = pygame.mixer.Sound("Sounds/game_over.mp3")
frog_attack_sound=pygame.mixer.Sound("Sounds/frog_attack.mp3")
level_up_sound=pygame.mixer.Sound("Sounds/level_up.mp3")


class Highscores:
    def __init__(self, filename):
        self.filename = filename

    def save_score(self, name, score):
        with open(self.filename, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([name, score])

    def get_scores(self):
        scores = []
        with open(self.filename, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                scores.append(row)
        scores.sort(key=lambda x: int(x[1]), reverse=True)
        return scores

    def display_scores(self):
        scores = self.get_scores()
        display_surf = pygame.display.set_mode((400, 400))
        pygame.display.set_caption("Highscores")
        font = pygame.font.Font(None, 36)
        clock = pygame.time.Clock()

        is_running = True
        while is_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_running = False

            display_surf.fill((255, 255, 255))

            x = 50
            y = 50
            for i, score in enumerate(scores, start=1):
                text_surface = font.render(f"{i}. {score[0]} - {score[1]}", True, (0, 0, 0))
                display_surf.blit(text_surface, (x, y))
                y += 50

            pygame.display.flip()
            clock.tick(60)

class Menu:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.buttons = []
        self.background_color = (255, 255, 255)
        self.button_offset = 75

    def set_background(self, image_path="Images/menu.png"):
        self.background_image = pygame.image.load(image_path)
        self.background_image = pygame.transform.scale(self.background_image, (self.width, self.height))
    def add_button(self, text, action, font, y_offset=0):
        button_width = 200
        button_height = 50
        button = Button(text, action, font)
        button.x = self.width // 2 - button_width // 2
        button.y = width_screen // 2 - button_height // 2 + y_offset
        self.buttons.append(button)

    def add_second_button(self, text, action, font, y_offset=0):
        button_width = 200
        button_height = 50
        button = Second_Button(text, action, font)
        button.x = self.width // 2 - button_width // 2
        button.y = width_screen // 2 - button_height // 2 + y_offset
        self.buttons.append(button)

    def add_record_button(self, text, action, font, y_offset=0):
        button_width = 200
        button_height = 50
        button = Second_Button(text, action, font)
        button.x = self.width // 2 - button_width // 2
        button.y = width_screen // 2 - button_height // 2 + y_offset
        self.buttons.append(button)

    def draw(self, surface):
        surface.blit(self.background_image, (0, 0))
        for i, button in enumerate(self.buttons):
            button.draw(surface, i * self.button_offset)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for button in self.buttons:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    button.check_click(event.pos)

class Button:
    def __init__(self, text, callback, font):
        self.text = text
        self.callback = callback
        self.font = pygame.font.Font(head_font, 17)
        self.button_width = 200
        self.button_height = 50
        self.button_color = (87, 172, 190)
        self.text_color = (255, 255, 255)
        self.rect = pygame.Rect(0, 0, self.button_width, self.button_height)
        self._clicked = False
        self.offset = 50


    @property
    def clicked(self):
        return self._clicked

    @clicked.setter
    def clicked(self, value):
        self._clicked = value
    def draw(self, surface, offset):
        screen_width = surface.get_width()
        screen_height = surface.get_height()
        button_rect = pygame.Rect(screen_width // 2 - self.rect.width // 2, screen_height // 2 - self.rect.height // 2, self.rect.width, self.rect.height
        )
        self.rect = button_rect
        pygame.draw.rect(surface, self.button_color, button_rect)
        text_surface = self.font.render(self.text, True, self.text_color, None)
        text_rect = text_surface.get_rect(center=button_rect.center)
        surface.blit(text_surface, text_rect)

    def check_click(self, pos):
        if self.rect.collidepoint(pos):
            self.callback()
            self.clicked = False


class Second_Button:
    def __init__(self, text, callback, font):
        self.text = text
        self.callback = callback
        self.font = pygame.font.Font(head_font, 17)
        self.button_width = 200
        self.button_height = 50
        self.button_color = (87, 172, 190)
        self.text_color = (255, 255, 255)
        self.rect = pygame.Rect(0, 0, self.button_width, self.button_height)
        self._clicked = False
        self.offset = 50

    @property
    def clicked(self):
        return self._clicked

    @clicked.setter
    def clicked(self, value):
        self._clicked = value
    def draw(self, surface, offset):
        screen_width = surface.get_width()
        screen_height = surface.get_height()
        button_rect = pygame.Rect(screen_width // 2 - 100 , 270 + offset, self.rect.width, self.rect.height
        )
        self.rect = button_rect
        pygame.draw.rect(surface, self.button_color, button_rect)
        text_surface = self.font.render(self.text, True, self.text_color, None)
        text_rect = text_surface.get_rect(center=button_rect.center)
        surface.blit(text_surface, text_rect)

    def check_click(self, pos):
        if self.rect.collidepoint(pos):
            self.callback()
            self.clicked = False

def start_game():
        print("Игра началась!")
        global game_started
        game_started = True

def quit_game():
        sys.exit()

class Record_Button:
    def __init__(self, text, callback, font):
        self.text = text
        self.callback = callback
        self.font = pygame.font.Font(head_font, 15)
        self.button_width = 200
        self.button_height = 50
        self.button_color = (87, 172, 190)
        self.text_color = (255, 255, 255)
        self.rect = pygame.Rect(0, 0, self.button_width, self.button_height)
        self._clicked = False
        self.offset = 100

    @property
    def clicked(self):
        return self._clicked

    @clicked.setter
    def clicked(self, value):
        self._clicked = value
    def draw(self, surface, offset):
        screen_width = surface.get_width()
        screen_height = surface.get_height()
        button_rect = pygame.Rect(screen_width // 2 - 100, 400 + offset, self.rect.width, self.rect.height)
        self.rect = button_rect
        pygame.draw.rect(surface, self.button_color, button_rect)
        text_surface = self.font.render(self.text, True, self.text_color, None)
        text_rect = text_surface.get_rect(center=button_rect.center)
        surface.blit(text_surface, text_rect)

    def check_click(self, pos):
        if self.rect.collidepoint(pos):
            self.callback()
            self.clicked = False

def open_highscores():
    highscores.display_scores()

class Entity:
    def __init__(self, image):
        self.image= image
        self.rect=self.image.get_rect()
        self.x_speed=0
        self.y_speed=0
        self.speed=5
        self.is_out=False
        self.is_dead=False
        self.jump_speed = -12
        self.gravity = 0.5
        self.is_grounded= False

    def handle_input(self):
        pass

    def kill(self, dead_image):
        self.image = dead_image
        self.is_dead=True
        self.x_speed= -self.x_speed
        self.y_speed=self.jump_speed

    def update(self):
        self.rect.x +=self.x_speed
        self.y_speed +=self.gravity
        self.rect.y += self.y_speed

        if self.is_dead:
            if self.rect.top > height_screen- ground_high:
                self.is_out=True
        else:
            self.handle_input()
            if self.rect.bottom > height_screen - ground_high:
                self.is_grounded=True
                self.y_speed=0
                self.rect.bottom=height_screen - ground_high

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Player(Entity):
    def __init__(self):
        super().__init__(player_image)
        self.respawn()

    def handle_input(self):
        self.x_speed=0

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.x_speed=-self.speed
        elif keys[pygame.K_d]:
            self.x_speed= self.speed

        if self.is_grounded and keys[pygame.K_SPACE]:
            self.is_grounded=False
            self.jump()

    def respawn(self):
        self.is_out=False
        self.is_dead=False
        self.rect.center=(width_screen//2 , height_screen//2)



    def jump(self):
        self.y_speed=self.jump_speed


class Frog(Entity):
    def __init__(self):
        super().__init__(enemy_image)
        self.spawn()

    def spawn(self):
        direction =random.randint(0,1)
        if direction ==0:
            self.x_speed =self.speed
            self.rect.bottomright= (0,0)
        else:
            self.x_speed= -self.speed
            self.rect.bottomleft = (width_screen , 0)

    def update(self):
        super().update()

        if self.is_dead:
            if self.rect.top > height_screen - ground_high:
                self.is_out = True
        else:
            # Установить состояние is_grounded, когда игрок находится на земле или начинает прыжок
            if self.y_speed <= 0:
                self.is_grounded = True
            else:
                self.is_grounded = False

            self.handle_input()
            if self.rect.bottom > height_screen - ground_high:
                self.is_grounded = True
                self.y_speed = 0
                self.rect.bottom = height_screen - ground_high


class Stone(Entity):
    def __init__(self):
        super().__init__(stone_image)
        self.second_spawn()


    def second_spawn(self):
        self.rect.x = random.randint(0, width_screen - self.rect.width)
        self.rect.y = random.randint(-150, -50)
        self.y_speed = 2


    def second_update(self):
        super().update()
        if self.rect.y >= height_screen:
            self.rect.y = -self.rect.height
            self.second_spawn()


player= Player()
score= 0
frogs=[]
stones=[]
INIT_DELAY = 2000
spawn_delay = INIT_DELAY
decrease_base = 1.01
last_spawn= pygame.time.get_ticks()
stone = Stone()

highscores = Highscores("templates/highscores.csv")

menu = Menu(800,600)
menu.set_background()
menu.add_button("Начать игру", start_game, head_font, y_offset=50)
menu.add_second_button("Выйти из игры", quit_game, head_font, y_offset= 50)
menu.add_record_button("Таблица рекордов", open_highscores, head_font, y_offset= 200)

game_started = False
running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            menu.handle_event(event)
        elif event.type == pygame.KEYDOWN:
            if player.is_out:
                score = 0
                spawn_delay = INIT_DELAY
                last_spawn = pygame.time.get_ticks()
                player.respawn()
                frogs.clear()
                stones.clear()

    if not game_started:
        menu.draw(screen)
    else:
        keys = pygame.key.get_pressed()
        player.handle_input()
        

        clock.tick(FPS)
        screen.fill((144, 160, 244))
        screen.blit(background_image, (0, 0))
        screen.blit(ground_image, (0, height_screen - ground_high - 20))

        if player.is_out:
            score_rect.center = (width_screen // 2, height_screen // 2)
            screen.blit(retry_text, retry_rect)
        else:
            player.update()
            player.draw(screen)
            now = pygame.time.get_ticks()
            elapsed = now - last_spawn
            if elapsed > spawn_delay:
                last_spawn = now
                frogs.append(Frog())

            for frog in list(frogs):
                if frog.is_out:
                    frogs.remove(frog)
                else:
                    frog.update()
                    frog.draw(screen)

                if not player.is_dead and not frog.is_dead and player.rect.colliderect(frog.rect):
                    if player.rect.bottom - player.y_speed < frog.rect.top:
                        frog.kill(enemy_image)
                        player.jump()
                        score += 1
                        frog_attack_sound.play()
                        if score == 4:
                            level_up_sound.play()
                        spawn_delay = INIT_DELAY / (decrease_base ** score)
                    else:
                        player.kill(player_image)
                        game_over_sound.play()

            for stone in list(stones):
                if stone.is_out:
                    stones.remove(stone)
                else:
                    stone.second_update()
                    stone.draw(screen)

                    if stone.rect.colliderect(player.rect):
                        player.kill(player_image)
                        game_over_sound.play()

                    if stone.rect.y >= height_screen - 90:
                        stones.remove(stone)
                    else:
                        stone.rect.y += stone.y_speed

            if score > 3:

                stone = Stone()
                stone.second_spawn()
                if elapsed > spawn_delay:
                    last_spawn = now
                    spawn_delay /= decrease_base
                    stones.append(stone)
    if not game_started:
        main_sound.play()

    score_text = font_head.render("Score: " + str(score), True, (255, 255, 255))
    score_rect = score_text.get_rect()
    score_rect.center = (width_screen // 2, 50)
    screen.blit(score_text, score_rect)
    pygame.display.flip()

quit()