import streamlit as st
import pandas as pd
import jieba
from sklearn.feature_extraction.text import CountVectorizer
from pyecharts.charts import Bar, Pie
from pyecharts import options as opts
from streamlit_echarts import st_pyecharts


def load_show():
    df = pd.read_csv("./data/Bytedance_job_msg.csv")
    return df


if __name__ == "__main__":
    # 加载数据
    df = load_show()

    # 设置页面标题
    st.title('字节跳动招聘岗位分析')
    # 显示数据表格
    st.write(df)

    # 侧边栏
    add_selectbox = st.sidebar.selectbox(
        label="数据分析选择:",
        options=('请选择', '岗位城市分布分析',"岗位类别分析","岗位词频分析")
    )

    if add_selectbox == '岗位城市分布分析':
        table = df.copy()

        # 直接用 city_info 作为城市列
        table['city'] = table['city_info']

        # 分组统计岗位数量
        city_job_count_s = table.groupby(by='city').size().sort_values(ascending=False)

        # 让用户选择要显示的排名数量
        rank_limit = st.sidebar.selectbox(
            '选择显示的城市排名数量:',
            [3, 5, 10, 15, 20]
        )

        # 根据选择的排名限制，取前 N 个城市
        top_cities = city_job_count_s.head(rank_limit)

        # 配置X轴样式
        xaxis_opts = opts.AxisOpts(
            name="城市",
            axislabel_opts=opts.LabelOpts(
                rotate=45,  # 旋转45度，避免中文和英文重叠
                font_size=12,  # 设置字体大小
                font_family="Microsoft YaHei"  # 强制使用支持中文的字体
            )
        )

        # 如果选择的排名大于10，增加工具栏和修改样式
        if rank_limit >= 15:
            bar = (
                Bar()
                .add_xaxis(top_cities.index.tolist())
                .add_yaxis("岗位数量", top_cities.values.tolist())
                .set_global_opts(
                    title_opts=opts.TitleOpts(title="不同城市岗位数量"),
                    xaxis_opts=xaxis_opts,  # 设置自定义X轴样式
                    toolbox_opts=opts.ToolboxOpts()  # 增加工具栏
                )
            )
        else:
            bar = (
                Bar()
                .add_xaxis(top_cities.index.tolist())
                .add_yaxis("岗位数量", top_cities.values.tolist())
                .set_global_opts(
                    title_opts=opts.TitleOpts(title="不同城市岗位数量")
                )
            )

        st_pyecharts(bar)


    def get_chinese_words(text):
        # 使用jieba进行中文分词
        return " ".join(jieba.cut(text))

    if add_selectbox == "岗位词频分析":
        table = df.copy()

        # 使用jieba对岗位要求进行中文分词
        table['requirement_cut'] = table['requirement'].dropna().apply(get_chinese_words)

        # 提取分词后的岗位要求
        corpus = table['requirement_cut'].tolist()

        # 设置CountVectorizer，只处理中文，去除停用词
        vectorizer = CountVectorizer(
            stop_words=["的", "和", "是", "在", "我", "有", "为", "与", "不", "了","and","具备","优先","to","相关","以上","our","in","以上学历"])  # 你可以根据需求添加更多停用词
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
        table = df.copy()

        # 使用jieba对岗位要求进行中文分词
        table['description_cut'] = table['description'].dropna().apply(get_chinese_words)

        # 提取分词后的岗位要求
        corpus = table['description_cut'].tolist()

        # 设置CountVectorizer，只处理中文，去除停用词
        vectorizer = CountVectorizer(
            stop_words=["的", "和", "是", "在", "我", "有", "为", "与", "不", "了", "and", "具备", "优先", "to", "相关",
                        "以上", "our", "in", "以上学历","负责","通过","the","of","we","is","for"])  # 你可以根据需求添加更多停用词
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
                title_opts=opts.TitleOpts(title="岗位描述词频分析"),
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

    elif add_selectbox == "岗位类别分析":
        table = df.copy()

        # 统计岗位类别的数量
        job_category_count = table['job_category'].value_counts()

        # 选择前N个最大类别（例如前10个）
        top_n = 15
        top_categories = job_category_count.head(top_n)

        # 合并剩余的为“其他”
        other_count = job_category_count.tail(-top_n).sum()

        # 使用 pd.concat 来合并 "其他" 类别
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
                toolbox_opts=opts.ToolboxOpts()  # 增加工具栏
            )
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {d}%"))
        )

        # 在 Streamlit 页面中显示图表
        #         # 在标题和图表之间插入空行
        st.markdown("<br><br>", unsafe_allow_html=True)
        st_pyecharts(pie)
        # 分类展示
        job_category = st.sidebar.selectbox('选择工作类别', df['job_category'].unique())
        # 动态修改header
        st.header(f" {job_category} 具体岗位：")
        # 过滤数据并展示
        filtered_df = df[df['job_category'] == job_category]
        st.write(filtered_df)


