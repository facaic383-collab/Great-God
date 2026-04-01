import streamlit as st
import pandas as pd
from scraper.healthgrades import scrape_healthgrades
from scraper.yellowpages import scrape_yellowpages

st.set_page_config(page_title="美国牙医信息查询", page_icon="🦷", layout="wide")
st.title("🦷 美国牙医真实联系电话批量查询 (Healthgrades & YellowPages)")
st.caption("输入城市（英文连字符，如los-angeles）和州（如ca），可批量查询平台数据（仅展示电话号码，不抓邮箱）。数据仅供学习与统计使用。")

if 'history' not in st.session_state:
    st.session_state['history'] = []

with st.form("search_form"):
    col1, col2, col3 = st.columns([5,2,2])
    city = col1.text_input("城市(英文连字符，如 los-angeles)", "los-angeles")
    state = col2.text_input("州缩写(如 ca)", "ca")
    max_pages = col3.slider("最大抓取页数", 1, 10, 2)
    channel_options = st.multiselect(
        "采集平台",
        options=["Healthgrades", "YellowPages"],
        default=["Healthgrades", "YellowPages"]
    )
    submitted = st.form_submit_button("查询")

if submitted:
    st.info(f"正在抓取 {city.title()}, {state.upper()} ...")
    all_results = []
    if "Healthgrades" in channel_options:
        st.write("🔍 Healthgrades...")
        all_results.extend(scrape_healthgrades(city, state, max_pages))
    if "YellowPages" in channel_options:
        st.write("🔍 YellowPages...")
        all_results.extend(scrape_yellowpages(city, state, max_pages))
    if all_results:
        df = pd.DataFrame(all_results)
        st.session_state['history'].append(df)
        st.success(f"共抓取到 {len(df)} 位牙医")
        st.dataframe(df, use_container_width=True)
        csv = df.to_csv(index=False)
        st.download_button(
            label="导出本次结果为CSV",
            data=csv,
            file_name=f"dentists_{state}_{city}.csv",
            mime='text/csv'
        )
    else:
        st.error("未抓取到内容，可能无数据或目标结构变更。")

st.header("查询历史 / 批量导出")
if st.session_state.get('history'):
    for idx, df in enumerate(st.session_state['history']):
        with st.expander(f"第{idx+1}次查询 ({len(df)} 条)"):
            st.dataframe(df, use_container_width=True)
            csv = df.to_csv(index=False)
            st.download_button(
                label=f"导出第{idx+1}次为CSV",
                data=csv,
                file_name=f"batch_{idx+1}_dentists.csv",
                mime='text/csv',
                key=f"history-csv-{idx}"
            )
else:
    st.info("暂无历史记录。")

st.markdown("""
---
**提示**：城市用英文、短横线分隔。平台有反爬限制，大量采集请适当分批。页面结构调整时脚本需适配。
""")