import pygame
import sys
import os

# Инициализация Pygame
pygame.init()

# Определение констант
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
CELL_SIZE = SCREEN_WIDTH // 8
INFO_PANEL_WIDTH = 200

# Определение цветов
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

LIGHT_SQUARE_COLOR = (240, 217, 181)
DARK_SQUARE_COLOR = (181, 136, 99)  
SELECTED_COLOR = (0, 255, 255)

# Инициализация экрана
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Шахматы")

# Загрузка изображений
image_path = "D:/All"  
WHITE_PIECES = {
    'K': pygame.image.load(os.path.join(image_path, "White king.png")),
    'Q': pygame.image.load(os.path.join(image_path, "White Queen.png")),
    'R': pygame.image.load(os.path.join(image_path, "White Rook.png")),
    'B': pygame.image.load(os.path.join(image_path, "White Bishop.png")),
    'N': pygame.image.load(os.path.join(image_path, "White knight.png")),
    'P': pygame.image.load(os.path.join(image_path, "White pawn.png"))
}

BLACK_PIECES = {
    'k': pygame.image.load(os.path.join(image_path, "Black king.png")),
    'q': pygame.image.load(os.path.join(image_path, "Black Queen.png")),
    'r': pygame.image.load(os.path.join(image_path, "Black Rook.png")),
    'b': pygame.image.load(os.path.join(image_path, "Black Bishop.png")),
    'n': pygame.image.load(os.path.join(image_path, "Black knight.png")),
    'p': pygame.image.load(os.path.join(image_path, "Black pawn.png"))
}

# Определение начальных значений
chess_board = [
    ["r", "n", "b", "q", "k", "b", "n", "r"],
    ["p", "p", "p", "p", "p", "p", "p", "p"],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["P", "P", "P", "P", "P", "P", "P", "P"],
    ["R", "N", "B", "Q", "K", "B", "N", "R"]
]

selected_piece = None
current_player = 2  # Игрок 1 начинает

last_move = None
info_font = pygame.font.Font(None, 24)

# Загрузка изображений
image_path = "D:/All" 
PLAY_IMAGE = pygame.image.load(os.path.join(image_path, "play.png"))
RULES_IMAGE = pygame.image.load(os.path.join(image_path, "RULES.png"))
EXIT_IMAGE = pygame.image.load(os.path.join(image_path, "EXIT.png"))


def draw_main_menu():
    screen.fill(WHITE)

    # Создание кнопок
    play_button_rect = screen.blit(PLAY_IMAGE, (200, 200))
    rules_button_rect = screen.blit(RULES_IMAGE, (200, 300))
    exit_button_rect = screen.blit(EXIT_IMAGE, (200, 400))

    # Центрирование кнопок по горизонтали
    play_button_rect.centerx = screen.get_rect().centerx
    rules_button_rect.centerx = screen.get_rect().centerx
    exit_button_rect.centerx = screen.get_rect().centerx

    # Центрирование кнопок по вертикали
    play_button_rect.centery = SCREEN_HEIGHT // 2
    rules_button_rect.centery = SCREEN_HEIGHT // 2 + 100
    exit_button_rect.centery = SCREEN_HEIGHT // 2 + 200

    pygame.display.flip()

    return play_button_rect, rules_button_rect, exit_button_rect

def show_rules():
    rules_text = [
        "Основные правила шахмат:",
        "1. Каждый игрок начинает с 16 фигур: король, ферзь, ладья, слон, конь и восемь пешек.",
        "2. Цель игры - поставить короля противника под угрозу матом.",
        "3. Фигуры двигаются по доске в соответствии с их типом (ладья, слон, конь, ферзь, король, пешка).",
        "4. Каждая фигура не может двигаться сквозь другие фигуры (за исключением коня).",
        "5. Пешки имеют ограниченное начальное движение и могут съедать фигуры по диагонали.",
        "6. Король может двигаться на одну клетку в любом направлении.",
        "7. Ферзь может двигаться по горизонтали, вертикали и диагонали.",
        "8. Ладья двигается по горизонтали и вертикали.",
        "9. Слон двигается по диагонали.",
        "10. Конь может совершать 'буквой Г' движение.",
        "11. Если король находится под угрозой и нет возможности ее снять, то это мат."
    ]

    rules_font = pygame.font.Font(None, 14)
    rule_texts = [rules_font.render(text, True, BLACK) for text in rules_text]

    rules_window = pygame.Surface((600, 600))
    rules_window.fill(WHITE)

    for i, text_surface in enumerate(rule_texts):
        rules_window.blit(text_surface, (10, 10 + i * 20))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return_to_menu = True
                    running = False  # Добавьте эту строку

        screen.blit(rules_window, (100, 100))
        pygame.display.flip()

    pygame.time.delay(200)
    return return_to_menu

