import streamlit as st
from datetime import date

# --- 修正點：模組已移至 modules/ 子目錄，恢復匯入路徑 ---
from modules.insurance import render_insurance
from modules.meeting import render_meeting
from modules.sludge import render_sludge
from modules.work import render_work
from modules.member import render_member
# --------------------------------------------------------------------

# 下面主頁資訊與原本相同

st.set_page_config(page_title="XX專案1 - PJ202501 主頁", layout="wide")
st.title("XX專案1 - PJ202501 主頁")
st.link_button("回到主選單", "/")

# 基本資訊
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

# 專案狀態計算
today = date.today()
start = date(2025,1,1)
end = date(2025,1,31)
if start <= today <= end: project_status = "進行中"
elif today < start: project_status = "準備中"
elif today > end: project_status = "已完成 (延遲)" # 修正：專案結束應該是已完成，但可以備註延遲
else: project_status = "已完成" # 預防性加入 else

st.write(f"專案狀況: {project_status}")

st.divider()

# 次頁面導航
subpage = st.radio("次頁面", ["保險", "會議", "公證量油", "施工紀要", "成員矩陣"])
project_no = basic_info["工作案號"]

if subpage == "保險":
    render_insurance(project_no)
elif subpage == "會議":
    render_meeting(project_no)
elif subpage == "公證量油":
    render_sludge(project_no)
elif subpage == "施工紀要":
    render_work(project_no)
elif subpage == "成員矩陣":
    render_member(project_no)
