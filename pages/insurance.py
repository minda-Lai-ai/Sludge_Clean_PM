import streamlit as st
import pandas as pd
import os
from datetime import date

st.set_page_config(page_title="保險填寫分頁", layout="wide")
st.title("工程保險及人員保險登錄")

excel_path = "Bao-Xian.xlsx"
preset_engineer_items = [
    "雇主意外責任險", "營繕承包商意外責任險", "自訂工程保險"
]
preset_people_items = [
    "團險1", "團險2", "勞保", "健保", "健檢", "自訂人員保險"
]
columns = [
    "保險分類", "保險項目", "保險公司", "保險額度", "保險開始日", "保險到期日", "被保人", "備註"
]

# 初次或出錯自動初始化
try:
    df = pd.read_excel(excel_path)
except Exception:
    df = pd.DataFrame(columns=columns)

tab1, tab2 = st.tabs(["工程保險", "人員保險"])

with tab1:
    st.header("工程保險資料")
    for item in preset_engineer_items:
        with st.form(f"eng_{item}"):
            st.subheader(item)
            company = st.text_input("保險公司", key=f"eng_company_{item}")
            amount = st.text_input("保險額度", key=f"eng_amt_{item}")
            start_date = st.date_input("保險開始日", key=f"eng_start_{item}", value=date.today())
            end_date = st.date_input("保險到期日", key=f"eng_end_{item}", value=date.today())
            insured_person = st.text_input("被保人", key=f"eng_person_{item}")
            note = st.text_area("備註", key=f"eng_note_{item}")
            submit_eng = st.form_submit_button("儲存/新增")
            if submit_eng:
                new_row = {
                    "保險分類": "工程",
                    "保險項目": item,
                    "保險公司": company,
                    "保險額度": amount,
                    "保險開始日": start_date,
                    "保險到期日": end_date,
                    "被保人": insured_person,
                    "備註": note
                }
                df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                df.to_excel(excel_path, index=False)
                st.success("資料已儲存")

with tab2:
    st.header("人員保險資料")
    for item in preset_people_items:
        with st.form(f"people_{item}"):
            st.subheader(item)
            company = st.text_input("保險公司", key=f"people_company_{item}")
            amount = st.text_input("保險額度", key=f"people_amt_{item}")
            start_date = st.date_input("保險開始日", key=f"people_start_{item}", value=date.today())
            end_date = st.date_input("保險到期日", key=f"people_end_{item}", value=date.today())
            insured_person = st.text_input("被保人", key=f"people_person_{item}")
            note = st.text_area("備註", key=f"people_note_{item}")
            submit_peo = st.form_submit_button("儲存/新增")
            if submit_peo:
                new_row = {
                    "保險分類": "人員",
                    "保險項目": item,
                    "保險公司": company,
                    "保險額度": amount,
                    "保險開始日": start_date,
                    "保險到期日": end_date,
                    "被保人": insured_person,
                    "備註": note
                }
                df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                df.to_excel(excel_path, index=False)
                st.success("資料已儲存")

st.markdown("---")
st.subheader("全部保險登錄明細（歷史查詢）")
st.dataframe(df, use_container_width=True)
