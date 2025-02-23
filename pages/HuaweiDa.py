import streamlit as st
import pandas as pd
import jieba
from sklearn.feature_extraction.text import CountVectorizer
from pyecharts.charts import Bar, Pie, Line
from pyecharts import options as opts
from streamlit_echarts import st_pyecharts

# 加载数据
def load_show():
    df = pd.read_csv("./data/HUAWEI_job_msg.csv")
    return df

# 分词处理函数
def get_chinese_words(text):
    return " ".join(jieba.cut(text))

# 主程序
if __name__ == "__main__":
    # 加载数据
    df = load_show()

    # 设置页面标题
    st.title('华为招聘岗位分析')
    # 显示数据表格
    st.write(df)

    # 侧边栏
    add_selectbox = st.sidebar.selectbox(
        label="数据分析选择:",
            options=('请选择', '工作地点柱状图', '岗位要求词频分析', '岗位类别分析',  '岗位职责关键词分析','岗位要求与岗位类别关联分析')
    )

    # 1. 工作地点柱状图
    if add_selectbox == '工作地点柱状图':
        table = df.copy()

        # 分组统计工作地点的岗位数量
        city_job_count_s = table.groupby(by='工作地点').size().sort_values(ascending=False)

        # 让用户选择要显示的排名数量
        rank_limit = st.sidebar.selectbox(
            '选择显示的工作地点排名数量:',
            [3, 5, 10, 15, 20]
        )

        # 根据选择的排名限制，取前 N 个城市
        top_cities = city_job_count_s.head(rank_limit)

        # 绘制柱状图
        bar = (
            Bar()
            .add_xaxis(top_cities.index.tolist())
            .add_yaxis("岗位数量", top_cities.values.tolist())
            .set_global_opts(
                title_opts=opts.TitleOpts(title="不同工作地点岗位数量"),
                xaxis_opts=opts.AxisOpts(
                    name="工作地点",
                    axislabel_opts=opts.LabelOpts(
                        rotate=45,  # 旋转45度，避免中文和英文重叠
                        font_size=12,  # 设置字体大小
                        font_family="Microsoft YaHei"  # 强制使用支持中文的字体
                    )
                ),
                toolbox_opts=opts.ToolboxOpts(),
            )
        )

        st_pyecharts(bar)

    # 2. 岗位要求词频分析
    if add_selectbox == "岗位要求词频分析":
        table = df.copy()

        # 使用jieba对岗位要求进行中文分词
        table['requirement_cut'] = table['岗位要求'].dropna().apply(get_chinese_words)

        # 提取分词后的岗位要求
        corpus = table['requirement_cut'].tolist()

        # 设置CountVectorizer，只处理中文，去除停用词
        vectorizer = CountVectorizer(
            stop_words=["的", "和", "是", "在", "我", "有", "为", "与", "不", "了", "背景", "具备", "优先", "要求", "相关", "以上", "熟悉", "in", "以上学历"])
        X = vectorizer.fit_transform(corpus)

        # 获取词频
        word_freq = pd.DataFrame(X.toarray(), columns=vectorizer.get_feature_names_out())
        word_count = word_freq.sum().sort_values(ascending=False)
        # 选择前20个词频
        word_count_top20 = word_count.head(10)
        # 绘制词频柱状图
        bar = (
            Bar()
            .add_xaxis(word_count_top20.index.tolist())
            .add_yaxis("词频", word_count_top20.values.tolist())
            .set_global_opts(
                title_opts=opts.TitleOpts(title="岗位要求词频分析"),
                xaxis_opts=opts.AxisOpts(
                    name="词汇",
                    axislabel_opts=opts.LabelOpts(
                        rotate=45,  # 旋转45度，避免中文和英文重叠
                        font_size=12,  # 设置字体大小
                        font_family="Microsoft YaHei"  # 强制使用支持中文的字体
                    )
                ),
                toolbox_opts=opts.ToolboxOpts(),
            )
        )

        st_pyecharts(bar)

    # 3. 岗位职责关键词分析
    if add_selectbox == "岗位职责关键词分析":
        table = df.copy()

        # 使用jieba对岗位职责进行中文分词
        table['responsibility_cut'] = table['岗位职责'].dropna().apply(get_chinese_words)

        # 提取分词后的岗位职责
        corpus = table['responsibility_cut'].tolist()

        # 设置CountVectorizer，只处理中文，去除停用词
        vectorizer = CountVectorizer(
            stop_words=["的", "和", "是", "在", "我", "有", "为", "与", "不", "了", "and", "具备", "优先", "to", "相关", "以上", "our", "in", "以上学历"])
        X = vectorizer.fit_transform(corpus)

        # 获取词频
        word_freq = pd.DataFrame(X.toarray(), columns=vectorizer.get_feature_names_out())
        word_count = word_freq.sum().sort_values(ascending=False)
        # 选择前20个词频
        word_count_top20 = word_count.head(10)
        # 绘制岗位职责词频柱状图
        bar = (
            Bar()
            .add_xaxis(word_count_top20.index.tolist())
            .add_yaxis("词频", word_count_top20.values.tolist())
            .set_global_opts(
                title_opts=opts.TitleOpts(title="岗位职责词频分析"),
                xaxis_opts=opts.AxisOpts(
                    name="职责",
                    axislabel_opts=opts.LabelOpts(
                        rotate=45,  # 旋转45度，避免中文和英文重叠
                        font_size=12,  # 设置字体大小
                        font_family="Microsoft YaHei"  # 强制使用支持中文的字体
                    )
                ),
                toolbox_opts=opts.ToolboxOpts(),
            )
        )

        st_pyecharts(bar)

    # 4. 岗位类别分析
    if add_selectbox == "岗位类别分析":
        table = df.copy()

        # 统计岗位类别的数量
        job_category_count = table['岗位类别'].value_counts()

        # 选择前N个最大类别（例如前10个）
        top_n = 15
        top_categories = job_category_count.head(top_n)

        # 合并剩余的为“其他”
        other_count = job_category_count.tail(-top_n).sum()
        other_category = pd.Series({"其他": other_count})
        top_categories = pd.concat([top_categories, other_category])

        # 转换为列表，便于绘图
        categories = top_categories.index.tolist()
        values = top_categories.values.tolist()

        # 创建饼状图
        pie = (
            Pie()
            .add(
                "岗位类别占比",
                [list(z) for z in zip(categories, values)],
                radius=["30%", "75%"],  # 设置内外圈半径
                rosetype="radius",  # 设置为圆形的比例图
            )
            .set_global_opts(
                title_opts=opts.TitleOpts(title="岗位类别占比"),
                legend_opts=opts.LegendOpts(is_show=True),
            )
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {d}%"))
        )

        st.markdown("<br><br>", unsafe_allow_html=True)
        st_pyecharts(pie)

    # 5.岗位要求与岗位类别关联分析
    if add_selectbox == "岗位要求与岗位类别关联分析":
        table = df.copy()

        # 使用jieba对岗位要求进行中文分词
        table['requirement_cut'] = table['岗位要求'].dropna().apply(get_chinese_words)

        # 提取分词后的岗位要求
        corpus = table['requirement_cut'].tolist()

        # 设置CountVectorizer，只处理中文，去除停用词
        vectorizer = CountVectorizer(
            stop_words=["的", "和", "是", "在", "我", "有", "为", "与", "不", "了", "and", "具备", "优先", "to",
                        "相关", "以上", "our", "in", "以上学历"])
        X = vectorizer.fit_transform(corpus)

        # 获取词频
        word_freq = pd.DataFrame(X.toarray(), columns=vectorizer.get_feature_names_out())
        word_count = word_freq.sum().sort_values(ascending=False)

        # 获取每个岗位类别的常见词汇（假设你要按类别分组分析）
        category_word_counts = {}
        for category in table['岗位类别'].unique():
            category_df = table[table['岗位类别'] == category]
            category_corpus = category_df['requirement_cut'].tolist()
            category_X = vectorizer.transform(category_corpus)
            category_word_freq = pd.DataFrame(category_X.toarray(), columns=vectorizer.get_feature_names_out())
            category_word_count = category_word_freq.sum().sort_values(ascending=False)
            category_word_counts[category] = category_word_count.head(10)

        # 绘制岗位要求与岗位类别关联的词频柱状图
        for category, words in category_word_counts.items():
            bar = (
                Bar()
                .add_xaxis(words.index.tolist())
                .add_yaxis(f"{category} 类别词频", words.values.tolist())
                .set_global_opts(
                    title_opts=opts.TitleOpts(title=f"{category} 岗位要求词频分析"),
                    xaxis_opts=opts.AxisOpts(
                        name="词汇",
                        axislabel_opts=opts.LabelOpts(
                            rotate=45,  # 旋转45度，避免中文和英文重叠
                            font_size=12,  # 设置字体大小
                            font_family="Microsoft YaHei"  # 强制使用支持中文的字体
                        )
                    ),
                    toolbox_opts=opts.ToolboxOpts(),
                )
            )
            st_pyecharts(bar)





