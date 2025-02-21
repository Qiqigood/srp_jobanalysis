from playwright.sync_api import sync_playwright
import time
with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=False)
    context = browser.new_context()

    page = context.new_page()
    page.goto("https://www.zhaopin.com/sou/jl801/kw01O00U80EG06G03F01N0/p1")
    # 获取cookie
    time.sleep(5)
    cookies = context.cookies()
    cookie_dict = {}
    for cookie in cookies:
        cookie_dict[cookie["name"]] = cookie["value"]
    print(cookie_dict)
from bs4 import BeautifulSoup
import requests
import time
from tqdm import tqdm
import pandas as pd

headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "cache-control": "max-age=0",
    "priority": "u=0, i",
    "referer": "https://www.zhaopin.com/sou/jl801/kw01O00U80EG06G03F01N0/p1",
    "sec-ch-ua": "\"Chromium\";v=\"128\", \"Not;A=Brand\";v=\"24\", \"Microsoft Edge\";v=\"128\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0",

}
cookies = {'_uab_collina': '172603833692980471099565',
           'acw_tc': '1a0c638f17260383368666189e00347e6ac270373627cb2b28b40bf7747fb6',
           'acw_sc__v2': '66e1413f368267fe14db235d7102befafd592806',
           'x-zp-client-id': '62556d7c-493b-4b3f-b799-4852d97e40a5',
           'FSSBBIl1UgzbN7NS': '5KhbTbuE1pM96Ujhm28DlCLRGMQdDm8ev2w9yTmAl1TxcLpfH.32gn9jHWAG63XY5m.zwJzIpwjpsWQypqhJRqq',
           'sensorsdata2015jssdkcross': '%7B%22distinct_id%22%3A%22191dfe6e4a11254-01e41e0f4f92ff8-26001151-921600-191dfe6e4a220c%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTkxZGZlNmU0YTExMjU0LTAxZTQxZTBmNGY5MmZmOC0yNjAwMTE1MS05MjE2MDAtMTkxZGZlNmU0YTIyMGMifQ%3D%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%22%2C%22value%22%3A%22%22%7D%2C%22%24device_id%22%3A%22191dfe6e4a11254-01e41e0f4f92ff8-26001151-921600-191dfe6e4a220c%22%7D',
           'sajssdk_2015_cross_new_user': '1', 'HMACCOUNT_BFESS': '5CE1833FAA2F8083',
           'Hm_lvt_21a348fada873bdc2f7f75015beeefeb': '1726038337',
           'Hm_lpvt_21a348fada873bdc2f7f75015beeefeb': '1726038337', 'HMACCOUNT': '5CE1833FAA2F8083',
           'locationInfo_search': '{%22code%22:%22801%22%2C%22name%22:%22%E6%88%90%E9%83%BD%22%2C%22message%22:%22%E5%8C%B9%E9%85%8D%E5%88%B0%E5%B8%82%E7%BA%A7%E7%BC%96%E7%A0%81%22}',
           'FSSBBIl1UgzbN7NT': '5RXmrHCMfAsZqqqDp65MjXayj2UoH1vC_Yw1wF8F4tofi7LSoYbUF_om_EhdyKyFar.pUPc.OI1g19MJPU8CPbKI8.Vq4R8.hdQZHCwBvXRaYKUYo1Dfqp6ROvOHQT4H2sELfG01VM5i6tXFohtYVF4ZSM8pg2nMp_5_JaC43_YOU2BTFOv.E8c6bC9i1J93sERm3jiefBNCllZtt4G0f1q_6dRW6PC1QPW6e1X5oNctO5dsUGf1cOs0hW5mUWzlkWUsW5vR29qXbPFhZ4X.S6p',
           '1420ba6bb40c9512e9642a1f8c243891': 'bb4a9dc0-b1d0-4824-98c2-ef484a86f8a5'}
infos = []
for i in range(1, 6):
    print(f"开始爬取{i}页")
    time.sleep(1)
    url = f"https://www.zhaopin.com/sou/jl801/kw01O00U80EG06G03F01N0/p{i}"
    referer = i if i == 1 else i - 1
    headers["referer"] = f"https://www.zhaopin.com/sou/jl801/kw01O00U80EG06G03F01N0/p{referer}"
    response = requests.get(url, headers=headers, cookies=cookies)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')  # 解析器
    divs = soup.find_all('div', class_='joblist-box__item')  # 找到所有职位块节点
    for div in tqdm(divs):
        job_name = div.find("a", class_="jobinfo__name").text.strip()
        salary = div.find("p", class_="jobinfo__salary").text.strip()
        skills = []
        skill_father = div.find('div', class_='jobinfo__tag')  # 技能要求所有标签
        if skill_father:
            skill_items = skill_father.find_all('div', class_="joblist-box__item-tag")
            for skill_item in skill_items:
                skills.append(skill_item.text)
        recruiter_name_recruiter_position = div.find('div', class_="companyinfo__staff-name").text.strip()
        if "·" in recruiter_name_recruiter_position:
            recruiter_name, recruiter_position = recruiter_name_recruiter_position.split('·')
        else:
            recruiter_name, recruiter_position = recruiter_name_recruiter_position, ""
        companyinfo_tag = div.find('div', class_="companyinfo__tag")
        companyinfo_items = companyinfo_tag.find_all('div', class_='joblist-box__item-tag')
        if companyinfo_items:
            financing = companyinfo_items[0].text.strip()
        else:
            financing = ""
        if len(companyinfo_items) >= 2:
            scale = companyinfo_items[1].text.strip()
        else:
            scale = ""
        if len(companyinfo_items) == 3:
            industry = companyinfo_items[2].text.strip()
        else:
            industry = ""
        otherinfo_father = div.find('div', class_='jobinfo__other-info')
        companyinfo_items = otherinfo_father.find_all('div', class_='jobinfo__other-info-item')
        areas = companyinfo_items[0].text.strip()
        areas = areas.split('·')
        try:
            area_grandfather = areas[0]
        except:
            area_grandfather = ""
        try:
            area_pather = areas[1]
        except:
            area_pather = ""
        try:
            area_son = areas[2]
        except:
            area_son = ""
        experience_requirement = companyinfo_items[1].text.strip()
        education_background_requirement = companyinfo_items[2].text.strip()
        info = {
            "岗位名称": job_name,
            "工资": salary,
            "技能要求": skills,
            "招聘人": recruiter_name,
            "招聘人职位": recruiter_position,
            "公司融资信息": financing,
            "公司规模": scale,
            "公司行业": industry,
            "工作地点": area_son,
            "工作区域": area_pather,
            "工作大区": area_grandfather
        }
        infos.append(info)

df = pd.DataFrame(infos)
df.to_excel("智联招聘招聘信息.xlsx", index=False)
