import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import st_folium

# 設定網頁標題與寬版排版
st.set_page_config(layout="wide", page_title="台灣區域天氣預報")

# 美化樣式 CSS
st.markdown("""<style>
.stApp {
    background-color: #FCFBF4;
    font-family: 'Helvetica Neue', Arial, 'Noto Sans TC', sans-serif;
}
.main-title {
    background-color: #E3F2FD;
    padding: 20px;
    border-radius: 15px;
    border-left: 8px solid #78A1BB;
    margin-bottom: 25px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.05);
}
.main-title h1 {
    color: #2C5E7A !important;
    margin: 0;
    font-size: 28px;
}
.main-title p {
    color: #5A7E95;
    margin: 5px 0 0 0;
    font-size: 14px;
}
.card {
    background-color: #FFFFFF;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.04);
    margin-bottom: 20px;
    border: 1px solid #F0EAD6;
}
.section-title {
    color: #3B6E8C;
    font-weight: bold;
    border-bottom: 2px solid #E3F2FD;
    padding-bottom: 8px;
    margin-bottom: 15px;
}
</style>""", unsafe_allow_html=True)

st.markdown("""
    <div class='main-title'>
        <h1>🗺️ 台灣區域天氣預報互動式地圖</h1>
        <p>提供您全台六大地區及離島的最新一週氣溫趨勢查詢</p>
    </div>
""", unsafe_allow_html=True)

conn = sqlite3.connect("data.db")
query_all = "SELECT regionName, dataDate, MinT, MaxT FROM TemperatureForecasts"
df_all = pd.read_sql_query(query_all, conn)
region_names = df_all["regionName"].unique()

region_coords = {
    "北部地區": [24.9, 121.3],
    "中部地區": [23.8, 120.8],
    "南部地區": [22.7, 120.4],
    "東北部地區": [24.6, 121.7],
    "東部地區": [23.9, 121.5],
    "東南部地區": [22.7, 121.0],
    "澎湖地區": [23.57, 119.58],
    "金門地區": [24.44, 118.37],
    "馬祖地區": [26.15, 119.95]
}

col1, col2 = st.columns([1.1, 1])

with col2:
    st.markdown("<div class='card'><h3 class='section-title'>🎯 快速選擇地區</h3>", unsafe_allow_html=True)
    selected_region = st.selectbox("請選擇欲查詢的地理區：", region_names)
    st.markdown("</div>", unsafe_allow_html=True)

with col1:
    st.markdown("<div class='card'><h3 class='section-title'>🗺️ 台灣地圖 (點擊圓圈直接切換地區)</h3>", unsafe_allow_html=True)
    m = folium.Map(location=[23.7, 121.0], zoom_start=7, tiles="OpenStreetMap")
    for region, coords in region_coords.items():
        region_latest = df_all[df_all["regionName"] == region]
        if not region_latest.empty:
            latest_row = region_latest.iloc[0]
            min_t = latest_row["MinT"]
            max_t = latest_row["MaxT"]
            popup_html = f"""
            <div style='font-family: sans-serif; font-size: 13px; line-height: 1.5;'>
                <b style='color:#2C5E7A;'>{region}</b><br>
                預報日期: {latest_row['dataDate']}<br>
                <span style='color: #4A90E2;'>❄️ 最低溫: {min_t}°C</span><br>
                <span style='color: #E25C5C;'>🔥 最高溫: {max_t}°C</span>
            </div>
            """
            tooltip_text = f"{region}: {min_t}°C ~ {max_t}°C"
            is_selected = (region == selected_region)
            folium.CircleMarker(
                location=coords,
                radius=14 if is_selected else 10,
                color="#78A1BB" if not is_selected else "#99C24D",
                fill=True,
                fill_color="#B5D6EB" if not is_selected else "#C5E1A5",
                fill_opacity=0.85,
                weight=3 if is_selected else 1.5,
                popup=folium.Popup(popup_html, max_width=180),
                tooltip=tooltip_text
            ).add_to(m)
    st_map = st_folium(m, height=450, width=580)
    st.markdown("</div>", unsafe_allow_html=True)

if st_map and st_map.get("last_object_clicked"):
    clicked_coords = [st_map["last_object_clicked"]["lat"], st_map["last_object_clicked"]["lng"]]
    for region, coords in region_coords.items():
        if abs(coords[0] - clicked_coords[0]) < 0.15 and abs(coords[1] - clicked_coords[1]) < 0.15:
            selected_region = region
            break

df_selected = df_all[df_all["regionName"] == selected_region].sort_values("dataDate")

with col2:
    st.markdown("<div class='card'><h3 class='section-title'>📈 氣溫變化趨勢</h3>", unsafe_allow_html=True)
    fig = px.line(
        df_selected,
        x="dataDate",
        y=["MinT", "MaxT"],
        labels={"value": "溫度 (°C)", "dataDate": "預報日期", "variable": "指標"},
        markers=True,
        color_discrete_map={"MinT": "#78A1BB", "MaxT": "#FF8C42"}
    )
    fig.update_layout(
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=20, r=20, t=10, b=20),
        hovermode="x unified",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)"
    )
    fig.update_xaxes(showgrid=True, gridcolor="#E3F2FD")
    fig.update_yaxes(showgrid=True, gridcolor="#E3F2FD")
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown(f"<div class='card'><h3 class='section-title'>📊 {selected_region} 一週預報詳細數據表</h3></div>", unsafe_allow_html=True)
st.dataframe(df_selected, use_container_width=True)
conn.close()
