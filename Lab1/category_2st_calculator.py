from __future__ import annotations

from itertools import product

from scipy.constants import value

from formula_script import *


class ResourceInfo2stCategory:
    def __init__(self, cost_IR_1st_category: dict[int:float], data_dictionary_constant: dict[int:dict[str:str|int|float]]):
        for number_IR, info_IR  in data_dictionary_constant.items():
            if number_IR in cost_IR_1st_category.keys():
                info_IR.update({"cost": cost_IR_1st_category[number_IR]})

        self.average_IR_cost_data = {}
        self.d_EK_table = []
        self.cost_IR_levels = {}

        # 1 этап. Построение вектора рангов ИР 1-й и 2-й категорий.
        # 2 этап. Группировка оценок ресурсов 1-й категории таким образом, чтобы в каждой группе были ресурсы с одинаковым значением ранга.
        data_list = list(data_dictionary_constant.items())
        sorted_data_list = sorted(data_list, key=lambda x: (x[1]['category'], -x[1]['rank']))
        self.ir_category_2_data = dict(sorted_data_list)

        # for _, info_IR in self.ir_category_2_data.items():
        #     print(info_IR)




    # 3 этап. Вычисление средней стоимости ресурсов с одним и тем же рангом
    def stage_3st(self):
        """
        Функция занимается обработкой информации, для расчета средней стоимости ИР.
        Наполняет словарь self.average_IR_cost_data

        :return:

        """
        grouped_costs = {}


        category_1st_IR = [item for index_IR,item in self.ir_category_2_data.items() if item.get('category') == 1 and 'cost' in item]

        for i in category_1st_IR:
            rank = i["rank"]
            cost = i["cost"]
            if rank not in grouped_costs:
                grouped_costs[rank] = []
            grouped_costs[rank].append(cost)

        for rank, list_cost in grouped_costs.items():
            cost, output_str = calculate_average_IR_cost(list_cost, rank)
            self.average_IR_cost_data.update({rank: cost})
            self.display_info(output_str)

        # for index_IR, info_IR in self.average_IR_cost_data.items():
        #     print(index_IR, info_IR)

        self.average_IR_cost_data = dict(list(self.average_IR_cost_data.items())[::-1])

    # 4 этап. Проверка выполнения условий ранжирования
    def stage_4st(self):
        """

        :return:
        """
        # На выходе по идее должны получить таблицу. Прим: Неплохо бы писать все в одни pdf, все расчеты смысле

        number_couple = 0
        list_d_Ek = []
        average_IR_cost_list = list(self.average_IR_cost_data.keys())

        # Считаем d_Ek
        for index_key in range(len(average_IR_cost_list)):
            number_couple += 1

            if index_key+1 < len(average_IR_cost_list):
                key = average_IR_cost_list[index_key]
                key_1 = average_IR_cost_list[index_key+1]
                d_EK, output = calculate_d_EK_couple_rank(self.average_IR_cost_data[key], self.average_IR_cost_data[key_1], key, key_1, number_couple)
                list_d_Ek.append(d_EK)
                self.d_EK_table.append({"№ пары": number_couple, "Пара рангов": f"{key}-{key_1}", "d_EK": d_EK, "Сравнение с sE": ""})
                self.display_info(output)

        # Считаем среднее геометрическое списка d_Ek
        mean_d_Ek, output = geometric_mean_d_Ek(list_d_Ek)
        self.d_EK_table.append({"Среднее геометрическое sE": mean_d_Ek})
        self.display_info(output)

        # Заполняем "Сравнение с sE" в self.d_EK_table
        for row in self.d_EK_table:
            if "d_EK" in row.keys():
                if row["d_EK"] >=  mean_d_Ek:
                    row["Сравнение с sE"] = "больше, допустимое"
                else:
                    row["Сравнение с sE"] = "меньше, недопустимое"

    # Проверка условий по 4 Этапу
    def stage_4st_check_conditions(self):
        counter_bad_dEk = 0
        data_d_Ek = []
        for row in self.d_EK_table:

            if "Сравнение с sE" in row and row["Сравнение с sE"] == "меньше, недопустимое":
                data_d_Ek.append(row["d_EK"])
                counter_bad_dEk += 1

        if counter_bad_dEk > 1:
            # Дописать странную проверку 1.15
            if check_rank_domination:
                self.display_info("5 этап. Пропуск. Коррекция рангов не требуется.")
                self.stage_6st()

            else:
                self.stage_5st()
        else:
            self.display_info("5 этап. Пропуск. Коррекция рангов не требуется.")
            self.stage_6st()

    # 5 этап
    def stage_5st(self):
        print("Написать что будет происходить при 5 Этапе!")

    # 6 этап. Всем информационным ресурсам из 2-й категории, имеющим ранг R присвоить значение стоимости равное Er
    def stage_6st(self):
        """
        Всем информационным ресурсам из 2-й категории, имеющим ранг R присвоить значение стоимости равное Er

        :return:
        """

        # Словарь для хранения рангов и соответствующих им стоимостей для category == 1
        rank_cost_map = {}

        # Проходим по всем элементам и заполняем rank_cost_map для category == 1
        for number, item in self.ir_category_2_data.items():
            if item['category'] == 1:
                rank = item['rank']
                cost = item['cost']
                if rank not in rank_cost_map:
                    rank_cost_map[rank] = cost

        # Проходим по всем элементам и добавляем стоимость для category == 2, если ранг совпадает
        for number, item in self.ir_category_2_data.items():
            if item['category'] == 2:
                rank = item['rank']
                if rank in rank_cost_map:
                    item['cost'] = rank_cost_map[rank]

    # 7 Этап
    def stage_7st(self):
        """
        Если во 2-й категории есть ресурсы, отнесённые к рангу,
        который не представлен ни одним ресурсом 1-й категории, то необходимо
        выполнить интерполяцию (экстраполяцию) неизвестных значений по известным.

        Поскольку на прошлом этапе мы присваиваем значения для одинаковых рангов
        из разных категорий, справедливо будет предложить интерполяцию (экстраполяцию)
        неизвестных значений по известным, для всех рангов из 2 категории без cost.

        :return:
        """

        iteration_list = list(self.average_IR_cost_data.keys())
        number_couple = 0
        list_d_Ek = []

        # Нужно получить таблицу расчета ступеней стоимости по известным ИР
        # Неплохо бы эту табличку выводить в Exel
        for i in range(len(iteration_list)):
            key = iteration_list[i]
            cost = self.average_IR_cost_data[key]
            for j in range(i+1, len(iteration_list)):
                number_couple+=1
                key_1 = iteration_list[j]
                cost_1 = self.average_IR_cost_data[key_1]
                d_Ek, output = calculate_d_EK_couple_rank(cost, cost_1, key, key_1, number_couple)
                self.cost_IR_levels.update({"№ пары": number_couple, "Пара рангов": f"{key}-{key_1}", "Величина": d_Ek})
                list_d_Ek.append(d_Ek)

        # Считаем среднее геометрическое списка d_Ek. (1.17)
        mean_d_E, output = geometric_mean_d_Ek(list_d_Ek)
        self.d_EK_table.append({"Среднее геометрическое sE": mean_d_E})
        self.display_info(output)

        # Для ИР с неизвестным cost должны провести determine_er_range()
        # Получаем список number_IR из 2 категории с неопределенным cost
        for number_IR, data_IR in self.ir_category_2_data.items():
            if "cost" not in data_IR:

                # Алгоритм поиска ближайших известных ИР по рангам
                R_rank =data_IR["rank"]
                list_rank = list(self.average_IR_cost_data.keys())


                # Интерполяция
                if list_rank[0] < R_rank < list_rank[-1]:
                    for i in range(len(list_rank) - 1):
                        if list_rank[i] < R_rank < list_rank[i + 1]:
                            R_1 = list_rank[i]
                            R_2 = list_rank[i + 1]
                            E_R1 = self.average_IR_cost_data[R_1]
                            E_R2 = self.average_IR_cost_data[R_2]
                            E_r = calculate_er_interpolation(E_R1, E_R2, mean_d_E, R_rank, R_1, R_2)
                            self.ir_category_2_data[number_IR]["cost"] = E_r
                # Экстраполяция
                else:
                    if R_rank < list_rank[0]:
                        R_border = list_rank[0]
                        Er_border =  self.average_IR_cost_data[R_border]
                        E_r, output = calculate_er_extrapolation(R_rank, R_border, mean_d_E, Er_border )
                        self.ir_category_2_data[number_IR]["cost"] = E_r
                    else:
                        R_border = list_rank[-1]
                        Er_border = self.average_IR_cost_data[R_border]
                        E_r, output = calculate_er_extrapolation(R_rank, R_border, mean_d_E, Er_border)
                        self.ir_category_2_data[number_IR]["cost"] = E_r


    def display_info(self, output):
        print(output)

    def run(self):
        self.stage_3st()
        self.stage_4st()
        self.stage_4st_check_conditions()
        self.stage_7st()

        sorted_data_list = sorted(self.ir_category_2_data.items(), key=lambda x: (x[0]))
        for number_IR, data_IR in sorted_data_list:
            print("number_IR: ", number_IR, "data_IR: ", data_IR )

        return sorted_data_list





