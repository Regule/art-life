import pygame


#==================================================================================================
#                                       PHYSICS MODEL 
#==================================================================================================

class PillbugBody:

    def __init__(self, shape, mass):
        self.shape = shape
        self.mass = mass

class Pillbug:

    def __init__(self):
        pass


# Initialize Pygame
pygame.init()

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600

PILLBUG_SIZE = 20
TRAIL_SIZE = 5
PILLBUG_VELOCITY = 50

# Set up the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

pillbug_x = CANVAS_WIDTH // 2
pillbug_y = CANVAS_HEIGHT // 2
velocity_x = 0
velocity_y = 0


# Create the canvas
canvas = pygame.display.set_mode((CANVAS_WIDTH, CANVAS_HEIGHT))
pygame.display.set_caption("Pillbug Trail")

# Create a surface to store the trail
trail_surface = pygame.Surface((CANVAS_WIDTH, CANVAS_HEIGHT))
trail_surface.set_alpha(80)  # Set the transparency of the trail

# Create a clock object to control the frame rate
clock = pygame.time.Clock()

# Game loop
running = True
while running:
    dt = clock.tick() / 1000
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                velocity_y = -PILLBUG_VELOCITY
            elif event.key == pygame.K_DOWN:
                velocity_y = PILLBUG_VELOCITY
            elif event.key == pygame.K_LEFT:
                velocity_x = -PILLBUG_VELOCITY
            elif event.key == pygame.K_RIGHT:
                velocity_x = PILLBUG_VELOCITY
            elif event.key == ord('q'):
                running = False
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                velocity_y = 0
            elif event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                velocity_x = 0

    pillbug_x += velocity_x * dt
    pillbug_y += velocity_y * dt

    # Draw the pillbug on the trail surface
    pygame.draw.ellipse(trail_surface, RED, (pillbug_x - TRAIL_SIZE// 2, pillbug_y - TRAIL_SIZE // 2, TRAIL_SIZE, TRAIL_SIZE))

    canvas.fill(BLACK)
    canvas.blit(trail_surface, (0, 0))

    # Draw the pillbug
    pygame.draw.ellipse(canvas, WHITE, (pillbug_x - PILLBUG_SIZE // 2, pillbug_y - PILLBUG_SIZE // 2, PILLBUG_SIZE, PILLBUG_SIZE))

    # Update the display
    pygame.display.flip()

pygame.quit()
