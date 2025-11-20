import streamlit as st
import pandas as pd
from datetime import date
import io
import os

# 設置頁面標題和佈局
st.set_page_config(layout="wide", page_title="專案會議紀錄管理")

def render_meeting(project_no):
    """
    渲染特定專案的會議紀錄介面。
    
    Args:
        project_no (str): 專案編號。
    """
    st.header(f"{project_no} 專案會議紀錄")
    
    # 使用 Streamlit 的 Session State 來模擬專案ID，如果沒有則設定一個預設值
    # 實際應用中，這會是您程式設計上定義的專案名稱或編號
    csv_path = f"Meeting_{project_no}.csv"
    columns = ["日期", "地點", "主題", "主持人", "出席人員", "會議記錄"]

    # 1. 讀取資料
    # 檢查檔案是否存在，否則創建一個空的 DataFrame
    try:
        if os.path.exists(csv_path):
            # 讀取現有 CSV 檔案
            df = pd.read_csv(csv_path, encoding="utf-8-sig")
            # 確保日期欄位是日期類型，以便於日期輸入元件處理
            df['日期'] = pd.to_datetime(df['日期']).dt.date
        else:
            # 檔案不存在，創建一個空的 DataFrame
            df = pd.DataFrame(columns=columns)
            # 寫入一個空文件，確保後續操作不會因為文件不存在而失敗
            df.to_csv(csv_path, index=False, encoding="utf-8-sig")
    except Exception as e:
        st.error(f"讀取資料時發生錯誤: {e}")
        df = pd.DataFrame(columns=columns)

    # 2. 新增功能表單
    st.subheader("新增會議記錄")
    with st.form("add_form", clear_on_submit=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            d = st.date_input("日期", value=date.today())
        with col2:
            loc = st.text_input("地點", placeholder="會議室名稱")
        with col3:
            sub = st.text_input("主題", placeholder="會議主題概要")
            
        col4, col5 = st.columns(2)
        with col4:
            host = st.text_input("主持人", placeholder="姓名")
        with col5:
            att = st.text_input("出席人員", placeholder="請以逗號分隔")
            
        note = st.text_area("會議記錄", placeholder="輸入詳細會議內容及決議事項", height=150)
        
        submit = st.form_submit_button("新增記錄")
        if submit:
            df_new = pd.DataFrame([[d, loc, sub, host, att, note]], columns=columns)
            # 將日期轉換為字串格式以便儲存
            df_new['日期'] = df_new['日期'].astype(str)
            
            df = pd.concat([df, df_new], ignore_index=True)
            df.to_csv(csv_path, index=False, encoding="utf-8-sig")
            st.success("已成功新增記錄！")
            # 使用 st.rerun() 強制 Streamlit 重新執行腳本，從而載入最新的 CSV 數據
            st.experimental_rerun()


    # 3. 顯示表格
    st.subheader("所有會議記錄")
    st.dataframe(df, use_container_width=True, hide_index=True)

    # 4. 修改與刪除功能
    if len(df) > 0:
        st.subheader("修改與刪除記錄")
        
        # 讓使用者選擇要操作的列索引 (從 0 開始)
        idx = st.number_input(
            "選擇作業列 (0 起)", 
            min_value=0, 
            max_value=len(df) - 1, 
            step=1, 
            key='select_index_op'
        )
        
        st.markdown(f"**當前選擇的列索引: {idx}**")
        
        # 創建兩個按鈕來控制修改或刪除操作的狀態
        col_edit, col_delete = st.columns(2)
        
        # 使用 Session State 來控制修改表單的顯示
        if 'show_edit_form' not in st.session_state:
            st.session_state.show_edit_form = False
        
        # 點擊「修改本列」按鈕，切換顯示狀態
        if col_edit.button("修改本列資料"):
             # 切換 Session State，但在 Streamlit 中，按鈕點擊後的表單顯示邏輯會變得複雜
             # 為了貼近您的原始邏輯 (依賴 rerun)，我們仍會直接在按鈕點擊後處理
             st.session_state.show_edit_form = not st.session_state.show_edit_form
             if st.session_state.show_edit_form:
                 # 強制重跑以確保在點擊後立即顯示表單
                 st.experimental_rerun()
        
        # 刪除功能
        if col_delete.button("刪除此列資料"):
            # 必須先將 df.drop 的結果賦值回 df
            df = df.drop(idx).reset_index(drop=True)
            df.to_csv(csv_path, index=False, encoding="utf-8-sig")
            st.success(f"已刪除第 {idx} 列記錄！")
            st.experimental_rerun()
            
        # 5. 修改功能表單 (只有在 show_edit_form 為 True 時顯示)
        if st.session_state.show_edit_form:
            st.markdown("---")
            st.subheader(f"修改第 {idx} 列記錄")
            
            # 使用一個新的 form 來處理修改
            with st.form("edit_form"):
                
                # 重新讀取該行數據
                current_row = df.loc[idx]
                
                # 將儲存為 date 物件的日期轉換回 datetime 物件，以便 date_input 顯示正確
                current_date = pd.to_datetime(current_row["日期"])
                
                col1_e, col2_e, col3_e = st.columns(3)
                with col1_e:
                    d_e = st.date_input("新日期", value=current_date)
                with col2_e:
                    loc_e = st.text_input("新地點", value=current_row["地點"])
                with col3_e:
                    sub_e = st.text_input("新主題", value=current_row["主題"])
                    
                col4_e, col5_e = st.columns(2)
                with col4_e:
                    host_e = st.text_input("新主持人", value=current_row["主持人"])
                with col5_e:
                    att_e = st.text_input("新出席人員", value=current_row["出席人員"])
                    
                note_e = st.text_area("新會議記錄", value=current_row["會議記錄"], height=150)
                
                ok = st.form_submit_button("確認修改並儲存")
                
                if ok:
                    # 更新 DataFrame
                    df.loc[idx] = [d_e, loc_e, sub_e, host_e, att_e, note_e]
                    # 將日期轉換為字串格式以便儲存
                    df.loc[idx, '日期'] = str(d_e)
                    
                    df.to_csv(csv_path, index=False, encoding="utf-8-sig")
                    st.success(f"已成功修改第 {idx} 列記錄！")
                    
                    # 提交後隱藏表單
                    st.session_state.show_edit_form = False
                    
                    # 使用 st.rerun() 重新載入數據並更新顯示
                    st.experimental_rerun()
                    

    # 6. 匯出功能
    st.markdown("---")
    if not df.empty:
        # 匯出為 csv 並加上 BOM (確保 Excel 開啟中文不亂碼)
        csv = df.to_csv(index=False, encoding='utf-8-sig').encode('utf-8-sig')
        st.download_button(
            label="下載 CSV 檔案（中文支援）",
            data=csv,
            file_name=f"Meeting_{project_no}.csv",
            mime='text/csv'
        )

# --- 應用程式入口點 ---
# 設置一個預設的專案編號
default_project_id = st.sidebar.text_input("輸入專案編號 (例如: PJ202501)", "PJ202501")

if default_project_id:
    render_meeting(default_project_id)
else:
    st.warning("請在側邊欄輸入一個專案編號以開始使用。")
