import streamlit as st
import pandas as pd
from datetime import date
import io

def render_meeting(project_no):
    st.header(f"{project_no} 專案會議紀錄")
    csv_path = f"Meeting_{project_no}.csv"
    columns = ["日期", "地點", "主題", "主持人", "出席人員", "會議記錄"]

    # 讀取
    try:
        df = pd.read_csv(csv_path, encoding="utf-8-sig")
    except Exception:
        df = pd.DataFrame(columns=columns)

    # 新增功能
    with st.form("add_form"):
        d = st.date_input("日期", value=date.today())
        loc = st.text_input("地點")
        sub = st.text_input("主題")
        host = st.text_input("主持人")
        att = st.text_input("出席人員")
        note = st.text_area("會議記錄")
        submit = st.form_submit_button("新增")
        if submit:
            df_new = pd.DataFrame([[d, loc, sub, host, att, note]], columns=columns)
            df = pd.concat([df, df_new], ignore_index=True)
            df.to_csv(csv_path, index=False, encoding="utf-8-sig")
            st.experimental_rerun()

    # 顯示表格
    st.dataframe(df, use_container_width=True)
    if len(df) > 0:
        idx = st.number_input("選擇作業列(0起)", min_value=0, max_value=len(df)-1, step=1)
        # 修改功能
        if st.button("修改本列"):
            with st.form("edit_form"):
                d = st.date_input("新日期", value=pd.to_datetime(df.loc[idx,"日期"]))
                loc = st.text_input("新地點", value=df.loc[idx,"地點"])
                sub = st.text_input("新主題", value=df.loc[idx,"主題"])
                host = st.text_input("新主持人", value=df.loc[idx,"主持人"])
                att = st.text_input("新出席人員", value=df.loc[idx,"出席人員"])
                note = st.text_area("新會議記錄", value=df.loc[idx,"會議記錄"])
                ok = st.form_submit_button("確認修改")
                if ok:
                    df.loc[idx] = [d, loc, sub, host, att, note]
                    df.to_csv(csv_path, index=False, encoding="utf-8-sig")
                    st.success("已修改")
                    st.experimental_rerun()
        # 刪除功能
        if st.button("刪除此列"):
            df = df.drop(idx).reset_index(drop=True)
            df.to_csv(csv_path, index=False, encoding="utf-8-sig")
            st.success("已刪除")
            st.experimental_rerun()

        # 匯出為 csv 並加上 BOM
        csv = df.to_csv(index=False, encoding='utf-8-sig')
        st.download_button(
            label="下載 CSV（中文支援）",
            data=csv,
            file_name=f"Meeting_{project_no}.csv",
            mime='text/csv'
        )

# 用法例:
# render_meeting("PJ202501")
