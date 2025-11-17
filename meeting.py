import streamlit as st
import pandas as pd

st.set_page_config(page_title="專案主頁", layout="wide")
st.title("XXXXXXXX作業專案")

def render():
    st.header("會議管理")
    if st.button("新增會議"):
        st.info("請於下方表單輸入新會議內容")
    df = pd.DataFrame([
        {"日期":"2025-01-06", "主題":"專案啟動", "主持人":"王主任", "參與人員":"單位A;王一;李二", "內容":"新專案討論", "備註":"無"},
        {"日期":"2025-01-15", "主題":"工程協調", "主持人":"李工", "參與人員":"單位B;林三;陳四", "內容":"協調施工期程", "備註":"待回覆"},
    ])
    st.dataframe(df, use_container_width=True)
    col1, col2, col3, col4 = st.columns(4)
    if col1.button("修改"):
        st.warning("點選某會議可進入編輯模式")
    if col2.button("儲存"):
        st.success("已儲存")
    if col3.button("列印"):
        st.info("PDF存檔/列印會議記錄")

