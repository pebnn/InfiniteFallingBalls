import pygame
import random
import os

# if score.txt does not exist, create score.txt
if os.path.exists("score.txt") == False:
    with open("score.txt", "w") as scores:
        pass

# Create score list and append each line from score.txt to this list
score_list = []
try:
    with open("score.txt", "r") as scores:
        scores_values = scores.readlines()
        for score in scores_values:
            score = score.strip("\n")
            score_list.append(int(score))
except FileNotFoundError:
    pass

# Sort list entries in descending order
score_list.sort(reverse=True)

# pygame setup
pygame.init()
screen = pygame.display.set_mode((690, 720))
clock = pygame.time.Clock()
pygame.display.set_caption("Infinite falling balls")
running = True

# Colors
grass_green = "#23b01e"
sky_blue = "#52d6fa"
dirt_brown = "#4f1c00"


# The Player class
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 20
        self.speed = 5

    def update(self, keys):
        # Move left if players x value is higher than 0
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed
        # Move right if players x value is lower than 650
        elif keys[pygame.K_RIGHT] and self.x < 650:
            self.x += self.speed

    # Player
    def draw(self, screen):
        pygame.draw.rect(surface=screen, color=("blue"), rect=(self.x, self.y, 40, 40))

# Obstacle properties
obstacle_radius = 20
obstacle_speed = 5
obstacle_spawn_interval = 1000  # in milliseconds
obstacle_spawn_interval_min = 200
last_spawn_time = pygame.time.get_ticks()
obstacles = []
obstacles_count = 0

# Player properties
player = Player(345, 510)
dead = False

# Random properties
death_time = 1
first_round = True
score = 0
highscore = False

# Main game loop
while running:
    # Quit game when the user clicks X to close the window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Reset game values on death
    if dead == True:
        dead = False
        obstacle_speed = 5
        obstacle_spawn_interval = 1000
        obstacles_count = 0
        player = Player(345, 510)
        obstacles = []


    # Handle player movement
    keys = pygame.key.get_pressed()
    player.update(keys)

    # fill the screen with blue
    screen.fill(sky_blue)

    # Spawn new obstacles with random x value (location)
    current_time = pygame.time.get_ticks()
    if current_time - last_spawn_time >= obstacle_spawn_interval:
        x = random.randrange(20, 670)
        while True:
            x2 = random.randrange(0, 690)
            # Stop obstacles from overlapping
            if x2 in range(x - 40, x + 40):
                continue
            else:
                break
        # Spawn a 3rd obstacle after 100 total obstacle drops
        if obstacles_count > 100:
            while True:
                x3 = random.randrange(20, 670)
                # Stop obstacles from overlapping
                if x3 in range(x2 - 40, x2 + 40) or x3 in range(x - 40, x + 40):
                    continue
                else:
                    obstacles.append((x3, -10))
                    break
        # Append obstacles to obstacle list
        obstacles.append((x, -10))
        obstacles.append((x2, -10))
        obstacles_count += 1
        last_spawn_time = current_time

    # Update obstacle fall positions
    for i, (x, y) in enumerate(obstacles):
        new_y = y + obstacle_speed
        obstacles[i] = (x, new_y)

        # Remove obstacles that reach the bottom of the screen
        if new_y + obstacle_radius >= 600:
            obstacles.pop(i)

    # increase obstacle fall/spawn speed over time
    if obstacle_spawn_interval != obstacle_spawn_interval_min:
        if obstacles_count > 20:
            obstacle_speed += 1
            obstacle_spawn_interval -= 200
            if obstacle_spawn_interval < 100:
                obstacle_spawn_interval = obstacle_spawn_interval_min
            obstacles_count = 0

    # Draw obstacles and detect hit registration
    for x, y in obstacles:
        pygame.draw.circle(surface=screen, color=("red"), center=(x, y), radius=obstacle_radius)
        if player.x + 40 in range(x - 20, x + 20) and player.y in range(y - 20, y + 20) or player.x in range(x - 20, x + 20) and player.y in range(y - 20, y + 20):
            score_list.append(score)
            score_list.sort(reverse=True)
            with open("score.txt", "a") as scores:
                scores.write(str(int(score)) + "\n")
            if score >= score_1st:
                highscore = True
            score = 0
            death_time = pygame.time.get_ticks()
            dead = True

    current_time = pygame.time.get_ticks()
    # Draw end of game text
    if score > 10:
        death_score = score
    if current_time - death_time <= 1500 and first_round == False:
        font = pygame.font.SysFont(None, 40)
        if highscore == False:
            img = font.render(("GAME OVER"), True, (0, 0, 0))
            screen.blit(img, (250, 250))
        end_score = font.render(("Score:" + str(int(death_score))), True, (0, 0, 0))
        screen.blit(end_score, (280, 280))
    if highscore == True:
        highscore_text = font.render(("Highscore!"), True, (0, 0, 0))
        screen.blit(highscore_text, (280, 250))
        if current_time - death_time >= 1500:
            highscore = False

    # reward player with 0.1 score every frame and draw score to screen as a rounded number
    score += 0.1
    font = pygame.font.SysFont(None, 40)
    img = font.render("Score: " + str(int(score)), True, (0, 0, 0))
    screen.blit(img, (20, 20))

    # Leaderboard
    try:
        score_1st = score_list[0]
    except IndexError:
        score_1st = 0
    try:
        score_2nd = score_list[1]
    except IndexError:
        score_2nd = 0
    try:
        score_3rd = score_list[2]
    except IndexError:
        score_3rd = 0
    leaderboard = font.render("Leaderboard", True, (0, 0, 0))
    screen.blit(leaderboard, (500, 20))
    one = font.render("1st: " + str(int(score_1st)), True, (0, 0, 0))
    screen.blit(one, (550, 60))
    two = font.render("2nd: " + str(int(score_2nd)), True, (0, 0, 0))
    screen.blit(two, (550, 90))
    three = font.render("3rd: " + str(int(score_3rd)), True, (0, 0, 0))
    screen.blit(three, (550, 120))


    # Draw player
    player.draw(screen)

    # Draw ground
    pygame.draw.rect(surface=screen, color=grass_green, rect=(0, 550, 690, 200))
    pygame.draw.rect(surface=screen, color=dirt_brown, rect=(0, 580, 690, 200))

    # flip() the display to put your work on screen
    pygame.display.flip()

    # Set fps to 60
    clock.tick(60)

    # Detects first round
    if current_time > 2000:
        first_round = False

# Quit game
pygame.quit()