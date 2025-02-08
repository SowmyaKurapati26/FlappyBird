import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
SKY_BLUE = (135, 206, 235)
GREEN = (0, 200, 0)
YELLOW = (255, 255, 0)

# Game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Flappy Bird Clone')

# Clock for controlling the frame rate
clock = pygame.time.Clock()

# Bird class
class Bird:
    def __init__(self):
        self.x = 50
        self.y = SCREEN_HEIGHT // 2
        self.width = 34
        self.height = 24
        self.gravity = 0.6
        self.lift = -9
        self.velocity = 0

    def update(self):
        self.velocity += self.gravity
        self.y += self.velocity

        # Prevent bird from going off the screen
        if self.y > SCREEN_HEIGHT - self.height:
            self.y = SCREEN_HEIGHT - self.height
            self.velocity = 0

        if self.y < 0:
            self.y = 0
            self.velocity = 0

    def flap(self):
        self.velocity = self.lift

    def draw(self, screen):
        pygame.draw.rect(screen, YELLOW, (self.x, self.y, self.width, self.height))

# Pipe class
class Pipe:
    def __init__(self):
        self.gap = 150
        self.top = random.randint(50, SCREEN_HEIGHT - self.gap - 50)
        self.bottom = SCREEN_HEIGHT - self.top - self.gap
        self.x = SCREEN_WIDTH
        self.width = 52
        self.speed = 3
        self.scored = False  # To keep track if the pipe has been scored

    def update(self):
        self.x -= self.speed

    def off_screen(self):
        return self.x < -self.width

    def draw(self, screen):
        # Top pipe
        pygame.draw.rect(screen, GREEN, (self.x, 0, self.width, self.top))
        # Bottom pipe
        pygame.draw.rect(screen, GREEN, (self.x, SCREEN_HEIGHT - self.bottom, self.width, self.bottom))

    def hits(self, bird):
        # Collision detection
        bird_rect = pygame.Rect(bird.x, bird.y, bird.width, bird.height)
        top_pipe_rect = pygame.Rect(self.x, 0, self.width, self.top)
        bottom_pipe_rect = pygame.Rect(self.x, SCREEN_HEIGHT - self.bottom, self.width, self.bottom)

        return bird_rect.colliderect(top_pipe_rect) or bird_rect.colliderect(bottom_pipe_rect)

# Function to draw text on the screen
def draw_text(text, font_size, x, y):
    font = pygame.font.SysFont('Arial', font_size, bold=True)
    label = font.render(text, True, WHITE)
    screen.blit(label, (x, y))

# Main game function
def main():
    bird = Bird()
    pipes = []
    score = 0
    frame_count = 0
    running = True
    game_over = False

    while running:
        clock.tick(60)  # Limit to 60 frames per second
        screen.fill(SKY_BLUE)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_over:
                    bird.flap()

                if event.key == pygame.K_SPACE and game_over:
                    main()  # Restart the game

        if not game_over:
            bird.update()

            # Add new pipes at regular intervals
            if frame_count % 90 == 0:
                pipes.append(Pipe())

            # Update and draw pipes
            for pipe in pipes[:]:
                pipe.update()
                pipe.draw(screen)

                # Check for collisions
                if pipe.hits(bird):
                    game_over = True

                # Increase score when bird passes the pipe
                if not pipe.scored and pipe.x + pipe.width < bird.x:
                    pipe.scored = True
                    score += 1

                # Remove off-screen pipes
                if pipe.off_screen():
                    pipes.remove(pipe)

            bird.draw(screen)
            draw_text(f'Score: {score}', 30, 10, 10)

            frame_count += 1

            # Increase difficulty over time
            for pipe in pipes:
                pipe.speed = 3 + score // 5  # Increase pipe speed every 5 points

        else:
            draw_text('Game Over!', 50, SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50)
            draw_text(f'Final Score: {score}', 40, SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2)
            draw_text('Press SPACE to Restart', 30, SCREEN_WIDTH // 2 - 130, SCREEN_HEIGHT // 2 + 50)

        pygame.display.update()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
