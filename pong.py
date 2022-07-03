import pygame, sys, random

game = {1: 0, 2: 0}
set = {1: 0, 2: 0}
match = {1: 0, 2: 0}
matchlist = []
record = []


class Block(pygame.sprite.Sprite):
    def __init__(self, path, x_pos, y_pos):
        super().__init__()
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect(center=(x_pos, y_pos))


class Player(Block):
    def __init__(self, path, x_pos, y_pos, speed):
        super().__init__(path, x_pos, y_pos)
        self.speed = speed
        self.movement = 0

    def screen_constrain(self):
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= screen_height:
            self.rect.bottom = screen_height

    def update(self, ball_group):
        self.rect.y += self.movement
        self.screen_constrain()


class Ball(Block):
    def __init__(self, path, x_pos, y_pos, speed_x, speed_y, paddles):
        super().__init__(path, x_pos, y_pos)
        self.speed_x = speed_x * random.choice((1, 1)) #------------------------------------------------------------------------------------------#
        self.speed_y = speed_y * random.choice((-1, 1)) #------------------------------------------------------------------------------------------#
        self.paddles = paddles
        self.active = True
        self.score_time = 0

    def update(self):
        if self.active:
            self.rect.x += self.speed_x
            self.rect.y += self.speed_y
            self.collisions()
        else:
            self.restart_counter()

    def collisions(self):
        if self.rect.top <= 0 or self.rect.bottom >= screen_height:
            #sound            pygame.mixer.Sound.play(plob_sound)
            self.speed_y *= -1

        if pygame.sprite.spritecollide(self, self.paddles, False):
            #sound            pygame.mixer.Sound.play(plob_sound)
            collision_paddle = pygame.sprite.spritecollide(self, self.paddles, False)[0].rect
            if abs(self.rect.right - collision_paddle.left) < 10 and self.speed_x > 0:
                self.speed_x *= -1
                self.speed_y *= -1
            if abs(self.rect.left - collision_paddle.right) < 10 and self.speed_x < 0:
                self.speed_x *= -1
                self.speed_y *= -1
            if abs(self.rect.top - collision_paddle.bottom) < 10 and self.speed_y < 0:
                self.rect.top = collision_paddle.bottom
                self.speed_y *= -1
            if abs(self.rect.bottom - collision_paddle.top) < 10 and self.speed_y > 0:
                self.rect.bottom = collision_paddle.top
                self.speed_y *= -1

    def reset_ball(self):
        self.active = False
        self.speed_x = abs(self.speed_x) * random.choice((1, 1)) #--------------------------------------------# abs() para que siempre vaya a la izquierda
        self.speed_y *= random.choice((1, 1)) #------------------------------------------------------------------------------------------#
        self.score_time = pygame.time.get_ticks()
        self.rect.center = (screen_width / 2, screen_height / 2)
        #sound        pygame.mixer.Sound.play(score_sound)

    def restart_counter(self): #contador 3, 2, 1 en saque de pelota desde el centro (no se esta usando)
        current_time = pygame.time.get_ticks()
        countdown_number = 3

        if current_time - self.score_time <= 700:
            countdown_number = 3
            self.active = True  #------------------------------------------------------------------------------------------# provisional (ahorra tiempo)
        if 700 < current_time - self.score_time <= 1400:
            countdown_number = 2
        if 1400 < current_time - self.score_time <= 2100:
            countdown_number = 1
        if current_time - self.score_time >= 2100:
            self.active = True

        time_counter = basic_font.render(str(countdown_number), True, color1)
        time_counter_rect = time_counter.get_rect(center=(screen_width / 2, screen_height / 2 + 50))
        #pygame.draw.rect(screen, bg_color, time_counter_rect)
        #screen.blit(time_counter, time_counter_rect)


class Opponent(Block):
    def __init__(self, path, x_pos, y_pos, speed):
        super().__init__(path, x_pos, y_pos)
        self.speed = speed

    def update(self, ball_group):
        if self.rect.top < ball_group.sprite.rect.y:
            self.rect.y += self.speed
        if self.rect.bottom > ball_group.sprite.rect.y:
            self.rect.y -= self.speed
        self.constrain()

    def constrain(self):
        if self.rect.top <= 0: self.rect.top = 0
        if self.rect.bottom >= screen_height: self.rect.bottom = screen_height


