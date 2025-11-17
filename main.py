import streamlit as st
from datetime import date
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "modules")))


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

# 嘗試取得目前 pages/ 中所有分頁檔案
try:
    page_py_files = [f for f in os.listdir("pages") if f.endswith(".py")]
except FileNotFoundError:
    page_py_files = [] 

if menu == "執行中的專案":
    st.subheader("執行中的專案")
    for proj in sorted(st.session_state["active_projects"], key=lambda x: x["no"], reverse=True):
        proj_no = proj["no"]
        py_filename = f"{proj_no}.py" if proj_no.startswith("PJ") or proj_no.startswith("LMD") else f"PJ_{proj_no}.py"

        # 檢查目前 pages/ 下是否有這個檔案
        if py_filename not in page_py_files:
            st.warning(f"找不到專案主頁：pages/{py_filename}（請確認 pages/ 有此檔案）")     
        else:
            if st.button(f"{proj['name']} │ 案號：{proj_no}", key=f"pj_open_{proj_no}"):
                # --- 修正點：使用完整的相對路徑 ---
                page_path = f"pages/{py_filename}"
                try:
                    st.switch_page(page_path)
                except Exception as e:
                    st.error(f"切換頁面失敗！請確認檔案路徑：`{page_path}` 是否正確。")
                    st.code(f"錯誤詳情：{e}", language="text")


elif menu == "新增專案":
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
    st.subheader("歷史專案")
    for proj in sorted(st.session_state["history_projects"], key=lambda x: x["start"], reverse=True):
        st.markdown(f"**{proj['name']}** │ 案號：{proj['no']} │ 開案日：{proj['start']}")



