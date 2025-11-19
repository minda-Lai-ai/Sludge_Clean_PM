import streamlit as st
import pandas as pd
import numpy as np
from datetime import date

COLUMNS = [
    "日期", "作業等級", "主要施工項目", "附加作業",
    "廠商作業人數", "監造人員", "工作紀要",
    "油泥處理量", "油泥餅桶量", "油泥直接裝桶量", "其他工作紀要"
]

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

def summary_table(df):
    if df.empty: return df
    new_df = df.copy().sort_values("日期").reset_index(drop=True)
    # 過濾全為空的紀錄（不納入總攬與累積和工作日）
    mask_not_empty = new_df.drop(columns=["日期"]).apply(
        lambda x: any([str(xx).strip() != "" and xx != 0 and xx != 0.0 for xx in x.values]), axis=1
    )
    new_df = new_df[mask_not_empty].reset_index(drop=True)
    for col, acc_col in [
        ("油泥處理量", "油泥處理累積量"),
        ("油泥餅桶量", "油泥餅桶累積量"),
        ("油泥直接裝桶量", "油泥直接裝桶累積量")
    ]:
        new_df[acc_col] = new_df[col].cumsum()
    new_df["棧板使用量"] = ((new_df["油泥餅桶累積量"] + new_df["油泥直接裝桶累積量"]) / 4).apply(np.ceil).astype(int)
    new_df["工作日"] = new_df.index + 1
    new_df["工作紀要"] = new_df["工作紀要"].apply(lambda x: str(x)[:25] + ("..." if len(str(x)) > 25 else ""))
    return new_df

def render_work(project_no):
    st.header(f"每日施工紀要 (案號: {project_no})")

    # =================== 萬年曆選日期、填報/編輯 ===================
    col1, col2 = st.columns([2,1])
    with col1:
        selected = st.date_input(
            "請選擇欲填報/修改的日期 (萬年曆)",
            value=date.today(),
            key="work_date_input"
        )
    # 保證型態安全
    if isinstance(selected, list):
        if len(selected) > 0:
            selected_date = selected[0]
        else:
            st.warning("請選擇日期！")
            st.stop()
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
        field_vals["作業等級"] = st.selectbox(
            "作業等級", ["A","B","C"],
            index=["A","B","C"].index(record["作業等級"]) if edit_mode and record["作業等級"] in ["A","B","C"] else 0,
            key="select_level"
        )
        field_vals["主要施工項目"] = st.text_input("主要施工項目", value=record["主要施工項目"], key="input_main_work")
        field_vals["附加作業"] = st.text_input("附加作業", value=record["附加作業"], key="input_add_work")
        field_vals["廠商作業人數"] = st.number_input("廠商作業人數", value=int(record["廠商作業人數"]) if edit_mode and str(record["廠商作業人數"]).isdigit() else 0, min_value=0, key="input_worker_count")
        field_vals["監造人員"] = st.text_input("監造人員", value=record["監造人員"], key="input_supervisor")
        field_vals["工作紀要"] = st.text_area("工作紀要（總攬限制25字顯示）", value=record["工作紀要"], max_chars=200, key="input_report")
        field_vals["油泥處理量"] = st.number_input("油泥處理量", value=float(record["油泥處理量"]) if edit_mode and str(record["油泥處理量"]).replace('.','',1).isdigit() else 0.0, min_value=0.0, key="input_oil")
        field_vals["油泥餅桶量"] = st.number_input("油泥餅桶量", value=float(record["油泥餅桶量"]) if edit_mode and str(record["油泥餅桶量"]).replace('.','',1).isdigit() else 0.0, min_value=0.0, key="input_cake")
        field_vals["油泥直接裝桶量"] = st.number_input("油泥直接裝桶量", value=float(record["油泥直接裝桶量"]) if edit_mode and str(record["油泥直接裝桶量"]).replace('.','',1).isdigit() else 0.0, min_value=0.0, key="input_bucket")
        field_vals["其他工作紀要"] = st.text_input("其他工作紀要", value=record["其他工作紀要"], key="input_other")
        submitted = st.form_submit_button("儲存")
        if submitted:
            df_new = df[df["日期"] != day_str]
            st.session_state.work_log = pd.concat([df_new, pd.DataFrame([field_vals])]).sort_values("日期").reset_index(drop=True)
            st.success("儲存成功！")
            st.experimental_rerun()

    # =================== 純表格總攬 ===================
    st.divider()
    st.subheader("每日紀要總攬")
    summary_df = summary_table(st.session_state.work_log)
    st.dataframe(summary_df, use_container_width=True)

    # =================== CSV 下載 ===================
    st.divider()
    st.subheader("資料下載")
    csv = st.session_state.work_log.to_csv(index=False, encoding="utf-8-sig")
    st.download_button("下載 CSV (可正常顯示中文)", data=csv, file_name=f"{project_no}_worklog.csv", mime="text/csv")

render_work("PJ202501")
