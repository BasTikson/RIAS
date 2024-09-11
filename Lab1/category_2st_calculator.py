from __future__ import annotations

from itertools import product

from formula_script import *


class ResourceInfo2stCategory:
    def __init__(self, cost_IR_1st_category: dict[int:float], data_dictionary_constant: dict[int:dict[str:str|int|float]]):
        for number_IR, info_IR  in data_dictionary_constant.items():
            if number_IR in cost_IR_1st_category.keys():
                info_IR.update({"cost": cost_IR_1st_category[number_IR]})

        self.average_IR_cost_data = {}
        self.d_EK_table = []

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
            # self.display_info(output_str)

        # for index_IR, info_IR in self.average_IR_cost_data.items():
        #     print(index_IR, info_IR)

        self.average_IR_cost_data = dict(list(self.average_IR_cost_data.items())[::-1])
        print("self.average_IR_cost_data: ", self.average_IR_cost_data)




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
                d_EK, output = calculate_d_EK_couple_rank(self.average_IR_cost_data[key], self.average_IR_cost_data[key_1], f"{key}-{key_1}", number_couple)
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

        for i in self.d_EK_table:
            print(i)

















    def display_info(self, output):
        print(output)

    def run(self):
        self.stage_3st()
        self.stage_4st()


