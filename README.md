# physproject

Даний репозиторій містить розробки, присвячені аналізу даних з ARPES.

У директорії utils лежать підпрограми Python для реалізації потрібних задач. Конкретно:
- formulas.py має програмні реалізації фізичних формул з ARPES теорії,
- visualisation.py має створення теплової карти,
- transformations.py містить додаткові перетворення над числовими масивами,
- miscellaneous.py містить допоміжні процедури на кшталт запису даних у словник, або ж робота з файлами.

Основні програми репозиторія (використання підпрограм вище):
- unit_simulation.py генерує теплову карту суми спектральних функцій за їх параметрами з JSON файлу, вказаним у тілі програми,
- random_simulations.py генерує задану кількість теплових карт для сум спектральних функцій, де параметри обираються із заданого діапазону випадковим чином.
