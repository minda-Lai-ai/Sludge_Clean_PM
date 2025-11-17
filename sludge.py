import streamlit as st

st.set_page_config(page_title="專案主頁", layout="wide")
st.title("XXXXXXXX作業專案")

def render():
    st.header("公證量油數據")
    st.write("公證量油廠商: 公證檢測公司")
    st.write("公證量油時間: 2025-01-18")
    st.write("公證量油數據: (匯入公證Excel功能)")
    st.write("報告提供日期: 2025-01-20")
    st.write("公證量油油泥量: 5.6 公秉")
    st.write("上傳現場圖片：")
    st.file_uploader("選擇圖片", accept_multiple_files=True)

