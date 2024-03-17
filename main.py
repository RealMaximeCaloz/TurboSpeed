import random
import pygame
import sys

# Define constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
CAR_WIDTH = 50
CAR_HEIGHT = 104
CAR_X = 175
CAR_Y = 490
FPS = 60

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("TurboSpeed")
clock = pygame.time.Clock()

# Load images
road = pygame.image.load('assets/road400x1000px.png').convert()
car = pygame.image.load('assets/car50x104px.png').convert_alpha()
rock = pygame.image.load('assets/rock40x40px.png').convert_alpha()

# Global variables
speed = 7  # Initial speed of the road
rock_speed = speed  # Initial speed of rocks
score = 0
car_speed = 5
road_y = 0
rocks = []  # List to store rock objects
game_active = True  # Flag to indicate if the game is active
rock_interval = 100  # Interval to generate new rocks
rock_timer = 0

# Define rock class
class Rock:
    def __init__(self):
        self.image = rock
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(75, 285)
        self.rect.y = random.randint(-SCREEN_HEIGHT, 0)  # Start off-screen
        self.speed = rock_speed

    def update(self):
        self.rect.y += self.speed

# Function to generate rocks
def generate_rocks():
    rocks = []
    for _ in range(2):  # Limit number of rocks generated
        rock = Rock()
        rocks.append(rock)
    return rocks

def title_screen():
    # Load background image
    background_image = pygame.image.load('assets/Turbospeed_title_image_1024x1024px.png').convert()

    # Resize background image to fit the width of the screen
    aspect_ratio = background_image.get_width() / background_image.get_height()
    new_height = int(SCREEN_WIDTH / aspect_ratio)
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, new_height))

    # Calculate the y-coordinate to center the image vertically
    y_center = (SCREEN_HEIGHT - new_height) // 2

    # Blit background image onto the screen
    screen.blit(background_image, (0, y_center))

    # Display title text
    font = pygame.font.Font(None, 30)
    title_text = font.render("Use LEFT/RIGHT to avoid the boulders!", True, (255, 255, 255))
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 150))
    screen.blit(title_text, title_rect)

    # Display instructions
    font2 = pygame.font.Font(None, 40)
    instructions_text = font2.render("Press SPACE to start", True, (255, 255, 255))
    instructions_rect = instructions_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 180))
    screen.blit(instructions_text, instructions_rect)

    # Update the display
    pygame.display.flip()

def main():
    global speed, rock_speed, score, road_y, CAR_X, rocks, game_active, rock_timer

    # Display title screen
    title_screen()

    # Wait for player to start the game
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False

    # Generate initial set of rocks
    rocks = generate_rocks()

    car_moving_left = False
    car_moving_right = False
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    car_moving_left = True
                elif event.key == pygame.K_RIGHT:
                    car_moving_right = True
                elif event.key == pygame.K_SPACE and not game_active:  # Restart game when spacebar is pressed
                    restart_game()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    car_moving_left = False
                elif event.key == pygame.K_RIGHT:
                    car_moving_right = False
        
        if game_active:
            update_game(car_moving_left, car_moving_right)
            draw_game()
        else:
            show_game_over_screen()
        
        clock.tick(FPS)

def restart_game():
    global speed, rock_speed, score, road_y, CAR_X, rocks, game_active, rock_timer
    speed = 7
    rock_speed = speed
    score = 0
    road_y = 0
    CAR_X = 175
    rocks = generate_rocks()
    game_active = True
    rock_timer = 0

def update_game(left, right):
    global speed, rock_speed, score, road_y, CAR_X, rocks, game_active, rock_timer
    
    # Update speed and score
    score += 1

    if left:
        if CAR_X == 75:
            CAR_X = 75
        else:
            CAR_X -= car_speed  # Adjust the movement speed as needed
    elif right:
        if CAR_X == 275:
            CAR_X = 275
        else:
            CAR_X += car_speed  # Adjust the movement speed as needed

    # Update road position based on speed
    road_y += speed
    
    # Reset road position when it goes out of the screen
    if road_y >= road.get_height():
        road_y = 0

    # Update rocks' positions
    for rock in rocks:
        rock.rect.y += speed  # Update rock position to match the road speed

    # Remove off-screen rocks to avoid memory buildup
    rocks = [rock for rock in rocks if rock.rect.y < SCREEN_HEIGHT]
    
    # Check for collisions with rocks
    car_rect = pygame.Rect(CAR_X, CAR_Y, CAR_WIDTH, CAR_HEIGHT)
    for rock in rocks:
        if car_rect.colliderect(rock.rect):
            game_active = False  # Collision detected, stop the game

    # Generate new rocks periodically
    global rock_timer
    rock_timer += 1
    if rock_timer >= rock_interval:
        new_rocks = generate_rocks()
        rocks.extend(new_rocks)
        rock_timer = 0

    # Increase speed over time
    if score % 500 == 0 and score != 0:  # Increase speed every 500 score
        speed += 1
        rock_speed = speed

def draw_game():
    global road_y, rocks
    
    # Clear the screen
    screen.fill((255, 255, 255))  
    
    # Draw road at different positions to create scrolling effect
    screen.blit(road, (0, road_y))
    screen.blit(road, (0, road_y - road.get_height()))
    
    # Draw rocks
    for rock in rocks:
        screen.blit(rock.image, rock.rect)
    
    # Draw car
    screen.blit(car, (CAR_X, CAR_Y))  
    
    # Draw score
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))  # Adjust position as needed
    
    # Update the display
    pygame.display.flip() 

def show_game_over_screen():
    # Fill the screen with black color
    screen.fill((0, 0, 0))

    # Load game over background image
    game_over_image = pygame.image.load('assets/game_over_image.png').convert()

    # Resize game over background image to fit the width of the screen
    aspect_ratio = game_over_image.get_width() / game_over_image.get_height()
    new_height = int(SCREEN_WIDTH / aspect_ratio)
    game_over_image = pygame.transform.scale(game_over_image, (SCREEN_WIDTH, new_height))

    # Calculate the y-coordinate to center the image vertically
    y_center = (SCREEN_HEIGHT - new_height) // 2

    # Blit game over background image onto the screen
    screen.blit(game_over_image, (0, y_center))

    # Display score
    font_score = pygame.font.Font(None, 30)
    score_text = font_score.render(f"Score: {score}", True, (255, 255, 255))
    score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 125))
    screen.blit(score_text, score_rect)

    # Display game over text in red
    font = pygame.font.Font(None, 30)
    text = font.render("Game Over! Press SPACE to restart.", True, (255, 0, 0))
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 150))
    screen.blit(text, text_rect)

    # Update the display
    pygame.display.flip()

# Run the game
if __name__ == "__main__":
    main()