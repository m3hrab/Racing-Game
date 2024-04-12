import pygame
import random
import csv

# Initialize Pygame
pygame.init()

# Set up the screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Top-Down Racing Game")

# Define colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Define player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.speed = 5

    def update(self, dx, dy):
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed

# Define point class
class Point(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

# Define function to generate random points
def generate_random_points(num_points):
    points = []
    for _ in range(num_points):
        x = random.randint(50, SCREEN_WIDTH - 50)
        y = random.randint(50, SCREEN_HEIGHT - 50)
        point = Point(x, y)
        points.append(point)
    return points

# Define function to save high scores to CSV file
def save_high_scores(scores):
    with open('high_scores.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Name', 'Score'])
        for score in scores:
            writer.writerow([score[0], score[1]])

# Define function to draw parallax background
def draw_parallax_background():
    screen.fill(BLUE)  # Fill background with sky color

    # Draw mountains (slowest layer)
    pygame.draw.polygon(screen, WHITE, [(200, 400), (300, 200), (400, 400)])
    pygame.draw.polygon(screen, WHITE, [(600, 400), (700, 200), (800, 400)])

    # Draw trees (medium layer)
    pygame.draw.rect(screen, GREEN, (0, 400, SCREEN_WIDTH, 200))

    # Draw ground (fastest layer)
    pygame.draw.rect(screen, (128, 64, 0), (0, 500, SCREEN_WIDTH, 100))

# Main function
def main():
    clock = pygame.time.Clock()
    running = True
    player = Player()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    points_group = pygame.sprite.Group()  # Create a sprite group for points
    points = generate_random_points(7)
    for point in points:  # Add each point to the sprite group
        points_group.add(point)
    current_point_index = random.randint(0, 6)
    score = 0
    high_scores = []

    # Game loop
    while running:
        draw_parallax_background()  # Draw parallax background layers

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Get user input
        keys = pygame.key.get_pressed()
        dx = 0
        dy = 0
        if keys[pygame.K_LEFT]:
            dx = -1
        if keys[pygame.K_RIGHT]:
            dx = 1
        if keys[pygame.K_UP]:
            dy = -1
        if keys[pygame.K_DOWN]:
            dy = 1

        # Update player position
        player.update(dx, dy)

        # Check collision with points
        collided_points = pygame.sprite.spritecollide(player, points_group, True)
        if collided_points:
            score += 1
            current_point_index = random.randint(0, 6)

        # Draw sprites
        all_sprites.draw(screen)
        points_group.draw(screen)  # Draw the points from the sprite group

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)

    # Save high score before exiting
    save_high_scores(high_scores)
    pygame.quit()

if __name__ == "__main__":
    main()
