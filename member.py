import streamlit as st
import pandas as pd

def render():
    st.header("成員矩陣")
    df = pd.DataFrame([
        {"單位":"A單位", "姓名":"張三", "聯絡方式":"0912345678", "代理人":"李四", "其他":""},
        {"單位":"B單位", "姓名":"王五", "聯絡方式":"0987654321", "代理人":"陳六", "其他":""},
    ])
    st.dataframe(df, use_container_width=True)
    col1, col2 = st.columns(2)
    if col1.button("編輯"):
        st.info("進入可編輯模式（建議使用st.form）")
    if col2.button("儲存"):
        st.success("已儲存")
