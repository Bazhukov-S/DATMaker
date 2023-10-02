
# from jinja2 import Environment, FileSystemLoader

# environment = Environment(loader=FileSystemLoader("E:\study\Maker_DAT_BOT\DATMaker\BOXTemplate"))
# template = environment.get_template("BOXTEMPLATE.data")

# NTG = 0.9
# PERM = 100
# PERMZ = PERM / 10
# PORO = 0.2

# param = {"NTG": NTG,
#          "PERM": PERM,
#          "PERMZ": PERMZ,
#          "PORO": PORO
#         }

# filename = f"output.inc"
# content = template.render(param)

# with open(filename, mode="w", encoding="utf-8") as message:
#     message.write(content)
#     print(f"... wrote {filename}")

import math

def calculate_boards(board_length, wall_height, boards_per_width):
    # Определяем высоту, которую можно покрыть одной доской
    board_height = board_length / boards_per_width
    
    # Определяем количество досок, необходимых для застройки стены
    required_boards = math.ceil(wall_height / board_height)
    
    return required_boards

# Пример использования функции
board_length = 6.0 # Длина одной доски
wall_height = 3.1 # Высота стены
boards_per_width = 5 # Количество досок по ширине

result = calculate_boards(board_length, wall_height, boards_per_width)
print(f"Минимальное количество досок, необходимых для застройки стены: {result}")
