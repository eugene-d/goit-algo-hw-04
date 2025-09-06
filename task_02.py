import matplotlib.pyplot as plt
import numpy as np
import argparse
import sys
from colorama import init, Fore, Style

init()


def setup_command_line_parser():
    parser = argparse.ArgumentParser(
        description="Генерація фракталу 'Сніжинка Коха' з використанням рекурсії",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Приклади використання:
  python task_02.py                    # рівень 3, розмір 300
  python task_02.py --level 4          # рівень 4, розмір 300  
  python task_02.py --level 2 --size 200  # рівень 2, розмір 200
  
Рекомендації:
  - Рівень 0-2: швидкий результат, проста форма
  - Рівень 3-4: гарний баланс деталей та швидкості
  - Рівень 5+: дуже детально
        """
    )
    
    parser.add_argument(
        "--level", "-l",
        type=int,
        default=3,
        help="Рівень рекурсії (глибина деталізації фракталу, за замовчуванням: 3)"
    )
    
    parser.add_argument(
        "--size", "-s", 
        type=int,
        default=300,
        help="Розмір сторони початкового трикутника (за замовчуванням: 300)"
    )
    
    return parser.parse_args()


def validate_input_parameters(recursion_level, triangle_size):
    if recursion_level < 0:
        raise ValueError("Рівень рекурсії не може бути від'ємним")
    
    if recursion_level > 6:
        print(f"{Fore.YELLOW}Попередження: високий рівень може бути повільним{Style.RESET_ALL}")
    
    if triangle_size <= 0:
        raise ValueError("Розмір трикутника повинен бути позитивним числом")
    
    if triangle_size > 800:
        print(f"{Fore.YELLOW}Попередження: великий розмір може не поміститися{Style.RESET_ALL}")


def koch_curve_points(start_point, end_point, recursion_level):
    """
    Генерує точки для сегменту кривої Коха рекурсивно.
    Повертає список точок, які формують криву Коха між двома точками.
    """
    if recursion_level == 0:
        return [start_point, end_point]
    
    # Обчислюємо ключові точки для побудови кривої Коха
    dx = end_point[0] - start_point[0]
    dy = end_point[1] - start_point[1]
    
    # Точки поділу лінії на три частини
    point1 = (start_point[0] + dx/3, start_point[1] + dy/3)
    point2 = (start_point[0] + 2*dx/3, start_point[1] + 2*dy/3)
    
    # Точка вершини трикутника (поворот на 60 градусів)
    angle = np.pi / 3  # 60 градусів
    cos_a = np.cos(angle)
    sin_a = np.sin(angle)
    
    # Вектор від point1 до point2
    seg_dx = point2[0] - point1[0]
    seg_dy = point2[1] - point1[1]
    
    # Поворот вектора на 60 градусів
    peak_x = point1[0] + seg_dx * cos_a - seg_dy * sin_a
    peak_y = point1[1] + seg_dx * sin_a + seg_dy * cos_a
    peak_point = (peak_x, peak_y)
    
    points = []
    segments = [
        (start_point, point1),
        (point1, peak_point),
        (peak_point, point2),
        (point2, end_point)
    ]
    
    for i, (seg_start, seg_end) in enumerate(segments):
        segment_points = koch_curve_points(seg_start, seg_end, recursion_level - 1)
        if i == 0:
            points.extend(segment_points)
        else:
            points.extend(segment_points[1:])
    
    return points


def create_koch_snowflake(recursion_level, side_length):
    height = side_length * np.sqrt(3) / 2
    triangle_vertices = [
        (-side_length/2, -height/3),
        (side_length/2, -height/3),
        (0, 2*height/3)
    ]
    
    print(f"{Fore.CYAN}Генерую сніжинку Коха, рівень {recursion_level}{Style.RESET_ALL}")
    
    all_points = []
    
    # Створюємо криву Коха для кожної сторони трикутника
    for i in range(3):
        start_vertex = triangle_vertices[i]
        end_vertex = triangle_vertices[(i + 1) % 3]
        
        print(f"{Fore.BLUE}   Обробляю сторону {i + 1}/3...{Style.RESET_ALL}")
        
        side_points = koch_curve_points(start_vertex, end_vertex, recursion_level)
        
        if i == 0:
            all_points.extend(side_points)
        else:
            all_points.extend(side_points[1:])
    
    all_points.append(all_points[0])
    
    x_coords = [point[0] for point in all_points]
    y_coords = [point[1] for point in all_points]
    
    return x_coords, y_coords


def setup_matplotlib_environment(window_title, side_length):
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(10, 10))
    
    fig.patch.set_facecolor('navy')
    ax.set_facecolor('navy')
    
    margin = side_length * 0.2
    ax.set_xlim(-side_length/2 - margin, side_length/2 + margin)
    ax.set_ylim(-side_length/2 - margin, side_length/2 + margin)
    
    ax.set_aspect('equal')
    ax.axis('off')
    
    plt.title(window_title, color='cyan', fontsize=16, pad=20)
    
    return fig, ax


def display_fractal_info(recursion_level, side_length):
    total_segments = 3 * (4 ** recursion_level)
    
    print("\n" + "="*60)
    print(f"{Fore.MAGENTA}{Style.BRIGHT}СНІЖИНКА КОХА{Style.RESET_ALL}")
    print("="*60)
    print(f"{Fore.CYAN}Рівень рекурсії:{Style.RESET_ALL} {recursion_level}")
    print(f"{Fore.CYAN}Розмір сторони:{Style.RESET_ALL} {side_length} пікселів")
    print(f"{Fore.CYAN}Кількість сегментів:{Style.RESET_ALL} {total_segments:,}")
    
    if recursion_level == 0:
        print(f"{Fore.GREEN}Простий трикутник{Style.RESET_ALL}")
    elif recursion_level <= 2:
        print(f"{Fore.GREEN}Проста сніжинка{Style.RESET_ALL}")
    elif recursion_level <= 4:
        print(f"{Fore.YELLOW}Деталізована сніжинка{Style.RESET_ALL}")  
    else:
        print(f"{Fore.RED}Дуже деталізована (повільно){Style.RESET_ALL}")
    
    print("="*60)


def main():
    try:
        args = setup_command_line_parser()
        recursion_level = args.level
        triangle_side_length = args.size
        
        validate_input_parameters(recursion_level, triangle_side_length)
        display_fractal_info(recursion_level, triangle_side_length)
        
        print(f"\n{Fore.CYAN}Генерую фрактал...{Style.RESET_ALL}")
        
        x_coords, y_coords = create_koch_snowflake(recursion_level, triangle_side_length)
        
        window_title = f"Сніжинка Коха - Рівень {recursion_level}"
        fig, ax = setup_matplotlib_environment(window_title, triangle_side_length)
        
        ax.plot(x_coords, y_coords, color='cyan', linewidth=2)
        
        print(f"\n{Fore.GREEN}Готово!{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Закрийте вікно для завершення програми{Style.RESET_ALL}")
        
        plt.tight_layout()
        plt.show()
        
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Генерацію перервано{Style.RESET_ALL}")
        sys.exit(0)
    except ValueError as error:
        print(f"\n{Fore.RED}Помилка: {error}{Style.RESET_ALL}")
        sys.exit(1)
    except Exception as error:
        print(f"\n{Fore.RED}Помилка: {error}{Style.RESET_ALL}")
        sys.exit(1)


if __name__ == "__main__":
    main()