# Определение функций
def is_opponent_piece(piece, current_player):
    return piece.isalpha() and (piece.islower() if current_player == 1 else piece.isupper())

def is_valid_pawn_move(start, end, piece):
    valid_directions = {"P": -1, "p": 1}
    direction = valid_directions[piece]

    if start[0] == 1 and piece.isupper() or start[0] == 6 and piece.islower():
        return (
        end[1] == start[1] and
        (end[0] - start[0] == direction or end[0] - start[0] == direction * 2) and
        is_path_clear(start, end) and
        chess_board[start[0] + direction][start[1]] == "" and
        (chess_board[start[0] + 2 * direction][start[1]] == "" if end[0] - start[0] == direction * 2 else True)
    )
    return end[1] == start[1] and chess_board[end[0]][end[1]] == "" and end[0] - start[0] == direction  

def is_valid_move(start, end):
    piece = chess_board[start[0]][start[1]]
    dest_piece = chess_board[end[0]][end[1]]

    if start == end or dest_piece != "" and (dest_piece.islower() == piece.islower()):
        return False

    if is_opponent_piece(dest_piece, current_player):
        return is_valid_capture(start, end, piece, dest_piece)

    while True:
        if piece.lower() == 'p':
            return is_valid_pawn_move(start, end, piece)
        elif piece.lower() == 'r':
            return is_valid_rook_move(start, end)
        elif piece.lower() == 'n':
            return is_valid_knight_move(start, end)
        elif piece.lower() == 'b':
            return is_valid_bishop_move(start, end)
        elif piece.lower() == 'q':
            return is_valid_queen_move(start, end)
        elif piece.lower() == 'k':
            return is_valid_king_move(start, end)
        return False
    
def is_path_clear(start, end):
    row_step = 0 if start[0] == end[0] else (end[0] - start[0]) // abs(end[0] - start[0])
    col_step = 0 if start[1] == end[1] else (end[1] - start[1]) // abs(end[1] - start[1])

    row, col = start
    while (row, col) != end:
        row += row_step
        col += col_step
        if chess_board[row][col] != "":
            return False
    return True

def is_valid_capture(start, end, piece, dest_piece):
    if piece.lower() == 'p':
        return is_valid_pawn_move(start, end, piece, dest_piece)
    elif piece.lower() == 'r':
        return is_valid_rook_move(start, end)
    elif piece.lower() == 'n':
        return is_valid_knight_move(start, end)
    elif piece.lower() == 'b':
        return is_valid_bishop_move(start, end)
    elif piece.lower() == 'q':
        return is_valid_queen_move(start, end)
    elif piece.lower() == 'k':
        return is_valid_king_move(start, end)
    return False

def is_valid_pawn_capture(start, end, piece, dest_piece):
    valid_directions = {"P": -1, "p": 1}
    direction = valid_directions[piece]

    return (
        abs(end[1] - start[1]) == 1 and
        end[0] - start[0] == direction and
        dest_piece != "" and
        dest_piece.islower() != piece.islower()
    )

def is_valid_rook_move(start, end):
    return start[0] == end[0] and is_path_clear(start, end) or start[1] == end[1] and is_path_clear(start, end)

def is_valid_knight_move(start, end):
    return (
        abs(start[0] - end[0]) == 2 and abs(start[1] - end[1]) == 1 or
        abs(start[0] - end[0]) == 1 and abs(start[1] - end[1]) == 2
    )

def is_valid_bishop_move(start, end):
    return abs(start[0] - end[0]) == abs(start[1] - end[1]) and is_path_clear(start, end)

def is_valid_queen_move(start, end):
    return is_valid_rook_move(start, end) or is_valid_bishop_move(start, end)

