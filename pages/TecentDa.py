import requests
import json
import pandas as pd
import csv
import streamlit as st
from collections import Counter
import jieba
from pyecharts.charts import Bar, WordCloud
from pyecharts import options as opts
from streamlit_echarts import st_pyecharts

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36"
}


def main(url):
    response = requests.get(url, headers=headers)
    jsonDic = json.loads(response.text)
    result = jsonDic["Data"]["Posts"]

    with open("Tecent_job_msg.csv", "a", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile, delimiter='#')
        for x in result:
            postID = x["PostId"]
            postUrl = "https://careers.tencent.com/tencentcareer/api/post/ByPostId?postId=" + postID
            resDetail = requests.get(postUrl, headers=headers)
            jsonDicDetail = json.loads(resDetail.text)

            RecruitPostName = jsonDicDetail["Data"]["RecruitPostName"]
            Responsibility = jsonDicDetail["Data"]["Responsibility"].replace("\n", "").replace("\r", "")
            Requirement = jsonDicDetail["Data"]["Requirement"].replace("\n", "").replace("\r", "")

            writer.writerow([RecruitPostName, Responsibility, Requirement])


def load_show():
    df = pd.read_csv('./data/Tecent_job_msg.csv', sep='#',
                     names=['岗位名称', '岗位职责', '岗位要求'], encoding='utf-8')
    return df


def analyze_job_titles(df):
    job_counts = df['岗位名称'].value_counts().head(10)
    bar = (
        Bar()
        .add_xaxis(job_counts.index.tolist())
        .add_yaxis("岗位数量", job_counts.values.tolist())
        .set_global_opts(title_opts=opts.TitleOpts(title="热门岗位"))
    )
    st_pyecharts(bar)


def analyze_word_frequency(column_data, title, stopwords=[]):
    words = " ".join(column_data.tolist())
    words_list = [word for word in jieba.cut(words) if word not in stopwords and len(word) > 1]
    word_counts = Counter(words_list)
    common_words = word_counts.most_common(50)

    wordcloud = (
        WordCloud()
        .add("", common_words, word_size_range=[20, 100])
        .set_global_opts(title_opts=opts.TitleOpts(title=title))
    )
    st_pyecharts(wordcloud)


if __name__ == '__main__':
    st.sidebar.text('数据加载+展示:')
    isClick_btn2 = st.sidebar.button(label='展示数据')
    if isClick_btn2:
        df = load_show()
        with st.expander("岗位信息", expanded=True):
            st.write(df)

    st.sidebar.text('数据分析:')
    isClick_btn4 = st.sidebar.button(label='岗位职责词频分析')
    if isClick_btn4:
        df = load_show()
        custom_stopwords = ["招聘", "负责", "要求", "相关","的","和","1","2","3","4"".",",","、"]  # 用户自定义停用词
        analyze_word_frequency(df['岗位职责'], "岗位职责高频词", stopwords=custom_stopwords)

    isClick_btn5 = st.sidebar.button(label='岗位要求词频分析')
    if isClick_btn5:
        df = load_show()
        custom_stopwords = ["熟悉", "经验", "能力", "以上"]  # 用户自定义停用词
        analyze_word_frequency(df['岗位要求'], "岗位要求高频词", stopwords=custom_stopwords)
