import random
import pygame

pygame.init()
WIDTH = 400
HEIGHT = 500
background = pygame.transform.scale(pygame.image.load("background.jpg"),
                                    (WIDTH, HEIGHT))

player = pygame.transform.scale(pygame.image.load("Doodle.png"), (90, 70))
platform_img = pygame.transform.scale(pygame.image.load("rect.png"), (90, 45))
fps = 60
font = pygame.font.Font("freesansbold.ttf", 16)
timer = pygame.time.Clock()
score = 0
high_score = 0
game_over = False

player_x = 170
player_y = 400
platforms = [[175, 480, 70, 10], [85, 370, 70, 10], [265, 370, 70, 10], [175, 260, 70, 10], [85, 150, 70, 10],
             [265, 150, 70, 10], [175, 40, 70, 10]]
jump = False
y_change = 0
x_change = 0
player_speed = 3
super_jumps = 2
jump_last = 0

screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Doodle Jump")


def check_collisions(rect_list, jump):
    global player_x
    global player_y
    global y_change
    player_rect = pygame.Rect(player_x + 20, player_y + 60, 35, 5)
    for platform in rect_list:
        platform_rect = pygame.Rect(platform[0], platform[1], platform[2], platform[3])
        if player_rect.colliderect(platform_rect) and not jump and y_change > 0:
            return True
    return False


def update_player(y_pos):
    global jump
    global y_change
    jump_height = 10
    gravity = 0.4
    if jump:
        y_change = -jump_height
        jump = False
    y_pos += y_change
    y_change += gravity
    return y_pos


def update_platforms(my_list, y_pos, change):
    global score
    if y_pos < 250 and y_change < 0:
        for i in range(len(my_list)):
            my_list[i][1] -= y_change
    else:
        pass
    for item in range(len(my_list)):
        if my_list[item][1] > 500:
            my_list[item] = [random.randint(10, 320), random.randint(-50, -10), 70, 10]
            score += 1
    return my_list


running = True
while running:
    timer.tick(fps)
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    screen.blit(player, (player_x, player_y))
    blocks = []
    score_text = font.render("Рекорд: " + str(high_score), True, "BLACK")
    screen.blit(score_text, (280, 0))

    high_score_text = font.render("Счёт: " + str(score), True, "BLACK")
    screen.blit(high_score_text, (320, 20))

    score_text = font.render("Супер прыжки(Вверх):" + str(super_jumps), True, "BLACK")
    screen.blit(score_text, (10, 10))

    if game_over:
        game_over_text = font.render("Game Over: Пробел для рестарта!", True, "BLACK")
        screen.blit(game_over_text, (80, 80))

    for i in range(len(platforms)):
        screen.blit(platform_img, (platforms[i][0], platforms[i][1]))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_over:
                game_over = False
                score = 0
                player_x = 170
                player_y = 400
                background = background
                score_last = 0
                super_jumps = 2
                jump_last = 0
                platforms = [[175, 480, 70, 10], [85, 370, 70, 10], [265, 370, 70, 10], [175, 260, 70, 10],
                             [85, 150, 70, 10],
                             [265, 150, 70, 10], [175, 40, 70, 10]]
            if event.key == pygame.K_UP and not game_over and super_jumps > 0:
                super_jumps -= 1
                y_change = -15
            if event.key == pygame.K_a:
                x_change = -player_speed
            if event.key == pygame.K_d:
                x_change = player_speed

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                x_change = 0
            if event.key == pygame.K_d:
                x_change = 0

    jump = check_collisions(platforms, jump)
    player_x += x_change
    if player_y < 440:
        player_y = update_player(player_y)
    else:
        game_over = True
        y_change = 0
        x_change = 0

    platforms = update_platforms(platforms, player_y, y_change)

    if player_x < -20:
        player_x = -20
    elif player_x > 330:
        player_x = 330

    if x_change > 0:
        player = pygame.transform.flip(pygame.transform.scale(pygame.image.load("Doodle.png"), (90, 70)),
                                       1, 0)
    elif x_change < 0:
        player = pygame.transform.scale(pygame.image.load("Doodle.png"), (90, 70))

    if score > high_score:
        high_score = score

    if score - jump_last > 50:
        jump_last = score
        super_jumps += 1

    pygame.display.flip()

pygame.quit()