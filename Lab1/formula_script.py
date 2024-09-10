# from constant_example import *
from data_samples.constant_3 import *


def multiply_elements(arr):
    product = 1
    for num in arr:
        product *= num
    return product

# 1) Рассчитать стоимость каждого ИР 1 категории (1.6 - 1.11)
def calculate_cost_of_kth_resource_in_1st_category(buy_cost: float, development_cost: float, service_cost: float, usage_profit: float):
    """
    Вычисляет стоимость k-го ресурса из 1-й категории.(1.5)

        :param buy_cost: Стоимость приобретенного ИР к текущему t-му году;
        :param development_cost: Стоимость разрабатываемого ИР к текущему t-му году, с учетом прошедшего года эксплуатации;
        :param service_cost: Стоимость обслуживания ресурса в течении t-го года;
        :param usage_profit: Прибыль от использования ресурса в течение года;

    :return:
        :cost_1st_category: Стоимость k-го ресурса из 1 категори к t-му году;
    """

    cost_1st_category = buy_cost + development_cost + service_cost + usage_profit
    cost_1st_category = round(cost_1st_category, 2)

    return cost_1st_category

# S_приобретенная
def calculate_buy_cost_of_kth_resource_at_year_t(purchase_year_IR_cost: int, first_year:int, tk:int, Tk_plan: int, k:int):
    """
    Рассчитывает приведённую к t-му году эксплуатации стоимость приобретённого k-го ресурса.(1.6)

        :param purchase_year_IR_cost: Стоимость ИР в год его приобретения;
        :param tk: Текущий год эксплуатации, в смысле по счету (Например: 2-й);
        :param first_year: Первый год эксплуатации;
        :param Tk_plan: Кол-во лет в которых планирует эксплуатировать;

    :return:
        :buy_cost: Приведенная стоимость k-го ресурса к t-му году эксплуатации

    """
    # массив отраслевых индексов изменения цен по прошествии g-го года эксплуатации ИР
    current_year = first_year+tk-1
    planned_year = first_year+Tk_plan-1

    industry_price_index_g_year_arr = [price_change_indices[year] for year in range(first_year, current_year) if year in price_change_indices]
    buy_cost = (purchase_year_IR_cost * multiply_elements(industry_price_index_g_year_arr) * (
                1 - ((tk - 1) / Tk_plan)))
    buy_cost = round(buy_cost, 2)

    output = (
        "\n"
        f"Рассчет стоимости эксплуатации ПРИОБРЕТЕННОГО, {k}-го ресурса \n"
        "---------------------------------------------------------------\n"
        f"Cтоимость {k}-го ИР в год его приобретения: {purchase_year_IR_cost}\n"
        f"Текущий год эксплуатации {k}-го ИР: {current_year}\n"
        f"Массив лет и отраслевых индексов, в которые велась эксплуатация: {[year for year in range(first_year, current_year)]}, {industry_price_index_g_year_arr}\n"
        f"До какого года планируется эксплуатация ИР: {planned_year}\n"
        f"ПРИВЕДЕННАЯ стоимость {k}-го ИР: {buy_cost}\n"
        "\n"
    )

    return buy_cost, output

# S_базовая
def calculate_base_development_IR_cost(employee_labor_costs:dict[int: dict[str: float]], material_costs_total:float):
    """
    Рассчитывает базовую стоимость разработки k-го ИР на g-ом году разработки.(1.7)

        :param employee_labor_costs: {number_employee: {"wages_coast": float, "insurance_contributions": float }}
                                     wages_coast затраты на оплату труда number_employee-го сотрудника, по разработке k-го ИР
                                     insurance_contributions_rate - отчисления в фонды страхования (процент от затрат на оплату труда) в течение g-го года;
        :param material_costs_total: Общие затраты на расходные материалы при разработке k-го ИР в течение g-го года разработки;

    :return:
        :base_development_cost_k_g: Базовая стоимость разработки k-го ИР на g-ом году разработки.

    """

    total_employee_cost = 0
    for i in employee_labor_costs.items():
        total_employee_cost = total_employee_cost + (i[1]["Зарплата сотрудников"] + i[1]["Отчисления сотрудников"])

    base_development_cost_k_g = total_employee_cost + material_costs_total
    base_development_cost_k_g = round(base_development_cost_k_g, 2)
    return base_development_cost_k_g

