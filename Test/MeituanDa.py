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
from bs4 import BeautifulSoup

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Cookie":"com.sankuai.recruitment.official.website_strategy=; com.sankuai.recruitment.official.website_random=; _lxsdk_cuid=192e2987e28c8-054e8f9b26aa29-26001d51-1bcab9-192e2987e28c8; weixinType=1; _lxsdk_s=192e81e18e5-3b9-bdc-fff%7C%7C118; logan_session_token=93flbid3yekx8ykkbr4o",
}
def main(url,i):
    url_job = "https://zhaopin.meituan.com/api/official/job/getJobList"

    payload = {
        "page": {
            "pageSize": 10,
            "pageNo": i
        },
        "jobType": [
            {
                "code": "1",
                "subCode": ["1", "3", "4"]
            }
        ],
        "jobShareType": "1",
        "u_query_id": "1dba53d6b643df137c71e616746dca82",
        "r_query_id": "173046734012518100171"
    }

    req = requests.post(url_job, headers=headers, json=payload)

    # 输出响应结果
    if req.status_code == 200:
        job_data =req.json()
        print("第"+str(i)+"页请求成功")
        extract_job_info(job_data)  # 调用提取函数
        #print("请求成功:", req.json())  # 确保调用json()函数
    else:
        print("请求失败，状态码:", req.status_code)


def extract_job_info(data, filename='Meituan_job_msg.csv'):
    # 提取职位信息并写入 CSV 文件,这里是追加模式
    with open(filename, mode='a', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter='#')

        # 写入表头
        #csvwriter.writerow(['职位名称', '城市', '职位职责'])

        for job in data.get('data', {}).get('list', []):
            job_name = job.get('name', '未知职位')
            # 检查 cityList 是否存在并为列表
            city_list = job.get('cityList', [])
            if isinstance(city_list, list):
                cities = [city['name'] for city in city_list]
            else:
                cities = ['未知城市']
            job_duty = job.get('jobDuty', '无职责描述').replace("\n", "").replace("\r", "")

            # 写入一行数据
            csvwriter.writerow([job_name, ', '.join(cities), job_duty])




def load_show():  #定义函数load_show( )
    df = pd.read_csv('../data/Meituan_job_msg.csv', sep='#',
                     names=['岗位名称','所在城市','岗位要求'], encoding='utf-8')
    return df


if __name__ == '__main__':

    st.sidebar.text('数据爬取+存储:')
    # 数据爬取+保存
    isClick_btn1 = st.sidebar.button(label='开始吧')
    if isClick_btn1:
        # 构造请求url
        url = "https://zhaopin.meituan.com/web/position?hiringType=1_1,1_3,1_4"
        for i in range(1, 12):
            # print(url + "&pageNo="+ str(i))
            main(url + "&pageNo=" + str(i), i)

    st.sidebar.text('数据加载+展示:')
    # 数据加载+展示
    isClick_btn2 = st.sidebar.button(label='一键启动')
    if isClick_btn2:
        df = load_show()
        # 折叠展示数据表格
        with st.expander("岗位信息", expanded=True):
            st.write(df)



