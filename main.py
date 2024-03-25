import pygame
import sys

pygame.init()

BLACK = (15, 15, 15)
WHITE = (255, 255, 255)

WIDTH = int(input("Enter screen width in pixels: ")) # example: 400
HEIGHT = int(input("Enter screen height in pixels: ")) # example 500

CELL_SIZE = 10

GRID_WIDTH = WIDTH // CELL_SIZE
GRID_HEIGHT = HEIGHT // CELL_SIZE

grid = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]
screen = pygame.display.set_mode((WIDTH, HEIGHT))


def count_neighbors(x, y):
    count = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            neighbour_x = (x + i + GRID_WIDTH) % GRID_WIDTH
            neighbour_y = (y + j + GRID_HEIGHT) % GRID_HEIGHT
            count += grid[neighbour_y][neighbour_x]

    count -= grid[y][x]
    return count


def main():

    timestep = int(input("Enter simulation frame rate: "))
    print("----------------------\nLeft click = remove cell")
    print("Right click = place cell \nspace = start/stop simulation")

    global grid

    clock = pygame.time.Clock()
    running = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running = not running

            elif pygame.mouse.get_pressed()[0] and not running:
                x, y = event.pos
                grid_x = x // CELL_SIZE
                grid_y = y // CELL_SIZE
                grid[grid_y][grid_x] = 1

            elif pygame.mouse.get_pressed()[2] and not running:
                x, y = event.pos
                grid_x = x // CELL_SIZE
                grid_y = y // CELL_SIZE
                grid[grid_y][grid_x] = 0

        if running:

            new_grid = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]

            for y in range(GRID_HEIGHT):
                for x in range(GRID_WIDTH):

                    neighbors = count_neighbors(x, y)

                    if grid[y][x] == 1:
                        if neighbors < 2 or neighbors > 3:
                            new_grid[y][x] = 0
                        else:
                            new_grid[y][x] = 1
                    else:
                        if neighbors == 3:
                            new_grid[y][x] = 1

            grid = new_grid

        screen.fill(BLACK)
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if grid[y][x] == 1:
                    pygame.draw.rect(screen, WHITE, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        if not running:
            for i in range(GRID_WIDTH + 1):
                pygame.draw.line(screen, WHITE, (i * CELL_SIZE, 0), (i * CELL_SIZE, HEIGHT))
            for i in range(GRID_HEIGHT + 1):
                pygame.draw.line(screen, WHITE, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE))

        pygame.display.flip()

        if not running:
            clock.tick(60)
        else:
            clock.tick(timestep)


if __name__ == "__main__":
    main()
