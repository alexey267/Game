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

point_color = (255, 0, 0)  # цвет точки

# Загрузка ассетов
pygame.mixer.init()  # Инициализация микшера
speed_sound = pygame.mixer.Sound('level_up.wav')  # Загрузка звука
score_sound = pygame.mixer.Sound('score.wav')
new_score = pygame.mixer.Sound('new_score.wav')
background_image = pygame.image.load('background.jpg')  # Загрузка фонового изображения
red_background = pygame.Surface((window_width, window_height))  # Создание красного фона
red_background.fill((255, 0, 0))  # Красный экран
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
high_score = 0  # Рекорд
game_speed = 1

# Главный игровой цикл
running = True
new_game_countdown = False
new_game_countdown_start_time = 0
new_game_countdown_duration = 5  # Время в секундах до начала новой игры
clock = pygame.time.Clock()
game_over = False  # Переменная для отслеживания состояния проигрыша


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
    global new_game_countdown, new_game_countdown_start_time, game_over, high_score

    # Проверка и обновление рекорда
    if score > high_score:
        high_score = score
        new_score.play()

    new_game_countdown = True
    new_game_countdown_start_time = time.time()
    game_over = True  # Пометить, что игра завершилась


while running:

    if new_game_countdown:
        window.blit(red_background, (0, 0))  # Красный фон при проигрыше

        # Обработка событий для возможности закрытия окна
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Отображение сообщения и отсчета времени
        text_font = pygame.font.Font(None, 40)
        text_font1 = pygame.font.Font(None, 50)
        score_text = text_font1.render(f"Ваш счёт: {str(score)}", True, (255, 255, 255))
        score_text_rect = score_text.get_rect(center=(window_width // 2, 50))
        window.blit(score_text, score_text_rect)

        high_score_text = text_font.render(f"Последний рекорд: {str(high_score)}", True, (255, 255, 255))
        high_score_text_rect = high_score_text.get_rect(center=(window_width // 2, 100))
        window.blit(high_score_text, high_score_text_rect)

        countdown = new_game_countdown_duration - int(time.time() - new_game_countdown_start_time)
        if countdown > 0:
            countdown_surface = text_font.render("Новая игра через", True, (255, 255, 255))
            countdown_time_surface = text_font.render(f"{str(countdown)} секунд(-ы)", True, (255, 255, 255))
        else:
            countdown_surface = text_font.render("Новая игра!", True, (255, 255, 255))
            countdown_time_surface = None
            new_game_countdown = False
            game_over = False  # Сброс состояния проигрыша
            # Сброс всех значений
            point_x = window_width // 2
            point_y = window_height - 50
            point_velocity = 0
            wall_x = window_width
            wall_y = -wall_gap
            score = 0
            game_speed = 1

        countdown_rect = countdown_surface.get_rect(center=(window_width // 2, window_height // 2))
        window.blit(countdown_surface, countdown_rect)

        if countdown_time_surface:
            countdown_time_rect = countdown_time_surface.get_rect(center=(window_width // 2, window_height // 2 + 40))
            window.blit(countdown_time_surface, countdown_time_rect)

        pygame.display.flip()

    else:
        window.blit(background_image, (0, 0))  # Оригинальный фон при новой игре

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
            score_sound.play()  # звук кирпичей

            if score % 10 == 0:  # Увеличиваем скорость игры каждые 10 очков
                game_speed += 0.5
                speed_sound.play()  # увеличение скорости

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
