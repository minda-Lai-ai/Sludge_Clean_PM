import streamlit as st

# 注意：st.set_page_config() 和 st.title() 已移除，應在 pages/PJ202501.py 中處理

# --- 修正點：將函式名稱改為 render_sludge 且接受 project_no 參數 ---
def render_sludge(project_no):
    """
    渲染公證量油數據的次頁面內容。

    Args:
        project_no (str): 目前專案的工作案號。
    """
    st.header(f"公證量油數據 (案號: {project_no})")
    
    st.markdown("---") # 分隔線
    
    # 使用 Streamlit columns 讓資訊排版更整齊
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**公證量油廠商**：公證檢測公司")
        st.write("**公證量油時間**：2025-01-18")
        st.write("**報告提供日期**：2025-01-20")
        st.write("**公證量油油泥量**：5.6 公秉")
    
    with col2:
        st.write("---") # 讓第二欄也有垂直對齊的空間

        # 圖片上傳區
        st.write("**上傳現場圖片**：")
        st.file_uploader("選擇圖片", accept_multiple_files=True, key=f"sludge_upload_{project_no}")
        
        # 匯入 Excel 功能的佔位符
        st.info("公證量油數據：(匯入公證Excel功能)")
        
    pass # 函式執行結束
