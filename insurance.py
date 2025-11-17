import streamlit as st
import pandas as pd

def render():
    st.header("保險列表")
    try:
        df = pd.read_excel("Bao-Xian.xlsx")
        st.dataframe(df, use_container_width=True)
    except Exception:
        st.error("找不到保險資料檔案，請確認 Bao-Xian.xlsx 位置")
    col1, col2, col3, col4 = st.columns(4)
    if col1.button("新增"):
        st.info("新增保險：請於下方表單輸入資料")
        # 可使用 st.form 製作表單
    if col2.button("修改"):
        st.warning("點選某一行可進入修改模式")
    if col3.button("儲存"):
        st.success("已儲存")
    if col4.button("列印"):
        st.info("PDF存檔或列印（需外部方案）")
