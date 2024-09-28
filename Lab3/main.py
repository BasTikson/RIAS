from const_2 import data_variant, data_const, map_fuzzy_set
# 1. Вычислить дополнения нечётких множеств A и B, и соответственно кардинальные числа этих дополнений.
# 2. Вычислить пересечения нечётких множеств A и B (двумя способами) и соответственно кардинальные числа этих пересечений.
# 3. Сравнить кардинальные числа по п.2 и объяснить их различия.
# 4. Вычислить объединения нечётких множеств A и B (двумя способами) и соответственно кардинальные числа этих объединений.
# 5. Сравнить кардинальные числа по п.4 и объяснить их различия.
# 6. Построить отображение нечёткого множества A в универсальном множестве Y согласно функции f(x) и вычислить
#    кардинальное число полученного нечёткого множества.
# 7. Вычислить меры энтропии нечётких множеств A и B (аксиоматически и метрически для расстояний Хэмминга и Евклида).
# 8. Сравнить меры энтропии по п.7 и объяснить их различия.
# 9. Вычислить функции доверия нечётким множествам A и B (для расстояний Хэмминга и Евклида).
# 10. Сравнить функции доверия по п.9 и объяснить их различия.


import math

class FuzzySetOperations:
    def __init__(self, membership_function_a, membership_function_b):
        self.membership_function_a = membership_function_a
        self.membership_function_b = membership_function_b

    def calculate_cardinal_numbers(self, fuzzy_set):
        """
        Вычисляет кардинальные числа дополнений.
        :param fuzzy_set:
        :return:
        """
        sum_values = sum(fuzzy_set)
        cardinal_complement_numbers = [round(sum_values, 2)] * len(fuzzy_set)
        return cardinal_complement_numbers

    def calculate_complement_fuzzy_set(self, fuzzy_set):
        return [round(1 - value, 2) for value in fuzzy_set]

    def calculate_intersection_fuzzy_set_1(self, fuzzy_set_a, fuzzy_set_b):
        return [min(a, b) for a, b in zip(fuzzy_set_a, fuzzy_set_b)]

    def calculate_intersection_fuzzy_set_2(self, fuzzy_set_a, fuzzy_set_b):
        return [round(a * b, 3) for a, b in zip(fuzzy_set_a, fuzzy_set_b)]

    def calculate_union_fuzzy_set_1(self, fuzzy_set_a, fuzzy_set_b):
        return [max(a, b) for a, b in zip(fuzzy_set_a, fuzzy_set_b)]

    def calculate_union_fuzzy_set_2(self, fuzzy_set_a, fuzzy_set_b):
        return [round(a + b, 3) if (a + b) < 1 else 1 for a, b in zip(fuzzy_set_a, fuzzy_set_b)]

    def calculate_unblurred_set(self, fuzzy_set):
        return [1 if value > 0.5 else 0 for value in fuzzy_set]

    def calculate_entropy_measure_log(self, fuzzy_set):
        s = [
            -value * math.log(value) - (1 - value) * math.log(1 - value)
            if value != 1 and value != 0 else 0
            for value in fuzzy_set
        ]
        return round(sum(s) / 16, 4)

    def calculate_entropy_measure_ham(self, fuzzy_set, unblurred_set):
        result = sum(abs(a - b) for a, b in zip(fuzzy_set, unblurred_set))
        return (2 / 16) * result

    def calculate_entropy_measure_evk(self, fuzzy_set):
        some_list = [(1 - abs(2 * value - 1)) ** 2 for value in fuzzy_set]
        return (sum(some_list) ** 0.5) / 4

    def calculate_average_fuzzy_set(self, fuzzy_set):
        return sum(fuzzy_set) / len(fuzzy_set)

    def calculate_trust_function_ham(self, fuzzy_set):
        average = self.calculate_average_fuzzy_set(fuzzy_set)
        result = sum(abs(value - average) for value in fuzzy_set)
        return 1 - (2 / 16) * result

    def calculate_trust_function_evk(self, fuzzy_set):
        average = self.calculate_average_fuzzy_set(fuzzy_set)
        some_list = [(value - average) ** 2 for value in fuzzy_set]
        return 1 - (2 / 4) * (sum(some_list) ** 0.5)

    def calculate_something(self):
        # Где-то неправильно считатет, массив считал сам
        # X = list(range(1, 17))
        # Y = list(range(2, 18))
        # A = data_variant["A"]
        # result = map_fuzzy_set(X, Y, A)
        result = [0.0, 0.22, 0.0, 0.0, 0.32, 0.0, 0.0, 0.45, 0.0, 0.0, 0.49, 0.0, 0.0, 0.62, 0.0, 0.0, 0.71]




        return result

    def run_operations(self):
        print('Вычислить дополнения нечётких множеств A и B , и соответственно кардинальные числа этих дополнений.')
        complement_a = self.calculate_complement_fuzzy_set(self.membership_function_a)
        complement_b = self.calculate_complement_fuzzy_set(self.membership_function_b)
        print('Дополнения A:', complement_a)
        print('Дополнения B:', complement_b)
        print('Кардинальные числа дополнения А:', self.calculate_cardinal_numbers(complement_a)[0])
        print('Кардинальные числа дополнения B:', self.calculate_cardinal_numbers(complement_b)[0])
        print()

        print('Вычислить пересечения нечётких множеств A и B (двумя способами), и соответственно кардинальные числа этих пересечений.')
        intersection_1 = self.calculate_intersection_fuzzy_set_1(self.membership_function_a, self.membership_function_b)
        intersection_2 = self.calculate_intersection_fuzzy_set_2(self.membership_function_a, self.membership_function_b)
        print('Пересечение 1:', intersection_1)
        print('Пересечение 2:', intersection_2)
        print('Кардинальные числа пересечения 1:', self.calculate_cardinal_numbers(intersection_1)[0])
        print('Кардинальные числа пересечения 2:', self.calculate_cardinal_numbers(intersection_2)[0])
        print()

        print('Вычислить объединения нечётких множеств A и B (двумя способами) и соответственно кардинальные числа этих объединений.')
        union_1 = self.calculate_union_fuzzy_set_1(self.membership_function_a, self.membership_function_b)
        union_2 = self.calculate_union_fuzzy_set_2(self.membership_function_a, self.membership_function_b)
        print('Объединение 1:', union_1)
        print('Объединение 2:', union_2)
        print('Кардинальные числа объединений 1:', self.calculate_cardinal_numbers(union_1)[0])
        print('Кардинальные числа объединений 2:', self.calculate_cardinal_numbers(union_2)[0])
        print()

        print('Построить отображение нечёткого множества A в универсальном множестве Y согласно функции f(x) и вычислить кардинальное число полученного нечёткого множества.')
        y_set = self.calculate_something()
        print('Y:', y_set)
        print('Кардинальное число полученного множества:', self.calculate_cardinal_numbers(y_set)[0])
        print()

        print("Вычислить меры энтропии нечётких множеств A и B (аксиоматически и метрически для расстояний Хэмминга и Евклида).")
        unblurred_a = self.calculate_unblurred_set(self.membership_function_a)
        unblurred_b = self.calculate_unblurred_set(self.membership_function_b)
        print('Нечеткое множество A:', self.membership_function_a)
        print('Неразмытое множество A_:', unblurred_a)
        print('d(A)лог: ', self.calculate_entropy_measure_log(self.membership_function_a))
        print('d(A)хэм:', self.calculate_entropy_measure_ham(self.membership_function_a, unblurred_a))
        print('d(A)евкл:', self.calculate_entropy_measure_evk(self.membership_function_a))
        print('Нечеткое множество B:', self.membership_function_b)
        print('Неразмытое множество B_:', unblurred_b)
        print('d(B)лог: ', self.calculate_entropy_measure_log(self.membership_function_b))
        print('d(B)хэм:', self.calculate_entropy_measure_ham(self.membership_function_b, unblurred_b))
        print('d(B)евкл:', self.calculate_entropy_measure_evk(self.membership_function_b))
        print()

        print("Вычислить функции доверия нечётким множествам A и B (для расстояний Хэмминга и Евклида).")
        print('Нечеткое множество A:', self.membership_function_a)
        print('d(A)хэм:', self.calculate_trust_function_ham(self.membership_function_a))
        print('d(A)евкл:', self.calculate_trust_function_evk(self.membership_function_a))
        print('Нечеткое множество B:', self.membership_function_b)
        print('d(B)хэм:', self.calculate_trust_function_ham(self.membership_function_b))
        print('d(B)евкл:', self.calculate_trust_function_evk(self.membership_function_b))

if __name__ == '__main__':
    fuzzy_operations = FuzzySetOperations(data_variant["A"], data_variant["B"])
    fuzzy_operations.run_operations()
