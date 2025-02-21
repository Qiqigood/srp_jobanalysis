import streamlit as st
from pages import DA,ByteDanceDa,HuaweiDa
# 创建一个字典来映射页面标题到页面函数
PAGES = {
    "拉勾网招聘信息": DA,
    "字节招聘信息": ByteDanceDa,
    "华为招聘信息": HuaweiDa,

}
def main():
    st.sidebar.title('导航')
    selected_page = st.sidebar.selectbox("选择页面", list(PAGES.keys()))
    # 根据用户选择的页面调用相应的函数
    page = PAGES[selected_page]
    page.app()
