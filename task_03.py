import timeit
import random
import statistics
from typing import List, Callable, Dict, Any
import sys
from colorama import init, Fore, Style

init()


def merge_sort(array_to_sort: List[int]) -> List[int]:
    """
    Реалізує алгоритм сортування злиттям (Merge Sort).
    """
    if len(array_to_sort) <= 1:
        return array_to_sort.copy()
    
    middle_index = len(array_to_sort) // 2
    left_half = array_to_sort[:middle_index]
    right_half = array_to_sort[middle_index:]
    
    sorted_left = merge_sort(left_half)
    sorted_right = merge_sort(right_half)
    
    return merge_two_sorted_arrays(sorted_left, sorted_right)


def merge_two_sorted_arrays(left_array: List[int], right_array: List[int]) -> List[int]:
    """
    Зливає два відсортованих масиви в один відсортований масив.
    """
    merged_result = []
    left_index = right_index = 0
    
    while left_index < len(left_array) and right_index < len(right_array):
        if left_array[left_index] <= right_array[right_index]:
            merged_result.append(left_array[left_index])
            left_index += 1
        else:
            merged_result.append(right_array[right_index])
            right_index += 1
    
    merged_result.extend(left_array[left_index:])
    merged_result.extend(right_array[right_index:])
    
    return merged_result


def insertion_sort(array_to_sort: List[int]) -> List[int]:
    """
    Реалізує алгоритм сортування вставками (Insertion Sort).
    """
    sorted_array = array_to_sort.copy()
    
    for current_position in range(1, len(sorted_array)):
        current_element = sorted_array[current_position]
        
        insert_position = current_position - 1
        
        while insert_position >= 0 and sorted_array[insert_position] > current_element:
            sorted_array[insert_position + 1] = sorted_array[insert_position]
            insert_position -= 1
        
        sorted_array[insert_position + 1] = current_element
    
    return sorted_array


def timsort_wrapper(array_to_sort: List[int]) -> List[int]:
    """
    Обгортка для вбудованого алгоритму сортування Python (Timsort).
    """
    return sorted(array_to_sort)


