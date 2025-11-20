import streamlit as st
import pandas as pd
from datetime import date
import io

# 核心邏輯: 使用 st.session_state 替代表地文件 I/O
def render_meeting(project_no: str):
    """
    渲染特定專案的會議記錄介面，並使用 st.session_state 進行資料管理。
    """
    # 使用專案編號作為 Session State 的唯一鍵
    STATE_KEY = f'meeting_data_{project_no}'
    columns = ["日期", "地點", "主題", "主持人", "出席人員", "會議記錄"]
    
    # 1. 初始化資料: 確保 DataFrame 存在於 session state 中
    if STATE_KEY not in st.session_state:
        st.session_state[STATE_KEY] = pd.DataFrame(columns=columns)
    
    # 從 session state 取得當前 DataFrame
    df = st.session_state[STATE_KEY]

    st.header(f"📅 {project_no} 專案會議紀錄")
    st.caption("資料已儲存在當前瀏覽器會話中 (Session State)。")
    
    # 輔助函式：更新 session state
    def update_dataframe(new_df):
        st.session_state[STATE_KEY] = new_df
        # 不需要 st.experimental_rerun()，Streamlit 會自動重跑

    # 2. 新增記錄功能
    with st.form("add_form", clear_on_submit=True):
        st.subheader("➕ 新增會議記錄")
        col1, col2 = st.columns(2)
        
        with col1:
            d = st.date_input("日期", value=date.today())
            loc = st.text_input("地點", key=f"add_loc_{project_no}")
            sub = st.text_input("主題", key=f"add_sub_{project_no}")
        with col2:
            host = st.text_input("主持人", key=f"add_host_{project_no}")
            att = st.text_area("出席人員 (請用逗號分隔)", key=f"add_att_{project_no}")
        
        note = st.text_area("會議記錄", height=150, key=f"add_note_{project_no}")
        
        submit = st.form_submit_button("✅ 新增記錄")
        
        if submit:
            new_record = {
                "日期": d,
                "地點": loc,
                "主題": sub,
                "主持人": host,
                "出席人員": att,
                "會議記錄": note
            }
            # 使用 pd.concat 避免直接修改 state 中的 df
            df_new = pd.DataFrame([new_record], columns=columns)
            updated_df = pd.concat([df, df_new], ignore_index=True)
            update_dataframe(updated_df)
            st.success("✅ 會議記錄已新增！")


    # 3. 顯示表格
    st.subheader("📋 所有會議記錄")
    st.dataframe(df, use_container_width=True)
    
    # 4. 修改 / 刪除區塊
    if not df.empty:
        total_rows = len(df)
        st.subheader("✏️ 修改或刪除記錄")
        
        # 選擇索引
        idx = st.number_input(
            "選擇要操作的列索引 (從 0 開始)", 
            min_value=0, 
            max_value=total_rows - 1, 
            step=1, 
            key=f"select_idx_{project_no}"
        )
        
        selected_row = df.iloc[idx]
        
        # --- 修改功能 ---
        with st.expander(f"編輯第 {idx} 列 ({selected_row['主題']})"):
            with st.form("edit_form"):
                # 確保日期是 date 物件
                current_date = pd.to_datetime(selected_row["日期"]).date()
                
                d_edit = st.date_input("新日期", value=current_date, key=f"edit_date_{project_no}")
                loc_edit = st.text_input("新地點", value=selected_row["地點"], key=f"edit_loc_{project_no}")
                sub_edit = st.text_input("新主題", value=selected_row["主題"], key=f"edit_sub_{project_no}")
                host_edit = st.text_input("新主持人", value=selected_row["主持人"], key=f"edit_host_{project_no}")
                att_edit = st.text_area("新出席人員", value=selected_row["出席人員"], key=f"edit_att_{project_no}")
                note_edit = st.text_area("新會議記錄", value=selected_row["會議記錄"], height=150, key=f"edit_note_{project_no}")
                
                ok = st.form_submit_button("💾 確認修改並儲存")
                
                if ok:
                    # 直接在 DataFrame 上更新資料 (Pandas 建議使用 .loc)
                    df.loc[idx, "日期"] = d_edit
                    df.loc[idx, "地點"] = loc_edit
                    df.loc[idx, "主題"] = sub_edit
                    df.loc[idx, "主持人"] = host_edit
                    df.loc[idx, "出席人員"] = att_edit
                    df.loc[idx, "會議記錄"] = note_edit
                    
                    update_dataframe(df.copy()) # 傳入副本以確保 Streamlit 偵測到變化
                    st.success(f"第 {idx} 列記錄已成功修改！")

        # --- 刪除功能 ---
        if st.button("🗑️ 刪除此列記錄", key=f"delete_btn_{project_no}"):
            updated_df = df.drop(idx).reset_index(drop=True)
            update_dataframe(updated_df)
            st.warning(f"第 {idx} 列記錄已刪除！")
            st.rerun() # 刪除後強制重跑以更新索引範圍


    # 5. 匯出功能
    if not df.empty:
        st.subheader("📤 資料匯出")
        
        # 匯出為 CSV (使用 io.StringIO)
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False, encoding='utf-8-sig')
        csv_data = csv_buffer.getvalue()
        
        st.download_button(
            label="下載 CSV（中文支援）",
            data=csv_data,
            file_name=f"Meeting_{project_no}.csv",
            mime='text/csv',
            help="推薦使用 CSV 格式匯出，中文支援度高。"
        )

        # 匯出為 Excel (使用 io.BytesIO)
        excel_buffer = io.BytesIO()
        try:
            # 這裡需要 openpyxl 或 xlsxwriter 函式庫，如果您的環境沒有安裝，此處會失敗
            df.to_excel(excel_buffer, index=False, engine='xlsxwriter') # 嘗試使用 xlsxwriter 引擎
            excel_data = excel_buffer.getvalue()
            st.download_button(
                label="下載 Excel (XLSX)",
                data=excel_data,
                file_name=f"Meeting_{project_no}.xlsx",
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                help="如果下載失敗，請安裝 openpyxl 或 xlsxwriter：pip install xlsxwriter"
            )
        except Exception:
            st.info("⚠️ 注意：若要下載 Excel 檔案，您的環境需要安裝 `openpyxl` 或 `xlsxwriter` 函式庫。")


# 應用程式主入口
def main():
    st.set_page_config(layout="wide", page_title="專案會議紀錄工具")
    st.title("簡易專案會議記錄管理應用 (Streamlit)")
    
    # 簡單的專案選擇/輸入
    project_options = ["PJ202501", "PJ202502", "PJ202503"]
    selected_project = st.selectbox("請選擇或輸入專案編號", project_options + ["--- 輸入新專案編號 ---"])
    
    project_no = ""
    if selected_project == "--- 輸入新專案編號 ---":
        new_project = st.text_input("輸入新的專案編號 (例如: PJ202601)")
        if new_project:
            project_no = new_project
    else:
        project_no = selected_project

    if project_no:
        render_meeting(project_no)
    else:
        st.info("請選擇一個專案或輸入新的專案編號開始記錄。")

if __name__ == '__main__':
    main()
