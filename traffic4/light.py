import pygame
import time

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 400, 300
LIGHT_WIDTH, LIGHT_HEIGHT = 60, 150
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)

# Setup the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Traffic Light Simulation")

# Function to draw a traffic light
def draw_traffic_light(x, y, current_color):
    # Draw the traffic light structure
    pygame.draw.rect(screen, WHITE, (x, y, LIGHT_WIDTH, LIGHT_HEIGHT), 2)
    
    # Draw the lights
    pygame.draw.circle(screen, RED if current_color == 'red' else (100, 0, 0), (x + LIGHT_WIDTH // 2, y + 30), 20)
    pygame.draw.circle(screen, YELLOW if current_color == 'yellow' else (100, 100, 0), (x + LIGHT_WIDTH // 2, y + 75), 20)
    pygame.draw.circle(screen, GREEN if current_color == 'green' else (0, 100, 0), (x + LIGHT_WIDTH // 2, y + 120), 20)

# Main loop
def main():
    clock = pygame.time.Clock()
    running = True
    traffic_lights = [(50, 50), (250, 50)]  # Positions for two traffic lights
    current_colors = ['red', 'red']  # Initial colors

    while running:
        screen.fill((0, 0, 0))  # Clear the screen

        # Draw the traffic lights
        for i, (x, y) in enumerate(traffic_lights):
            draw_traffic_light(x, y, current_colors[i])

        pygame.display.flip()  # Update the display

        # Change the lights
        for i in range(len(current_colors)):
            if current_colors[i] == 'red':
                current_colors[i] = 'green'
            elif current_colors[i] == 'green':
                current_colors[i] = 'yellow'
            elif current_colors[i] == 'yellow':
                current_colors[i] = 'red'

        time.sleep(2)  # Wait for 2 seconds

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        clock.tick(60)  # Limit the frame rate

    pygame.quit()

if __name__ == "__main__":
    main()