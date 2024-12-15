import copy


def get_rows_by_number(rows, start, stop = None, copy_table=False):
    """
    Получение таблицы из одной строки или из строк из интервала по номеру строки.

    Args:
        rows(list): внутреннее представление
        start(int): левая граница интревала
        stop(int): правая граница интревала
        copy_table(bool): если False, то изменения отобразятся в исходном файле.
        В противном случае исходный файл не изменится

    Returns:
        list: внутреннее представление

    Raises:
        Exception('Ошибка, использование значения start/stop с таким'
                        ' номером невозможно')
    """
    if start < 1 or stop > len(rows):
        raise Exception('Ошибка, использование значения start/stop с таким'
                        ' номером невозможно')
    try:
        if stop is None:
            table = [rows[0]] + rows[start]
        else:
            table = [rows[0]] + rows[start: stop + 1]
    except IndexError:
        print('Нет элемента с таким номером')
        return
    if copy_table:
        return table
    else:
        rows.clear()
        for row in table:
            rows.append(row)
        return rows


def get_rows_by_index(rows, *values, copy_table=False):
    """
    Получение новой таблицы из одной строки или из строк со значениями в первом столбце,
    совпадающими с переданными аргументами val1, … , valN.

    Args:
        rows(list): внутреннее представление
        *values(int, str, bool, float): значения, с которыми будет осуществляться проверка совпадений
        copy_table(bool): если False, то изменения отобразятся в исходном файле. В противном случае исходный файл не изменится

    Returns:
        list: внутреннее представление
    Raises:
        None
    """
    if copy_table is False:
        table = copy.deepcopy(rows)
        rows.clear()
    else:
        table = rows
    result = [table[0]]
    table = table[1:]
    vals = [val for val in values]
    for indx1, row in enumerate(table):
        for indx2, el in enumerate(table):
            try:
                table[indx1][indx2] = int(table[indx1][indx2])
            except ValueError:
                try:
                    table[indx1][indx2] = float(table[indx1][indx2])
                except ValueError:
                    pass
    for row in table:
        if row[0] in vals:
            result.append([str(el) for el in row])
    if copy_table:
        return result
    else:
        for row in result:
            rows.append(row)
        return rows


def get_column_types(rows, by_number=True):
    """
    Получение словаря вида столбец:тип_значений. Тип значения: int, float, bool, str (по умолчанию для всех столбцов).

    Args:
        rows(list): внутреннее представление
        by_number(bool): Если True, то ключи в словарях - индекс столбцов, иначе - их строковые представления

    Returns:
        dict: словарь вида столбец: тип_значений.
    Raises:
        None
    """
    dct = {}
    columns = []
    for indx in range(len(rows[0])):
        column = []
        for row in rows:
            column.append(row[indx])
        columns.append(column)

    for indx, column in enumerate(columns):
        if by_number is False:
            indx = column[0]
        if column[1] == 'True' or column[1] == 'False':
            dct[indx] = bool
            continue
        try:
            crutch = int(column[1])
            dct[indx] = int
        except ValueError:
            try:
                crutch = float(column[1])
                dct[indx] = float
            except ValueError:
                dct[indx] = str
    return dct


