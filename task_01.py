import argparse
import shutil
from pathlib import Path
import sys
from colorama import init, Fore, Style

init()


def setup_command_line_arguments():
    parser = argparse.ArgumentParser(
        description="Рекурсивне копіювання та сортування файлів за розширенням",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Приклади використання:
  python task_01.py /path/to/source
  python task_01.py /path/to/source /path/to/destination
  python task_01.py ./test_folder ./sorted_files
        """
    )
    
    parser.add_argument(
        "source_directory",
        type=Path,
        help="Шлях до вихідної директорії"
    )
    
    parser.add_argument(
        "destination_directory", 
        type=Path,
        nargs='?',
        default=Path("dist"),
        help="Шлях до директорії призначення (за замовчуванням: dist)"
    )
    
    return parser.parse_args()


def create_destination_subdirectory(destination_base_path, file_extension):
    """
    Створює піддиректорію для файлів із вказанним розширенням.
    
    Функція створює директорію, якщо вона не існує.
    
    """
    extension_clean = file_extension.lstrip('.') if file_extension else 'no_extension'
    
    subdirectory_path = destination_base_path / extension_clean
    
    try:
        subdirectory_path.mkdir(parents=True, exist_ok=True)
        return subdirectory_path
    
    except OSError as error:
        print(f"{Fore.RED}Помилка створення директорії {subdirectory_path}: {error}{Style.RESET_ALL}")
        raise


def copy_file_to_destination(source_file_path, destination_directory_path):
    """
    Копіює файл до відповідної піддиректорії на основі розширення.
    """
    try:
        file_extension = source_file_path.suffix.lower()
        
        target_subdirectory = create_destination_subdirectory(
            destination_directory_path, 
            file_extension
        )
        
        destination_file_path = target_subdirectory / source_file_path.name
        
        if destination_file_path.exists():
            counter = 1
            original_stem = source_file_path.stem
            extension = source_file_path.suffix
            
            while destination_file_path.exists():
                new_name = f"{original_stem}_{counter}{extension}"
                destination_file_path = target_subdirectory / new_name
                counter += 1
        
        shutil.copy2(source_file_path, destination_file_path)
        print(f"{Fore.GREEN}Скопійовано:{Style.RESET_ALL} {source_file_path.name} -> {Fore.CYAN}{file_extension or 'no_extension'}/{Style.RESET_ALL}")
        return True
        
    except Exception as error:
        print(f"{Fore.RED}Помилка копіювання файлу {source_file_path}: {error}{Style.RESET_ALL}")
        return False


def process_directory_recursively(current_directory_path, destination_directory_path):
    """
    Рекурсивно обробляємо директорію, копіюючи всі файли.

    1. Перебираємо всі елементи у директорії
    2. Якщо елемент файл - копіюємо його
    3. Якщо елемент директорія - викликаємо рекурсивно
    """
    processed_files_count = 0
    errors_count = 0
    
    try:
        print(f"{Fore.BLUE}Обробляю директорію:{Style.RESET_ALL} {current_directory_path}")
        
        for item_path in current_directory_path.iterdir():
            try:
                if item_path.is_file():
                    if copy_file_to_destination(item_path, destination_directory_path):
                        processed_files_count += 1
                    else:
                        errors_count += 1
                
                elif item_path.is_dir():
                    sub_files, sub_errors = process_directory_recursively(
                        item_path, 
                        destination_directory_path
                    )
                    processed_files_count += sub_files
                    errors_count += sub_errors
                    
            except PermissionError:
                print(f"{Fore.RED}Немає доступу до: {item_path}{Style.RESET_ALL}")
                errors_count += 1
            except Exception as error:
                print(f"{Fore.RED}Помилка обробки {item_path}: {error}{Style.RESET_ALL}")
                errors_count += 1
                
    except PermissionError:
        print(f"{Fore.RED}Немає доступу до директорії: {current_directory_path}{Style.RESET_ALL}")
        errors_count += 1
    except Exception as error:
        print(f"{Fore.RED}Помилка читання директорії {current_directory_path}: {error}{Style.RESET_ALL}")
        errors_count += 1
    
    return processed_files_count, errors_count


def validate_input_arguments(source_path, destination_path):
    if not source_path.exists():
        raise ValueError(f"Вихідна директорія не існує: {source_path}")
    
    if not source_path.is_dir():
        raise ValueError(f"Вказаний шлях не є директорією: {source_path}")
    
    try:
        destination_absolute = destination_path.resolve()
        source_absolute = source_path.resolve()
        
        if destination_absolute == source_absolute:
            raise ValueError("Директорія призначення не може співпадати з вихідною")
        
        try:
            destination_absolute.relative_to(source_absolute)
            raise ValueError("Директорія призначення не може бути піддиректорією вихідної")
        except ValueError:
            pass
            
    except Exception as error:
        print(f"{Fore.YELLOW}Попередження: {error}{Style.RESET_ALL}")
    
    return True


def display_stats(processed_files, errors_count, destination_path):
    print("\n" + "="*60)
    print(f"{Fore.MAGENTA}{Style.BRIGHT}ПІДСУМКОВА СТАТИСТИКА{Style.RESET_ALL}")
    print("="*60)
    print(f"{Fore.GREEN}[OK]{Style.RESET_ALL} Файлів успішно оброблено: {processed_files}")
    print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Помилок під час обробки: {errors_count}")
    print(f"{Fore.BLUE}[INFO]{Style.RESET_ALL} Файли збережено в: {destination_path.resolve()}")
    
    if destination_path.exists():
        print(f"\n{Fore.YELLOW}Створені категорії файлів:{Style.RESET_ALL}")
        try:
            subdirectories = [d for d in destination_path.iterdir() if d.is_dir()]
            subdirectories.sort()
            
            for subdir in subdirectories:
                files_count = len(list(subdir.glob("*")))
                print(f"   {Fore.CYAN}-{Style.RESET_ALL} {subdir.name}: {files_count} файл(ів)")
                
        except Exception as error:
            print(f"{Fore.YELLOW}Не вдалося проаналізувати структуру: {error}{Style.RESET_ALL}")
    
    print("="*60)


def main():
    print(f"{Fore.CYAN}{Style.BRIGHT}Файловий органайзер{Style.RESET_ALL}")
    print(f"{Fore.WHITE}Сортування файлів за розширенням{Style.RESET_ALL}")
    print("="*60)
    
    try:
        args = setup_command_line_arguments()
        source_directory = args.source_directory.resolve()
        destination_directory = args.destination_directory.resolve()
        
        print(f"{Fore.BLUE}Вихідна директорія:{Style.RESET_ALL} {source_directory}")
        print(f"{Fore.BLUE}Директорія призначення:{Style.RESET_ALL} {destination_directory}")
        
        validate_input_arguments(source_directory, destination_directory)
        
        destination_directory.mkdir(parents=True, exist_ok=True)
        
        print(f"\n{Fore.CYAN}Початок обробки...{Style.RESET_ALL}")
        
        processed_files, errors_count = process_directory_recursively(
            source_directory, 
            destination_directory
        )
        
        display_stats(processed_files, errors_count, destination_directory)
        
        exit_code = 0 if errors_count == 0 else 1
        
        if errors_count == 0:
            print(f"{Fore.GREEN}Програма завершена успішно!{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}Програма завершена з помилками.{Style.RESET_ALL}")
        
        sys.exit(exit_code)
        
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Операція перервана{Style.RESET_ALL}")
        sys.exit(1)
    except ValueError as error:
        print(f"{Fore.RED}Помилка: {error}{Style.RESET_ALL}")
        sys.exit(1)
    except Exception as error:
        print(f"{Fore.RED}Помилка: {error}{Style.RESET_ALL}")
        sys.exit(1)


if __name__ == "__main__":
    main()
