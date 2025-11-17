import streamlit as st
from datetime import date
import os

st.set_page_config(page_title="Minda的專案管理系統", layout="wide")
st.title("Minda的專案管理系統")

menu = st.radio("主選單", ["執行中的專案", "新增專案", "歷史專案"])

if "active_projects" not in st.session_state:
    st.session_state["active_projects"] = [{"name": "XX專案1", "no": "PJ202501"}, {"name": "YY專案2", "no": "PJ202411"}]
if "history_projects" not in st.session_state:
    st.session_state["history_projects"] = [{"name": "ZZ專案3", "no": "PJ202301", "start": date(2023,6,1)}, 
                                            {"name": "AA專案4", "no": "PJ202210", "start": date(2022,10,15)}]

if menu == "執行中的專案":
    st.subheader("執行中的專案")
    for proj in sorted(st.session_state["active_projects"], key=lambda x: x["no"], reverse=True):
        proj_no = proj["no"]
        if st.button(f"{proj['name']} │ 案號：{proj_no}", key=f"pj_open_{proj_no}"):
           st.session_state["open_project_no"] = proj_no
#            st.switch_page(f"PJ_{proj_no}.py")
           st.write("pages中現在有：", [f for f in os.listdir("pages") if f.endswith(".py")])
# minda
        pages = ["PJ202501.py", "PJ202502.py", "LMD113249.py"]    
        selected_page = st.selectbox("選擇專案", pages)
        if st.button("進入專案"):
            st.switch_page(selected_page)
# minda

elif menu == "新增專案":
    st.subheader("新增專案")
    new_name = st.text_input("專案名稱")
    new_no = st.text_input("工作案號")
    if st.button("建立"):
        if new_name and new_no:
            st.session_state["active_projects"].insert(0, {"name": new_name, "no": new_no})
            st.success("專案已建立！")
        else:
            st.error("請完整填寫")
elif menu == "歷史專案":
    st.subheader("歷史專案")
    for proj in sorted(st.session_state["history_projects"], key=lambda x: x["start"], reverse=True):
        st.markdown(f"**{proj['name']}** │ 案號：{proj['no']} │ 開案日：{proj['start']}")







