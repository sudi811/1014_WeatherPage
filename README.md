# 🗺️ 台灣區域天氣預報互動式地圖

### 🔗 網頁即時預覽 (Live App)
👉 **[https://buffer-have-geometry-invision.trycloudflare.com](https://buffer-have-geometry-invision.trycloudflare.com)**
*(註：網頁採用 Cloudflare Tunnel 託管，點擊即可直接開啟瀏覽)*

---

這是一個使用 **Streamlit**、**SQLite** 以及 **Folium (Leaflet)** 地圖技術打造的台灣一週氣溫預報互動式網頁 App。本專案資料介接自中央氣象署 (CWA) 開放資料 API。

### 🎨 專案特點
* **溫馨配色與卡片排版**：提供直覺流暢的視覺體驗。
* **互動式地圖連動**：點擊地圖上的區域圓圈，右側折線圖與下方數據表會自動即時同步更新。
* **離線資料快取**：使用 SQLite 資料庫儲存一週溫度預報數據。

### 📸 網頁畫面預覽
![網頁截圖](thumbnail.png)
