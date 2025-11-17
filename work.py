import streamlit as st
from datetime import datetime, timedelta

st.set_page_config(page_title="專案主頁", layout="wide")
st.title("XXXXXXXX作業專案")

def render():
    st.header("每日施工紀要")
    st.write("（萬年曆顯示功能，可用日曆套件或 python 內建方式）")
    st.button("總攬")
    st.write("請點選日曆進入填報/瀏覽當日施工細節")
    # 施工紀要範例
    table = [
        {"日期":"2025-01-01", "作業等級":"A", "主要施工":"油槽清洗", "附加作業":"高處作業", "廠商人數":8, "監造人員":"王小明", "工作紀要":"順利完成", "油泥處理量":2.5, "油泥餅桶裝桶量":4, "木棧板數量":1, "其他":""},
        {"日期":"2025-01-02", "作業等級":"B", "主要施工":"油桶搬運", "附加作業":"吊掛作業", "廠商人數":7, "監造人員":"李小華", "工作紀要":"部分延期", "油泥處理量":2, "油泥餅桶裝桶量":3, "木棧板數量":1, "其他":"備註"}
    ]
    st.dataframe(table)

