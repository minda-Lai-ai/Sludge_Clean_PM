import streamlit as st
import pandas as pd
from datetime import date
import io

def render_insurance(project_no):
    st.header(f"{project_no} 專案保險管理")
    csv_path = f"Bao-Xian_{project_no}.csv"
    preset_engineer = ["雇主意外責任險", "營繕承包商意外責任險", "自訂工程保險"]
    preset_people = ["團險1", "團險2", "勞保", "健保", "健檢", "自訂人員保險"]
    columns = ["保險分類", "保險項目", "保險公司", "保險額度", "保險開始日", "保險到期日", "被保人", "備註"]
    try:
        df = pd.read_csv(csv_path)
    except Exception:
        df = pd.DataFrame(columns=columns)

    tab1, tab2 = st.tabs(["工程保險", "人員保險"])
    with tab1:
        item = st.selectbox("保險項目", preset_engineer, key="eng_select")
        with st.form("eng_form"):
            company = st.text_input("保險公司")
            amount = st.text_input("額度")
            start = st.date_input("開始日", value=date.today())
            end = st.date_input("到期日", value=date.today())
            person = st.text_input("被保人")
            note = st.text_area("備註")
            submit = st.form_submit_button("送出")
            if submit:
                new_row = {
                    "保險分類": "工程",
                    "保險項目": item,
                    "保險公司": company,
                    "保險額度": amount,
                    "保險開始日": str(start),
                    "保險到期日": str(end),
                    "被保人": person,
                    "備註": note,
                }
                df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                df.to_csv(csv_path, index=False)
                st.success("已儲存")
                

    with tab2:
        item = st.selectbox("保險項目", preset_people, key="people_select")
        with st.form("people_form"):
            company = st.text_input("保險公司")
            amount = st.text_input("額度")
            start = st.date_input("開始日", value=date.today())
            end = st.date_input("到期日", value=date.today())
            person = st.text_input("被保人")
            note = st.text_area("備註")
            submit = st.form_submit_button("送出")
            if submit:
                new_row = {
                    "保險分類": "人員",
                    "保險項目": item,
                    "保險公司": company,
                    "保險額度": amount,
                    "保險開始日": str(start),
                    "保險到期日": str(end),
                    "被保人": person,
                    "備註": note,
                }
                df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                df.to_csv(csv_path, index=False)
                st.success("已儲存")
 
    st.dataframe(df, use_container_width=True)
    # 下載 CSV
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    st.download_button("下載CSV", data=csv_buffer.getvalue(), file_name=f"Bao-Xian_{project_no}.csv", mime="text/csv")
    # 下載 Excel（如需，動態產生無需本地儲存）
    #excel_buffer = io.BytesIO()
    #df.to_excel(excel_buffer, index=False, engine="xlsxwriter")
    #st.download_button("下載Excel", data=excel_buffer.getvalue(), file_name=f"Bao-Xian_{project_no}.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    
