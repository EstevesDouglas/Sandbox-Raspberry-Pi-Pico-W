from machine import Pin, SoftI2C, ADC
from ssd1306 import SSD1306_I2C
import time

# Configuração do OLED
i2c = SoftI2C(scl=Pin(15), sda=Pin(14))
oled = SSD1306_I2C(128, 64, i2c)

# Configuração do Joystick
joystick_x = ADC(Pin(27))
joystick_y = ADC(Pin(26))
button = Pin(22, Pin.IN, Pin.PULL_UP)

# Dimensões do display OLED
WIDTH = 128
HEIGHT = 64

# Configuração do jogo
PADDLE_WIDTH = 2
PADDLE_HEIGHT = 10
BALL_SIZE = 2

# Posição inicial da raquete
paddle_y = (HEIGHT // 2) - (PADDLE_HEIGHT // 2)

# Posição e velocidade iniciais da bola
ball_x = WIDTH // 2
ball_y = HEIGHT // 2
ball_dx = 2
ball_dy = 2

# Função para desenhar a raquete
def draw_paddle(y):
    oled.fill_rect(0, y, PADDLE_WIDTH, PADDLE_HEIGHT, 1)

# Função para desenhar a bola
def draw_ball(x, y):
    oled.fill_rect(x, y, BALL_SIZE, BALL_SIZE, 1)

# Função para atualizar a posição da raquete com o joystick
def update_paddle():
    global paddle_y
    # Leitura do valor do joystick
    joystick_val = joystick_y.read_u16()

    # Mapeamento do valor do joystick para a posição da raquete
    paddle_y = int((joystick_val / 65535) * (HEIGHT - PADDLE_HEIGHT))

# Função principal do jogo
def game_loop():
    global ball_x, ball_y, ball_dx, ball_dy, paddle_y

    while True:
        oled.fill(0)  # Limpa a tela

        # Atualiza a posição da raquete
        update_paddle()
        draw_paddle(paddle_y)

        # Atualiza a posição da bola
        ball_x += ball_dx
        ball_y += ball_dy

        # Colisões com as paredes superior e inferior
        if ball_y <= 0 or ball_y >= HEIGHT - BALL_SIZE:
            ball_dy = -ball_dy

        # Colisões com a raquete
        if ball_x <= PADDLE_WIDTH and paddle_y <= ball_y <= paddle_y + PADDLE_HEIGHT:
            ball_dx = -ball_dx

        # Colisões com a parede direita
        if ball_x >= WIDTH - BALL_SIZE:
            ball_dx = -ball_dx

        # Desenha a bola
        draw_ball(ball_x, ball_y)

        # Atualiza o display
        oled.show()

        # Pequena pausa para controlar a velocidade do jogo
        time.sleep(0.05)

# Inicia o jogo
game_loop()