class GameManager:
    def __init__(self, ball_group, paddle_group):
        self.player_score = 0
        self.opponent_score = 0
        self.ball_group = ball_group
        self.paddle_group = paddle_group

    def run_game(self):
        # Drawing the game objects
        self.paddle_group.draw(screen)
        self.ball_group.draw(screen)

        # Updating the game objects
        self.paddle_group.update(self.ball_group)
        self.ball_group.update()
        self.reset_ball()
        self.draw_score()

    def reset_ball(self):
        if self.ball_group.sprite.rect.right >= screen_width:
            self.opponent_score += 1
            f_game(2) #------------------------------------------------------------------------------------------#
            self.ball_group.sprite.reset_ball()
        if self.ball_group.sprite.rect.left <= 0:
            self.player_score += 1
            f_game(1) #------------------------------------------------------------------------------------------#
            self.ball_group.sprite.reset_ball()

    def draw_score(self):

        player1_text = pygame.font.SysFont(None, 40)
        player2_text = pygame.font.SysFont(None, 40)
        set_text = pygame.font.SysFont(None, 22)
        game_text = pygame.font.SysFont(None, 22)
        point_text = pygame.font.SysFont(None, 22)
        player1_set = pygame.font.SysFont(None, 40)
        player2_set = pygame.font.SysFont(None, 40)
        player1_game = pygame.font.SysFont(None, 40)
        player2_game = pygame.font.SysFont(None, 40)
        player1_point = pygame.font.SysFont(None, 40)
        player2_point = pygame.font.SysFont(None, 40)
        
        player1_text_img = player1_text.render('Player 1', True, color0)
        player2_text_img = player2_text.render('Player 2', True, color0)
        set_text_img = set_text.render('SETS', True, color0)
        game_text_img = game_text.render('GAMES', True, color0)
        point_text_img = point_text.render('POINTS', True, color0)
        player1_set_img = player1_set.render(str(match[1]), True, color0)
        player2_set_img = player2_set.render(str(match[2]), True, color0)
        player1_game_img = player1_game.render(str(set[1]), True, color0)
        player2_game_img = player2_game.render(str(set[2]), True, color0)
        player1_point_img = player1_point.render(str(game[1]), True, color0)
        player2_point_img = player2_point.render(str(game[2]), True, color0)

        screen.blit(player1_text_img, ((screen_width / 3) + 80, (screen_height / 8) + 20))
        screen.blit(player2_text_img, ((screen_width / 3) + 80, (screen_height / 8) + 60))
        screen.blit(set_text_img, ((screen_width / 3) + 218, screen_height / 9))
        screen.blit(game_text_img, ((screen_width / 3) + 280, screen_height / 9))
        screen.blit(point_text_img, ((screen_width / 3) + 360, screen_height / 9))
        screen.blit(player1_set_img, ((screen_width / 3) + 230, (screen_height / 8) + 20))
        screen.blit(player2_set_img, ((screen_width / 3) + 230, (screen_height / 8) + 60))
        screen.blit(player1_game_img, ((screen_width / 3) + 300, (screen_height / 8) + 20))
        screen.blit(player2_game_img, ((screen_width / 3) + 300, (screen_height / 8) + 60))
        screen.blit(player1_point_img, ((screen_width / 3) + 370, (screen_height / 8) + 20))
        screen.blit(player2_point_img, ((screen_width / 3) + 370, (screen_height / 8) + 60))

def sets_number():
    global sets
    '''
    while True:
        sets = input('How many sets?\n[3 or 5]')
        if (sets == '3') or (sets == '5'):
            sets = int(sets)
            break
        else:
            print('3 or 5')
    '''
    sets = 3

def f_change(self):
    if self == 1:
        return 2
    elif self == 2:
        return 1

def print_long(self):
    print("\nPoint player{}\nPlayer 1 - Player 2\nGames:    {} - {}\nSets:  {} - {}".format(self, set[1], set[2], match[1], match[2]))

