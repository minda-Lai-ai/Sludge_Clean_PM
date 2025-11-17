import streamlit as st
import pandas as pd
import os

#minda
def insurance_input():
    with st.form("保險資料表單"):
        # 特定表單內容...
        submit = st.form_submit_button("送出")
        return submit  # 或 return new_row
#minda

st.set_page_config(page_title="專案主頁", layout="wide")
st.title("工程專案保險管理")

# 檔案名與load
excel_path = "Bao-Xian.xlsx"
if not os.path.exists(excel_path):
    st.warning("首次使用請先在下方表單輸入保險資料")

try:
    df = pd.read_excel(excel_path)
    st.dataframe(df, use_container_width=True)
except Exception:
    df = pd.DataFrame(columns=[
        "保險分類", "保險名稱", "保險公司", "保險額度", "保險開始日", "保險到期日", "被保人", "備註"
    ])
    st.dataframe(df, use_container_width=True)

st.markdown("---")
# 新增/編輯表單
with st.form("保險資料表單"):
    st.subheader("新增或編輯保險資料")
    insurance_cat = st.selectbox(
        "保險分類", ["工程項目", "團體險", "勞保", "健保", "健檢", "其他"]
    )
    insurance_name = st.text_input("保險名稱", value="雇主意外責任險" if insurance_cat == "工程項目" else "")
    insurance_company = st.text_input("保險公司")
    insurance_amount = st.text_input("保險額度")
    insurance_start = st.date_input("保險開始日")
    insurance_end = st.date_input("保險到期日")
    insured_person = st.text_input("被保人（可多人用逗號分隔）")
    note = st.text_area("備註")
    submit = st.form_submit_button("送出")

if submit:
    # 新資料合併進df
    new_row = {
        "保險分類": insurance_cat,
        "保險名稱": insurance_name,
        "保險公司": insurance_company,
        "保險額度": insurance_amount,
        "保險開始日": insurance_start,
        "保險到期日": insurance_end,
        "被保人": insured_person,
        "備註": note
    }
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_excel(excel_path, index=False)
    st.success("已新增/儲存保險資料！")
    st.dataframe(df, use_container_width=True)

st.markdown("---")
st.info("如需編輯現有資料，可在 Excel 編輯後重新上傳，或進階串接 Streamlit AgGrid 互動編輯（可升級）。")
