import pygame
import random
import time

# Инициализация Pygame
pygame.init()

# Создание окна игры
window_width = 400
window_height = 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("FALLING BRICKS")

# Цвета
point_color = (255, 0, 0)

# Загрузка ассетов
pygame.mixer.init()  # Инициализация микшера
level_up_sound = pygame.mixer.Sound('level_up.wav')  # Загрузка звука
background_image = pygame.image.load('background.jpg')  # Загрузка фонового изображения
background_image = pygame.transform.scale(background_image, (400, 600))  # Изменение размера изображения

# Загрузка текстуры стены
wall_texture = pygame.image.load('wall.png')

# Настройки игры
point_radius = 10
point_speed = 5
wall_width = 120
wall_gap = 60
wall_speed = 4

# Позиция и скорость точки
point_x = window_width // 2
point_y = window_height - 50
point_velocity = 0

# Позиция и скорость стены
wall_x = window_width
wall_y = -wall_gap
wall_velocity = wall_speed

# Счетчик пройденных стен и скорость игры
score = 0
game_speed = 1

# Главный игровой цикл
running = True
new_game_countdown = False
new_game_countdown_start_time = 0
new_game_countdown_duration = 5  # Время в секундах до начала новой игры
clock = pygame.time.Clock()


def draw_point():
    pygame.draw.circle(window, point_color, (int(point_x), int(point_y)), point_radius)


def draw_wall(x, y):
    window.blit(wall_texture, (x, y), (0, 0, wall_width, wall_gap))


# рисуем коллизию для точки
def is_collision():
    if point_y - point_radius <= wall_y + wall_gap and point_y + point_radius >= wall_y:
        if point_x + point_radius >= wall_x and point_x - point_radius <= wall_x + wall_width:
            return True
    return False


# запуск таймера новой игры
def start_new_game_countdown():
    global new_game_countdown, new_game_countdown_start_time
    new_game_countdown = True
    new_game_countdown_start_time = time.time()


while running:
    window.blit(background_image, (0, 0))  # Отрисовка фонового изображения

    if new_game_countdown:
        # Обработка возможности закрытия окна
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        text_font = pygame.font.Font(None, 40)
        text_font1 = pygame.font.Font(None, 40)
        score_text = text_font1.render(f"Вы набрали: {str(score)} очков", True, (0, 0, 0), (255, 255, 255))
        score_text_rect = score_text.get_rect(center=(window_width // 2, 50))
        window.blit(score_text, score_text_rect)

        countdown = new_game_countdown_duration - int(time.time() - new_game_countdown_start_time)
        if countdown > 0:
            countdown_surface = text_font.render("Новая игра через " + str(countdown) + "  секунд", True, (0, 0, 0),
                                                 (255, 255, 255))
        else:
            countdown_surface = text_font.render("Новая игра!", True, (0, 0, 0), (255, 255, 255))
            new_game_countdown = False
            # Сброс всех значений
            point_x = window_width // 2
            point_y = window_height - 50
            point_velocity = 0
            wall_x = window_width
            wall_y = -wall_gap
            score = 0
            game_speed = 1

        countdown_rect = countdown_surface.get_rect(center=(window_width // 2, window_height // 2 + 50))
        window.blit(countdown_surface, countdown_rect)
        pygame.display.flip()

    else:
        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    point_velocity = -point_speed
                elif event.key == pygame.K_d:
                    point_velocity = point_speed

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_a or event.key == pygame.K_d:
                    point_velocity = 0

        # Обновление позиции точки
        point_x += point_velocity

        if point_x - point_radius < 0:
            point_x = point_radius
        elif point_x + point_radius > window_width:
            point_x = window_width - point_radius

        # Обновление позиции стены
        wall_y += wall_velocity * game_speed

        if wall_y > window_height:
            wall_y = -wall_gap
            wall_x = random.randint(0, window_width - wall_width)
            score += 1

            if score % 10 == 0:  # Увеличиваем скорость игры каждые 10 очков
                game_speed += 0.5
                level_up_sound.play()

        # Проверка столкновения
        if is_collision():
            start_new_game_countdown()

        # Отрисовка объектов
        draw_point()
        draw_wall(wall_x, wall_y)

        # Отрисовка счетчика стен
        score_font = pygame.font.Font(None, 40)
        score_surface = score_font.render("Очки: " + str(score), True, (0, 0, 0), (255, 255, 255))
        window.blit(score_surface, (10, 10))

        # Отрисовка скорости игры
        speed_surface = score_font.render("Скорость: " + str(game_speed), True, (0, 0, 0), (255, 255, 255))
        speed_rect = speed_surface.get_rect(topright=(window_width - 10, 10))
        window.blit(speed_surface, speed_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
