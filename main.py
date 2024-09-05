import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 600
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
gray = (169, 169, 169)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

# Clock to control the game's frame rate
clock = pygame.time.Clock()

# Load images
player_car_images = [
    pygame.transform.scale(pygame.image.load('car1.png'), (50, 100)),
    pygame.transform.scale(pygame.image.load('car2.png'), (50, 100)),
    pygame.transform.scale(pygame.image.load('car3.png'), (50, 100))
]
enemy_car = pygame.transform.scale(pygame.image.load('enemy_car.png'), (50, 100))
gold_coin = pygame.transform.scale(pygame.image.load('gold_coin.png'), (30, 30))

# Load sounds
pygame.mixer.music.load('background_music.mp3')
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)  # Loop the background music
collect_sound = pygame.mixer.Sound('collect_coin.mp3')
collision_sound = pygame.mixer.Sound('collision.mp3')

# Initial car setup
selected_car_index = 0
player_car = player_car_images[selected_car_index]

# Get car dimensions
car_width = player_car.get_width()
car_height = player_car.get_height()

# Car starting positions
player_x = screen_width // 2 - car_width // 2
player_y = screen_height - car_height - 20
player_y_velocity = 0
player_on_ground = True

# Speed variables
player_speed = 10
enemy_speed = 7
jump_speed = -15  # Speed when the player jumps
gravity = 1  # Gravity applied to bring the car back down after a jump

# Enemy car list
enemy_list = []
min_enemy_distance = 300  # Minimum distance between enemy cars
last_enemy_spawn_y = 0  # Track the last y-position where an enemy was spawned

# Currency and scoring
score = 0
currency = 0
high_score = 0
font = pygame.font.SysFont(None, 36)

# Gold coin list
coin_list = []

# Car prices
car_prices = [0, 500, 1000]  # Prices for each car

# Game states
START, PLAYING, END, CAR_STORE = 'start', 'playing', 'end', 'car_store'
game_state = START

# Button dimensions
button_width = 200
button_height = 50

# Function to draw cars on the screen
def draw_cars(px, py, enemies):
    screen.blit(player_car, (px, py))
    for ex, ey in enemies:
        screen.blit(enemy_car, (ex, ey))

# Function to draw gold coins on the screen
def draw_coins(coins):
    for cx, cy in coins:
        screen.blit(gold_coin, (cx, cy))

# Function to check for collisions
def check_collision(px, py, enemies):
    for ex, ey in enemies:
        if py + car_height > ey and py < ey + car_height:
            if px + car_width > ex and px < ex + car_width:
                return True
    return False

# Function to check for coin collection
def check_coin_collection(px, py, coins):
    global currency
    collected_coins = []
    for coin in coins:
        cx, cy = coin
        if py < cy + 30 and py + car_height > cy:
            if px < cx + 30 and px + car_width > cx:
                collected_coins.append(coin)
                currency += 1
                collect_sound.play()
    return collected_coins

# Function to reset enemy cars when they go off screen
def reset_enemies(enemies):
    return [enemy for enemy in enemies if enemy[1] <= screen_height]

# Function to reset gold coins when they go off screen
def reset_coins(coins):
    return [coin for coin in coins if coin[1] <= screen_height]

# Function to display the score
def show_score(s, c):
    score_text = font.render(f"Score: {s}", True, white)
    screen.blit(score_text, (10, 10))
    currency_text = font.render(f"Gold: {c}", True, white)
    screen.blit(currency_text, (10, 50))

# Function to display the high score
def show_high_score(hs):
    high_score_text = font.render(f"High Score: {hs}", True, white)
    screen.blit(high_score_text, (10, 90))

# Function to spawn enemies at reasonable intervals
def spawn_enemy():
    global last_enemy_spawn_y
    if len(enemy_list) == 0 or (enemy_list[-1][1] > last_enemy_spawn_y + min_enemy_distance):
        enemy_x = random.randrange(0, screen_width - car_width)
        enemy_y = random.randrange(-800, -100)
        enemy_list.append([enemy_x, enemy_y])
        last_enemy_spawn_y = enemy_y

