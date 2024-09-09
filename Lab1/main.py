from reportlab.lib.pagesizes import elevenSeventeen
from reportlab.pdfgen.textobject import fribidiText

from Lab1.constant import PriceChangeIndex
from constant_example import *
from lab_1 import *


# Идея для строк data, хранить двумерный массив с годами


# По идее, это класс, который будет заниматься расчетом стоимости для ИР 1 категории
# ToDo Вынести отдельно логирование-print информации о выполнении расчетов
# ToDo Придумать правильное заполнение таблицы data для формирование отчета в Exel/PDF формате
# ToDo Придумать матрицу, для хранения информации, полученной после расчета стоимости 1-ой категории для расчета второй


class ResourceInfo:
    def __init__(self, obs_ir, list_ir_info):
        self.obs_ir = obs_ir
        self.ir_info = list_ir_info

    def process_obs_ir(self):

        # Идем по общему словарю с ресурсами
        for number_IR, info_IR in self.obs_ir.items():
            property_IR = info_IR[0]
            first_year = info_IR[1]
            tk = info_IR[2]
            Tk_plan = info_IR[3] if info_IR[3] >= tk else tk
            data_exel = []

            # Проверяем, есть ли информация по ресурсу
            if f'ir_{number_IR}' in list(self.ir_info.keys()):

                if "приобретаемый" in property_IR:
                    data = self.calculateAcquisitionCost(number_IR, first_year, tk, Tk_plan)
                    data_exel = data_exel + data

                if "обслуживаемый" in property_IR:
                    data = self.calculateMaintenanceCost(number_IR)
                    data_exel = data_exel + data

                if "разрабатываемый" in property_IR:
                    data = self.calculateDevelopmentCost(number_IR, tk, Tk_plan, )
                    # print(data)
                    # data_exel = data_exel + data

                if "приносящий прибыль" in property_IR:
                    profit = self.calculateProfitGeneratingCost(number_IR)

    # Расчет приобретаемой части ресурса
    def calculateAcquisitionCost(self, number_IR: int, first_year: int, tk: int, Tk_plan: int):
        """
        По идее должна собирать данные, для расчета и маршрутизировать что ли расчеты +
        формировать правильные массивы, приведенные для Exel таблицы, а так-же записывать в глобальную переменную класса итоговую стоимость

        :return:
        """

        IR_info = self.ir_info.get(f'ir_{number_IR}', None)

        if IR_info:
            IR_info = IR_info["Сведения по приобретению ресурса"]
            purchase_year_IR_cost = IR_info["Стоимость в год приобретения"]
            buy_cost = calculate_buy_cost_of_kth_resource_at_year_t(purchase_year_IR_cost, first_year, tk, Tk_plan,
                                                                    number_IR)

            # ToDo расчет в какой ячейке относительно года будет располагаться информация
            data = [
                [number_IR, "Стоимость приобретения", purchase_year_IR_cost, "", "", "", ""],
                [number_IR, "Приведенаая стоимость приобретения", "", "", "", "", buy_cost]

            ]
            return data

    # Расчет обсуживаемой части ресурса
    def calculateMaintenanceCost(self, number_IR: int):
        """
        По идее должна собирать данные, для расчета и маршрутизировать что ли расчеты +
        формировать правильные массивы, приведенные для Exel таблицы, а так-же записывать в глобальную переменную класса итоговую стоимость

        :return:
        """

        employee_labor_costs = {}
        IR_info = self.ir_info.get(f'ir_{number_IR}', None)

        if IR_info:
            IR_info = IR_info["Сведения по обслуживанию ресурса"]
            material_costs_total = float(IR_info["Затраты на расходные материалы"][0])

            for key, value in IR_info.items():
                if isinstance(value, dict):
                    for employee, amounts in value.items():
                        employee_id = int(employee)
                        if employee_id not in employee_labor_costs:
                            employee_labor_costs[employee_id] = {}
                        employee_labor_costs[employee_id][key] = float(amounts[0])

            # Расчеты
            total_cost_g_year = calculate_current_IR_maintenance_cost(employee_labor_costs, material_costs_total)

            # Теперь бы надо правильно сформировать данные для Exel таблицы
            print("\n")
            print(f"Расчет стоимости обслуживания ресурса №{number_IR}")
            print("------------------------------------")
            print(f"Стоимость обслуживания: {total_cost_g_year}")
            print("\n")

            data = [number_IR, "Стоимость обслуживания", "", "", "", "", total_cost_g_year]

            return data

        else:
            print("\n")
            print(f"Расчет стоимости обслуживания ресурса №{number_IR}")
            print("------------------------------------")
            print(f"По ресурсу №{number_IR} НЕТ ИНФОРМАЦИИ ")
            print("\n")
            return None

    def calculateDevelopmentCost(self, number_IR: int, tk: int, Tk_plan: int):
        """
        По идее должна собирать данные, для расчета и маршрутизировать что ли расчеты +
        формировать правильные массивы, приведенные для Exel таблицы, а так-же записывать в глобальную переменную класса итоговую стоимость

        :return:
        """

        IR_info = self.ir_info.get(f'ir_{number_IR}', None)

        if IR_info:
            employee_labor_costs = {}
            development_data_by_year = {}
            IR_info = IR_info["Сведения по разработке ресурса"]
            first_year_development = IR_info["Первый год разработки"]
            list_years_development = IR_info["Годы разработки"]
            staff_wages = IR_info["Зарплата сотрудников"]
            staff_contributions = IR_info["Отчисления сотрудников"]
            material_expenses = IR_info["Затраты на расходные материалы"]

            # Идем по годам разработки
            for index_year in range(len(list_years_development)):

                # Считаем базовую стоимость
                # ToDo Вывести в отдельную функцию
                for index_staff, wage in staff_wages.items():
                    if wage[index_year]:
                        employee_labor_costs[index_staff] = {"Зарплата сотрудников": wage[index_year]}
                for index_staff, contributions in staff_contributions.items():
                    if contributions[index_year]:
                        employee_labor_costs[index_staff].update({"Отчисления сотрудников": contributions[index_year]})

                material_costs_total = material_expenses[index_year]
                base_development_cost_k_g = calculate_base_development_IR_cost(employee_labor_costs,
                                                                               material_costs_total)

                # ToDo Вынести в отдельную функцию
                # Считаем накопленную стоимость
                if list_years_development[index_year] == first_year_development:
                    development_data_by_year[first_year_development] = {"Базовая стоимость": base_development_cost_k_g,
                                                                        "Накопительная стоимость": base_development_cost_k_g}
                else:
                    year = list_years_development[index_year - 1]
                    base_development_cost_k_g = base_development_cost_k_g
                    accumulated_IR_cost = calculate_accumulated_IR_cost(
                        development_data_by_year[year]["Накопительная стоимость"], base_development_cost_k_g, year,
                        number_IR)

                    development_data_by_year[year + 1] = {"Базовая стоимость": base_development_cost_k_g,
                                                          "Накопительная стоимость": accumulated_IR_cost}

            # Косяк в том, что года могут быть разные и я неправильно формирую data
            data = []

            print("\n")
            print(f"Расчет стоимость разработки {number_IR}-го ресурса")
            print("--------------------")
            for year, data in development_data_by_year.items():
                print(year,
                      f"Базовая стоимость: {data['Базовая стоимость']}, Накопительная стоимость: {data['Накопительная стоимость']}")
            print("\n")

            # В каком году закончили разрабатывать и начали эксплуатировать
            last_year = list(development_data_by_year.keys())[-1]
            purchase_year_IR_cost = development_data_by_year[last_year]["Накопительная стоимость"]
            development_cost = discounted_IR_cost_to_l_year(purchase_year_IR_cost, tk, last_year, Tk_plan, number_IR)

            return data

    def calculateProfitGeneratingCost(self, number_IR):
        """
        Все прост, найти по номеру ресурса прибыль
        :param number_IR:
        :return:
        """
        IR_info = self.ir_info.get(f'ir_{number_IR}', None)
        if IR_info:
            IR_info = IR_info["Сведения по приносимой прибыли"]
            generated_profit = IR_info["Приносимая прибыль"]
            print("\n")
            print(f"Расчет приносимой прибыли {number_IR}-го ресурса")
            print("----------------------------------------------------")
            print(f"Приносимая прибыль: {generated_profit}")
            print("\n")
            return generated_profit

    #
    # def calculateTotalCost():


list_ir = {"ir_1": ir_1_info, "ir_2": ir_2_info, "ir_3": ir_3_info, "ir_4": ir_4_info, "ir_5": ir_5_info}
res_inf = ResourceInfo(resource_info, list_ir)
res_inf.process_obs_ir()
