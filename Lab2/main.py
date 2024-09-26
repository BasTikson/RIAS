import os
from time import perf_counter

import pandas as pd
import numpy as np
from scipy.spatial.distance import cdist, pdist, squareform


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

        self.distance_matrix_means = pd.DataFrame()
        self.distance_matrix = pd.DataFrame()
        self.total_score_matrix = pd.DataFrame()
        self.pk_matrix = pd.DataFrame()
        self.matrix_gamma = pd.DataFrame()
        self.pss_matrix = pd.DataFrame()
        self.variant = variant
        self.constant_patch = constant_path
        self.variant_patch = variant_path

        # df с исходными данными для вариантов
        self.vulnerability_matrix = pd.DataFrame()
        self.vulnerability_comparison_matrix = pd.DataFrame()

        # словарь с df уязвимостей
        self.vulnerability_tables = {}

        # Список с уязвимостями, характерными варианту
        self.list_vulnerability_by_variant = []

        self.defining_input_constant_vulnerability_table()
        self.defining_input_table()

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
            self.vulnerability_matrix.columns = ['№ Типа', '№ Группы', '1', '2', '3', '4', '5', '6','7']
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

    def defining_input_constant_vulnerability_table(self):
        """
        Функция инициализирует df уязвимостей. При этом оставляет только нужный контекст от таблиц.
        'Уязвимости физического типа'               (2.2)
        'Уязвимости организационного типа'          (2.3)
        'Уязвимости технического типа'              (2.4)
        'Уязвимости программного типа'              (2.5)
        'Уязвимости программно-аппаратного типа'    (2.6)
        :return:
        """

        id_type_name_table = {
            1: ["2.2.xlsx", "Уязвимости физического типа"],
            2: ["2.3.xlsx", "Уязвимости организационного типа"],
            3: ["2.4.xlsx", "Уязвимости технического типа"],
            4: ["2.5.xlsx", "Уязвимости программного типа"],
            5: ["2.6.xlsx", "Уязвимости программно-аппаратного типа"],
        }
        list_columns_to_drop = ["№ группы", "Наименование группы"]

        for id_table, name_table in id_type_name_table.items():
            path = f"{self.constant_patch}/{name_table[0]}"
            df = read_excel_to_dataframe(path)
            check_columns_to_drop = all(column in df.columns for column in list_columns_to_drop)
            if check_columns_to_drop:
                df_trimmed = df.drop(list_columns_to_drop, axis=1)
                df_cleaned = df_trimmed.dropna()
                df = df_cleaned.reset_index(drop=True)

                print("\n")
                print(name_table[1])
                print(df.to_markdown(index=False))
                self.vulnerability_tables[id_table] = df

    def defining_input_constant_threat_IS_table(self):
        """
        Функция инициализирует df угроз ИБ. При этом оставляет только нужный контекст от таблиц.

        'Взаимосвязи угроз ИБ и уязвимостей физического типа',                     (2.8)
        'Взаимосвязи угроз ИБ и уязвимостей физического и организационного типа',
        'Взаимосвязи угроз ИБ и уязвимостей организационного типа',
        'Взаимосвязи угроз ИБ и уязвимостей организационного и технического типа',
        'Взаимосвязи угроз ИБ и уязвимостей технического типа',
        'Взаимосвязи угроз ИБ и уязвимостей технического и программного типа',
        'Взаимосвязи угроз ИБ и уязвимостей программного типа',
        'Взаимосвязи угроз ИБ и уязвимостей программно-аппаратного типа'

        :return:
        """

        path = f"{self.constant_patch}/2.8.xlsx"
        df = read_excel_to_dataframe(path)
        columns_df = set(df.columns.to_list())
        arr = set([i["code_vulnerability"] for i in self.list_vulnerability_by_variant])
        columns_to_drop = list(columns_df - arr)
        columns_to_drop.remove("№ Угрозы")
        self.pss_matrix = df.drop(columns_to_drop, axis=1)

        for i in range(self.pss_matrix.shape[0]):
            for j in range(self.pss_matrix.shape[1]):
                if self.pss_matrix.iat[i, j] == '+':
                    self.pss_matrix.iat[i, j] = 1
                elif pd.isna(self.pss_matrix.iat[i, j]):
                    self.pss_matrix.iat[i, j] = 0

        print("\n")
        print("Матрица угроз ИБ, характерная для варианта")
        print(self.pss_matrix)

    def transform_to_inverse_symmetric(self):
        """
        Во-первых, необходимо преобразовать матрицу парных сравнений всех уязвимостей
        (которые приводятся в таблице 2.16 по вариантам)
        из противоположно симметричной в обратно симметричную.(2.23)
        :return:
        """
        self.vulnerability_comparison_matrix = self.vulnerability_comparison_matrix.map(lambda x: float(x))
        for i in range(self.vulnerability_comparison_matrix.shape[0]):
            for j in range(1, self.vulnerability_comparison_matrix.shape[1]):
                value_i_J = self.vulnerability_comparison_matrix.iat[i, j]
                if value_i_J > 0:
                    value_i_J = value_i_J + 1
                else:
                    value_i_J = 1 / (1 - value_i_J)
                self.vulnerability_comparison_matrix.iat[i, j] = float(round(value_i_J, 3))



        print("\n")
        print("Матрица парных сравнений, преобразованная по формуле 2.23, в обратно симметричную")
        print(self.vulnerability_comparison_matrix.to_markdown(index=False))

    def search_vulnerability(self, number_type: int, code:str ):
        """
        Функция, которая по заданным параметрам ищет название уязвимости в
        vulnerability_tables - словарь с df уязвимостей
        :return:
        """

        df = self.vulnerability_tables[number_type]

        for _, row in df.iterrows():
            if row["№ уязвимости"] == code:
                return row["Наименование уязвимости"]

    def scan_for_vulnerabilities(self):
        """
        Функция анализирует матрицу vulnerability_matrix и определяет уязвимости, характерные, для переданного варианта.

        :return:
        """

        number_type = 0

        for index_df, row in self.vulnerability_matrix.iterrows():
            if str(row["№ Типа"]) != "nan":
                number_type = int(row["№ Типа"])
            number_group = row["№ Группы"]
            list_number_vulnerability = row[2:].to_dict()
            for index_dict, value_dict in list_number_vulnerability.items():
                if value_dict == "+":
                    code = f"{number_group}.{index_dict}"
                    name_vulnerability = self.search_vulnerability(number_type, code)
                    self.list_vulnerability_by_variant.append(
                        {
                            "number_type": number_type,
                            "number_group": number_group,
                            "code_vulnerability": code,
                            "name_vulnerability": name_vulnerability
                        }
                    )

    def calculate_gamma_matrix(self):
        """
        Функция создает матрицу гамма.
        :return:
        """
        arr = [i["code_vulnerability"] for i in self.list_vulnerability_by_variant]
        df = pd.DataFrame(index=arr, columns=arr)
        df_columns = df.columns.to_list()

        for index, row in df.iterrows():
            code_row = str(index)
            code_comparison_matrix_row = code_row.split(".")[0]

            for imdex_column in range(len(row)):
                code_column = str(df_columns[imdex_column])
                code_comparison_matrix_column = code_column.split(".")[0]
                value = self.vulnerability_comparison_matrix.loc[int(code_comparison_matrix_row) - 1, code_comparison_matrix_column] # Костыль, code_comparison_matrix_row это не индекс
                df.loc[index, code_column] = value
        self.matrix_gamma = df
        print("\n")
        print("Масштабированная матрица парных сравнений")
        print(df)

    def calculate_pk_matrix(self):
        """
        Функция, для получения матрицы показателей критичности уязвимостей. М_пк.(2.31)
        :return:
        """
        index = self.pss_matrix.loc[:, "№ Угрозы"]
        new_index = index.to_list()
        pss_matrix = self.pss_matrix.drop(["№ Угрозы"], axis=1)
        result = pss_matrix.dot(self.matrix_gamma)
        self.pk_matrix = pd.DataFrame(result, columns=self.matrix_gamma.columns)
        self.pk_matrix.index = new_index

        print("\n")
        print("Матрица показателей критичности уязвимости")
        print(self.pk_matrix)

    def calculate_total_score_matrix(self):
        """
        Функция вычисляет интегральный показатель влияния всех уязвимостей на частоту возникновения l-й угрозы:
        :return:
        """
        self.total_score_matrix = self.pk_matrix.sum(axis=1)

        print("\n")
        print("Матрица интегральных показателей")
        print(self.total_score_matrix)

    def calculate_relative_frequencies(self):
        """
        Функция вычисляет относительные частоты возникновения угроз безопасности по
        оценкам j-го эксперта. (2.33)

        :return:
        """

        sum_total_score = self.total_score_matrix.sum()
        arr = []
        self.total_score_matrix = self.total_score_matrix.to_frame()

        for index, row in self.total_score_matrix.iterrows():
            value_tsm = row[0] / sum_total_score
            arr.append(value_tsm)
        self.total_score_matrix[""] = arr
        self.total_score_matrix.columns = ["Интегральный показатель ВУ", "Относительные частоты ВУ"]

        print("\n")
        print("Относительные частоты возникновения угроз безопасности по оценкам j-го эксперта")
        print(self.total_score_matrix)

    # Анализ относительных частот возникновения угроз ИБ
    def step_1st(self):
        """
        1 шаг. Построим матрицу расстояний между оценками.(2.38)
        :return:
        """
        index = self.total_score_matrix.index.to_list()
        frequencies_vy = self.total_score_matrix.loc[: ,"Относительные частоты ВУ"]
        df = pd.concat([frequencies_vy], axis=1)
        dist_matrix = cdist(df, df, metric='euclidean')
        self.distance_matrix = pd.DataFrame(dist_matrix, index=index, columns=index)

        print("\n")
        print("Матрица расстояний между оценками")
        print(self.distance_matrix)

    def step_2st(self):
        """
        2 шаг. Вычислим средние значения расстояний частот возникновения для каждой пары угроз.
        :return:
        """

        row_means= self.distance_matrix.mean(axis=1)
        self.distance_matrix_means = pd.DataFrame(row_means)

        print("\n")
        print("Средние значения расстояний частот возникновения для каждой пары угроз")
        print(self.distance_matrix_means)

    def step_3st(self):
        """
        3 шаг. Сделаем предварительные привязки потенциальных «одногруппников» для каждой угрозы: возьмём те угрозы, расстояния до
        которых будет строго меньше среднего расстояния базовой угрозы в
        группе. Количество таких «одногруппников» может быть любым.
        Кроме того, одни и те же угрозы могут встречаться в разных группах.
        :return:
        """
        len_column = len(self.distance_matrix.index.to_list())
        df = pd.DataFrame(index=self.distance_matrix.index.to_list(), columns=range(len_column))
        for i in range(self.distance_matrix.shape[0]):
            arr = []
            for j in range(self.distance_matrix.shape[1]):
                value_distance_matrix = self.pss_matrix.iat[i, j]
                value_distance_matrix_means = self.distance_matrix_means.iat[i, 0]
                if value_distance_matrix < value_distance_matrix_means:
                    name = self.distance_matrix.columns.to_list()[j]
                    arr.append(name)
            arr = np.pad(arr, (0, len_column - len(arr)), mode='constant',  constant_values=np.nan)
            df.iloc[i] = arr



        df.columns = [i for i in range(1,28)]
        print("\n")
        print("Предварительные привязки по группам угроз")
        print(df)

    def step_4st(self):
        """
        4 шаг. Просмотрим все предварительные группы и выберем из
        них те угрозы, расстояния до которых от базовой угрозы минимальны.
        При этом общее количество угроз в группе не должно превышать заданного значения, приблизительно равного отношению общего числа
        угроз к количеству планируемых групп. Угрозы, которые в процессе
        просмотра уже были включены в какую-то группу, в другие группы не
        включаем. Просмотр сделаем в прямом порядке

        :return:
        """
























    def run(self):
        self.transform_to_inverse_symmetric()
        self.scan_for_vulnerabilities()
        self.calculate_gamma_matrix()
        self.defining_input_constant_threat_IS_table()
        self.calculate_pk_matrix()
        self.calculate_total_score_matrix()
        self.calculate_relative_frequencies()
        print("\n")
        print("Анализ относительных частот возникновения угроз ИБ")
        self.step_1st()
        self.step_2st()
        self.step_3st()

        # print("\n")
        #
        # for i in self.list_vulnerability_by_variant:
        #     print(i)
        # print(len(self.list_vulnerability_by_variant))