def set_column_types(rows, types_dict, by_number=True):
    """
    Задание словаря вида столбец:тип_значений. Тип значения: int, float, bool, str (по умолчанию для всех столбцов).

    Args:
        rows(list): внутреннее представление
        types_dict(dict): словарь
        by_number(bool): Если True, то ключи в словарях - индекс столбцов,
         иначе - их строковые представления

    Returns:
        list: внутреннее представление
    Raises:
        None
    """
    header = rows[0]
    res_rows = [header]
    columns = []
    for indx in range(len(rows[0])):
        column = []
        for row in rows:
            column.append(row[indx])
        columns.append(column)
    if by_number is True:
        dct = {indx: el[1:] for indx, el in enumerate(columns)}
    else:
        dct = {el[0]: el[1:] for el in columns}
    try:
        for key, value in types_dict.items():
            for indx, el in enumerate(dct[key]):
                if el == 'True':
                    dct[key][indx] = True
                elif el == 'False':
                    dct[key][indx] = False
                else:
                    try:
                        dct[key][indx] = int(dct[key][indx])
                    except ValueError:
                        try:
                            dct[key][indx] = float(dct[key][indx])
                        except ValueError:
                            pass
                dct[key][indx] = str(value(dct[key][indx]))
    except KeyError:
        print('В таблице нет столбца с таким названием/индексом')
        return
    except ValueError:
        print('Ошибка! Нельзя конвертировать значение в указанный тип данных')
        return
    for indx in range(len(columns[0]) - 1):
        row = []
        for value in dct.values():
            row.append(value[indx])
        res_rows.append(row)
    return res_rows


def get_value(rows, column=0):
    """
    Аналог get_values(column=0) для представления таблицы с одной строкой

    Args:
        rows(list): внутреннее представление
        column(int, str): либо номер столбца, либо его строковое представление

    Returns:
       list: значение, которое надо было получить, типизованное согласно типу столбца
     Raises:
        Exception('Ошибка, в таблице не одна строка!')
        Exception('Столбца с таким номером не существует')
   """


    if type(column) == int and column < 1:
        raise Exception('Столбца с таким номером не существует')
    if len(rows) != 2:
        raise Exception('Ошибка, в таблице не одна строка!')
    dct = {}
    for indx, el in enumerate(rows[1]):
        if type(column) != int:
            indx = rows[0][indx]
        else:
            indx += 1
        if el == 'True':
            dct[indx] = True
        elif el == 'False':
            dct[indx] = False
        else:
            try:
                dct[indx] = int(el)
            except ValueError:
                try:
                    dct[indx] = float(el)
                except ValueError:
                    dct[indx] = el
    try:
        return dct[column]
    except KeyError:
        print('Столбца с таким индексом/названием не существует')
        return


def get_values(rows, column=0):
    """
    Получение списка значений (типизированных согласно типу столбца).

    Args:
        rows(list): внутреннее представление
        column(int, str): либо номер столбца, либо его строковое представление

    Returns:
        list: столбец в виде списка
    Raises:
        Exception('Столбца с таким номером не существует')
    """
    if type(column) == int:
        if column < 1:
            raise Exception('Столбца с таким номером не существует')
    header = rows[0]
    dct = {}
    value_dct = {}
    columns = []
    for indx in range(len(rows[0])):
        col = []
        for row in rows:
            col.append(row[indx])
        columns.append(col)
    for indx, col in enumerate(columns):
        if type(column) != int:
            indx = col[0]
        else:
            indx += 1
        if col[1] == 'True' or col[1] == 'False':
            dct[indx] = bool
            continue
        try:
            crutch = int(col[1])  # ну тут соминительно(является ли заголовок столбца его первой строккой?)
            dct[indx] = int
        except ValueError:
            try:
                crutch = float(col[1])  # ну тут соминительно(является ли заголовок столбца его первой строккой?)
                dct[indx] = float
            except ValueError:
                dct[indx] = str

    iteration = 0
    for key, value in dct.items():
        lst = []
        for el in columns[iteration]:
            if el == 'True':
                lst.append(True)
            elif el == 'False':
                lst.append(False)
            else:
                try:
                    lst.append(int(el))
                except ValueError:
                    try:
                        lst.append(float(el))
                    except ValueError:
                        lst.append(el)
        value_dct[key] = [value(el) for el in lst[1:]]
        iteration += 1
    try:
        return value_dct[column]
    except KeyError:
        print('Столбца с таким индексом/названием не существует')
        return


