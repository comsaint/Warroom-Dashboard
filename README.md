# Warroom-Dashboard
A carousel dashboard showing high-level internal/external indices and data, for exhibition purpose in Executive Office.

## Features
- Carousel display of business metrics (e.g. Revenue, Visitation)
- Simple, full-screen dashboard for executive view

## Getting Started

### 1. 安裝依賴
請先安裝 Python 3.7+ 及 pip，然後安裝 Flask：

```
pip install flask
```

### 2. 啟動專案

在專案目錄下執行：

```
python app.py
```

啟動後，瀏覽器開啟 http://127.0.0.1:5000/ 即可看到輪播儀表板。

## Project Structure
```
app.py
README.md
templates/
    home.html
```

## Customization
- 修改 `app.py` 以新增或串接更多商業指標
- 調整 `templates/home.html` 以美化前端介面

---

歡迎依需求擴充資料來源與前端設計。
