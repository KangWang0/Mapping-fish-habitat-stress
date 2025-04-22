import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import Point
from matplotlib.patches import FancyArrowPatch
from matplotlib.ticker import FuncFormatter

# 设置图形属性
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.size'] = 30  # 设置全局字体大小

# 文件路径
file_path = r"C:\Users\Antonio\Desktop\desk\论文\对季节性吞吐型湖泊的水温变化研究\论文图片\Iestyn\Chanodichthys mongolicus.csv"

# 读取文件
data = pd.read_csv(file_path)

# 转换为GeoDataFrame
gdf_data = gpd.GeoDataFrame(data, geometry=[Point(xy) for xy in zip(data.X, data.Y)])

# 确保数据有一个明确的Y坐标列
gdf_data['Y'] = gdf_data.geometry.y

# 排序，确保数据按照Y值排序
gdf_data = gdf_data.sort_values('Y').reset_index(drop=True)

# 创建一个等距的分组标签，每500个点一组
num_points = 1000
group_labels = np.arange(len(gdf_data)) // num_points

# 按这些分组标签计算每组的均值
grouped = gdf_data.groupby(group_labels)['Emergence days'].mean().reset_index(drop=True)

# 创建一个新的DataFrame，包含每100个点的Y坐标均值和对应的Emergence days均值
# 这里Y坐标的均值用于绘图的Y轴
average_Y = gdf_data.groupby(group_labels)['Y'].mean().reset_index(drop=True)
result = pd.DataFrame({'Average Emergence Days': grouped, 'Average Y': average_Y})

# 绘制折线图，调换x轴和y轴
plt.figure(figsize=(4, 4))
plt.plot(result['Average Emergence Days'] / 3, result['Average Y'], marker='o', linestyle='-', color='black', linewidth=2, markerfacecolor='black', markeredgecolor='black', markersize=5, markeredgewidth=1)

# 设置X轴范围和间距
# plt.xticks(np.arange(50, 171, 30))
# plt.yticks(np.arange(3.14e6, 3.30e6, 0.05e6))

# 设置坐标轴箭头
def add_arrow(ax, position):
    arrow = FancyArrowPatch(position, (0, 1), linestyle='-', color='black', arrowstyle='-|>', mutation_scale=15)
    ax.add_patch(arrow)
# 添加箭头 
ax = plt.gca()
# 添加箭头，确保箭头朝向正确的方向
ax.annotate('', xy=(1, 0), xycoords='axes fraction', xytext=(-0.1, 0),
            textcoords='offset points', arrowprops=dict(arrowstyle="->", lw=1))
ax.annotate('', xy=(0, 1), xycoords='axes fraction', xytext=(0, -0.1),
            textcoords='offset points', arrowprops=dict(arrowstyle="->", lw=1))

# 移除刻度线
ax.tick_params(which='both',  # 应用到主刻度和副刻度
               bottom=False,  # 移除底部刻度线
               top=False,     # 移除顶部刻度线
               left=False,    # 移除左侧刻度线
               right=False)   # 移除右侧刻度线

# 定制y轴标签格式以仅显示数字部分
def format_func(value, _):
    return r'${:.2f}$'.format(value / 1e6)  # 仅格式化数字部分

ax = plt.gca()

# 移除y轴刻度值标签
ax.set_yticklabels([])


# # 在y轴顶端添加*10^6的文字标签
# ax.annotate(r'$\times10^6$', xy=(0.04, 0.92), xycoords='axes fraction',
#             xytext=(-20, 20), textcoords='offset points',
#             ha='right', va='bottom')
# 在x轴末端添加days的文字标签
ax.annotate(r'(days)', xy=(0.4, 0), xycoords='axes fraction',
            xytext=(0, 10), textcoords='offset points',
            ha='right', va='bottom')

# # 设置Y轴刻度范围
# plt.yticks(np.arange(plt.ylim()[0], plt.ylim()[1], 0.04e6))

plt.ylabel('Lat (m)')  # 注意这里的标签也要交换
# plt.xlabel('Average Emergence Days')
# 移除上侧和右侧的坐标轴
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)

# 指定保存路径和文件名
save_path = r"C:\Users\Antonio\Desktop\desk\论文\对季节性吞吐型湖泊的水温变化研究\论文图片\Iestyn\average_emergence_days_Chanodichthys mongolicus.pdf"
save_path1 = r"C:\Users\Antonio\Desktop\desk\论文\对季节性吞吐型湖泊的水温变化研究\论文图片\Iestyn\average_emergence_days_Chanodichthys mongolicus.svg"

# 保存图形
plt.savefig(save_path, dpi=600, format='pdf', bbox_inches='tight')
plt.savefig(save_path1, dpi=600, format='svg', bbox_inches='tight')

# 显示图形
plt.show()