def set_value(rows, value, column=0):
    """
    Aналог set_values(value, column=0) для представления таблицы с одной строкой

    Args:
        rows(list): внутреннее представление
        value(int, str, bool, float): одно значение (типизированное согласно типу столбца).
        column(int, str): либо номер столбца, либо его строковое представление

    Returns:
        list: внутреннее представление
    Raises:
        Exception('Тип введенного value не соответствует требованиям')
        Exception('столбца с таким номером не существует')
        Exception('В таблице не одна строка, ошибка')
        KeyError('Столбца с таким индексом/названием не существует')
    """
    header = rows[0]
    if type(value) != int and type(value) != float and type(value) != bool and type(value) != str:
        raise Exception('Тип введенного value не соответствует требованиям')
    dct = {}
    types_dct = {}
    if type(column) == int:
        if column < 1:
            raise Exception('столбца с таким номером не существует')
    if len(rows) != 2:
        raise Exception('В таблице не одна строка, ошибка')
    for indx, col in enumerate(rows[1]):
        if type(column) != int:
            indx = rows[0][indx]
        else:
            indx += 1
        dct[indx] = col

    for key, val in dct.items():
        el = val
        if el == 'True' or el == 'False':
            types_dct[key] = bool
        else:
            try:
                crutch = int(el)
                types_dct[key] = int
            except ValueError:
                try:
                    crutch = float(el)
                    types_dct[key] = float
                except ValueError:
                    types_dct[key] = str
    if column not in dct:
        raise KeyError('Столбца с таким индексом/названием не существует')
    typ = types_dct[column]
    value = typ(value)
    if value is True:
        value = 'True'
    elif value is False:
        value = 'False'
    dct[column] = str(value)
    res_columns = [value for value in dct.values()]
    return [header] + [res_columns]


def set_values(rows, values, column=0):
    """
    Задание списка значений values для столбца таблицы (типизированных согласно типу столбца)

    Args:
        rows(list): внутреннее представление
        values(list): список значений для столбца таблицы
        column(int, str): либо номер столбца, либо его строковое представление

    Returns:
       list: внутреннее представление
    Raises:
        Exception('Cтолбца с таким номером не существует')
    """
    header = rows[0]
    dct = {}
    types_dct = {}
    if type(column) == int:
        if column < 1:
            raise Exception('Cтолбца с таким номером не существует')
    columns = []
    res_rows = []
    for indx in range(len(rows[0])):
        col = []
        for row in rows:
            col.append(row[indx])
        columns.append(col)
    for indx, col in enumerate(columns):
        if type(column) != int:
            indx = col[0]
        else:
            indx += 1
        dct[indx] = col[1:]

    for key, value in dct.items():
        el = value[0]
        if el == 'True' or el == 'False':
            types_dct[key] = bool
        else:
            try:
                crutch = int(el)
                types_dct[key] = int
            except ValueError:
                try:
                    crutch = float(el)
                    types_dct[key] = float
                except ValueError:
                    types_dct[key] = str
    try:
        if len(dct[column]) != len(values):
            print('Кол-во значений в задаваемом столбце не соответcтвует размеру таблицы')
            return
    except KeyError:
        print('Столбца с таким индексом/названием не существует')
        return
    else:
        typ = types_dct[column]
        try:
            values = [str(typ(el)) for el in values]
        except ValueError:
            print('Вы ввели данные, которые нельзя типизировать')
            return
        for indx in range(len(values)):
            if values[indx] is True:
                values[indx] = 'True'
            elif values[indx] is False:
                values[indx] = 'False'
        dct[column] = values
    res_columns = [value for value in dct.values()]
    for indx in range(len(res_columns[0])):
        row = []
        for col in res_columns:
            row.append(col[indx])
        res_rows.append(row)
    return [header] + res_rows


def print_table(rows):
    """
    Aналог set_values(value, column=0) для представления таблицы с одной строкой

    Args:
        rows(list): внутреннее представления модуля(список списков)
    Returns:
        None
    Raises:
        None
    """
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
    print(res_str)