def f_game(self):
    if (game[self] == 0) or (game[self] == 15):
        game[self] += 15
        print("\n{} - {}".format(game[1], game[2]))
    elif game[self] == 30:
        game[self] += 10
        if game[f_change(self)] == 40:
           print('\nDeuce')
        else:
            print("\n{} - {}".format(game[1], game[2]))
    elif game[self] == 40:
        if game[f_change(self)] == 'AD':
            game[f_change(self)] = 40
            print('\nDeuce')
        elif game[f_change(self)] == 40:
            game[self] = 'AD'
            print('\nAdventure player{}'.format(self))
        elif game[f_change(self)] < 40:
            f_set(self)
    elif game[self] == 'AD':
        f_set(self)
    else:
        print('\nError game')

def f_set(self):
    game[self] = 0
    game[f_change(self)] = 0
    if set[self] < 5:
        set[self] += 1
        print_long(self)
    elif set[self] == 5:
        if set[f_change(self)] < 5:
            f_match(self)
        elif set[f_change(self)] == 5:
            set[self] += 1
            print_long(self)
        elif set[f_change(self)] ==6:
            set[self] += 1
            print_long(self)
            if match[1] + match[2] < sets-1:
                f_tiebreak()
            else:
                return
    elif set[self] == 6:
        if set[f_change(self)] == 5:
            f_match(self)
        elif set[f_change(self)] > 5:
            if set[self] == set[f_change(self)] + 1:
                f_match(self)
            else:
                set[self] += 1
                print_long(self)
    elif set[self] > 6:
        if set[self] == set[f_change(self)] + 1:
            f_match(self)
        else:
            set[self] += 1
            print_long(self)
    else:
        print('\nerror set')

