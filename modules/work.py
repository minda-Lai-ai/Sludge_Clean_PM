import streamlit as st
import pandas as pd

COLUMNS = [
    "日期", "作業等級", "主要施工項目", "附加作業",
    "廠商作業人數", "監造人員", "工作紀要",
    "油泥處理量", "油泥餅桶量", "油泥直接裝桶量", "其他工作紀要"
]

# 保證初始化且只執行一次
if "work_log" not in st.session_state:
    sample = [
        {"日期": "2025-01-01", "作業等級": "A", "主要施工項目": "油槽清洗", "附加作業": "高處作業",
         "廠商作業人數": 8, "監造人員": "王小明", "工作紀要": "順利完成",
         "油泥處理量": 2.5, "油泥餅桶量": 4, "油泥直接裝桶量": 1, "其他工作紀要": ""},
        {"日期": "2025-01-02", "作業等級": "B", "主要施工項目": "油桶搬運", "附加作業": "吊掛作業",
         "廠商作業人數": 7, "監造人員": "李小華", "工作紀要": "部分延期",
         "油泥處理量": 2, "油泥餅桶量": 3, "油泥直接裝桶量": 2, "其他工作紀要": "備註"}
    ]
    st.session_state.work_log = pd.DataFrame(sample, columns=COLUMNS).sort_values("日期")

def render_work(project_no):
    # ...前面略...
    with st.form("edit_form", clear_on_submit=False):    # <--- 不要漏掉 with
        # 所有表單欄位
        submitted = st.form_submit_button("儲存")
        if submitted:
            # 儲存邏輯
            pass

    col1, col2 = st.columns([2,1])
    with col1:
        selected = st.date_input(
            "請選擇欲填報/修改的日期 (萬年曆)",
            value=date.today(),
            key="work_date_input"
        )
    if isinstance(selected, list):
        selected_date = selected[0] if len(selected) > 0 else date.today()
    else:
        selected_date = selected
    day_str = selected_date.strftime("%Y-%m-%d")

    df = st.session_state.work_log
    sel_row = df[df["日期"] == day_str]
    edit_mode = not sel_row.empty

    with st.form("edit_form", clear_on_submit=False):
        st.subheader("填報/編輯紀要內容")
        record = sel_row.iloc[0] if edit_mode else {k:"" for k in COLUMNS}
        field_vals = {}
        field_vals["日期"] = day_str
        field_vals["作業等級"] = st.text_input("作業等級", value=str(record["作業等級"]), key="input_level")
        field_vals["主要施工項目"] = st.text_input("主要施工項目", value=str(record["主要施工項目"]), key="input_main_work")
        field_vals["附加作業"] = st.text_input("附加作業", value=str(record["附加作業"]), key="input_add_work")
        field_vals["廠商作業人數"] = st.number_input("廠商作業人數", value=int(record["廠商作業人數"]) if edit_mode and str(record["廠商作業人數"]).isdigit() else 0, min_value=0, key="input_worker_count")
        field_vals["監造人員"] = st.text_input("監造人員", value=str(record["監造人員"]), key="input_supervisor")
        field_vals["工作紀要"] = st.text_area("工作紀要（總攬限制25字顯示）", value=str(record["工作紀要"]), max_chars=200, key="input_report")
        field_vals["油泥處理量"] = st.number_input("油泥處理量", value=float(record["油泥處理量"]) if edit_mode and str(record["油泥處理量"]).replace('.','',1).isdigit() else 0.0, min_value=0.0, key="input_oil")
        field_vals["油泥餅桶量"] = st.number_input("油泥餅桶量", value=float(record["油泥餅桶量"]) if edit_mode and str(record["油泥餅桶量"]).replace('.','',1).isdigit() else 0.0, min_value=0.0, key="input_cake")
        field_vals["油泥直接裝桶量"] = st.number_input("油泥直接裝桶量", value=float(record["油泥直接裝桶量"]) if edit_mode and str(record["油泥直接裝桶量"]).replace('.','',1).isdigit() else 0.0, min_value=0.0, key="input_bucket")
        field_vals["其他工作紀要"] = st.text_input("其他工作紀要", value=str(record["其他工作紀要"]), key="input_other")
        submitted = st.form_submit_button("儲存")
        if submitted:
            df_new = df[df["日期"] != day_str]
            st.session_state.work_log = pd.concat([df_new, pd.DataFrame([field_vals])]).sort_values("日期").reset_index(drop=True)
            st.success("儲存成功！請手動刷新或操作其他日期以更新。")

    st.divider()
    st.subheader("每日紀要總攬")
    summary_df = summary_table(st.session_state.work_log)
    st.dataframe(summary_df, use_container_width=True)

    st.divider()
    st.subheader("資料下載")
    csv = st.session_state.work_log.to_csv(index=False, encoding="utf-8-sig")
    st.download_button("下載 CSV (可正常顯示中文)", data=csv, file_name=f"{project_no}_worklog.csv", mime="text/csv")

render_work("PJ202501")
