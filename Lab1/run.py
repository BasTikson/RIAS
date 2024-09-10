from resource_cost_calculator import ResourceInfo
from drawTable import ExcelGenerator

from data_samples.constant_5 import *

years_list = list(price_change_indices.keys())
years_list.append(years_list[-1] + 1)



# Считаем стоимость ИР 1 категории
list_ir = {"ir_1": ir_1_info, "ir_2": ir_2_info, "ir_3": ir_3_info, "ir_4": ir_4_info, "ir_5": ir_5_info}
res_inf = ResourceInfo(resource_info, list_ir)
res_inf.process_obs_ir()
exel_data = res_inf.data_exel

generator = ExcelGenerator(data_dictionary, years_list, exel_data)
generator.run()
