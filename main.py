import streamlit as st
from datetime import date
import os

# --- 程式碼維持不變部分 ---

st.set_page_config(page_title="Minda的專案管理系統", layout="wide")
st.title("Minda的專案管理系統")

menu = st.radio("主選單", ["執行中的專案", "新增專案", "歷史專案"])

if "active_projects" not in st.session_state:
    st.session_state["active_projects"] = [
        {"name": "XX專案1", "no": "PJ202501"}, {"name": "YY專案2", "no": "PJ202411"}
    ]
if "history_projects" not in st.session_state:
    st.session_state["history_projects"] = [
        {"name": "ZZ專案3", "no": "PJ202301", "start": date(2023,6,1)}, {"name": "AA專案4", "no": "PJ202210", "start": date(2022,10,15)}
    ]

# 取得目前 pages/ 中所有分頁檔案
# 注意：這個檢查是為了提示使用者，但 st.switch_page 不會使用這個 list
# 我們保留這個檢查，但將 st.switch_page 的參數調整為 Streamlit 預期的格式
try:
    page_py_files = [f for f in os.listdir("pages") if f.endswith(".py")]
except FileNotFoundError:
    st.error("找不到 pages/ 目錄，多頁面功能可能無法正常運作。請確認您的應用程式根目錄下有 pages/ 目錄。")
    page_py_files = [] # 設為空列表，避免後續程式碼崩潰

# --- 專案執行區塊主要修正 ---

if menu == "執行中的專案":
    st.subheader("執行中的專案")
    for proj in sorted(st.session_state["active_projects"], key=lambda x: x["no"], reverse=True):
        proj_no = proj["no"]
        
        # 這是 pages/ 目錄下期望的檔案名稱
        py_filename = f"{proj_no}.py" if proj_no.startswith("PJ") or proj_no.startswith("LMD") else f"PJ_{proj_no}.py"
        
        # Streamlit 在切換頁面時，只需要 pages/ 下的檔案名稱（不含 .py 後綴），
        # 或者直接使用檔案名稱 (含 .py 後綴) 也可以，但它會自行檢查 pages/。
        # 最保險的做法是傳入 pages/ 下的檔案名稱（不含 .py 後綴，或直接傳入檔名）。
        # 由於您原程式碼使用 st.switch_page(py_filename) 報錯，
        # 並且 py_filename 已經是 pages/ 下的檔案名稱，
        # 我們假設問題出在 Streamlit 在您的環境下無法正確識別 pages/ 目錄。
        
        # 檢查 pages/ 下是否有這個檔案
        if py_filename not in page_py_files:
            st.warning(f"找不到專案主頁：pages/{py_filename}（請確認 pages/ 有此檔案）")
        else:
            # 修正後的 st.switch_page 呼叫：傳入 pages/ 下的檔案名稱 (含 .py)
            if st.button(f"{proj['name']} │ 案號：{proj_no}", key=f"pj_open_{proj_no}"):
                
                # --- 主要修正點：確保 pages/ 目錄下有 PJ202501.py 這個檔案存在 ---
                # st.switch_page 只需要頁面檔案名稱
                try:
                    st.switch_page(py_filename)
                except Exception as e:
                    # 如果再次失敗，給出更詳細的提示
                    st.error(f"切換頁面失敗：{py_filename}。請確認：")
                    st.markdown("* 1. 您的應用程式根目錄下有 **`pages/`** 子目錄。")
                    st.markdown(f"* 2. **`pages/`** 目錄內有 **`{py_filename}`** 檔案。")
                    st.markdown(f"* 3. 您的 **`main.py`**（或應用程式主檔案）不在 **`pages/`** 內。")
                    st.code(f"錯誤詳情：{e}", language="text")


elif menu == "新增專案":
    # --- 程式碼維持不變部分 ---
    st.subheader("新增專案")
    new_name = st.text_input("專案名稱")
    new_no = st.text_input("工作案號")
    if st.button("建立"):
        if new_name and new_no:
            st.session_state["active_projects"].insert(0, {"name": new_name, "no": new_no})
            st.success("專案已建立！請手動複製 pages/PJ範本或建立新專案檔案進入主頁")
        else:
            st.error("請完整填寫")

elif menu == "歷史專案":
    # --- 程式碼維持不變部分 ---
    st.subheader("歷史專案")
    for proj in sorted(st.session_state["history_projects"], key=lambda x: x["start"], reverse=True):
        st.markdown(f"**{proj['name']}** │ 案號：{proj['no']} │ 開案日：{proj['start']}")
