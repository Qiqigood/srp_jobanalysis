import re
from pyecharts.charts import Bar
from pyecharts import options as opts
from streamlit_echarts import st_pyecharts
import streamlit as st
import pandas as pd
import jieba
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer
from matplotlib import rcParams

# 设置matplotlib的字体为Microsoft YaHei
rcParams['font.family'] = ['Microsoft YaHei']

def plot_word_frequency(df, column_name="要求"):
    # 确保数据列是字符串类型
    df[column_name] = df[column_name].astype(str)
    # 使用jieba进行中文分词
    df[column_name] = df[column_name].apply(lambda x: " ".join(jieba.cut(x)))
    # 创建CountVectorizer对象
    vectorizer = CountVectorizer(stop_words=None, max_features=1000)  # 不考虑英文停用词，最多1000个特征
    word_matrix = vectorizer.fit_transform(df[column_name])  # 文本转为矩阵
    # 获取单词频率
    word_freq = word_matrix.sum(axis=0).A1
    words = vectorizer.get_feature_names_out()
    # 创建词频的DataFrame
    word_freq_df = pd.DataFrame(list(zip(words, word_freq)), columns=["Word", "Frequency"])
    word_freq_df = word_freq_df.sort_values(by="Frequency", ascending=False)
    # Streamlit界面部分
    st.write("## 词频分析")
    # 动态选择展示的词频数量
    num_words = st.selectbox(
        '选择展示的高频词个数',
        [3, 5, 10, 15, 20]
    )
    # 获取前N个高频词
    top_words = word_freq_df.head(num_words)
    st.write(f"前{num_words}个高频词：")
    st.write(top_words)
    # 绘制柱状图
    plt.figure(figsize=(10, 6))
    plt.bar(top_words['Word'], top_words['Frequency'])
    plt.xticks(rotation=45, ha='right')
    plt.title(f"Top {num_words} 高频词")
    plt.xlabel("词汇")
    plt.ylabel("频率")
    st.pyplot(plt)


def load_show():
    df = pd.read_csv("./data/IT行业数据.csv")
    return df

#清洗薪资数据
def clean_salary(salary_str):
    if not salary_str:
        return None  # 如果薪资为空，返回None

    # 匹配区间格式如6-12K
    salary_range = re.findall(r'(\d+)-(\d+)', salary_str)

    if salary_range:
        # 处理区间数据，取区间的中值作为薪资代表
        low, high = map(int, salary_range[0])
        if 'K' in salary_str:
            return (low + high) / 2 * 1000  # 转换为千元
        else:
            return (low + high) / 2  # 直接按元计算

    # 匹配带有·N薪的格式
    elif '·' in salary_str:
        if 'K' in salary_str:
            # 处理如40-65K·16薪 格式
            base_salary = re.findall(r'(\d+)-(\d+)', salary_str.split('·')[0])
            if base_salary:
                low, high = map(int, base_salary[0])
                monthly_salary = (low + high) / 2 * 1000
                multiplier = int(re.findall(r'(\d+)', salary_str.split('·')[1])[0])  # 提取倍数
                return monthly_salary * multiplier

        elif '元/天' in salary_str:
            # 处理如150-200元/天 格式
            daily_salary_range = re.findall(r'(\d+)-(\d+)', salary_str)
            if daily_salary_range:
                low, high = map(int, daily_salary_range[0])
                avg_daily_salary = (low + high) / 2
                return avg_daily_salary * 30  # 按30天计算月薪

        elif '元/周' in salary_str:
            # 处理如100-1000元/周 格式
            weekly_salary_range = re.findall(r'(\d+)-(\d+)', salary_str)
            if weekly_salary_range:
                low, high = map(int, weekly_salary_range[0])
                avg_weekly_salary = (low + high) / 2
                return avg_weekly_salary * 4  # 假设每月有4个工作周，计算月薪

    elif 'K' in salary_str:
        # 处理单一如30-40K 格式，取区间中值并转为千元
        salary_range = re.findall(r'(\d+)-(\d+)', salary_str)
        if salary_range:
            low, high = map(int, salary_range[0])
            return (low + high) / 2 * 1000  # 转换为千元

    elif '元' in salary_str:
        # 如果没有K，可能是“元”，需要按具体数值计算
        salary_range = re.findall(r'(\d+)-(\d+)', salary_str)
        if salary_range:
            low, high = map(int, salary_range[0])
            return (low + high) / 2  # 直接取区间中值，不乘以千

    # 如果薪资格式不符合预期，返回 NaN
    return None

