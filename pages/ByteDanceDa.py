import streamlit as st
import pandas as pd

# 加载处理后的数据
df = pd.read_csv("./data/Bytedance_job_msg.csv")

# 设置页面标题
st.title('字节跳动岗位表')
# 显示数据表格
st.write(df)

# 你也可以自定义更多展示，比如过滤器等
st.sidebar.header('数据分析')

job_category = st.sidebar.selectbox('选择工作类别', df['job_category'].unique())
filtered_df = df[df['job_category'] == job_category]

st.title('分类的岗位')
# 展示过滤后的数据
st.write(filtered_df)
