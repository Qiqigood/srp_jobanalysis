import streamlit as st
import pandas as pd

# 加载处理后的数据
df = pd.read_csv("./data/Meituan_job_msg.csv")


# 设置页面标题
st.title('美团岗位表')

# 显示数据表格
st.write(df)


