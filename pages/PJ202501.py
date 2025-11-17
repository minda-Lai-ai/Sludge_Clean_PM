import streamlit as st
from datetime import date

st.set_page_config(page_title="XX專案1 - PJ202501 主頁", layout="wide")

st.title("XX專案1 - PJ202501 主頁")
st.link_button("回到主選單", "/")

# 專案基本資訊
basic_info = {
    "工作案號": "PJ202501",
    "預算編號": "B12345",
    "監造單位": "監造公司A",
    "監造姓名及分機": "王小明 | 1234",
    "轄區單位": "單位B",
    "轄區姓名及分機": "李小華 | 5678",
    "油槽清洗方式": "水洗",
    "油槽資訊": "油槽A, 柴油, 1000KL, 圓筒直立, (02)5555555, 其他備註",
    "清洗廠商資訊": "廠商A, 12345678, 吳老闆, (03)6666666, 許現場, 其他備註",
    "預計工期": "30 天",
    "工作期間": "2025-01-01 ~ 2025-01-31",
}

for k, v in basic_info.items():
    st.write(f"{k}: {v}")

# 專案狀況判斷
project_status = ""
today = date.today()
start = date(2025,1,1)
end = date(2025,1,31)
if start <= today <= end:
    project_status = "進行中"
elif today < start:
    project_status = "準備中"
elif today > end:
    project_status = "延遲"
st.write(f"專案狀況: {project_status}")

st.divider()
subpage = st.radio("次頁面", ["保險", "會議", "公證量油", "施工紀要", "成員矩陣"])

# 分頁資料互動區
if subpage == "保險":
    from insurance import render_insurance
    render_insurance(project_no=basic_info["工作案號"])
elif subpage == "會議":
    from meeting import render_meeting
    render_meeting(project_no=basic_info["工作案號"])
elif subpage == "公證量油":
    from sludge import render_sludge
    render_sludge(project_no=basic_info["工作案號"])
elif subpage == "施工紀要":
    from work import render_work
    render_work(project_no=basic_info["工作案號"])
elif subpage == "成員矩陣":
    from member import render_member
    render_member(project_no=basic_info["工作案號"])
