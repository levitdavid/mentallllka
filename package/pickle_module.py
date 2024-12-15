import pickle


def load_table(file_name):
    """
    Создает внутреннее представление таблицы.

    Args:
        file_name(str): название файла, который хотите загрузить,
         или полный путь к нему !С обязательным указанием расширения!
    Returns:
        list: Внутреннее представление таблицы(список списков)
    Raises:
        None
    """
    try:
        with open(file_name, 'rb') as file:
            rows = pickle.load(file)
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
    Сохраняет внутреннее представления таблицы в файл.

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
        with open(name, 'wb') as file:
            pickle.dump(rows, file)

    except PermissionError:
        print('Файл открыт, его нельзя изменить')
        return