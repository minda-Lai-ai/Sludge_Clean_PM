import streamlit as st
import pandas as pd
from datetime import date
import io

def render_insurance(project_no):
    st.header(f"{project_no} 專案保險管理")
    csv_path = f"Bao-Xian_{project_no}.csv"
    preset_engineer = ["雇主意外責任險", "營繕承包商意外責任險", "自訂工程保險"]
    preset_people = ["團險1", "團險2", "勞保", "健保", "健檢", "自訂人員保險"]
    columns = ["保險分類", "保險項目", "保險公司", "保險額度", "保險開始日", "保險到期日", "被保人", "備註"]

    # 讀取CSV
    try:
        df = pd.read_csv(csv_path, dtype=str).fillna('')
    except Exception:
        df = pd.DataFrame(columns=columns)

    # 新增資料
    with st.expander("新增保險資料"):
        colA, colB = st.columns(2)
        with colA:
            is_engineer = st.radio("保險分類", ["工程", "人員"])
        if is_engineer == "工程":
            item = st.selectbox("項目", preset_engineer)
        else:
            item = st.selectbox("項目", preset_people)
        company = st.text_input("保險公司")
        amount = st.text_input("額度")
        start = st.date_input("開始日", value=date.today())
        end = st.date_input("到期日", value=date.today())
        person = st.text_input("被保人")
        note = st.text_area("備註")
        if st.button("新增儲存"):
            new_row = {
                "保險分類": is_engineer,
                "保險項目": item,
                "保險公司": company,
                "保險額度": amount,
                "保險開始日": str(start),
                "保險到期日": str(end),
                "被保人": person,
                "備註": note
            }
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            df.to_csv(csv_path, index=False)
            st.success("已新增！請下方確認資料表")


    # 資料編輯列
    st.subheader("保險資料清單（點選欲「修改/刪除」資料列）")
    if not df.empty:
        key_edit = st.text_input("欲修改資料列編號(0起算)", value="", placeholder="輸入列數後按Enter")
        key_del = st.text_input("欲刪除資料列編號(0起算)", value="", placeholder="輸入列數後按Enter", key="del_row")
        st.dataframe(df, use_container_width=True)

        # 修改功能
        if key_edit.isdigit():
            idx = int(key_edit)
            if 0 <= idx < len(df):
                st.markdown("### 編輯保險內容")
                row = df.iloc[idx]
                c0, c1 = st.columns(2)
                with c0:
                    edit_class = st.selectbox("保險分類", ["工程", "人員"], index=0 if row["保險分類"] == "工程" else 1, key=f"class_{idx}") 
                    edit_item = st.text_input("保險項目", value=row["保險項目"], key=f"item_{idx}")
                    edit_company = st.text_input("保險公司", value=row["保險公司"], key=f"company_{idx}")
                    edit_amt = st.text_input("額度", value=row["保險額度"], key=f"amt_{idx}")
                    edit_start = st.text_input("開始日", value=row["保險開始日"], key=f"start_{idx}")
                with c1:
                    edit_end = st.text_input("到期日", value=row["保險到期日"], key=f"end_{idx}")
                    edit_person = st.text_input("被保人", value=row["被保人"], key=f"person_{idx}")
                    edit_note = st.text_area("備註", value=row["備註"], key=f"note_{idx}")                    
                if st.button("新增儲存"):
                    # 存檔邏輯
                    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                    df.to_csv(csv_path, index=False)
                    st.success("已新增！")
                    # 主動重讀 csv 以顯示新資料
                    df = pd.read_csv(csv_path)
                

        # 刪除功能
        if key_del.isdigit():
            idx = int(key_del)
            if 0 <= idx < len(df):
                if st.button(f"確認刪除第{idx}列", key="del_btn"):
                    df = df.drop(idx).reset_index(drop=True)
                    df.to_csv(csv_path, index=False)
                    st.warning(f"第{idx}列已刪除")
                    st.experimental_rerun()

    else:
        st.info("目前沒有任何資料")

    # 下載按鈕
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    st.download_button("下載CSV", data=csv_buffer.getvalue(), file_name=f"Bao-Xian_{project_no}.csv", mime="text/csv")
