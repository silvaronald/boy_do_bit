import pygame
import os
import random
from pygame import mixer


def main():
    pygame.init()

    SCREEN_WIDTH = 1000
    SCREEN_HEIGHT = 600

    win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    game_speed = 20

    # Função para padronizar o volume dos sons
    def create_sound(name):
        fullname = "Assets/sounds/" + name     # path + name of the sound file
        sound = pygame.mixer.Sound(fullname)
        sound.set_volume(0.40)
        return sound

    # Sons utilizados
    bg_music = create_sound("pixel_king_hall.mp3")

    # Como o background_sound vai rolar no jogo inteiro, vai começar a tocar logo daqui
    bg_music.play(-1)

    # Os sons seguintes serao implementados depois (sound effects)

    death_sound = create_sound("death_sound.mp3")

    collect_Sound = create_sound("collect.wav")

    collide_Sound = create_sound("collision.wav")

    bullet_Sound = create_sound("laser1.wav")

    # Imagens que serão utilizadas
    run_animation = []

    jump_animation = []

    background_image = pygame.image.load(os.path.join("Assets/background", "rua_da_aurora.png"))
    background_image = pygame.transform.scale(background_image, (1000, 600)).convert()

    projectile_image = pygame.image.load(os.path.join("Assets/projectile", "Aceito.png"))

    obstacle_images = [pygame.image.load(os.path.join("Assets/barrier", "pixel_wrong.png")),
                       pygame.image.load(os.path.join("Assets/barrier", "pixel_runtime-error.png"))]

    img_coins = [pygame.image.load(os.path.join("Assets/collectables", "pixel 0.png")),
                 pygame.image.load(os.path.join("Assets/collectables", "pixel 1.png"))]

    game_over_bg = pygame.image.load(os.path.join("Assets/gameover", "game_over_background.png"))

    # A posição ta zoada, ta sendo controlado de acordo com o game_speed (line 322-330)
    diff_images = [pygame.image.load(os.path.join("Assets/diff", "easy.png")),
                 pygame.image.load(os.path.join("Assets/diff", "medium.png")), pygame.image.load(os.path.join("Assets/diff", "hard.png"))]

    heart_image = pygame.image.load(os.path.join("Assets/collectables", "heart pixel art 64x64.png"))

    slow_item = pygame.image.load(os.path.join("Assets/collectables", "slow passion fruit.png"))

    up, down = pygame.image.load(os.path.join("Assets/enemy", "dikastis_up_pixel.png")), pygame.image.load(
        os.path.join("Assets/enemy", "dikastis_down_pixel.png"))
    up, down = pygame.transform.scale(up, (80, 130)), pygame.transform.scale(down, (100, 130))

    dikastis_animation = [up, down]

    destruction_animation = []

    for i in os.listdir("Assets/destroy"):
        destro = pygame.image.load(os.path.join("Assets/destroy", f"{i}"))
        destro_scaled = pygame.transform.scale(destro, (80, 130))
        destruction_animation.append(destro_scaled)

    for i in os.listdir("Assets/player/run"):
        run = pygame.image.load(os.path.join("Assets/player/run", f"{i}"))
        run_scaled = pygame.transform.scale(run, (100, 125))
        run_animation.append(run_scaled)

    for i in os.listdir("Assets/player/jump"):
        jump = pygame.image.load(os.path.join("Assets/player/jump", f"{i}"))
        jump_scaled = pygame.transform.scale(jump, (100, 125))
        jump_animation.append(jump_scaled)

    class BG(object):
        def __init__(self):
            self.x = 0
            self.y = 0

            self.bg_img = background_image
            self.bg_width = self.bg_img.get_width()

        def update(self):
            if self.x <= -self.bg_width:
                self.x = 0

            self.x -= game_speed

        def draw(self, SCREEN):
            SCREEN.blit(self.bg_img, (self.x, self.y))
            SCREEN.blit(self.bg_img, (self.bg_width + self.x, self.y))

    class player(object):
        def __init__(self, y):
            self.x = 50
            self.y = y

            self.run_img = run_animation
            self.jump_img = jump_animation
            self.stepindex = 1
            self.isJump = False
            self.isrun = True
            self.stop = 0

            self.image = self.run_img[0]
            self.boy_rect = self.image.get_rect()
            self.boy_rect.x = self.x
            self.boy_rect.y = self.y

        # Atualiza as informações do player a cada loop
        def update(self, userInput):
            if self.isrun:
                self.run()
            if self.isJump:
                self.jump()
            if self.isJump:
                self.isrun = False

        # Animação de corrida
        def run(self):
            self.image = self.run_img[self.stepindex // 2]
            self.boy_rect.x = self.x
            self.boy_rect.y = self.y
            if self.stepindex < len(run_animation):
                self.stepindex += 1
            else:
                self.stepindex = 0

        # Animação do pulo
        def jump(self):
            self.image = self.jump_img[self.stepindex // 2]
            self.boy_rect.x = self.x
            self.boy_rect.y = self.y
            if self.stepindex < len(jump_animation):
                self.stepindex += 1
            else:
                self.stepindex = 0

        def draw(self, SCREEN):
            SCREEN.blit(self.image, (self.boy_rect.x, self.boy_rect.y))

    class projectile(object):
        def __init__(self, x, y):
            self.x = x
            self.y = y
            self.vel = 40

            self.image = projectile_image
            self.proj_rect = self.image.get_rect()
            self.proj_rect.x = self.x
            self.proj_rect.y = self.y

        def draw(self, SCREEN):
            SCREEN.blit(self.image, (self.proj_rect.x, self.proj_rect.y))

    # Super-classe dos obstáculos
    class obstacle:
        def __init__(self, image, type, category):
            self.image = image
            self.type = type
            self.category = category
            self.rect = self.image[self.type].get_rect()
            self.rect.x = 1000

        def update(self):
            self.rect.x -= game_speed
            if self.rect.x < -self.rect.width:
                obstacles.pop()

        def draw(self, SCREEN):
            SCREEN.blit(self.image[self.type], (self.rect.x, self.rect.y))

    class unacceptable(obstacle):
        def __init__(self, image):
            self.type = random.randint(0, 1)
            self.category = "obstacle"
            super().__init__(image, self.type, self.category)
            self.rect.y = 445

    class dikastis(obstacle):
        def __init__(self, image):
            self.type = 0
            self.category = "enemy"
            super().__init__(image, self.type, self.category)
            self.rect.y = random.randint(220, 340)
            self.index = 0

        def draw(self, SCREEN):
            SCREEN.blit(self.image[self.index // 2], self.rect)
            if self.index > 1:
                self.index = 0
            self.index += 1

    # Super-classe para os coletáveis
    class collecty:
        def __init__(self, image, type, category):
            self.image = image
            self.type = type
            self.category = category
            #se o obj for apenas uma imagem self.type recebe None
            if self.type == None:
                self.rect = self.image.get_rect()
            #se o obj for uma lista de imagens, self.type receberá um valor que representa o index da lista
            else:
                self.rect = self.image[self.type].get_rect()
            self.rect.x = 1000

        #coloquei um parâmetro lista pois inicialmente a função se baseava apenas na lista collectable
        def update(self, lista):
            self.rect.x -= game_speed
            if self.rect.x < -self.rect.width:
                try:
                    lista.pop()
                except:
                    None

        def draw(self, SCREEN):
            if self.type == None:
                SCREEN.blit(self.image, (self.rect.x, self.rect.y))
            else:
                SCREEN.blit(self.image[self.type], (self.rect.x, self.rect.y))

    # Classe dos 0's e 1's
    class coin(collecty):
        def __init__(self, image):
            self.type = random.randint(0, 1)
            self.category = "coin"
            super().__init__(image, self.type, self.category)
            self.rect.y = random.randint(230, 350)

    #classe dos corações s
    class life_heart(collecty):
        def __init__(self, image):
            self.type = None
            self.category = "heart"
            super().__init__(image, self.type, self.category)
            self.rect.y = obstacle.rect.y
            self.rect.x = obstacle.rect.x

    #classe do item que desacelera o jogo (é um maracujá)
    class slow_item_passion(collecty):
        def __init__(self, image):
            self.type = None
            self.category = "maracuja"
            super().__init__(image, self.type, self.category)
            self.rect.y = obstacle.rect.y
            self.rect.x = obstacle.rect.x

    jumpcount = 10

    pygame.display.set_caption("Boy do Bit")

    font = pygame.font.SysFont('comicsans', 20, True)

    # Criando objeto boy --> (player)
    boy = player(400)

    background = BG()
    bullets = []
    obstacles = []
    collectable = []
    hearts = []
    passion_fruit = []

    wait_animation_player = 0
    wait_animation_enemy = 0

    time = 0
    lives = 3
    zeros = 0
    ones = 0

    run = True
    while run:
        # Desenha o background
        background.draw(win)
        background.update()
        
        pygame.time.delay(50)

        time += 1

        # Aumenta a dificuldade (velocidade dos objetos) conforme o tempo passa
        if time % 50 == 0:
            game_speed += 0.6

        # Condições de dificuldade (exibir na tela easy, medium ou hard feito o Dikastis)
        if game_speed < 25:
            win.blit(diff_images[0], (818,70))

        elif game_speed < 35:
            win.blit(diff_images[1], (818,70))

        else:
            win.blit(diff_images[2], (818,70))

        # Exclui o check quando ele sai da visão
        for bullet in bullets:
            if bullet.x < 1000 and bullet.x > 0:
                bullet.x += bullet.vel
                bullet.proj_rect.x += bullet.vel

            else:
                bullets.pop(bullets.index(bullet))

        # Fecha o jogo quando o player clica no X
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        userInput = pygame.key.get_pressed()

        # Atira um check quando o player aperta ESPAÇO
        if userInput[pygame.K_SPACE]:
            if len(bullets) < 1:
                bullets.append(projectile(165, boy.y + 55))

        # Pula quando o player aperta W
        if not (boy.isJump):
            if userInput[pygame.K_w]:
                boy.isJump = True

        else:
            if jumpcount >= -10:
                neg = 1

                if jumpcount < 0:
                    neg = -1

                boy.y -= 0.40 * jumpcount ** 2 * neg

                jumpcount -= 1

            else:
                boy.isJump = False
                boy.isrun = True
                jumpcount = 10

        boy.draw(win)
        boy.update(userInput)

        for bullet in bullets:
            bullet.draw(win)

        # Cria um obstáculo aleatório
        if len(obstacles) == 0:
            if random.randint(0, 1) == 0:
                obstacles.append(unacceptable(obstacle_images))

            else:
                obstacles.append(dikastis(dikastis_animation))

        for obstacle in obstacles:
            obstacle.draw(win)
            obstacle.update()

            # O player perde uma vida quando bate em algum obstáculo
            if boy.boy_rect.colliderect(obstacle.rect):
                obstacles.pop(obstacles.index(obstacle))
                collide_Sound.play()
                lives -= 1

            # Destrói um Dikastis se o player o atingir com um check
            for bullet in bullets:
                if bullet.proj_rect.colliderect(obstacle.rect) and obstacle.category == "enemy":
                    # Quando um Dikastis é destruído, existe 5% de chance de surgir um coração em seu lugar
                    if random.randint(1, 100) <= 5:
                        hearts.append(life_heart(heart_image))
                    #Pode ter a chance de aparecer uma fruta que diminui velocidade (probabilidade de 10%)
                    elif random.randint(1, 100) <= 10:
                        passion_fruit.append(slow_item_passion(slow_item))

                    bullet_Sound.play()
                    try:
                        obstacles.pop(obstacles.index(obstacle))
                    except:
                        None

                    bullets.pop(bullets.index(bullet))
                    bullet.draw(win)
                    obstacle.draw(win)

        # Cria 0's e 1's
        if len(collectable) == 0:
            collectable.append(coin(img_coins))

        # Aumenta a pontuação conforme o usuário coleta 0's e 1's 
        for collect in collectable:
            collect.draw(win)
            collect.update(collectable)

            if boy.boy_rect.colliderect(collect.rect):
                collect_Sound.play()

                if collect.type == 0:
                    zeros += 1

                if collect.type == 1:
                    ones += 1

                collectable.pop(collectable.index(collect))
        
        # Ganha +1 vida ao colidir com um coração
        for heart in hearts:
            heart.draw(win)
            heart.update(hearts)

            if boy.boy_rect.colliderect(heart.rect):
                lives += 1

                if lives > 3:
                    lives = 3
                
                hearts.pop(hearts.index(heart))

        #se pegar um maracuja (slow passion fruit) a velocidade do jogo diminui
        for maracuja in passion_fruit:
            maracuja.draw(win)
            maracuja.update(passion_fruit)

            if boy.boy_rect.colliderect(maracuja.rect):
                game_speed -= 0.6

                passion_fruit.pop(passion_fruit.index(maracuja))


        # Mostra na tela os status de vidas e bits coletados
        text0 = font.render('Lives: ' + str(lives), True, (0, 0, 0))
        text1 = font.render('0: ' + str(zeros), True, (0, 0, 0))
        text2 = font.render('1: ' + str(ones), True, (0, 0, 0))

        win.blit(text0, (50, 50))
        win.blit(text1, (50, 80))
        win.blit(text2, (50, 100))

        pygame.display.update()

        if lives == 0:
            bg_music.stop()
            death_sound.play()

            Game_Over(game_over_bg, zeros, ones)

            break

    pygame.quit()


def Game_Over(bg,zeros=0, ones=0):
    pygame.init()

    win = pygame.display.set_mode((1000, 600))

    pygame.display.set_caption("Boy do Bit")

    font = pygame.font.Font('Assets/fonts/zorque.otf', 20)

    run = True
    while run:
        pygame.time.delay(50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        userInput = pygame.key.get_pressed()

        if userInput[pygame.K_SPACE]:
            main()
            break

        #background do Game Over
        bg = pygame.image.load(os.path.join("Assets/gameover", "game_over_background.png")).convert()
        win.blit(bg, (0,0))

        # Mostra o menu de fim de jogo
        text0 = font.render('GAME OVER', True, (255, 255, 255))
        text1 = font.render("press 'space' to restart", True, (0, 0, 0))
        text_zeros = font.render("0's collected:" + str(zeros), True, (255, 255, 255))
        text_ones = font.render("1's collected:" + str(ones), True, (255, 255, 255))

        text0_rect = text0.get_rect(center=(500, 200))
        text1_rect = text1.get_rect(center=(500, 240))
        text_zeros_rect = text_zeros.get_rect(center=(500, 300))
        text_ones_rect = text_ones.get_rect(center=(500, 340))


        pygame.draw.rect(win,(201,34,46), pygame.Rect(360, 140, 290, 270), 0, 3)

        win.blit(text0, text0_rect)
        win.blit(text1, text1_rect)
        win.blit(text_zeros, text_zeros_rect)
        win.blit(text_ones, text_ones_rect)

        pygame.display.update()

    pygame.quit()

main()