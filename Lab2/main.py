import math
import os
import heapq
from tabnanny import check

import pandas as pd
import numpy as np

from k_means_classifier import KMeansClusterer
from scipy.spatial.distance import cdist


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


def find_closest_elements(mean, number_ugroz_value, element_group, lock_number_ugroz_value):
    # Инициализируем список для хранения ближайших элементов
    closest_elements = []

    # Преобразуем lock_number_ugroz_value в множество для быстрого поиска
    lock_set = set(lock_number_ugroz_value)

    # Проходим по всем элементам в number_ugroz_value
    for item in number_ugroz_value:
        if isinstance(item, dict):
            # Извлекаем ключ и значение из словаря
            key, value = next(iter(item.items()))
            # Проверяем, находится ли ключ в lock_set
            if key in lock_set:
                continue  # Пропускаем элемент, если он в lock_set
            # Вычисляем абсолютную разницу между значением и средним
            diff = abs(value - mean)
            # Добавляем элемент в список ближайших элементов
            heapq.heappush(closest_elements, (diff, key, value))

    # Возвращаем count_element_group ближайших элементов в виде списка словарей
    return [{key: value} for _, key, value in heapq.nsmallest(element_group, closest_elements)]


def select_indices(total_indices, count_group):
    step = (total_indices - 1) // (count_group - 1)
    selected_indices = [i * step for i in range(count_group)]

    return selected_indices


def extract_keys(x):
    if isinstance(x, dict):
        return list(x.keys())[0]
    return x


