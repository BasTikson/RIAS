import os
import pandas as pd
"""
Для вычисления количественного значения Pl ВУ необходимо:
    – определить полное конечное множество уязвимостей, характерных для данной ИС,
    – получить лингвистические экспертные оценки от каждого j-го эксперта,
    – определить причинно-следственные связи между уязвимостями ИС и угрозами ИБ,
    – вычислить значения Plj_ВУ по оценкам каждого j-го эксперта,
    – агрегировать полученные значения Pl(j)_ВУ в общую оценку.
"""


def read_excel_to_dataframe(file_path):
    """
    Читает файл Excel по указанному пути и возвращает датафрейм.

    :param file_path: Путь до файла Excel с расширением .xlsx
    :return: Датафрейм с данными из файла Excel или None в случае ошибки
    """
    if not os.path.exists(file_path):
        print(f"Файл не найден: {file_path}")
        return None

    if os.path.getsize(file_path) == 0:
        print(f"Файл пустой: {file_path}")
        return None

    try:
        df = pd.read_excel(file_path)
        if df.empty:
            print(f"Файл содержит пустой датафрейм: {file_path}")
            return None
        return df
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return None



class SecurityIncidentAnalyzer:
    def __init__(self, variant:int, constant_path="Constant", variant_path="Variant_input"):
        """
            Нумерация таблиц взята из файла с лабораторной. НЕ МЕТОДИЧКИ!

            :param variant: Номер варианта;
            :param constant_path: Путь до папки с таблицами:
                ('Уязвимости физического типа',                                             (2.2)
                 'Уязвимости организационного типа',                                        (2.3)
                 'Уязвимости технического типа',                                            (2.4)
                 'Уязвимости программного типа',                                            (2.5)
                 'Уязвимости программно-аппаратного типа',                                  (2.6)
                 'Общая классификация угроз ИБ организации',                                (2.7)
                 'Взаимосвязи угроз ИБ и уязвимостей физического типа',                     (2.8)
                 'Взаимосвязи угроз ИБ и уязвимостей физического и организационного типа',  (2.9)
                 'Взаимосвязи угроз ИБ и уязвимостей организационного типа',                (2.10)
                 'Взаимосвязи угроз ИБ и уязвимостей организационного и технического типа', (2.11)
                 'Взаимосвязи угроз ИБ и уязвимостей технического типа',                    (2.12)
                 'Взаимосвязи угроз ИБ и уязвимостей технического и программного типа',     (2.13)
                 'Взаимосвязи угроз ИБ и уязвимостей программного типа',                    (2.14)
                 'Взаимосвязи угроз ИБ и уязвимостей программно-аппаратного типа')          (2.15)

            :param variant_path: Путь до папки с вариантами:
                ('Исходные данные о наличии уязвимостей ИС',                                (2.1)
                'Исходные данные парного сравнения типов уязвимостей')                      (2.16)


        """
        self.variant = variant
        self.constant_patch = constant_path
        self.variant_patch = variant_path
        self.vulnerability_comparison_matrix = pd.DataFrame()
        self.vulnerability_matrix = pd.DataFrame()

    def defining_input_table(self):
        """
        Функция собирает входные данные по варианту
        :return:
        """
        path = f"{self.variant_patch}/2.1.xlsx"
        df = read_excel_to_dataframe(path)
        row = df.loc[df['№ варианта'] == int(self.variant)]

        if row.empty is False:
            start_index = row.index[0]
            df_trimmed = df.drop('№ варианта', axis=1)
            self.vulnerability_matrix = df_trimmed.iloc[start_index:start_index + 23]
            self.vulnerability_matrix.columns = ['№ Типа', ' № Группы ', '1', '2', '3', '4', '5', '6','7']
            self.vulnerability_matrix = self.vulnerability_matrix.reset_index(drop=True)


        path = f"{self.variant_patch}/2.16.xlsx"
        df = read_excel_to_dataframe(path)
        row = df.loc[df['№ варианта'] == int(self.variant)]

        if row.empty is False:
            start_index = row.index[0]
            df = df.iloc[start_index:start_index + 6]
            df_trimmed = df.drop('№ варианта', axis=1)
            df_trimmed = df_trimmed.drop([start_index])
            self.vulnerability_comparison_matrix = df_trimmed
            self.vulnerability_comparison_matrix.columns = ['Типы', '1', '2', '3', '4', '5',]
            self.vulnerability_comparison_matrix = self.vulnerability_comparison_matrix.reset_index(drop=True)



        print("\n")
        print("Матрица уязвимостей")
        print(self.vulnerability_matrix.to_markdown(index=False))

        print("\n")
        print("Матрица парного сравнения типов уязвимостей")
        print(self.vulnerability_comparison_matrix.to_markdown(index=False))


    def run(self):
        self.defining_input_table()
