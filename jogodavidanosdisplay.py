from machine import Pin, SoftI2C, PWM
from ssd1306 import SSD1306_I2C
import time
import random
import neopixel

# Configuração do OLED
i2c = SoftI2C(scl=Pin(15), sda=Pin(14))
oled = SSD1306_I2C(128, 64, i2c)

# Dimensões do display OLED
WIDTH = 128
HEIGHT = 64

# Dimensões da grade do Jogo da Vida
GRID_WIDTH = WIDTH // 2
GRID_HEIGHT = HEIGHT // 2

# Inicialização da grade com células vivas e mortas aleatórias
grid = [[random.randint(0, 1) for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

# Configuração dos LEDs RGB
led_red = PWM(Pin(12))
led_green = PWM(Pin(13))
led_blue = PWM(Pin(11))

# Configuração da frequência dos LEDs RGB
led_red.freq(1000)
led_green.freq(1000)
led_blue.freq(1000)

# Configuração da matriz de LEDs (5x5 Neopixel)
NUM_LEDS = 25
np = neopixel.NeoPixel(Pin(7), NUM_LEDS)

# Definindo a matriz de LEDs
LED_MATRIX = [
    [24, 23, 22, 21, 20],
    [15, 16, 17, 18, 19],
    [14, 13, 12, 11, 10],
    [5, 6, 7, 8, 9],
    [4, 3, 2, 1, 0]
]

def update_grid(grid):
    new_grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            live_neighbors = 0
            for dy in range(-1, 2):
                for dx in range(-1, 2):
                    if dx == 0 and dy == 0:
                        continue
                    ny, nx = y + dy, x + dx
                    if 0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT:
                        live_neighbors += grid[ny][nx]
            if grid[y][x] == 1:
                if live_neighbors < 2 or live_neighbors > 3:
                    new_grid[y][x] = 0
                else:
                    new_grid[y][x] = 1
            else:
                if live_neighbors == 3:
                    new_grid[y][x] = 1
    return new_grid

def draw_grid(oled, grid):
    oled.fill(0)
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if grid[y][x] == 1:
                oled.pixel(x * 2, y * 2, 1)
                oled.pixel(x * 2 + 1, y * 2, 1)
                oled.pixel(x * 2, y * 2 + 1, 1)
                oled.pixel(x * 2 + 1, y * 2 + 1, 1)
    oled.show()

def update_leds_rgb():
    led_red.duty_u16(random.randint(0, 65535))
    led_green.duty_u16(random.randint(0, 65535))
    led_blue.duty_u16(random.randint(0, 65535))

def draw_face(np, happy):
    np.fill((0, 0, 0))  # Apagar todos os LEDs
    color = (0, 255, 0) if happy else (0, 0, 255)  # Verde se feliz, azul se normal

    # Olhos
    np[LED_MATRIX[1][1]] = color
    np[LED_MATRIX[1][3]] = color

    # Boca
    if happy:
        np[LED_MATRIX[3][1]] = color
        np[LED_MATRIX[3][2]] = color
        np[LED_MATRIX[3][3]] = color
    else:
        np[LED_MATRIX[2][1]] = color
        np[LED_MATRIX[2][2]] = color
        np[LED_MATRIX[2][3]] = color

    np.write()

def game_of_life():
    global grid
    happy = True
    while True:
        draw_grid(oled, grid)
        grid = update_grid(grid)
        update_leds_rgb()
        draw_face(np, happy)
        happy = not happy  # Alterna entre feliz e normal
        time.sleep(0.5)

# Executar o jogo
game_of_life()

