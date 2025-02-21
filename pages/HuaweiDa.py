import streamlit as st
import pandas as pd

# 加载处理后的数据
df = pd.read_csv("./data/HUAWEI_job_msg.csv")



# 加载处理后的数据
df = pd.read_csv("./data/HUAWEI_job_msg.csv")


# 设置表格样式
st.dataframe(df.style.set_properties(**{'width': '200px', 'height': '50px'})
             .set_table_styles([{'selector': 'thead th',
                                 'props': [('background-color', 'lightblue'),
                                           ('color', 'black'),
                                           ('font-weight', 'bold')]}]))

# 设置页面标题
st.title('华为岗位表')

# 显示数据表格
st.write(df)