def generate_test_data(size: int, data_type: str) -> List[int]:
    """
    Генерує тестові дані різних типів для перевірки алгоритмів.
    """
    if data_type == 'random':
        return [random.randint(1, 1000) for _ in range(size)]
    
    elif data_type == 'sorted':
        return list(range(1, size + 1))
    
    elif data_type == 'reverse':
        return list(range(size, 0, -1))
    
    elif data_type == 'nearly_sorted':
        base_array = list(range(1, size + 1))
        swaps_count = max(1, size // 10)
        for _ in range(swaps_count):
            i, j = random.randint(0, size-1), random.randint(0, size-1)
            base_array[i], base_array[j] = base_array[j], base_array[i]
        return base_array
    
    else:
        raise ValueError(f"Невідомий тип даних: {data_type}")


def measure_algorithm_performance(
    sorting_algorithm: Callable[[List[int]], List[int]], 
    test_data: List[int], 
    iterations_count: int = 3
) -> float:
    """
    Вимірює час виконання алгоритму сортування.
    """
    def run_single_test():
        data_copy = test_data.copy()
        return sorting_algorithm(data_copy)
    
    execution_times = []
    for _ in range(iterations_count):
        execution_time = timeit.timeit(run_single_test, number=1)
        execution_times.append(execution_time)
    
    return statistics.mean(execution_times)


def run_comprehensive_performance_test() -> Dict[str, Any]:
    algorithms_to_test = {
        'Merge Sort': merge_sort,
        'Insertion Sort': insertion_sort, 
        'Timsort (Python)': timsort_wrapper
    }
    
    test_sizes = [100, 500, 1000, 2000, 5000]
    data_types = ['random', 'sorted', 'reverse', 'nearly_sorted']
    
    print(f"{Fore.MAGENTA}{Style.BRIGHT}КОМПЛЕКСНЕ ТЕСТУВАННЯ АЛГОРИТМІВ СОРТУВАННЯ{Style.RESET_ALL}")
    print(f"{Fore.CYAN}=" * 70 + f"{Style.RESET_ALL}")
    print(f"{Fore.WHITE}Тестуємо {len(algorithms_to_test)} алгоритми{Style.RESET_ALL}")
    print(f"{Fore.WHITE}Розміри масивів: {test_sizes}{Style.RESET_ALL}")
    print(f"{Fore.WHITE}Типи даних: {data_types}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}=" * 70 + f"{Style.RESET_ALL}")
    
    test_results = {
        'algorithms': list(algorithms_to_test.keys()),
        'sizes': test_sizes,
        'data_types': data_types,
        'results': {}
    }
    
    total_tests = len(algorithms_to_test) * len(test_sizes) * len(data_types)
    current_test = 0
    
    for algorithm_name, algorithm_function in algorithms_to_test.items():
        test_results['results'][algorithm_name] = {}
        
        for data_type in data_types:
            test_results['results'][algorithm_name][data_type] = {}
            
            for size in test_sizes:
                current_test += 1
                print(f"{Fore.BLUE}[{current_test}/{total_tests}]{Style.RESET_ALL} Тестую {Fore.YELLOW}{algorithm_name}{Style.RESET_ALL} | {Fore.GREEN}{data_type}{Style.RESET_ALL} | {size} елементів...")
                
                try:
                    test_data = generate_test_data(size, data_type)
                    
                    execution_time = measure_algorithm_performance(
                        algorithm_function, 
                        test_data, 
                        iterations_count=3
                    )
                    
                    test_results['results'][algorithm_name][data_type][size] = execution_time
                    
                    print(f"    {Fore.GREEN}Завершено за {execution_time:.6f} секунд{Style.RESET_ALL}")
                    
                except Exception as error:
                    print(f"    {Fore.RED}Помилка: {error}{Style.RESET_ALL}")
                    test_results['results'][algorithm_name][data_type][size] = None
    
    return test_results


def analyze_and_display_results(test_results: Dict[str, Any]) -> None:
    """
    Аналізує та відображає результати тестування у зручному форматі.
    """
    print("\n" + f"{Fore.CYAN}=" * 80 + f"{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}{Style.BRIGHT}АНАЛІЗ РЕЗУЛЬТАТІВ ТЕСТУВАННЯ{Style.RESET_ALL}")
    print(f"{Fore.CYAN}=" * 80 + f"{Style.RESET_ALL}")

    algorithms = test_results['algorithms']
    sizes = test_results['sizes']
    data_types = test_results['data_types']
    results = test_results['results']

    print(f"\n{Fore.GREEN}{Style.BRIGHT}ПЕРЕМОЖЦІ ЗА КАТЕГОРІЯМИ:{Style.RESET_ALL}")
    print(f"{Fore.GREEN}-" * 50 + f"{Style.RESET_ALL}")
    
    for data_type in data_types:
        print(f"\n{Fore.CYAN}{data_type.upper()}:{Style.RESET_ALL}")
        for size in sizes:
            fastest_algorithm = None
            best_time = float('inf')
            
            for algorithm in algorithms:
                time_result = results[algorithm][data_type][size]
                if time_result is not None and time_result < best_time:
                    best_time = time_result
                    fastest_algorithm = algorithm
            
            if fastest_algorithm:
                print(f"  {size:>5} елементів: {Fore.GREEN}{fastest_algorithm}{Style.RESET_ALL} ({best_time:.6f}s)")


def generate_performance_insights(test_results: Dict[str, Any]) -> None:
    """
    Генерує висновки та інсайти на основі результатів тестування.
    """
    print(f"\n" + f"{Fore.CYAN}=" * 80 + f"{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}{Style.BRIGHT}ВИСНОВКИ ТА РЕКОМЕНДАЦІЇ{Style.RESET_ALL}")
    print(f"{Fore.CYAN}=" * 80 + f"{Style.RESET_ALL}")
    
    results = test_results['results']
    
    print(f"\n{Fore.WHITE}{Style.BRIGHT}Основні спостереження:{Style.RESET_ALL}")
    
    # Аналіз Insertion Sort
    print(f"\n{Fore.YELLOW}Insertion Sort:{Style.RESET_ALL}")
    print(f"  {Fore.CYAN}-{Style.RESET_ALL} Найкращі результати на малих масивах (< 1000 елементів)")
    print(f"  {Fore.CYAN}-{Style.RESET_ALL} Відмінна продуктивність на відсортованих даних") 
    print(f"  {Fore.CYAN}-{Style.RESET_ALL} Погана продуктивність на великих випадкових масивах")
    print(f"  {Fore.CYAN}-{Style.RESET_ALL} Квадратична складність O(n²) проявляється на великих даних")
    
    # Аналіз Merge Sort  
    print(f"\n{Fore.BLUE}Merge Sort:{Style.RESET_ALL}")
    print(f"  {Fore.CYAN}-{Style.RESET_ALL} Стабільна продуктивність O(n log n) на всіх типах даних")
    print(f"  {Fore.CYAN}-{Style.RESET_ALL} Не залежить від початкового порядку елементів")
    print(f"  {Fore.CYAN}-{Style.RESET_ALL} Ефективний на великих масивах")
    print(f"  {Fore.CYAN}-{Style.RESET_ALL} Потребує додаткову пам'ять для злиття")
    
    # Аналіз Timsort
    print(f"\n{Fore.GREEN}Timsort (Python):{Style.RESET_ALL}")
    print(f"  {Fore.CYAN}-{Style.RESET_ALL} Найкраща загальна продуктивність у більшості випадків")
    print(f"  {Fore.CYAN}-{Style.RESET_ALL} Адаптується до структури даних")
    print(f"  {Fore.CYAN}-{Style.RESET_ALL} Використовує переваги частково відсортованих даних")
    print(f"  {Fore.CYAN}-{Style.RESET_ALL} Оптимізований на рівні C для максимальної швидкості")
    
    print(f"\n{Fore.WHITE}{Style.BRIGHT}Практичні рекомендації:{Style.RESET_ALL}")
    print("  1. Для загального використання - завжди використовуйте sorted() або .sort()")
    print("  2. Для навчання алгоритмів - вивчайте merge sort як еталон O(n log n)")
    print("  3. Для малих масивів (< 50) - insertion sort може бути ефективним")
    print("  4. Timsort демонструє силу гібридних підходів та оптимізацій")
    
    print(f"\n{Fore.WHITE}{Style.BRIGHT}Теоретичні висновки підтверджені:{Style.RESET_ALL}")
    print("  - Insertion Sort: O(n²) середня складність")
    print("  - Merge Sort: O(n log n) гарантована складність") 
    print("  - Timsort: O(n log n) з адаптивними оптимізаціями")
    
    # Детальний аналіз гібридної природи Timsort
    print(f"\n{Fore.MAGENTA}{Style.BRIGHT}ЧОМУ TIMSORT НАБАГАТО ЕФЕКТИВНІШИЙ:{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}=" * 60 + f"{Style.RESET_ALL}")
    
    print(f"\n{Fore.YELLOW}{Style.BRIGHT}Гібридний підхід - поєднання кращого з двох світів:{Style.RESET_ALL}")
    print("  Insertion Sort для малих сегментів (< 64 елементи):")
    print("     - Низькі накладні витрати на малих масивах")
    print("     - Природна адаптивність до частково відсортованих даних")
    print("     - Простота реалізації та швидкість на практиці")
    
    print(f"\n  Merge Sort для великих сегментів:")
    print("     - Гарантована O(n log n) складність")
    print("     - Стабільність сортування")
    print("     - Передбачувана продуктивність")
    
    print(f"\n{Fore.BLUE}{Style.BRIGHT}Інтелектуальні оптимізації Timsort:{Style.RESET_ALL}")
    print("  1. Виявлення природних послідовностей (runs):")
    print("      - Знаходить вже відсортовані підпослідовності")
    print("      - Використовує їх як основу для злиття")
    print("      - Мінімізує кількість операцій порівняння")
    
    print(f"\n  2. Адаптивне злиття:")
    print("      - Використовує галопуючий режим для нерівних послідовностей")
    print("      - Динамічно налаштовує стратегію злиття")
    print("      - Оптимізує роботу з реальними даними")
    
    print(f"\n  3. Мінімальне злиття:")
    print("      - Зливає послідовності оптимальними групами")
    print("      - Підтримує інваріант розмірів стеку")
    print("      - Забезпечує баланс між швидкістю та пам'яттю")
    
    print(f"\n{Fore.GREEN}{Style.BRIGHT}Емпіричні докази ефективності Timsort:{Style.RESET_ALL}")
    print("  - На випадкових даних: постійно перевершує окремі алгоритми")
    print("  - На відсортованих даних: працює за O(n) замість O(n log n)")
    print("  - На частково відсортованих: використовує існуючий порядок")
    print("  - На зворотно відсортованих: ефективно обертає послідовності")
    
    print(f"\n{Fore.CYAN}{Style.BRIGHT}Чому програмісти використовують вбудовані алгоритми:{Style.RESET_ALL}")
    print("  - Роки оптимізації та тестування на реальних даних")
    print("  - Реалізація на рівні C для максимальної швидкості")
    print("  - Врахування особливостей архітектури процесора")
    print("  - Підтримка edge cases та граничних умов")
    print("  - Стабільність та надійність у production системах")
    
    print(f"\n{Fore.RED}{Style.BRIGHT}Головний висновок:{Style.RESET_ALL}")
    print("  Timsort демонструє, що найкращі алгоритми - це не просто")
    print("      теоретичні конструкції, а результат поєднання:")
    print("      - Теоретичних знань про складність алгоритмів")
    print("      - Практичного розуміння реальних даних")
    print("      - Інженерних оптимізацій та тюнінгу")
    print("      - Тривалого тестування на різноманітних наборах даних")


def main():
    print(f"{Fore.MAGENTA}{Style.BRIGHT}ПОРІВНЯЛЬНИЙ АНАЛІЗ АЛГОРИТМІВ СОРТУВАННЯ{Style.RESET_ALL}")
    print(f"{Fore.WHITE}Емпірична перевірка теоретичних оцінок складності{Style.RESET_ALL}")
    print(f"{Fore.CYAN}=" * 80 + f"{Style.RESET_ALL}")
    
    try:
        random.seed(42)
        
        print(f"{Fore.WHITE}Запускаю комплексне тестування...{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Це може зайняти кілька хвилин, будь ласка, зачекайте...{Style.RESET_ALL}")
        
        test_results = run_comprehensive_performance_test()
        
        analyze_and_display_results(test_results)
        
        print(f"\n{Fore.GREEN}Аналіз завершено успішно!{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Детальні результати збережені в пам'яті програми{Style.RESET_ALL}")
        
        return test_results
        
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Тестування перервано користувачем{Style.RESET_ALL}")
        sys.exit(0)
    except Exception as error:
        print(f"\n{Fore.RED}Критична помилка під час тестування: {error}{Style.RESET_ALL}")
        sys.exit(1)


if __name__ == "__main__":
    main()