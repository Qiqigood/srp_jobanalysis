
import pandas as pd
import streamlit as st
from pyecharts import options as opts
from streamlit_echarts import st_pyecharts
from pyecharts.charts import Bar
from pyecharts.charts import Pie

def load_show():  #定义函数load_show( )
    df = pd.read_csv("./data/Bytedance_job_msg.csv")
    return df


if __name__=="__main__":
    # 加载处理后的数据
    df = pd.read_csv("./data/Bytedance_job_msg.csv")
    # 设置页面标题
    st.title('字节跳动岗位表')
    # 显示数据表格
    st.write(df)

    # 侧边下拉条
    #侧边栏下拉框
    add_selectbox = st.sidebar.selectbox(
        label="数据分析:",
        options=('请选择','不同城市岗位数量&平均薪资','不同经验的岗位占比',"岗位分类")
    )
    #获取下拉选项
    if add_selectbox == '不同城市岗位数量&平均薪资':
        table = load_show()
        def get_city_name(x):
            return x.split('·')[0].split('[')[1]
        table['city'] = table['地区'].map(get_city_name)
        #不同城市岗位数量
        city_job_count_s = table.groupby(by='city').size().sort_values(ascending=False)

        #不同城市平均薪资
        # 求出salary每个元素表示薪资范围的均值:7k-10k
        ret = table['薪资'].str.extract(r'(\d+)k-(\d+)k')
        # 注意：正则返回结果为字符串类型,将其转成数字类型
        ret = ret.astype('int')
        table['mean_sal'] = ret.apply(lambda s:s.mean(), axis=1)
        table['mean_sal'] = table['mean_sal']
        mean_sal_city = table.groupby(by='city')['mean_sal'].mean().sort_values(ascending=False)
        mean_sal_city = mean_sal_city.map(lambda x:format(x,'.2f'))
        #绘制柱状图
        b = (
            Bar()
                .add_xaxis(city_job_count_s.index.tolist())
                .add_yaxis(
                "岗位数量", city_job_count_s.values.tolist())
                .add_yaxis(
                "平均薪资", mean_sal_city.values.tolist())
                .set_global_opts(
                    title_opts=opts.TitleOpts(
                        title="岗位分析", subtitle="不同城市的岗位数量&平均薪资"
                    ),  # 工具栏
                    toolbox_opts=opts.ToolboxOpts(),
            )
        )
        st_pyecharts(b)

    if add_selectbox == '不同经验的岗位占比':
        table = load_show()
        #学历
        table["degree"] = table['学历/经验要求'].str.extract('(.*)/(.*)')[0]
        ret = table.groupby(by='degree').size()
        #饼图
        cate = ret.index.tolist()
        data = ret.values.tolist()
        pie = (Pie()
               .add('i am bobo', [list(z) for z in zip(cate, data)],
                    radius=["30%", "75%"],  # 设置半径（内外圈半径）
                    rosetype="radius"  # 半径形式的玫瑰型样式（经典）
                    )
               .set_global_opts(title_opts=opts.TitleOpts(title="数据分析", subtitle="经验占比"))
               .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {d}%"))
               )

        st_pyecharts(pie)

    if add_selectbox == '不同城市岗位数量&平均薪资':
        # 你也可以自定义更多展示，比如过滤器等
        st.sidebar.header('数据分析')

        job_category = st.sidebar.selectbox('选择工作类别', df['job_category'].unique())
        filtered_df = df[df['job_category'] == job_category]

        st.title('分类的岗位')
        # 展示过滤后的数据
        st.write(filtered_df)