def f_match(self):
    game[self] = 0
    game[f_change(self)] = 0
    set[self] += 1
    matchlist.append(set[1])
    matchlist.append(set[2])
    set[self] = 0
    set[f_change(self)] = 0
    match[self] += 1
    if match[self] > sets/2:
        print('\nGame, set and match player{}'.format(self))
        for i in range(len(matchlist) // 2):
            print('{} - {}'.format(matchlist[i * 2], matchlist[i * 2 + 1]))
    else:
        print('\nSet player{}'.format(self))
        print("\nPlayer 1 - Player 2\nGames:    {} - {}\nSets:  {} - {}".format(set[1], set[2], match[1], match[2]))

def f_tiebreak():
    print('\nTie Break')
    game[1] = 0
    game[2] = 0
    while True:
        while True:
            dato = (int(input('\nPoint for:')))
            if (dato == 1) or (dato == 2):
                break
            else:
                print('\n[1 or 2]')
        if (game[dato] < 6) or (game[dato] == game[f_change(dato)]) or (game[dato] + 1 == game[f_change(dato)]):
            game[dato] += 1
            print("\n{} - {}".format(game[1], game[2]))
        elif (game[dato] == game[f_change(dato)] + 1) or ((game[dato] == 6) and (game[f_change(dato) < 6])):
            f_match(dato)
            break
        else:
            print('\nerror tiebreak')


# Previous
sets_number()

# General setup
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
clock = pygame.time.Clock()

# Main Window
screen_width = 1440 #1920
screen_height = 850 #1030 ok for hp
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Pong')

# Global Variables
bg_color = pygame.Color(27, 35, 43)
color0 = (255, 255, 255)
color1 = (108, 147, 92) #------------------------------------------------------------------------------------------# accent_color
color2 = (60, 99, 142) #------------------------------------------------------------------------------------------#
basic_font = pygame.font.Font('freesansbold.ttf', 32) #letter type/size
#sound plob_sound = pygame.mixer.Sound("pong.ogg")
#sound score_sound = pygame.mixer.Sound("score.ogg")
court1 = pygame.Rect(0, screen_height / 2 - screen_width * (9.13 / 36.58), screen_width, 2 * screen_width * (9.13 / 36.58))
court2 = pygame.Rect((6.4 / 36.58) * screen_width, screen_height / 2 - screen_width * (5.48 / 36.58), screen_width * (23.78 / 36.58), 2 * screen_width * (5.48 / 36.58))

line1 = pygame.Rect((6.4 / 36.58) * screen_width, screen_height / 2 - screen_width * (5.48 / 36.58), screen_width * (0.05 / 36.58), 2 * screen_width * (5.48 / 36.58))
line2 = pygame.Rect((6.4 / 36.58) * screen_width, screen_height / 2 - screen_width * (5.48 / 36.58), screen_width * (23.78 / 36.58), screen_width * (0.05 / 36.58))
line3 = pygame.Rect((30.13 / 36.58) * screen_width, screen_height / 2 - screen_width * (5.48 / 36.58), screen_width * (0.05 / 36.58), 2 * screen_width * (5.48 / 36.58))
line4 = pygame.Rect((6.4 / 36.58) * screen_width, screen_height / 2 + screen_width * (5.48 / 36.58), screen_width * (23.78 / 36.58), screen_width * (0.05 / 36.58))
line5 = pygame.Rect((6.4 / 36.58) * screen_width, screen_height / 2 - screen_width * (4.11 / 36.58), screen_width * (23.78 / 36.58), screen_width * (0.05 / 36.58))
line6 = pygame.Rect((6.4 / 36.58) * screen_width, screen_height / 2 + screen_width * (4.11 / 36.58), screen_width * (23.78 / 36.58), screen_width * (0.05 / 36.58))
line7 = pygame.Rect((11.88 / 36.58) * screen_width, screen_height / 2 - screen_width * (4.11 / 36.58), screen_width * (0.05 / 36.58), 2 * screen_width * (4.11 / 36.58))
line8 = pygame.Rect((24.65 / 36.58) * screen_width, screen_height / 2 - screen_width * (4.11 / 36.58), screen_width * (0.05 / 36.58), 2 * screen_width * (4.11 / 36.58))
line9 = pygame.Rect((11.88 / 36.58) * screen_width, screen_height / 2 - screen_width * (0.025 / 36.58), screen_width * (12.82 / 36.58), screen_width * (0.05 / 36.58))
line10 = pygame.Rect((6.4 / 36.58) * screen_width, screen_height / 2 - screen_width * (0.025 / 36.58), screen_width * (0.1 / 36.58), screen_width * (0.05 / 36.58))
line11 = pygame.Rect((30.08 / 36.58) * screen_width, screen_height / 2 - screen_width * (0.025 / 36.58), screen_width * (0.1 / 36.58), screen_width * (0.05 / 36.58))


#court = pygame.Rect(0,30,60,90) # red

# Game objects
player = Player('Paddle.png', screen_width - 20, screen_height / 2, 5)
opponent = Opponent('Paddle.png', 20, screen_width / 2, 5)
paddle_group = pygame.sprite.Group()
paddle_group.add(player)
# paddle_group.add(opponent)

ball = Ball('Ball.png', screen_width / 2, screen_height / 2, 8, 1, paddle_group) #max speed 22?
ball_sprite = pygame.sprite.GroupSingle()
ball_sprite.add(ball)

game_manager = GameManager(ball_sprite, paddle_group)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player.movement -= player.speed
            if event.key == pygame.K_DOWN:
                player.movement += player.speed
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                player.movement += player.speed
            if event.key == pygame.K_DOWN:
                player.movement -= player.speed

    # Background Stuff

    screen.fill(bg_color)
    pygame.draw.rect(screen, color1, court1)
    pygame.draw.rect(screen, color2, court2)
    pygame.draw.rect(screen, color0, line1)
    pygame.draw.rect(screen, color0, line2)
    pygame.draw.rect(screen, color0, line3)
    pygame.draw.rect(screen, color0, line4)
    pygame.draw.rect(screen, color0, line5)
    pygame.draw.rect(screen, color0, line6)
    pygame.draw.rect(screen, color0, line7)
    pygame.draw.rect(screen, color0, line8)
    pygame.draw.rect(screen, color0, line9)
    pygame.draw.rect(screen, color0, line10)
    pygame.draw.rect(screen, color0, line11)

    # Run the game
    game_manager.run_game()

    # Rendering
    pygame.display.flip()
    clock.tick(120)
