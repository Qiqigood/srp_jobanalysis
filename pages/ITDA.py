import re
import os
import pandas as pd
import jieba
import matplotlib.pyplot as plt
import streamlit as st
from collections import Counter
from pyecharts.charts import Bar, WordCloud
from pyecharts import options as opts
from streamlit_echarts import st_pyecharts
from wordcloud import WordCloud as WC

# 加载数据
@st.cache_data
def load_data():
    df = pd.read_csv("./data/IT行业数据.csv")
    df["薪资"] = df["薪资"].apply(clean_salary)
    df["城市"] = df["城市"].apply(lambda x: x.split("·")[0] if isinstance(x, str) else x)
    return df.dropna(subset=["薪资", "城市", "领域"])

# 清洗薪资数据
def clean_salary(salary):
    if not isinstance(salary, str) or not salary.strip():
        return None
    salary = salary.replace("元", "").replace("K", "000")
    match = re.search(r"(\d+)-(\d+)", salary)
    if match:
        return (int(match.group(1)) + int(match.group(2))) / 2
    return None

# 词频分析

def plot_word_frequency(df, column="要求"):
    words = " ".join(df[column].dropna()).strip()
    words_list = [word for word in jieba.cut(words) if len(word) > 1]
    word_counts = Counter(words_list).most_common(50)

    st.write("## 词频分析")
    num_words = st.selectbox("选择展示的高频词个数", [3, 5, 10, 15, 20])
    st.write(pd.DataFrame(word_counts[:num_words], columns=["词语", "频率"]))

    # **修正：确保字体路径正确**
    font_path = "C:/Windows/Fonts/simhei.ttf"  # Windows 下 SimHei.ttf 的正确路径
    if not os.path.exists(font_path):  # 如果 SimHei.ttf 不存在，则尝试使用其他字体
        font_path = None

    # **生成词云**
    wc = WC(font_path=font_path, background_color="white")
    wc.generate_from_frequencies(dict(word_counts[:num_words]))

    # **修正 plt.imshow() 语法**
    plt.figure(figsize=(10, 6))
    plt.imshow(wc, interpolation="bilinear")  # 传入生成的词云对象
    plt.axis("off")  # 关闭坐标轴

    # **Streamlit 显示**
    st.pyplot(plt)
    plt.close()  # 避免 Streamlit 画图混乱


# 城市分析
def plot_city_analysis(df):
    city_count = df["城市"].value_counts()
    city_salary = df.groupby("城市")["薪资"].mean().round(0).astype(int).sort_values(ascending=False)

    bar = Bar().add_xaxis(city_salary.index.tolist()).add_yaxis("平均薪资", city_salary.values.tolist()).set_global_opts(
        title_opts=opts.TitleOpts(title="城市与平均薪资"),
        xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=45, font_size=12))
    )
    st_pyecharts(bar)

# 领域分析
def plot_field_distribution(df):
    field_count = df["领域"].value_counts()
    top_n = st.sidebar.selectbox("选择显示的领域数量", [3, 5, 10, 15, 20])
    top_fields = field_count.head(top_n)

    bar = Bar().add_xaxis(top_fields.index.tolist()).add_yaxis("岗位数量", top_fields.values.tolist()).set_global_opts(
        title_opts=opts.TitleOpts(title="不同领域的岗位数量"),
        xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=45, font_size=12))
    )
    st_pyecharts(bar)

# 主界面
st.title("IT行业招聘分析")
df = load_data()
st.write(df)

option = st.sidebar.selectbox("选择分析内容", ["请选择", "岗位领域分析", "热门岗位分析"])

if option == "岗位领域分析":
    plot_field_distribution(df)

elif option == "热门岗位分析":
    field = st.sidebar.selectbox("选择领域", ["请选择"] + df["领域"].unique().tolist())
    if field != "请选择":
        df_filtered = df[df["领域"] == field]
        st.write(f"显示领域: {field}")
        plot_city_analysis(df_filtered)
        plot_word_frequency(df_filtered)