# Function to spawn gold coins at reasonable intervals
def spawn_coin():
    if len(coin_list) == 0 or (coin_list[-1][1] > last_enemy_spawn_y + min_enemy_distance):
        coin_x = random.randrange(0, screen_width - 30)
        coin_y = random.randrange(-800, -100)
        coin_list.append([coin_x, coin_y])

# Function to display the end screen
def end_screen(final_score, hs):
    screen.fill(black)
    end_text = font.render(f"Game Over! Your Score: {final_score}", True, white)
    high_score_text = font.render(f"High Score: {hs}", True, white)
    restart_text = font.render("Restart", True, black)
    quit_text = font.render("Quit", True, black)
    menu_text = font.render("Back to Menu", True, black)

    screen.blit(end_text, (screen_width // 2 - end_text.get_width() // 2, screen_height // 2 - 100))
    screen.blit(high_score_text, (screen_width // 2 - high_score_text.get_width() // 2, screen_height // 2 - 50))

    restart_button = pygame.Rect(screen_width // 2 - button_width // 2, screen_height // 2, button_width, button_height)
    quit_button = pygame.Rect(screen_width // 2 - button_width // 2, screen_height // 2 + 70, button_width, button_height)
    menu_button = pygame.Rect(screen_width // 2 - button_width // 2, screen_height // 2 + 140, button_width, button_height)

    pygame.draw.rect(screen, green, restart_button)
    pygame.draw.rect(screen, red, quit_button)
    pygame.draw.rect(screen, blue, menu_button)

    screen.blit(restart_text, (restart_button.x + (button_width - restart_text.get_width()) // 2, restart_button.y + 10))
    screen.blit(quit_text, (quit_button.x + (button_width - quit_text.get_width()) // 2, quit_button.y + 10))
    screen.blit(menu_text, (menu_button.x + (button_width - menu_text.get_width()) // 2, menu_button.y + 10))

    pygame.display.update()
    
    return restart_button, quit_button, menu_button

# Function to display the start screen
def start_screen():
    screen.fill(black)
    title_text = font.render("Welcome to Suhaan's Car Game!", True, white)
    start_text = font.render("Start Game", True, black)
    buy_car_text = font.render("Buy New Car", True, black)
    currency_text = font.render(f"Gold: {currency}", True, white)

    screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, screen_height // 2 - 150))
    screen.blit(currency_text, (screen_width // 2 - currency_text.get_width() // 2, screen_height // 2 - 100))

    start_button = pygame.Rect(screen_width // 2 - button_width // 2, screen_height // 2 - 50, button_width, button_height)
    buy_car_button = pygame.Rect(screen_width // 2 - button_width // 2, screen_height // 2 + 20, button_width, button_height)

    pygame.draw.rect(screen, green, start_button)
    pygame.draw.rect(screen, blue, buy_car_button)

    screen.blit(start_text, (start_button.x + (button_width - start_text.get_width()) // 2, start_button.y + 10))
    screen.blit(buy_car_text, (buy_car_button.x + (button_width - buy_car_text.get_width()) // 2, buy_car_button.y + 10))

    pygame.display.update()

    return start_button, buy_car_button

# Function to display car selection screen
def car_selection_screen():
    screen.fill(black)
    select_text = font.render("Select Your Car", True, white)
    screen.blit(select_text, (screen_width // 2 - select_text.get_width() // 2, 50))
    
    car_buttons = []
    for i, car_img in enumerate(player_car_images):
        car_button = pygame.Rect(100 + i * 150, 200, 100, 200)
        car_buttons.append(car_button)
        screen.blit(car_img, (car_button.x, car_button.y))
        price_text = font.render(f"{car_prices[i]} Gold", True, white)
        screen.blit(price_text, (car_button.x + (100 - price_text.get_width()) // 2, car_button.y + 210))

    back_text = font.render("Back to Menu", True, black)
    back_button = pygame.Rect(screen_width // 2 - button_width // 2, screen_height - 70, button_width, button_height)

    pygame.draw.rect(screen, red, back_button)

    screen.blit(back_text, (back_button.x + (button_width - back_text.get_width()) // 2, back_button.y + 10))

    pygame.display.update()
    
    return car_buttons, back_button

# Game loop
while True:
    if game_state == START:
        start_button, buy_car_button = start_screen()

        while game_state == START:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if start_button.collidepoint(event.pos):
                        game_state = PLAYING
                    elif buy_car_button.collidepoint(event.pos):
                        game_state = CAR_STORE

    elif game_state == PLAYING:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < screen_width - car_width:
            player_x += player_speed
        if keys[pygame.K_SPACE] and player_on_ground:
            player_y_velocity = jump_speed
            player_on_ground = False

        # Apply gravity
        player_y += player_y_velocity
        player_y_velocity += gravity

        # Ensure the player doesn't fall below the ground
        if player_y >= screen_height - car_height - 20:
            player_y = screen_height - car_height - 20
            player_y_velocity = 0
            player_on_ground = True

        # Move the enemy cars
        enemy_list = [[ex, ey + enemy_speed] for ex, ey in enemy_list]
        enemy_speed = 7 + score // 100  # Increase enemy speed based on score

        # Move the gold coins
        coin_list = [[cx, cy + enemy_speed] for cx, cy in coin_list]

        # Check for collisions
        if check_collision(player_x, player_y, enemy_list):
            collision_sound.play()
            # Update the high score if the current score is higher
            if score > high_score:
                high_score = score
            currency += score // 100  # Update currency based on score
            game_state = END
            continue  # Restart the loop

        # Check for coin collection
        collected_coins = check_coin_collection(player_x, player_y, coin_list)
        # Remove collected coins from the list
        coin_list = [coin for coin in coin_list if coin not in collected_coins]

        # Reset enemy and coin positions if they go off screen
        enemy_list = reset_enemies(enemy_list)
        coin_list = reset_coins(coin_list)

        # Fill the screen with a road-like background
        screen.fill(gray)

        # Draw road lines
        for i in range(0, screen_height, 40):
            pygame.draw.rect(screen, white, (screen_width // 2 - 5, i, 10, 20))

        # Draw the cars and coins
        draw_cars(player_x, player_y, enemy_list)
        draw_coins(coin_list)

        # Update the score
        score += 1
        show_score(score, currency)
        show_high_score(high_score)

        # Update the screen
        pygame.display.update()

        # Cap the frame rate
        clock.tick(60)

        # Spawn a new enemy car and coin
        spawn_enemy()
        spawn_coin()

    elif game_state == END:
        restart_button, quit_button, menu_button = end_screen(score, high_score)

        while game_state == END:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if restart_button.collidepoint(event.pos):
                        game_state = PLAYING
                        score = 0  # Reset the score
                        player_x = screen_width // 2 - car_width // 2  # Reset player position
                        player_y = screen_height - car_height - 20
                        player_y_velocity = 0
                        enemy_list.clear()  # Clear enemies
                        coin_list.clear()  # Clear coins
                    elif quit_button.collidepoint(event.pos):
                        pygame.quit()
                        exit()
                    elif menu_button.collidepoint(event.pos):
                        game_state = START

    elif game_state == CAR_STORE:
        car_buttons, back_button = car_selection_screen()

        while game_state == CAR_STORE:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for i, car_button in enumerate(car_buttons):
                        if car_button.collidepoint(event.pos):
                            if currency >= car_prices[i]:  # Check if player has enough currency
                                selected_car_index = i
                                player_car = player_car_images[selected_car_index]
                                currency -= car_prices[i]  # Deduct the cost
                                game_state = START
                    if back_button.collidepoint(event.pos):
                        game_state = START