# 清洗城市数据
def clean_city(city_str):
    # 提取城市部分，去掉·后的内容
    city_name = city_str.split('·')[0]
    return city_name

# 使用.loc修改数据
def clean_data(df):
    # 使用 .loc 确保在 DataFrame 上修改，而不是视图
    df.loc[:, '薪资'] = df['薪资'].apply(clean_salary)
    df.loc[:, '城市'] = df['城市'].apply(clean_city)
    return df

#城市薪资分析图
def plot_city_job_analysis(df):
    clean_data(df)
    # 计算每个城市的岗位数量
    city_job_count = df['城市'].value_counts()
    # 确保薪资列为数值类型（防止出现NaN或非数值数据）
    df.loc[:, '薪资'] = pd.to_numeric(df['薪资'], errors='coerce')  # 确保薪资列为数值型
    # 按城市分组，计算平均薪资
    df_grouped = df.groupby('城市').agg({'薪资': 'mean'}).sort_values(by='薪资', ascending=False)  # 按城市分组，计算平均薪资
    # 排序城市的岗位数量和平均薪资数据
    city_job_count_s = city_job_count.sort_values(ascending=False)  # 排序城市的岗位数量
    mean_sal_city = df_grouped['薪资'].sort_values(ascending=False)  # 排序城市的平均薪资
    mean_sal_city = mean_sal_city.round(0).astype(int)  # 取整，转为整数
    # 创建两个柱状图：一个是城市与薪资，一个是城市与岗位数量
    st.write(df)
    # 1. 城市与平均薪资柱状图
    sal_bar = (
        Bar()
        .add_xaxis(mean_sal_city.index.tolist())  # X轴为城市名称
        .add_yaxis("平均薪资", mean_sal_city.values.tolist())  # Y轴为平均薪资
        .set_global_opts(
            title_opts=opts.TitleOpts(title="城市与平均薪资", subtitle="不同城市的平均薪资"),
            xaxis_opts=opts.AxisOpts(
                name="城市",
                axislabel_opts=opts.LabelOpts(
                    rotate=45,  # 旋转45度，避免中文和英文重叠
                    font_size=12,
                    font_family="Microsoft YaHei"  # 强制使用支持中文的字体
                )
            ),
            toolbox_opts=opts.ToolboxOpts(),
        )
    )

    # 2. 城市与岗位数量柱状图
    job_count_bar = (
        Bar()
        .add_xaxis(city_job_count_s.index.tolist())  # X轴为城市名称
        .add_yaxis("岗位数量", city_job_count_s.values.tolist())  # Y轴为岗位数量
        .set_global_opts(
            title_opts=opts.TitleOpts(title="城市与岗位数量", subtitle="不同城市的岗位数量"),
            xaxis_opts=opts.AxisOpts(
                name="城市",
                axislabel_opts=opts.LabelOpts(
                    rotate=45,  # 旋转45度，避免中文和英文重叠
                    font_size=12,
                    font_family="Microsoft YaHei"  # 强制使用支持中文的字体
                )
            ),
            toolbox_opts=opts.ToolboxOpts(),
        )
    )

    # 显示两张图表
    st_pyecharts(sal_bar)
    st_pyecharts(job_count_bar)

