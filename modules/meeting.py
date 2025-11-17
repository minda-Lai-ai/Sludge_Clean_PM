import streamlit as st
import pandas as pd
from datetime import date
def render_meeting(project_no):
    st.header(f"{project_no} 專案會議紀錄")
    excel_path = f"Meeting_{project_no}.xlsx"
    columns = ["日期", "地點", "主題", "主持人", "出席人員", "會議記錄"]
    try:
        df = pd.read_excel(excel_path)
    except Exception:
        df = pd.DataFrame(columns=columns)
    with st.form("meeting_form"):
        meeting_date = st.date_input("日期", value=date.today())
        location = st.text_input("地點")
        topic = st.text_input("主題")
        host = st.text_input("主持人")
        attendees = st.text_input("出席人員")
        notes = st.text_area("會議記錄")
        submit = st.form_submit_button("送出")
        if submit:
            new_row = {
                "日期": meeting_date, "地點": location, "主題": topic, "主持人": host, "出席人員": attendees, "會議記錄": notes
            }
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            df.to_excel(excel_path, index=False)
            st.success("已儲存")
    st.dataframe(df, use_container_width=True)
