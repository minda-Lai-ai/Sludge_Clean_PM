import streamlit as st
import pandas as pd

def render_member(project_no):
    csv_path = f"Member_{project_no}.csv"
    columns = ["單位", "姓名", "職務類別", "相關證照", "登錄協議組織紀錄", "聯絡方式", "代理人", "其他"]

    # 初始化 session_state
    if f"member_df_{project_no}" not in st.session_state:
        try:
            df = pd.read_csv(csv_path, encoding="utf-8-sig")
        except Exception:
            df = pd.DataFrame(columns=columns)
        st.session_state[f"member_df_{project_no}"] = df
    else:
        df = st.session_state[f"member_df_{project_no}"]

    st.header(f"成員矩陣 (案號: {project_no})")
    st.markdown("### 專案參與人員清單")

    # 顯示序號欄
    if len(df) > 0:
        display_df = df.copy()
        display_df.insert(0, "序號", range(len(df)))
        st.dataframe(display_df, use_container_width=True, hide_index=True)
    else:
        st.info("目前尚無任何人員資料。")

    # 新增成員
    with st.expander("➕ 新增成員"):
        with st.form("add_member_form"):
            unit = st.text_input("單位")
            name = st.text_input("姓名")
            duty = st.text_input("職務類別")
            cert = st.text_input("相關證照")
            reg = st.selectbox("登錄協議組織紀錄", ["是", "否"])
            phone = st.text_input("聯絡方式")
            proxy = st.text_input("代理人")
            note = st.text_input("其他")
            submitted = st.form_submit_button("新增")
            if submitted:
                new_row = pd.DataFrame([[unit, name, duty, cert, reg, phone, proxy, note]], columns=columns)
                df = pd.concat([df, new_row], ignore_index=True)
                df.to_csv(csv_path, index=False, encoding="utf-8-sig")
                st.session_state[f"member_df_{project_no}"] = df
                st.success("新增成功！")

    # 編輯/刪除
    if len(df) > 0:
        idx = st.number_input("請選擇人員序號進行編輯或刪除", min_value=0, max_value=len(df)-1, step=1)
        col1, col2 = st.columns(2)
        with col1:
            if st.button("編輯選取成員", key=f"edit_member_{project_no}"):
                with st.form("edit_member_form"):
                    unit = st.text_input("單位", value=df.loc[idx, "單位"])
                    name = st.text_input("姓名", value=df.loc[idx, "姓名"])
                    duty = st.text_input("職務類別", value=df.loc[idx, "職務類別"])
                    cert = st.text_input("相關證照", value=df.loc[idx, "相關證照"])
                    reg = st.selectbox("登錄協議組織紀錄", ["是", "否"], index=0 if df.loc[idx, "登錄協議組織紀錄"]=="是" else 1)
                    phone = st.text_input("聯絡方式", value=df.loc[idx, "聯絡方式"])
                    proxy = st.text_input("代理人", value=df.loc[idx, "代理人"])
                    note = st.text_input("其他", value=df.loc[idx, "其他"])
                    ok = st.form_submit_button("確認修改")
                    if ok:
                        df.loc[idx] = [unit, name, duty, cert, reg, phone, proxy, note]
                        df.to_csv(csv_path, index=False, encoding="utf-8-sig")
                        st.session_state[f"member_df_{project_no}"] = df
                        st.success("已完成編輯")
        with col2:
            if st.button("刪除選取成員", key=f"del_member_{project_no}"):
                df = df.drop(idx).reset_index(drop=True)
                df.to_csv(csv_path, index=False, encoding="utf-8-sig")
                st.session_state[f"member_df_{project_no}"] = df
                st.success("已刪除該成員")

        # 匯出
        csv = df.to_csv(index=False, encoding="utf-8-sig")
        st.download_button(
            label="下載人員清單 CSV（中文支援）",
            data=csv,
            file_name=f"Member_{project_no}.csv",
            mime='text/csv'
        )

# 用法範例
# render_member("PJ202501")