#S_накопленная
def calculate_accumulated_IR_cost(accumulated_IR_cost_years:float, total_cost_g_year:float, year:int, k):
    """
    Расчет приведенной к t-му году разработки накопленной стоимости разрабатываемого k-го ИР.(1.8 - 1.9)

        :param accumulated_IR_cost_years: Накопительная стоимость разработки, за прошлые годы;
        :param total_cost_g_year: Базовая стоимость разработки за t год;
        :param year: Год, за который необходимо посчитать накопительную стоимость разработки;

    :return:
        :accumulated_IR_k_cost_new: Накопительная стоимость разработки к t году;

    """

    accumulated_IR_cost = (accumulated_IR_cost_years * price_change_indices[year]) + total_cost_g_year
    accumulated_IR_cost = round(accumulated_IR_cost, 2)

    # print("\n")
    # print(f"Рассчет НАКОПИТЕЛЬНОЙ стоимости разработанного ИР, {k}-го ресурса ")
    # print("---------------------------------------------------------------")
    # print(f"Cтоимость {k}-го ИР в год его приобретения: {purchase_year_IR_cost}")
    # print(f"ПРИВЕДЕННАЯ стоимость {k}-го ИР: {buy_cost}")
    # print(f"Текущий год эксплуатации {k}-го ИР: {current_year}")
    # print(
    #     f"Массив лет и отраслевых индексов, в которые велась эксплуатация: {[year for year in range(first_year, current_year)]}, {industry_price_index_g_year_arr}")
    # print(f"До какого года планируется эксплуатация ИР: {planned_year}")
    # print("\n")


    return accumulated_IR_cost

# S_разработанная
def discounted_IR_cost_to_l_year(accumulated_IR_cost: int, tk: int,
                                                 first_year: int, Tk_plan: int, k:int):
    """
    Рассчитывает приведённую к l-му году эксплуатации стоимость разработанного k-го ИР.(1.10)

        :param accumulated_IR_cost: Накопительная стоимость приведенной к t-му году разработки k-го ИР;
        :param current_IR_year: Текущий год эксплуатации;
        :param first_year: Первый год, в который началась вестись эксплуатация;
        :param planned_IR_service_life: Планируемый срок эксплуатации ИР

    :return:
        :buy_cost: Приведенная стоимость разработанного k-го ресурса к l-му году эксплуатации

    """
    current_year = first_year + tk - 1
    planned_year = first_year + Tk_plan - 1
    # массив отраслевых индексов изменения цен по прошествии g-го года эксплуатации разработанных ИР
    industry_price_index_g_year_arr = [price_change_indices[year] for year in range(first_year, current_year) if
                                       year in price_change_indices]


    # массив отраслевых индексов изменения цен по прошествии g-го года эксплуатации разработанных ИР
    buy_cost = (accumulated_IR_cost * multiply_elements(industry_price_index_g_year_arr) * (
                1 - ((tk - 1) / Tk_plan)))
    buy_cost = round(buy_cost, 2)

    # print("\n")
    # print(f"Рассчет стоимости эксплуатации, РАЗРАБОТАННОГО {k}-го ресурса ")
    # print("---------------------------------------------------------------")
    # print(f"Накопительная стоимость приведенной к t-му году разработки {k}-го ИР: {accumulated_IR_cost}")
    # print(f"Текущий год эксплуатации k-го ИР, после разработки: {tk}")
    # print(f"Массив лет и отраслевых индексов, в которые велась разработка: {[year for year in range(first_year, current_year)]}, {industry_price_index_g_year_arr}")
    # print(f"Планируемый срок эксплуатации ИР: {planned_year}")
    # print("\n")

    # print("\n")
    # print(f"Рассчет стоимости эксплуатации РАЗРАБАТЫВАЕМОГО, {k}-го ресурса ")
    # print("---------------------------------------------------------------")
    # print(f"Cтоимость {k}-го ИР в год окончания его разработки: {accumulated_IR_cost}")
    # print(f"ПРИВЕДЕННАЯ стоимость {k}-го ИР: {buy_cost}")
    # print(f"Текущий год эксплуатации {k}-го ИР: {current_year}")
    # print(f"Массив лет и отраслевых индексов, в которые велась эксплуатация: {[year for year in range(first_year, current_year)]}, {industry_price_index_g_year_arr}")
    # print(f"До какого года планируется эксплуатация ИР: {planned_year}")
    # print("\n")

    return buy_cost
#S_обслуживания
def calculate_current_IR_maintenance_cost(employee_labor_costs:dict[int: dict[str: float]], material_costs_total:float, k:int):
    """
    Рассчитывает стоимость обслуживания k-го ИР в текущем году.(1.11)

        :param k: Номер ресурса;
        :param employee_labor_costs: {number_employee: {"wages_coast": float, "insurance_contributions": float}}
                                     wages_coast затраты на оплату труда number_employee-го сотрудника, по обслуживанию k-го ИР
                                     insurance_contributions_rate - отчисления в фонды страхования в течение текущего года;
        :param material_costs_total: Общие затраты на расходные материалы при обслуживании k-го ИР в течение текущего года;

    :return:
        :total_cost_g_year: Общая стоимость обслуживания k-го ИР в текущем году.

    """
    total_employee_cost = 0

    for i in employee_labor_costs.items():
        total_employee_cost = total_employee_cost + (i[1]["Зарплата сотрудников"] + i[1]["Отчисления сотрудников"])

    total_cost_g_year = total_employee_cost + material_costs_total
    total_cost_g_year = round(total_cost_g_year, 2)
    output = (
        "\n"
        f"Расчет стоимости обслуживания ресурса №{k}\n"
        "------------------------------------\n"
        f"Стоимость обслуживания: {total_cost_g_year}\n"
        "\n"
    )
    return total_cost_g_year,output



# 2) Рассчитать стоимость каждого ИР 2 категории (1.12 - 1.22)