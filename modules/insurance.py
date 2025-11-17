import streamlit as st
import pandas as pd
from datetime import date
import os

def render_insurance(project_no):
    st.header(f"{project_no} 專案保險管理")
    excel_path = f"Bao-Xian_{project_no}.xlsx"
    preset_engineer = ["雇主意外責任險", "營繕承包商意外責任險", "自訂工程保險"]
    preset_people = ["團險1", "團險2", "勞保", "健保", "健檢", "自訂人員保險"]
    columns = ["保險分類", "保險項目", "保險公司", "保險額度", "保險開始日", "保險到期日", "被保人", "備註"]
    try:
        df = pd.read_excel(excel_path)
    except Exception:
        df = pd.DataFrame(columns=columns)

    tab1, tab2 = st.tabs(["工程保險", "人員保險"])
    with tab1:
        for item in preset_engineer:
            with st.form(f"eng_form_{item}"):
                st.write(item)
                company = st.text_input("保險公司", key=f"eng_company_{item}")
                amount = st.text_input("額度", key=f"eng_amt_{item}")
                start = st.date_input("開始日", key=f"eng_start_{item}", value=date.today())
                end = st.date_input("到期日", key=f"eng_end_{item}", value=date.today())
                person = st.text_input("被保人", key=f"eng_person_{item}")
                note = st.text_area("備註", key=f"eng_note_{item}")
                submit = st.form_submit_button("送出")
                if submit:
                    new_row = {
                        "保險分類": "工程",
                        "保險項目": item,
                        "保險公司": company,
                        "保險額度": amount,
                        "保險開始日": start,
                        "保險到期日": end,
                        "被保人": person,
                        "備註": note
                    }
                    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                    df.to_excel(excel_path, index=False)
                    st.success("已儲存")

    with tab2:
        for item in preset_people:
            with st.form(f"people_form_{item}"):
                st.write(item)
                company = st.text_input("保險公司", key=f"people_company_{item}")
                amount = st.text_input("額度", key=f"people_amt_{item}")
                start = st.date_input("開始日", key=f"people_start_{item}", value=date.today())
                end = st.date_input("到期日", key=f"people_end_{item}", value=date.today())
                person = st.text_input("被保人", key=f"people_person_{item}")
                note = st.text_area("備註", key=f"people_note_{item}")
                submit = st.form_submit_button("送出")
                if submit:
                    new_row = {
                        "保險分類": "人員",
                        "保險項目": item,
                        "保險公司": company,
                        "保險額度": amount,
                        "保險開始日": start,
                        "保險到期日": end,
                        "被保人": person,
                        "備註": note
                    }
                    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                    df.to_excel(excel_path, index=False)
                    st.success("已儲存")

    st.dataframe(df, use_container_width=True)

