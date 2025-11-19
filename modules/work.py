import streamlit as st
import pandas as pd
import numpy as np
import io
from datetime import date

# =========== 固定欄位名稱 ============
COLUMNS = [
    "日期", "作業等級", "主要施工項目", "附加作業",
    "廠商作業人數", "監造人員", "工作紀要",
    "油泥處理量", "油泥餅桶量", "油泥直接裝桶量", "其他工作紀要"
]

# =========== 初始化範例資料，只執行一次 ============
if "work_log" not in st.session_state:
    sample = [
        {
            "日期": "2025-01-01", "作業等級": "A", "主要施工項目": "油槽清洗", "附加作業": "高處作業",
            "廠商作業人數": 8, "監造人員": "王小明", "工作紀要": "順利完成",
            "油泥處理量": 2.5, "油泥餅桶量": 4, "油泥直接裝桶量": 1, "其他工作紀要": ""
        },
        {
            "日期": "2025-01-02", "作業等級": "B", "主要施工項目": "油桶搬運", "附加作業": "吊掛作業",
            "廠商作業人數": 7, "監造人員": "李小華", "工作紀要": "部分延期",
            "油泥處理量": 2, "油泥餅桶量": 3, "油泥直接裝桶量": 2, "其他工作紀要": "備註"
        }
    ]
    st.session_state.work_log = pd.DataFrame(sample, columns=COLUMNS).sort_values("日期")
if "pending_delete" not in st.session_state:
    st.session_state.pending_delete = None  # 用於確認刪除

# =========== 累積欄位產生函數 ============
def summary_table(df):
    if df.empty: return df
    new_df = df.copy().sort_values("日期").reset_index(drop=True)
    # 累積量
    for col, acc_col in [
        ("油泥處理量", "油泥處理累積量"),
        ("油泥餅桶量", "油泥餅桶累積量"),
        ("油泥直接裝桶量", "油泥直接裝桶累積量")
    ]:
        new_df[acc_col] = new_df[col].cumsum()
    # 棧板計算
    new_df["棧板使用量"] = ((new_df["油泥餅桶累積量"] + new_df["油泥直接裝桶累積量"]) / 4).apply(np.ceil).astype(int)
    new_df["工作日"] = new_df.index + 1  # 編號
    new_df["工作紀要"] = new_df["工作紀要"].apply(lambda x: str(x)[:25] + ("..." if len(str(x)) > 25 else ""))
    return new_df

# =========== 主功能頁 ============
def render_work(project_no):
    st.header(f"每日施工紀要 (案號: {project_no})")

    # 選日期並編輯/新增
    col1, col2 = st.columns([2,1])
    with col1:
        selected = st.date_input("請選擇欲填報/修改的日期 (萬年曆)", value=date.today())
    day_str = selected.strftime("%Y-%m-%d")
    df = st.session_state.work_log
    sel_row = df[df["日期"] == day_str]
    edit_mode = not sel_row.empty

    with st.form("edit_form", clear_on_submit=False):
        st.subheader("填報/編輯紀要內容")
        record = sel_row.iloc[0] if edit_mode else {k:"" for k in COLUMNS}
        field_vals = {}
        field_vals["日期"] = day_str
        field_vals["作業等級"] = st.selectbox("作業等級", ["A","B","C"], index=["A","B","C"].index(record["作業等級"]) if edit_mode else 0)
        field_vals["主要施工項目"] = st.text_input("主要施工項目", value=record["主要施工項目"])
        field_vals["附加作業"] = st.text_input("附加作業", value=record["附加作業"])
        field_vals["廠商作業人數"] = st.number_input("廠商作業人數", value=int(record["廠商作業人數"]) if edit_mode else 0, min_value=0)
        field_vals["監造人員"] = st.text_input("監造人員", value=record["監造人員"])
        field_vals["工作紀要"] = st.text_area("工作紀要（總攬限制25字顯示）", value=record["工作紀要"], max_chars=200)
        field_vals["油泥處理量"] = st.number_input("油泥處理量", value=float(record["油泥處理量"]) if edit_mode else 0.0, min_value=0.0)
        field_vals["油泥餅桶量"] = st.number_input("油泥餅桶量", value=float(record["油泥餅桶量"]) if edit_mode else 0.0, min_value=0.0)
        field_vals["油泥直接裝桶量"] = st.number_input("油泥直接裝桶量", value=float(record["油泥直接裝桶量"]) if edit_mode else 0.0, min_value=0.0)
        field_vals["其他工作紀要"] = st.text_input("其他工作紀要", value=record["其他工作紀要"])
        submitted = st.form_submit_button("儲存")
        if submitted:
            df_new = df[df["日期"] != day_str]
            st.session_state.work_log = pd.concat([df_new, pd.DataFrame([field_vals])]).sort_values("日期").reset_index(drop=True)
            st.success("儲存成功！")
            st.experimental_rerun()

    # ====== 顯示總攬表和刪除 ======
    st.divider()
    st.subheader("每日紀要總攬")
    summary_df = summary_table(st.session_state.work_log)

    for row_idx, row in summary_df.iterrows():
        cols = st.columns(len(summary_df.columns) + 1)
        for col_idx, col in enumerate(summary_df.columns):
            cols[col_idx].write(row[col])
        # 刪除帶確認
        if st.session_state.pending_delete == row["日期"]:
            if cols[-1].button("確定刪除", key=f"confirm_{row['日期']}"):
                st.session_state.work_log = st.session_state.work_log[st.session_state.work_log["日期"] != row["日期"]]
                st.session_state.pending_delete = None
                st.experimental_rerun()
            if cols[-1].button("取消", key=f"cancel_{row['日期']}"):
                st.session_state.pending_delete = None
        else:
            if cols[-1].button("刪除", key=f"del_{row['日期']}"):
                st.session_state.pending_delete = row["日期"]

    # 再加一個共同的 DataFrame 總覽，不產生多餘內容
    st.dataframe(summary_df, use_container_width=True)

    # ====== 下載 CSV/Excel ======
    st.divider()
    st.subheader("資料下載")
    csv = st.session_state.work_log.to_csv(index=False, encoding="utf-8-sig")
    st.download_button("下載 CSV", data=csv, file_name=f"{project_no}_worklog.csv", mime="text/csv")
    out = io.BytesIO()
    st.session_state.work_log.to_excel(out, index=False)
    st.download_button("下載 Excel", data=out.getvalue(), file_name=f"{project_no}_worklog.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

# =========== 主程式呼叫 ============
render_work("PJ202501")
