import numpy as np
import pandas as pd


class KMeansClusterer:
    def __init__(self, k, max_iterations=100):
        """
        Инициализация класса KMeansClusterer.

        :param k: Количество кластеров.
        :param max_iterations: Максимальное количество итераций.
        """
        self.k = k
        self.max_iterations = max_iterations
        self.centroids = None
        self.clusters = None

    def fit(self, df, column_name):
        """
        Выполняет кластеризацию данных с использованием алгоритма k-means.

        :param df: DataFrame с данными.
        :param column_name: Название колонки, содержащей данные для кластеризации.
        """
        # Извлекаем данные из DataFrame
        data = df[column_name].values

        # Инициализация центроидов случайным образом
        self.centroids = np.random.choice(data, size=self.k, replace=False)

        for _ in range(self.max_iterations):
            # Кластеризация точек данных
            self.clusters = [[] for _ in range(self.k)]
            for i, point in enumerate(data):
                distances = np.abs(self.centroids - point)
                cluster_index = np.argmin(distances)
                self.clusters[cluster_index].append(df.index[i])

            # Обновление центроидов
            new_centroids = [np.mean([data[df.index.get_indexer([idx])[0]] for idx in cluster]) for cluster in
                             self.clusters]

            # Проверка на сходимость
            if np.all(self.centroids == new_centroids):
                break

            self.centroids = new_centroids

    def get_clusters(self):
        """
        Возвращает массив с массивами групп, где каждый внутренний массив содержит индексы строк DataFrame,
        принадлежащих соответствующему кластеру.

        :return: Массив с массивами групп.
        """
        return self.clusters


