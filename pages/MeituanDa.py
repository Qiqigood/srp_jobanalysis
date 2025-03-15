import pandas as pd
import csv
import streamlit as st
import requests
from collections import Counter
import jieba
from pyecharts.charts import Bar, Pie, WordCloud
from pyecharts import options as opts
from streamlit_echarts import st_pyecharts

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Cookie": "com.sankuai.recruitment.official.website_strategy=; com.sankuai.recruitment.official.website_random=; _lxsdk_cuid=192e2987e28c8-054e8f9b26aa29-26001d51-1bcab9-192e2987e28c8; weixinType=1; _lxsdk_s=192e81e18e5-3b9-bdc-fff%7C%7C118; logan_session_token=93flbid3yekx8ykkbr4o",
}


def main(url, i):
    url_job = "https://zhaopin.meituan.com/api/official/job/getJobList"
    payload = {
        "page": {"pageSize": 10, "pageNo": i},
        "jobType": [{"code": "1", "subCode": ["1", "3", "4"]}],
        "jobShareType": "1",
        "u_query_id": "1dba53d6b643df137c71e616746dca82",
        "r_query_id": "173046734012518100171"
    }
    req = requests.post(url_job, headers=headers, json=payload)
    if req.status_code == 200:
        job_data = req.json()
        extract_job_info(job_data)


def extract_job_info(data, filename='Meituan_job_msg.csv'):
    with open(filename, mode='a', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter='#')
        for job in data.get('data', {}).get('list', []):
            job_name = job.get('name', '未知职位')
            city_list = job.get('cityList', [])
            cities = [city['name'] for city in city_list] if isinstance(city_list, list) else ['未知城市']
            job_duty = job.get('jobDuty', '无职责描述').replace("\n", "").replace("\r", "")
            csvwriter.writerow([job_name, ', '.join(cities), job_duty])


def load_show():
    df = pd.read_csv('./data/Meituan_job_msg.csv', sep='#', names=['职位名称', '城市', '职位职责'], encoding='utf-8')
    return df


def analyze_city_distribution(df):
    city_series = df['城市'].dropna().astype(str).str.split(', ')
    all_cities = [city for sublist in city_series for city in sublist]
    city_counts = pd.Series(all_cities).value_counts()
    top_n = 10
    top_cities = city_counts.head(top_n)
    other_count = city_counts.iloc[top_n:].sum()
    other_series = pd.Series({"其他": other_count})
    top_cities = pd.concat([top_cities, other_series])

    pie = (
        Pie()
        .add(
            "城市分布",
            [list(z) for z in zip(top_cities.index.tolist(), top_cities.values.tolist())],
            radius=["30%", "75%"],
            rosetype="radius"
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title="城市岗位分布"),
            legend_opts=opts.LegendOpts(is_show=True),
            toolbox_opts=opts.ToolboxOpts()
        )
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {d}%"))
    )
    st.markdown("<br><br>", unsafe_allow_html=True)
    st_pyecharts(pie)


def analyze_word_frequency(column_data, title):
    words = " ".join(column_data.tolist())
    words_list = jieba.cut(words)
    word_counts = Counter(words_list)
    common_words = word_counts.most_common(50)
    wordcloud = (
        WordCloud()
        .add("", common_words, word_size_range=[20, 100])
        .set_global_opts(title_opts=opts.TitleOpts(title=title))
    )
    st_pyecharts(wordcloud)


if __name__ == '__main__':
    st.title('美团招聘岗位分析')
    df = load_show()
    with st.expander("岗位信息", expanded=True):
        st.write(df)
    st.sidebar.text('数据分析:')
    if st.sidebar.button(label='城市分布分析'):
        analyze_city_distribution(df)
    if st.sidebar.button(label='岗位职责词频分析'):
        analyze_word_frequency(df['职位职责'], "岗位职责高频词")