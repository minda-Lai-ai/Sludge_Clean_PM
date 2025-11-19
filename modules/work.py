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
    # 過濾全部空的紀錄
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
    # 編輯表單部分（略，與前段同）
    # …表單略…
    st.divider()
    st.subheader("每日紀要總攬")
    summary_df = summary_table(st.session_state.work_log)

    if not summary_df.empty:
        st.dataframe(summary_df.drop(columns=["刪除"]) if "刪除" in summary_df else summary_df, use_container_width=True)
        for row in summary_df.itertuples():
            btn_key = f"del_{row.日期}"
            if st.button("刪除", key=btn_key):
                st.session_state.work_log = st.session_state.work_log[st.session_state.work_log["日期"] != row.日期]
                st.experimental_rerun()
    else:
        st.info("目前無有效施工紀要紀錄。")

    st.divider()
    st.subheader("資料下載")
    csv = st.session_state.work_log.to_csv(index=False, encoding="utf-8-sig")
    st.download_button("下載 CSV (可正常顯示中文)", data=csv, file_name=f"{project_no}_worklog.csv", mime="text/csv")

render_work("PJ202501")
