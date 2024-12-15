import csv


def load_table(file_name):
    """
    Создает внутреннее представление таблицы, загруженной из csv-файла.

    Args:
        file_name(str): название файла, который хотите загрузить, или полный путь к нему !С обязательным указанием расширения!

    Returns:
        list: Внутреннее представление таблицы(список списков)
    Raises:
        None
    """
    try:
        with open(file_name, newline='') as file:
            file_csv = csv.reader(file, delimiter=';')
            rows = [_ for _ in file_csv]
    except FileNotFoundError:
        print('Неправильно указан адрес файла или файл не существует')
        return
    except PermissionError:
        print('Необходимо указать путь к файлу, а не к папке')
        return
    else:
        return rows


def save_table(rows, name):
    """
    Сохраняет внутреннее представления таблицы в csv-файл.

    Args:
        rows(list): внутреннее представления модуля(список списков)
        name(str): название файла, который хотите создать, или полный путь к нему
        !С обязательным указанием расширения!
    Returns:
        None
    Raises:
        None
    """
    try:
        with open(name, 'w', newline='') as file:
            file_csv = csv.writer(file, delimiter=';')
            for row in rows:
                file_csv.writerow([el for el in row])
    except PermissionError:
        print('Файл открыт, его нельзя изменить')
        return

