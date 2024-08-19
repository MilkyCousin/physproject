def init_directory(dirname: str, rmfiles: bool = True) -> str:
    """
    Проміжна процедура. Створює директорію **dirname** якщо не існує такої.
    Інакше видаляє контент директорії, якщо значенням **rmfiles** є істина.
    Повертає назву директорії **dirname**.
    """
    from os import makedirs, remove
    from os.path import join, exists
    from glob import glob

    if not exists(dirname):
        makedirs(dirname)
    else:
        if rmfiles:
            files = glob(join(dirname, "*"))
            for f in files:
                remove(f)
    return dirname


def generate_object(image_path: str, nzones: int, params: list) -> dict:
    """
    Створення об'єкту для запису в JSON файл.
    Об'єкт містить шлях параметри суми спектральних функцій по типу кількості
    доданків **nzones** та набору параметрів кожної з спектральних функцій **parameters**.
    """
    return {"image": image_path, "nzones": nzones, "parameters": params}
