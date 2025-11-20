import streamlit as st
import pandas as pd

# 注意：st.set_page_config() 和 st.title() 已移除，應在 pages/PJ202501.py 中處理

# --- 修正點：將函式名稱改為 render_member 且接受 project_no 參數 ---
def render_member(project_no):
    """
    渲染成員矩陣的次頁面內容。

    Args:
        project_no (str): 目前專案的工作案號。
    """
    st.header(f"成員矩陣 (案號: {project_no})")
    
    # 建立範例 DataFrame
    df = pd.DataFrame([
        {"單位":"A單位", "姓名":"張三", "職務類別":"工安", "相關證照":"甲種職業作業主管", "登錄協議組織紀錄":"是", "聯絡方式":"0912345678", "代理人":"李四", "其他":""},
        {"單位":"A單位", "姓名":"張三", "職務類別":"工安", "相關證照":"甲種職業作業主管", "登錄協議組織紀錄":"是", "聯絡方式":"0912345678", "代理人":"李四", "其他":""},
    ])
    
    st.markdown("### 專案參與人員")
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    # 編輯與儲存按鈕
    col1, col2 = st.columns(2)
    with col1:
        if st.button("編輯", key=f"member_edit_{project_no}"):
            st.info("進入可編輯模式（建議使用st.form）")
    with col2:
        if st.button("儲存", key=f"member_save_{project_no}"):
            st.success("已儲存")
            
    # 提醒：如果您希望使用者可以編輯表格，可以考慮使用 st.data_editor 或 st.experimental_data_editor
