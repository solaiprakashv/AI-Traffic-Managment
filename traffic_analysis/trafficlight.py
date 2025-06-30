import pygame
import time
import mysql.connector

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
LIGHT_WIDTH, LIGHT_HEIGHT = 60, 150
FONT_SIZE = 24
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)

# Database connection details
db_config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'traffic_vehicle_count'
}

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

# Function to draw the heading
def draw_heading(x, y, text):
    font = pygame.font.Font(None, FONT_SIZE)
    heading = font.render(text, True, WHITE)
    screen.blit(heading, (x, y))

# Function to get vehicle counts from the database
def get_vehicle_counts():
    db_connection = mysql.connector.connect(**db_config)
    cursor = db_connection.cursor()
    cursor.execute("SELECT lane_number, SUM(total_count) FROM `vehicle count` GROUP BY lane_number")
    results = cursor.fetchall()
    cursor.close()
    db_connection.close()
    return {lane: count for lane, count in results}

# Main loop
def main():
    clock = pygame.time.Clock()
    running = True
    traffic_lights = [(100, 200), (300, 200), (500, 200), (700, 200)]  # Positions for four traffic lights
    headings = ["Lane 1", "Lane 2", "Lane 3", "Lane 4"]  # Headings for each traffic light
    current_colors = ['red', 'red', 'red', 'red']  # Initial colors

    while running:
        screen.fill((0, 0, 0))  # Clear the screen

        # Get vehicle counts from the database
        vehicle_counts = get_vehicle_counts()

        # Set timing based on vehicle counts
        green_times = [max(5, count // 10) for count in [vehicle_counts.get(1, 0), vehicle_counts.get(2, 0), vehicle_counts.get(3, 0), vehicle_counts.get(4, 0)]]
        red_times = [green_times[0] + green_times[1], green_times[2] + green_times[3]]  # Total time for red lights

        # Draw the headings and traffic lights
        for i, (x, y) in enumerate(traffic_lights):
            draw_heading(x, y - 50, headings[i])
            draw_traffic_light(x, y, current_colors[i])

        pygame.display.flip()  # Update the display

        # Change the lights
        for i in range(len(current_colors)):
            if current_colors[i] == 'red':
                current_colors[i] = 'green'
                time.sleep(green_times[i // 2])  # Use green time for the lane
            elif current_colors[i] == 'green':
                current_colors[i] = 'yellow'
                time.sleep(2)  # Yellow light duration
            elif current_colors[i] == 'yellow':
                current_colors[i] = 'red'
                time.sleep(red_times[i // 2])  # Use red time for the opposite lane

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        clock.tick(60)  # Limit the frame rate

    pygame.quit()

if __name__ == "__main__":
    main()