def is_valid_king_move(start, end):
    return abs(start[0] - end[0]) <= 1 and abs(start[1] - end[1]) <= 1

def draw_board():
    for row in range(8):
        for col in range(8):
            color = LIGHT_SQUARE_COLOR if (row + col) % 2 == 0 else DARK_SQUARE_COLOR
            pygame.draw.rect(screen, color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def draw_selected_square(square):
    pygame.draw.rect(screen, SELECTED_COLOR, (square[1] * CELL_SIZE, square[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE), 4)

def draw_pieces():
    for row in range(8):
        for col in range(8):
            piece = chess_board[row][col]
            if piece != "":
                x, y = col * CELL_SIZE, row * CELL_SIZE
                if piece.isupper():
                    screen.blit(WHITE_PIECES[piece], (x, y))
                else:
                    screen.blit(BLACK_PIECES[piece], (x, y))

def move_piece(start, end):
    chess_board[end[0]][end[1]] = chess_board[start[0]][start[1]]
    chess_board[start[0]][start[1]] = ""

def is_king_in_check_after_move(start, end):
    temp_piece = chess_board[end[0]][end[1]]
    chess_board[end[0]][end[1]] = chess_board[start[0]][start[1]]
    chess_board[start[0]][start[1]] = ""

    king_position = find_king((current_player, chess_board))
    in_check = is_in_check(king_position)

    chess_board[start[0]][start[1]] = chess_board[end[0]][end[1]]
    chess_board[end[0]][end[1]] = temp_piece

    return in_check

def is_in_check(king_position):
    opponent = 3 - current_player

    for i in range(8):
        for j in range(8):
            if chess_board[i][j] and is_opponent_piece(chess_board[i][j], current_player):
                if is_valid_move((i, j), king_position) and is_valid_capture((i, j), king_position, chess_board[i][j], chess_board[king_position[0]][king_position[1]]):
                    return True
    return False

def find_king(args):
    player, board = args
    for i in range(8):
        for j in range(8):
            if board[i][j] == 'K' and player == 1 or board[i][j] == 'k' and player == 2:
                return i, j

def main_menu():
    while True:
        play_button_rect, rules_button_rect, exit_button_rect = draw_main_menu()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if play_button_rect.collidepoint(pos):
                    last_move = None  # Сбросим last_move перед началом игры
                    return "play"
                elif rules_button_rect.collidepoint(pos):
                    show_rules()
                elif exit_button_rect.collidepoint(pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()

def return_to_main_menu():
    global selected_piece, current_player
    global chess_board
    selected_piece = None
    current_player = 1
    chess_board = [
        ["r", "n", "b", "q", "k", "b", "n", "r"],
        ["p", "p", "p", "p", "p", "p", "p", "p"],
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["P", "P", "P", "P", "P", "P", "P", "P"],
        ["R", "N", "B", "Q", "K", "B", "N", "R"]
    ]

def main():
    global selected_piece, current_player, last_move
    clock = pygame.time.Clock()
    return_to_menu = False
    

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return_to_main_menu()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = pos[1] // CELL_SIZE, pos[0] // CELL_SIZE

                if selected_piece is None:
                    if chess_board[row][col] != "" and (chess_board[row][col].islower() == (current_player == 1)):
                        selected_piece = (row, col)
                    else:
                        selected_piece = None
                else:
                    if is_valid_move(selected_piece, (row, col)) and not is_king_in_check_after_move(selected_piece, (row, col)):
                        last_move = f"{chess_board[selected_piece[0]][selected_piece[1]]} - {chr(ord('A') + selected_piece[1])}{8 - selected_piece[0]} to {chr(ord('A') + col)}{8 - row}"
                        move_piece(selected_piece, (row, col))
                        selected_piece = None
                        current_player = 3 - current_player
                    else:
                        selected_piece = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return_to_main_menu()

            if return_to_menu:
                return_to_main_menu()
                return

        draw_board()
        draw_pieces()

        if selected_piece is not None:
            draw_selected_square(selected_piece)

        pygame.display.flip()
        clock.tick(60)

        if return_to_menu:
            return_to_main_menu()
            return

if __name__ == "__main__":
    if main_menu() == "play":
        main()
    pygame.quit()
    sys.exit()