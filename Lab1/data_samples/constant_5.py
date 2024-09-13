# Индексы изменения цен для расчётов
price_change_indices = {
    2018: 1.08,
    2019: 1.10,
    2020: 1.12,
    2021: 1.15
}

# Наименования, категории и первичные ранги ИР
data_dictionary = {
    1: {"NameIR": "сведения_о_новых_технологиях", "category": 1, "rank": 8},
    2: {"NameIR": "решения_совещаний", "category": 1, "rank": 4},
    3: {"NameIR": "бухгалтерские_документы", "category": 1, "rank": 7},
    4: {"NameIR": "маркетинговые_исследования", "category": 1, "rank": 7},
    5: {"NameIR": "АСУ_бизнес-процессами", "category": 1, "rank": 6},
    6: {"NameIR": "персональные_данные_сотрудников", "category": 2, "rank": 9},
    7: {"NameIR": "разработки_отдела_планирования", "category": 2, "rank": 5},
    8: {"NameIR": "резервные_копии_документов", "category": 2, "rank": 2}
}
# Общая информация по ресурсам
resource_info = {
    1: (("разрабатываемый", "приносящий прибыль"), 2018, 5, 7),
    2: (("обслуживаемый",), 2020, 3, 2),
    3: (("обслуживаемый",), 2018, 5, 3),
    4: (("разрабатываемый", "приносящий прибыль"), 2021, 2, 3),
    5: (("приобретаемый", "разрабатываемый", "обслуживаемый"), 2022, 1, 1)
}
# Сведения о новых технологиях
ir_1_info = {
    "Сведения по разработке ресурса": {
        "Первый год разработки": 2019,
        "Количество лет разработки": 3,
        "Годы разработки": [2019, 2020, 2021],
        "Количество сотрудников по годам разработки": [1, 2, 3],
        "Зарплата сотрудников": {
            1: [720000, 690000, 740000],
            2: [None,   560000, 690000],
            3: [None,   None,   580000]
        },
        "Отчисления сотрудников": {
            1: [187200, 179400, 192400],
            2: [None,   145600, 179400],
            3: [None,   None,   150800]
        }
    },
    "Сведения по приносимой прибыли": {
        "Приносимая прибыль": 8000000
    }
}
# Решения совещаний
ir_2_info = {
    "Сведения по обслуживанию ресурса": {
        "Количество сотрудников": [1],
        "Зарплата сотрудников": {
            1: [550000]
        },
        "Отчисления сотрудников": {
            1: [143000]
        },
        "Затраты на расходные материалы": [230000]
    }
}
# Бухгалтерские документы
ir_3_info = {
    "Сведения по обслуживанию ресурса": {
        "Количество сотрудников": [2],
        "Зарплата сотрудников": {
            1: [710000],
            2: [550000]
        },
        "Отчисления сотрудников": {
            1: [184600],
            2: [143000]
        },
        "Затраты на расходные материалы": [230000]
    }
}
# Маркетинговые исследования
ir_4_info = {
    "Сведения по разработке ресурса": {
        "Первый год разработки": 2020,
        "Количество лет разработки": 3,
        "Годы разработки": [2020, 2021, 2022],
        "Количество сотрудников по годам разработки": [2, 3, 3],
        "Зарплата сотрудников": {
            1: [630000, 610000, 540000],
            2: [740000, 640000, 580000],
            3: [None,   770000, 760000]
        },
        "Отчисления сотрудников": {
            1: [163800, 158600, 140400],
            2: [192400, 166400, 150800],
            3: [None,   200200, 197600]
        }
    },
    "Сведения по приносимой прибыли": {
        "Приносимая прибыль": 8400000
    }
}
# АСУ бизнес-процессов
ir_5_info = {
    "Сведения по приобретению ресурса": {
        "Стоимость в год приобретения": 1770000
    },
    "Сведения по разработке ресурса": {
        "Первый год разработки": 2022,
        "Количество лет разработки": 1,
        "Годы разработки": [2022],
        "Количество сотрудников по годам разработки": [3],
        "Зарплата сотрудников": {
            1: [760000],
            2: [550000],
            3: [630000]
        },
        "Отчисления сотрудников": {
            1: [197600],
            2: [143000],
            3: [163800]
        }
    },
    "Сведения по обслуживанию ресурса": {
        "Количество сотрудников": [2],
        "Зарплата сотрудников": {
            1: [500000],
            2: [690000]
        },
        "Отчисления сотрудников": {
            1: [130000],
            2: [179400]
        },
        "Затраты на расходные материалы": [360000]
    }
}