import requests
import json
import pandas as pd
import csv
import streamlit as st
import pandas as pt
import requests
from pyecharts.charts import Line
from pyecharts import options as opts
from streamlit_echarts import st_pyecharts
from pyecharts.charts import Bar
from pyecharts.charts import Pie

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36"
}
def main(url):
    response = requests.get(url, headers=headers)
    # 将json字符串转字典
    jsonDic = json.loads(response.text)

    result = jsonDic["Data"]["Posts"]
    with open("Tecent_job_msg.csv", "a",encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile, delimiter='#')  # 使用 # 作为分隔符
        for x in result:
            postID = x["PostId"]
            postUrl = "https://careers.tencent.com/tencentcareer/api/post/ByPostId?postId=" + postID
            resDetail = requests.get(postUrl, headers=headers)

            jsonDicDetail = json.loads(resDetail.text)

            # 获取需要的信息，这里还转换了换行信息
            RecruitPostName = jsonDicDetail["Data"]["RecruitPostName"]
            Responsibility = jsonDicDetail["Data"]["Responsibility"].replace("\n", "").replace("\r", "")
            Requirement = jsonDicDetail["Data"]["Requirement"].replace("\n", "").replace("\r", "")

            # 将数据拼接成一行写入，再输入换行
            writer.writerow([RecruitPostName, Responsibility, Requirement])



def load_show():  #定义函数load_show( )
    df = pd.read_csv('./data/Tecent_job_msg.csv',sep='#',
                     names=['岗位名称','岗位职责','岗位要求'],encoding='utf-8')
    return df


if __name__ == '__main__':
    st.sidebar.text('数据爬取+存储:')
    # 数据爬取+保存
    isClick_btn1 = st.sidebar.button(label='开始吧')
    if isClick_btn1:
        # 构造请求url
        url = "https://careers.tencent.com/tencentcareer/api/post/Query?pageIndex="
        for i in range(1, 11):
            main(url + str(i) + "&pageSize=10")

    st.sidebar.text('数据加载+展示:')
    # 数据加载+展示
    isClick_btn2 = st.sidebar.button(label='一键启动')
    if isClick_btn2:
        df = load_show()
        # 折叠展示数据表格
        with st.expander("岗位信息", expanded=True):
            st.write(df)



