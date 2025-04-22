# -*- coding: utf-8 -*-
"""
Created on Sat Mar 23 11:04:15 2024

@author: Antonio
"""

import mikeio
import pandas as pd

# 定义鱼类的适宜水温区间
fish_optimal_temp = {
    'Hemiculter bleekeri': (26, 30),
    'Hypophthalmichthys molitrix': (25, 30),
    'Coilia brachygnathus': (20, 28),
    'Ctenopharyngodon idella': (20, 28),
    'Carassius auratus': (20, 30),
    'Chanodichthys mongolicus': (12, 18),
    'Megalobrama amblycephala': (20, 29),
    'Chanodichthys dabryi': (18, 27),
    'Parabramis pekinensis': (18, 24),
    'Tachysurus fulvidraco': (25, 30),
    'Culter alburnus': (18, 25),
    'Cyprinus carpio': (18, 28),
}

# 定义DFSU文件路径
dfsu_file_path = r"C:\Users\Antonio\Desktop\desk\poyang_lake\Temperature 20230303\Comprehensive_model.m21fm - Result Files\wet area.dfsu"

# 创建DFSU对象
dfsu = mikeio.Dfsu(dfsu_file_path)

# 读取DFSU文件中的"Temperature"数据
temperature_data = dfsu.read(items='Temperature')

# 获取元素的面积
element_areas = dfsu.get_element_area()

# 初始化结果字典
results = {fish: [] for fish in fish_optimal_temp}
results['Date'] = []

# 对于每个时间步
for timestep, time in enumerate(temperature_data.time):
    # 记录日期
    results['Date'].append(time.strftime('%Y-%m-%d'))
    water_temp_values = temperature_data[0][timestep].values
    
    # 对于每种鱼
    for fish, temp_range in fish_optimal_temp.items():
        # 确定水温落在适宜范围内的元素
        suitable_mask = (water_temp_values >= temp_range[0]) & (water_temp_values <= temp_range[1])
        
        # 计算适宜的水面面积，并转换为平方千米
        suitable_area_km2 = element_areas[suitable_mask].sum() / 1_000_000
        
        # 记录结果
        results[fish].append(suitable_area_km2)

# 转换结果为DataFrame
results_df = pd.DataFrame(results)

# 导出数据到Excel文件
output_excel_path = r"C:\Users\Antonio\Desktop\desk\poyang_lake\Temperature 20230303\fish_suitable_areas.xlsx"
results_df.to_excel(output_excel_path, index=False)

print("The suitable area calculation is complete. The data has been saved to:", output_excel_path)