if __name__ == "__main__":
    # 数据清洗：去除可能的空值或者多余空格
    df = load_show()
    # 设置页面标题
    st.title('IT领域招聘岗位分析')
    # 显示数据表格
    st.write(df)

    # 侧边栏
    add_selectbox = st.sidebar.selectbox(
        label="数据分析选择:",
        options=('请选择', '岗位领域分布分析','热门岗位分析')
    )

    # 1. 工作地点柱状图
    if add_selectbox == '岗位领域分布分析':
        df['领域'] = df['领域'].str.strip().dropna()
        # 统计各个领域的岗位数量
        field_job_count = df['领域'].value_counts()

        # 设置页面标题
        st.title('岗位领域统计分析')
        # 让用户选择要显示的领域排名数量
        rank_limit = st.sidebar.selectbox(
            '选择显示的领域排名数量:',
            [3, 5, 10, 15, 20]
        )
        # 根据选择的排名限制，取前 N 个领域
        top_fields = field_job_count.head(rank_limit)
        # 配置X轴样式
        xaxis_opts = opts.AxisOpts(
            name="领域",
            axislabel_opts=opts.LabelOpts(
                rotate=45,  # 旋转45度，避免中文和英文重叠
                font_size=12,  # 设置字体大小
                font_family="Microsoft YaHei"  # 强制使用支持中文的字体
            )
        )

        # 如果选择的排名大于等于15，增加工具栏和修改样式
        if rank_limit >= 10:
            bar = (
                Bar()
                .add_xaxis(top_fields.index.tolist())
                .add_yaxis("岗位数量", top_fields.values.tolist())
                .set_global_opts(
                    title_opts=opts.TitleOpts(title="不同领域的岗位数量"),
                    xaxis_opts=xaxis_opts,  # 设置自定义X轴样式
                    toolbox_opts=opts.ToolboxOpts()  # 增加工具栏
                )
            )
        else:
            bar = (
                Bar()
                .add_xaxis(top_fields.index.tolist())
                .add_yaxis("岗位数量", top_fields.values.tolist())
                .set_global_opts(
                    title_opts=opts.TitleOpts(title="不同领域的岗位数量")
                )
            )

        # 展示图表
        st_pyecharts(bar)

    # 2.热门岗位分析
    if add_selectbox == '热门岗位分析':
        # 筛选出各个领域的数据
        df_computer_software = df[df['领域'] == '计算机软件']
        df_internet = df[df['领域'] == '互联网']
        df_ecommerce = df[df['领域'] == '电子商务']
        # 将筛选出来的数据分别保存为CSV文件
        df_computer_software.to_csv("./data/computer_software.csv", index=False)
        df_internet.to_csv("./data/internet.csv", index=False)
        df_ecommerce.to_csv("./data/ecommerce.csv", index=False)
        # 设置页面标题
        st.title('热门岗位分析')

        # 侧边栏领域选择
        selected_field = st.sidebar.selectbox(
            label="选择领域",
            options=["请选择", "计算机软件", "互联网", "电子商务"]
        )

        # 根据选择的领域展示数据
        if selected_field == "计算机软件":
            df_computer_software = df[df['领域'] == '计算机软件']
            st.write(f"显示领域: {selected_field}")
            st.write(df_computer_software)
            plot_city_job_analysis(df_computer_software)
            plot_word_frequency(df_computer_software)

        elif selected_field == "互联网":
            df_internet = df[df['领域'] == '互联网']
            st.write(f"显示领域: {selected_field}")
            st.write(df_internet)
            plot_city_job_analysis(df_internet)
            plot_word_frequency(df_internet)

        elif selected_field == "电子商务":
            df_ecommerce = df[df['领域'] == '电子商务']
            st.write(f"显示领域: {selected_field}")
            st.write(df_ecommerce)
            plot_city_job_analysis(df_ecommerce)
            plot_word_frequency(df_ecommerce)