class SecurityIncidentAnalyzer:
    def __init__(self, variant: int, count_group: int, constant_path="Constant", variant_path="Variant_input"):
        """
            Нумерация таблиц взята из файла с лабораторной. НЕ МЕТОДИЧКИ!

            :param variant: Номер варианта;
            :param count_group: Кол-во групп, на которое хотим разделить выборку;
            :param constant_path: Путь до папки с таблицами:
                ('Уязвимости физического типа',                                             (2.2)
                 'Уязвимости организационного типа',                                        (2.3)
                 'Уязвимости технического типа',                                            (2.4)
                 'Уязвимости программного типа',                                            (2.5)
                 'Уязвимости программно-аппаратного типа',                                  (2.6)
                 'Общая классификация угроз ИБ организации',                                (2.7)

                 'Взаимосвязи угроз ИБ и уязвимостей физического типа',                     (2.8)
                 'Взаимосвязи угроз ИБ и уязвимостей физического и организационного типа',
                 'Взаимосвязи угроз ИБ и уязвимостей организационного типа',
                 'Взаимосвязи угроз ИБ и уязвимостей организационного и технического типа',
                 'Взаимосвязи угроз ИБ и уязвимостей технического типа',
                 'Взаимосвязи угроз ИБ и уязвимостей технического и программного типа',
                 'Взаимосвязи угроз ИБ и уязвимостей программного типа',
                 'Взаимосвязи угроз ИБ и уязвимостей программно-аппаратного типа')

            :param variant_path: Путь до папки с вариантами:
                ('Исходные данные о наличии уязвимостей ИС',                                (2.1)
                'Исходные данные парного сравнения типов уязвимостей')                      (2.16)


        """
        self.matrix_distributed_ugroz = pd.DataFrame()
        self.matrix_groups = {
            "matrix_up_down": pd.DataFrame(),
            "matrix_down_up": pd.DataFrame()
        }
        self.PGA_matrix = pd.DataFrame()
        self.distance_matrix_means = pd.DataFrame()
        self.distance_matrix = pd.DataFrame()
        self.total_score_matrix = pd.DataFrame()
        self.pk_matrix = pd.DataFrame()
        self.matrix_gamma = pd.DataFrame()
        self.pss_matrix = pd.DataFrame()
        self.variant = variant
        self.constant_patch = constant_path
        self.variant_patch = variant_path

        self.count_group = count_group

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
            self.vulnerability_matrix.columns = ['№ Типа', '№ Группы', '1', '2', '3', '4', '5', '6', '7']
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
            self.vulnerability_comparison_matrix.columns = ['Типы', '1', '2', '3', '4', '5', ]
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

    def search_vulnerability(self, number_type: int, code: str):
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
                value = self.vulnerability_comparison_matrix.loc[
                    int(code_comparison_matrix_row) - 1, code_comparison_matrix_column]  # Костыль, code_comparison_matrix_row это не индекс
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
        frequencies_vy = self.total_score_matrix.loc[:, "Относительные частоты ВУ"]
        df = pd.concat([frequencies_vy], axis=1)
        dist_matrix = cdist(df, df, metric='euclidean')
        self.distance_matrix = pd.DataFrame(dist_matrix, index=index, columns=index)

        print("\n")
        print("Матрица расстояний между оценками")
        print(self.distance_matrix)

        # KMeansClusterer().fit(self.distance_matrix)

    def step_2st(self):
        """
        2 шаг. Вычислим средние значения расстояний частот возникновения для каждой пары угроз.
        :return:
        """

        row_means = self.distance_matrix.mean(axis=1)
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

        len_column = len(self.distance_matrix.index.to_list()) + 1
        df = pd.DataFrame(index=self.distance_matrix.index.to_list(), columns=range(len_column))
        for i in range(self.distance_matrix.shape[0]):
            arr = []
            value_distance_matrix_means = self.distance_matrix_means.iat[i, 0]
            for j in range(self.distance_matrix.shape[1]):
                value_distance_matrix = self.distance_matrix.iat[i, j]
                if value_distance_matrix < value_distance_matrix_means:
                    name = self.distance_matrix.columns.to_list()[j]
                    arr.append({name: value_distance_matrix})
            arr = np.pad(arr, (0, len_column - 1 - len(arr)), mode='constant', constant_values=np.nan)
            arr = arr.tolist()
            value_dmm = float(value_distance_matrix_means)
            arr.append(value_dmm)
            arr = np.array(arr)
            df.iloc[i] = arr

        df.columns = [i for i in range(1, 28)] + ["Means"]
        df = df.sort_values(by='Means', ascending=True)
        self.PGA_matrix = df  # Preliminary Group Affiliation Matrix - Предварительная таблица принадлежности к группе

        def extract_keys(x):
            if isinstance(x, dict):
                return list(x.keys())[0]
            return x

        display_df = df.apply(lambda col: col.map(extract_keys))
        display_df = display_df.reset_index(drop=True)
        display_df.drop(columns=['Means'], inplace=True)

        print("\n")
        print("Предварительные привязки по группам угроз")
        print(display_df)

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
        total_indices = len(self.PGA_matrix.index.to_list())
        selected_indices = select_indices(total_indices, self.count_group)
        element_group = math.ceil(total_indices / self.count_group)

        def calculate_matrix_groups(input_matrix, inf, reverse_m=False):
            lock_number_ugroz_value = []
            result_arr = []
            df = input_matrix.reset_index(drop=True)
            df = df.loc[selected_indices]

            for index, row in df.iterrows():
                number_ugroz_value = row.to_list()[:-1]
                mean = row.to_list()[-1]
                # mean = mean / 2  # Д. А. Полянский, что-то говорил про половину расстояния до базового=среднего кажется так
                nearest = find_closest_elements(mean, number_ugroz_value, element_group, lock_number_ugroz_value)
                lock_keys = [list(i.keys())[0] for i in nearest]
                lock_number_ugroz_value += lock_keys
                result_arr.append(nearest)

            df_result = pd.DataFrame(result_arr)

            # В методичке написано с приколами, так что не уверен
            df_result = df_result.iloc[::-1].reset_index(drop=True) if reverse_m == True else df_result

            display_df = df_result.apply(lambda col: col.map(extract_keys))
            print("\n")
            print(inf)
            print(display_df)
            return df_result

        self.matrix_groups = {
            "matrix_up_down": calculate_matrix_groups(self.PGA_matrix, "Проход сверху внз"),
            "matrix_down_up": calculate_matrix_groups(self.PGA_matrix.iloc[::-1], "Проход снизу вверх", reverse_m=True)
        }

    def step_5_6st(self):
        """
        5 шаг. Повторим шаг 4 в обратном порядке перечисления базовых
        угроз, полученных на шаге 3.

        6 шаг. Те угрозы, которые оказались в одних группах, включим в
        итоговые подмножества. Оставшиеся угрозы назовём неоднозначно
        распределяемыми.

        :return:
        """
        print("\n")
        print("По алгоритму из методички")
        df1 = self.matrix_groups["matrix_up_down"].apply(lambda col: col.map(extract_keys))
        df2 = self.matrix_groups["matrix_down_up"].apply(lambda col: col.map(extract_keys))

        def compare_rows(row1, row2):
            # Не уверен, в том, что нужно NaN-ить элементы, в которых встречается меньше 2 одинаковых элементов.(6 шаг в методичке)
            new_row = [x if x in row2.values else np.nan for x in row1.values]
            if np.sum(~np.isnan(new_row)) < 2:
                new_row = [np.nan] * len(new_row)
            return new_row

        result = df1.apply(lambda row: compare_rows(row, df2.loc[row.name]), axis=1)
        df = pd.DataFrame(result.tolist(), index=df1.index, columns=df1.columns)
        self.matrix_distributed_ugroz = df

        print("\n")
        print("Однозначно распределенные угрозы")
        print(df)

    def step_7st(self):
        """
        7 шаг. Проанализируем неоднозначно распределяемые угрозы.
        Для каждой из них найдём минимальное расстояние до любой другой
        угрозы, которая была однозначно распределена и включим их в те же
        подмножества.

        :return:
        """
        min_distance_mapping = {}
        groups = []
        list_distributed_ugroz = self.matrix_distributed_ugroz.stack().replace('NaN', np.nan).dropna().tolist()
        list_not_distributed_ugroz = list(set(self.distance_matrix.columns.to_list()) - set(list_distributed_ugroz))

        print("\n")
        print(f"Однозначно распределенные угрозы: {list_distributed_ugroz}")
        print(f"Неоднозначно распределенные угрозы: {list_not_distributed_ugroz}")

        for index, row in self.matrix_distributed_ugroz.iterrows():
            row = row.replace('NaN', np.nan).dropna().tolist()
            groups.append(row)

        for ambiguous_threat in list_not_distributed_ugroz:
            min_distance = float('inf')
            closest_one_to_one_threat = None

            for one_to_one_threat in list_distributed_ugroz:
                distance = self.distance_matrix.loc[one_to_one_threat, ambiguous_threat]
                if distance < min_distance:
                    min_distance = distance
                    closest_one_to_one_threat = one_to_one_threat
            min_distance_mapping[ambiguous_threat] = closest_one_to_one_threat

        for key, value in min_distance_mapping.items():
            for i in groups:
                if value in i:
                    i.append(key)

        # Теперь надо обращаться куда-то, и получать значения
        for i in groups:
            for j in i:
                index_arr = i.index(j)
                value = self.total_score_matrix.loc[j, "Относительные частоты ВУ"]
                value = round(float(value), 4)
                i[index_arr] = {j: value}

        print("\n")
        for i in groups:
            print(i)


    def classification_witch_k_means(self):
        """
        Делает то же самое разделелние по группам, но с помощью готово ой библиотеки
        :return:
        """

        max_iterations = 100
        kmeans = KMeansClusterer(self.count_group, max_iterations)
        kmeans.fit(self.total_score_matrix, 'Относительные частоты ВУ')
        clusters = kmeans.get_clusters()

        for i in clusters:
            for j in i:
                index_arr = i.index(j)
                value = self.total_score_matrix.loc[j, "Относительные частоты ВУ"]
                value = round(float(value), 4)
                i[index_arr] = {str(j): value}

        print("\n")
        for i in clusters:
            print(i)


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
        self.step_4st()
        self.step_5_6st()
        self.step_7st()

        print("\n")
        print("Анализ относительных частот возникновения угроз ИБ применяя алгоритм ближайших соседей")
        self.classification_witch_k_means()


