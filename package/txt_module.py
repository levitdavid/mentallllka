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
        res_str = ''
        len_set = set()
        for row in rows:
            for el in row:
                len_set.add(len(el))
        try:
            for row in rows:
                for indx in range(len(row)):
                    while len(row[indx]) != max(len_set):
                        row[indx] += ' '
        except ValueError:
            print('Вы подали на вход пустой файл')
            return
        for row in rows:
            for el in row:
                res_str += el + ' '
            res_str += '\n'
        with open(name, 'w') as file:
            file.writelines(res_str)
    except PermissionError:
        print('Файл открыт, его нельзя изменить')
        return