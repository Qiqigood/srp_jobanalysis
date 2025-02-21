import pandas as pd
import streamlit as st
import pandas as pt
import requests
from pyecharts.charts import Line
from pyecharts import options as opts
from streamlit_echarts import st_pyecharts
from pyecharts.charts import Bar
from pyecharts.charts import Pie
from lxml import etree


headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0',
    'Cookie':'index_location_city=%E5%85%A8%E5%9B%BD; user_trace_token=20240903205512-1fd9f70b-bc88-409f-8133-e9ef2508587c; LGUID=20240903205512-12b82591-1c14-4aec-af24-034708f64ae6; _ga=GA1.2.1718322362.1725368112; _gid=GA1.2.908793952.1725368113; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1725368112,1725432822,1725501474; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1725501474; HMACCOUNT=0FC2F7C6F4F15F63; LGSID=20240905095757-fe46a5b7-362d-4c8e-90ea-08108adcefbf; PRE_UTM=; PRE_HOST=; PRE_SITE=; PRE_LAND=https%3A%2F%2Fpassport.lagou.com%2Flogin%2Flogin.html%3Fmsg%3Dneedlogin%26clientIp%3D120.238.248.4; LGRID=20240905095757-abea2ac0-bcfa-43ae-8e92-7e4aaf921902; _ga_DDLTLJDLHH=GS1.2.1725501479.2.0.1725501479.60.0.0; sm_auth_id=jlnjp5fbav5rh9c6; gate_login_token=v1####6a010e4474990630d07877341977f11c7198155b00251c0d71ba0bc36cd7d5a6; LG_HAS_LOGIN=1; _putrc=31727500962659A1123F89F2B170EADC; JSESSIONID=ABAACCCABEGACCCB71C2C03F0AD0438838DB39355320B0C; login=true; hasDeliver=0; privacyPolicyPopup=false; WEBTJ-ID=20240905095932-191bfe884fa157a-030b40d9fa3f27-4c657b58-1821369-191bfe884fb224d; sensorsdata2015session=%7B%7D; unick=%E5%88%98%E4%BD%B3%E6%80%A1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22191b7f41f8a653-0fd45fbcf1b2fa-4c657b58-1821369-191b7f41f8b249a%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24os%22%3A%22Linux%22%2C%22%24browser%22%3A%22Chrome%22%2C%22%24browser_version%22%3A%22128.0.0.0%22%7D%2C%22%24device_id%22%3A%22191b7f41f8a653-0fd45fbcf1b2fa-4c657b58-1821369-191b7f41f8b249a%22%7D; __lg_stoken__=55311a989676c23f0e35b3949243b3e7f7b83d01ea2947f20cd9bdc89b5b8a150fa83c9c2896aa53a81d18dc42df4a3a694e914864c7c51bb0904e3347b65ab2ec1a1bad112e'
}
#按钮点击事件-数据爬取+保存
#从招聘网中抓取信息，保存到csv文件中
def get_job_msg(): #定义函数
    #打开文件，存到job_msg.csv的文件中
    fp = open('../data/job_msg.csv', 'a', encoding='utf-8')
    for page in range(2,5):
        #构建url，其实我觉得就是这里有问题。所以
        url = f'https://www.lagou.com/wn/zhaopin?fromSearch=true&kd=%25E6%2595%25B0%25E6%258D%25AE%25E5%2588%2586%25E6%259E%2590%25E5%25B8%2588&labelWords=sug&suginput=%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90&pn={page}'
        #request get发送HTTP请求，获取网页的HTML内容，etree.HTML()函数对thml内容进行解析
        page_text = requests.get(url, headers=headers).text
        tree = etree.HTML(page_text)
        #提取数据
        div_list = tree.xpath('//*[@id="jobList"]/div[1]/div')
        #在div_list循环中逐个提取并处理每个div元素
        for div in div_list:
            job_title_area = div.xpath('./div[1]/div[1]/div[1]/a//text()')
            salary_degree = div.xpath('./div[1]/div[1]/div[2]//text()')
            #岗位名称
            job_title = job_title_area[0]
            # 地区area
            area = job_title_area[1]
            #薪资
            salary = salary_degree[0]
            #学历degree
            degree = div.xpath('./div[1]/div[1]//div[@class="p-bom__JlNur"]/text()')[0]
            #公司名称company_title
            company_title = div.xpath('./div[1]/div[2]/div[1]/a/text()')[0]
            #公司信息company_msg
            company_msg = div.xpath('./div[1]/div[2]/div[2]/text()')
            if company_msg:
                company_msg = company_msg[0]
            else:
                company_msg = "暂无信息"
            #公司福利company_welfare
            company_welfare =  div.xpath('./div[2]/div[2]/text()')[0]
            #岗位要求job_require
            job_require = div.xpath('./div[2]/div[1]/span/text()')
            if job_require:
                job_require = job_require[0]
            else:
                job_require = "暂无信息"
            #写入csv文件
            fp.write(job_title+'#'+salary+'#'+area+'#'+degree+'#'+company_title+'#'+company_msg+'#'+company_welfare+'#'+job_require+'\n')
   #关闭文件
    fp.close()
    st.write('数据抓取结束')

#按钮点击事件-数据展示
def load_show():  #定义函数load_show( )
    df = pd.read_csv('../data/job_msg.csv', sep='#',
                     names=['岗位名称','薪资','地区','学历/经验要求','公司名称','公司信息','福利','岗位要求'], encoding='utf-8')
    return df

if __name__ == '__main__':
    #侧边栏布局
    st.sidebar.text('数据爬取+存储:')
    #数据爬取+保存
    isClick_btn1 = st.sidebar.button(label='开始吧')
    if isClick_btn1:
        get_job_msg()

    st.sidebar.text('数据加载+展示:')
    #数据加载+展示
    isClick_btn2 = st.sidebar.button(label='一键启动')
    if isClick_btn2:
        df = load_show()
        # 折叠展示数据表格
        with st.expander("岗位信息", expanded=True):
            st.write(df)


    #侧边栏下拉框
    add_selectbox = st.sidebar.selectbox(
        label="数据分析:",
        options=('请选择','不同城市岗位数量&平均薪资','不同经验的岗位占比')
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

    #if add_selectbox == '不同学历的岗位数量':
        #st.write('兄弟们，自己玩起来吧！')
