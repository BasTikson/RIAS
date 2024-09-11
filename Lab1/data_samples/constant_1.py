# Индексы изменения цен для расчётов
price_change_indices = {
    2018: 1.08,
    2019: 1.10,
    2020: 1.12,
    2021: 1.15
}
# Наименования, категории и первичные ранги ИР
data_dictionary = {
    1: {"NameIR": "Сведения о новых технологиях", "category": 1, "rank": 8},
    2: {"NameIR": "Решения совещаний", "category": 1, "rank": 4},
    3: {"NameIR": "Бухгалтерские документы", "category": 1, "rank": 7},
    4: {"NameIR": "Маркетинговые исследования", "category": 1, "rank": 7},
    5: {"NameIR": "АСУ бизнес-процессами", "category": 1, "rank": 6},
    6: {"NameIR": "Персональные данные сотрудников", "category": 2, "rank": 9},
    7: {"NameIR": "Разработки отдела планирования", "category": 2, "rank": 5},
    8: {"NameIR": "Резервные копии документов", "category": 2, "rank": 2}
}
# Общая информация по ресурсам
resource_info = {
    1: (("приобретаемый", "разрабатываемый", "приносящий прибыль"), 2019, 4, 7),
    2: (("обслуживаемый", "приносящий прибыль"), 2021, 2, 2),
    3: (("обслуживаемый",), 2018, 5, 5),
    4: (("разрабатываемый", "приносящий прибыль"), 2022, 1, 1),
    5: (("приобретаемый", "обслуживаемый"), 2018, 5, 6)
}
# Сведения о новых технологиях
ir_1_info = {
    "Сведения по приобретению ресурса": {
        "Стоимость в год приобретения": 4960.000
    },
    "Сведения по разработке ресурса": {
        "Первый год разработки": 2019,
        "Количество лет разработки": 3,
        "Годы разработки": [2019, 2020, 2021],
        "Количество сотрудников по годам разработки": [2, 3, 3],
        "Зарплата сотрудников": {
            1: [670.000, 540.000, 560.000],
            2: [760.000, 680.000, 580.000],
            3: [550.000, 680.000, None]
        },
        "Отчисления сотрудников": {
            1: [174.200, 140400.0, 145.600],
            2: [197.600, 176800.0, 150.800],
            3: [143.000, 176800.0, None]
        }
    },
    "Сведения по приносимой прибыли": {
        "Приносимая прибыль": 6800.000
    }
}
# Решения совещаний
ir_2_info = {
    "Сведения по обслуживанию ресурса": {
        "Количество сотрудников": [3],
        "Зарплата сотрудников": {
            1: [620.000],
            2: [610.000],
            3: [640.000]
        },
        "Отчисления сотрудников": {
            1: [161.200],
            2: [158.600],
            3: [166.400]
        },
        "Затраты на расходные материалы": [350.000]
    },
    "Сведения по приносимой прибыли": {
        "Приносимая прибыль": 4000.000
    }
}
# Бухгалтерские документы
ir_3_info = {
    "Сведения по обслуживанию ресурса": {
        "Количество сотрудников": [2],
        "Зарплата сотрудников": {
            1: [570.000],
            2: [540.000]
        },
        "Отчисления сотрудников": {
            1: [148.200],
            2: [140.400]
        },
        "Затраты на расходные материалы": [290.000]
    }
}
# Маркетинговые исследования
ir_4_info = {
    "Сведения по разработке ресурса": {
        "Первый год разработки": 2022,
        "Количество лет разработки": [1],
        "Годы разработки": [2022],
        "Количество сотрудников по годам разработки": [3],
        "Зарплата сотрудников": {
            1: [690.000],
            2: [790.000],
            3: [610.000]
        },
        "Отчисления сотрудников": {
            1: [179.400],
            2: [205.400],
            3: [158.600]
        },
        "Затраты на расходные материалы": [200.000]
    },
    "Сведения по приносимой прибыли": {
        "Приносимая прибыль": 18700.000
    }
}
# АСУ бизнес-процессов
ir_5_info = {
    "Сведения по приобретению ресурса": {
        "Стоимость в год приобретения": 1560.000
    },
    "Сведения по обслуживанию ресурса": {
        "Количество сотрудников": [2],
        "Зарплата сотрудников": {
            1: [630.000],
            2: [520.000]
        },
        "Отчисления сотрудников": {
            1: [163.800],
            2: [135.200]
        },
        "Затраты на расходные материалы": [260.000]
    }
}





