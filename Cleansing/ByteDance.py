import pandas as pd

# 读取原始数据
df = pd.read_csv('bytedance_jobs.csv')  # 请确保使用正确的文件路径

# 选择需要的列
columns_to_keep = ['title', 'description', 'requirement', 'job_category', 'city_info']
df_filtered = df[columns_to_keep]

# 导出为新的 CSV 文件
df_filtered.to_csv('filtered_data.csv', index=False)
