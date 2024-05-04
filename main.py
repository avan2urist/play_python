import pygame
import time
from random import randint

day_time = True

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        super().__init__()
        self.x = x
        self.y = y
        self.speed = speed
        self.is_jump = False
        self.jump_count = 10
        self.health = 6
        self.boss_collision_handled = False
        self.walk_left = [
            pygame.transform.scale(pygame.image.load('assets/hero_right/hero_right1.png'), (80, 80)),
            pygame.transform.scale(pygame.image.load('assets/hero_right/hero_right2.png'), (80, 80)),
            pygame.transform.scale(pygame.image.load('assets/hero_right/hero_right3.png'), (80, 80)),
            pygame.transform.scale(pygame.image.load('assets/hero_right/hero_right4.png'), (80, 80)),
            
        ]
        self.walk_right = [
            pygame.transform.scale(pygame.image.load('assets/hero_left/hero_left1.png'), (80, 80)),
            pygame.transform.scale(pygame.image.load('assets/hero_left/hero_left2.png'), (80, 80)),
            pygame.transform.scale(pygame.image.load('assets/hero_left/hero_left3.png'), (80, 80)),
            pygame.transform.scale(pygame.image.load('assets/hero_left/hero_left4.png'), (80, 80)), 
        ]
        self.player_anim_count = 0
        self.rect = self.walk_right[0].get_rect()
        self.rect.topleft = (x, y)
        self.action = 'idle'

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed
            self.action = 'left'
        elif keys[pygame.K_RIGHT] and self.x < 900:
            self.x += self.speed
            self.action = 'right'

    def jump(self, keys):
        if not self.is_jump:
            if keys[pygame.K_SPACE]:
                self.is_jump = True
        else:
            if self.jump_count >= -10:
                if self.jump_count > 0:
                    self.y -= (self.jump_count ** 2) / 2
                else:
                    self.y += (self.jump_count ** 2) / 2
                self.jump_count -= 1
            else:
                self.is_jump = False
                self.jump_count = 10

    def draw(self, screen, keys):
        self.player_anim_count = (self.player_anim_count + 1) % 4
        self.rect.y = self.y - 140  
        if self.action == 'left':
            screen.blit(self.walk_left[self.player_anim_count], self.rect.topleft)
        elif self.action == 'right':
            screen.blit(self.walk_right[self.player_anim_count], self.rect.topleft)
        else:
            screen.blit(self.walk_right[0], self.rect.topleft)

class Boss(pygame.sprite.Sprite):
    def __init__(self, speed, x, y):
        super().__init__()
        self.images = [
            pygame.image.load('assets/villain/villain_left1.png'),
            pygame.image.load('assets/villain/villain_left2.png'),
            pygame.image.load('assets/villain/villain_left3.png'),
            pygame.image.load('assets/villain/villain_left4.png'),
        ]
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = 1000
        self.rect.y = randint(0, 0)
        self.x = x
        self.y = y
        self.speed = speed
        self.animation_speed = 8
        self.last_update = pygame.time.get_ticks()
        self.rect = self.images[0].get_rect()
        self.rect.topleft = (self.x, self.y)
        self.action = 'idle'

    def update(self):
        self.rect.x -= self.speed
        if self.rect.x < -150:
            self.kill()
        now = pygame.time.get_ticks()
        if now - self.last_update > self.animation_speed:
            self.last_update = now
            self.index = (self.index + 1) % len(self.images)
            self.image = self.images[self.index]

class Game:
    def __init__(self):
        
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((1000, 563))
        pygame.display.set_caption("Bird_Play")
        self.bg_day = pygame.image.load('assets/scenery/day_background.png')  
        self.bg_night = pygame.image.load('assets/scenery/night_background.png')  
        self.bg = self.bg_day  # Начальное изображение фона
        self.bg_sound_day = pygame.mixer.Sound('sounds/daytime_tune.mp3')  
        self.bg_sound_night = pygame.mixer.Sound('sounds/nighttime_tune.mp3')  
        self.bg_sound = self.bg_sound_day  
        self.bg_sound.play(loops=-1)  
        self.menu = True  
        self.bg_rt = self.bg_day  
        self.bg_x = 0  
        self.font = pygame.font.Font(None, 36)  
        self.player_speed = 5  #
        self.last_boss_spawn_time = 0  
        self.boss_spawn_delay = 2000  
        self.hp_gf = pygame.image.load('assets/ui/health_icon.png') 
        
    def toggle_day_night(self):
        global day_time
        day_time = not day_time
        self.bg_sound.stop() 
        if day_time:
            self.bg = self.bg_day
            self.bg_sound = self.bg_sound_day
        else:
            self.bg = self.bg_night
            self.bg_sound = self.bg_sound_night
        self.bg_sound.play(loops=-1)  
        
    def game_over(self):
        self.screen.fill((238, 134, 244))
        self.draw_text("Конец", self.font, (255, 255, 255), self.screen, 500, 251)
        pygame.display.update()
        time.sleep(5)
        waiting = True
        self.bg_sound.stop()
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        waiting = False
    
    def run(self):
        while self.menu:
            self.screen.blit(self.bg_rt, (self.bg_x, 0))
            self.draw_text("Приветсвенное сообщение по тз. Можем начинать игру", self.font, (255, 255, 255), self.screen, 500, 251)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.menu = False
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.menu = False
            pygame.display.update()
        running = True
        player = Player(350, 420, self.player_speed)
        boss_group = pygame.sprite.Group()
        while running:
            self.screen.blit(self.bg, (self.bg_x, 0))
            self.screen.blit(self.bg, (self.bg_x + 1000, 0))
            keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_n:
                        self.toggle_day_night()
            player.move(keys)
            player.jump(keys)
            player.draw(self.screen, keys)
            current_time = pygame.time.get_ticks()
            if current_time - self.last_boss_spawn_time > self.boss_spawn_delay:
                boss = Boss(10, 1000, randint(320, 320))
                boss_group.add(boss)
                self.last_boss_spawn_time = current_time
            boss_group.update()
            boss_group.draw(self.screen)
            player.rect.topleft = (player.x, player.y-50)
            collided_bosses = pygame.sprite.spritecollide(player, boss_group, True)
            for boss in collided_bosses:
                player.health -= 1
            if player.health <= 0:
                self.game_over()
                running = False
            self.bg_x -= 5
            if self.bg_x == -1000:
                self.bg_x = 0
            self.draw_health(player)
            pygame.display.update()
            self.clock.tick(20)

    def draw_health(self, player):
        x = 10
        for _ in range(player.health):
            self.screen.blit(self.hp_gf, (x, 40))
            x += 40

    def draw_text(self, text, font, color, surface, x, y):
        text_obj = font.render(text, True, 'white')
        text_rect = text_obj.get_rect()
        text_rect.center = (x, y)
        surface.blit(text_obj, text_rect)

if __name__ == "__main__":
    game = Game()
    game.run()
