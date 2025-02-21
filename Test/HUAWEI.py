# -*- coding: utf-8 -*-
"""
Author: @CSDN盲敲代码的阿豪
Time: 2024/12/10 11:26
Project: 华为社会招聘

目标网站：https://career.huawei.com/reccampportal/portal5/social-recruitment.html
抓取字段：['岗位名称','岗位类别','岗位职责','岗位要求','工作地点','入职部门','jobId','详情页链接']
"""
import time
import requests
from jsonpath import jsonpath
import openpyxl
import os

class Spider:

    # 1、信息准备
    def __init__(self):
        # 目标网站
        # 标题页url
        self.url = "https://career.huawei.com/reccampportal/services/portal/portalpub/getJob/newHr/page/10/1"

        # 头部信息
        self.headers = {
            'Cookie': 'JSESSIONID=67E8DB7374C763FBB0A070377119CC73; __hau=HuaweiConnect.1684306459.2113559840; _ga_3X7GKW06CQ=GS1.1.1703083828.73.1.1703084124.0.0.0; _ga_XXDVNPW2GY=GS1.1.1720671404.9.0.1720671434.0.0.0; language=zh_CN; Hm_lvt_48e5a2ca327922f1ee2bb5ea69bdd0a6=1731333573; utag_main=v_id:018804be330c00253227d384506e05081003707900978$_sn:14$_se:3$_ss:0$_st:1731335377195$ses_id:1731333571361;exp-session$_pn:1;exp-session; _ga_8GRJ7QNG8D=GS1.1.1731333572.6.0.1731333684.0.0.0; idss_cid=a503408b-e6b3-48bf-bab5-510def48cb1c; browsehappy=browsehappy; supportelang=zh; support_last_vist=enterprise; lang=zh_CN; career_huawei_com_reccampportal_sticky=pro_mcls#pro_7.185.153.184_61475:3; ztsg_ruuid=17a51c8ec188e0b0-81e8-4fee-bd93-0c1653c378a5; _gid=GA1.2.1538698158.1733752599; _ga=GA1.2.1385979375.1683706754; _gat_gtag_UA_7728030_15=1; _ga_CW901KCGC7=GS1.1.1733801297.2.1.1733801397.21.0.0',
            'Referer': 'https://career.huawei.com/reccampportal/portal5/social-recruitment.html',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.43'
        }

        # 查询参数
        self.params ={
          'curPage': 1,
          'pageSize': 10,
          'jobFamilyCode': '',
          'deptCode': '',
          'keywords': '',
          'searchType': '1',
          'orderBy': 'P_COUNT_DESC',
          'jobType': '1',
    }

        # 创建excel表格
        if not os.path.exists('华为社招.xlsx'):
            self.workbook = openpyxl.Workbook()
            self.sheet = self.workbook.active
            self.sheet.title = '华为社招'
            self.sheet.append(['岗位名称','岗位类别','岗位职责','岗位要求','工作地点','入职部门','jobId','详情页链接'])
        else:
            self.workbook = openpyxl.load_workbook('华为社招.xlsx')
            self.sheet = self.workbook.active


    # 2、发起请求
    def get(self):
        response = requests.get(url=self.url,headers=self.headers,params=self.params)
        if response.status_code == 200:
            json_data = response.json()
            return json_data
        else:
            print('请求失败')


    # 3、解析数据
    def parse(self,json_data):
        jobname = jsonpath(json_data,'$..jobname') # 岗位名称
        jobFamilyName = jsonpath(json_data,'$..jobFamilyName') # 岗位类别
        mainBusiness = jsonpath(json_data,'$..mainBusiness') # 岗位职责
        jobRequire = jsonpath(json_data,'$..jobRequire') # 岗位要求
        jobArea = jsonpath(json_data,'$..jobArea') # 工作地点
        deptName = jsonpath(json_data,'$..deptName') # 入职部门
        jobId = jsonpath(json_data,'$..jobId') # 详情页id
        return jobname,jobFamilyName,mainBusiness,jobRequire,jobArea,deptName,jobId

    # 4、保存数据
    def save(self,jobname,jobFamilyName,mainBusiness,jobRequire,jobArea,deptName,jobId):
        for name,famil,bus,req,area,dep,id in zip(jobname,jobFamilyName,mainBusiness,jobRequire,jobArea,deptName,jobId):
            # 排除特殊字符，以免存入Excel表格时报错
            bus = bus.replace('','')
            req = req.replace('','')
            # 详情页链接
            detal_url = 'https://career.huawei.com/reccampportal/portal5/social-recruitment-detail.html?jobId={}&dataSource=1'.format(id)
            self.sheet.append([name,famil,bus,req,area,dep,id,detal_url])
            self.workbook.save('华为社招.xlsx')
            print('岗位名称:', name)
            print('岗位类别:', famil)
            print('岗位职责:', bus)
            print('岗位要求:', req)
            print('工作地点:', area)
            print('入职部门:', dep)
            print('jobId:',id)
            print('详情页链接：',detal_url)
            print('=============================')

    # 5、启动程序
    def start(self):
        json_data = self.get()
        jobname,jobFamilyName,mainBusiness,jobRequire,jobArea,deptName,jobId = self.parse(json_data)
        self.save(jobname,jobFamilyName,mainBusiness,jobRequire,jobArea,deptName,jobId)
        return jobname

	# 6、实现翻页抓取
    def run(self):
        # 翻页抓取每一页数据
        num = 1
        while True:
            time.sleep(2)
            print(f'正在抓取第{num}页数据，请稍等....')
            self.url = "https://career.huawei.com/reccampportal/services/portal/portalpub/getJob/newHr/page/10/{}".format(num)
            self.params['curPage'] = num  # 修改翻页参数
            try:
                jobname = spider.start()
            except:
                print('所有数据抓取完毕')
                break
            print(f'第{num}页数据抓取完毕！！！')
            num += 1

if __name__ == '__main__':
    spider = Spider()
    spider.run()