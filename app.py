from flask import Flask, render_template, jsonify
import pandas as pd
import os
from datetime import timedelta
import logging
from dotenv import load_dotenv # 1. 引入 load_dotenv
from config import config_by_name # 引入設定

load_dotenv() # 2. 在程式一開始就載入 .env 檔案

app = Flask(__name__)

# 根據環境變數載入設定
# 這段程式碼現在可以無縫地從 .env 檔案或終端機設定中讀取 FLASK_ENV
env = os.getenv('FLASK_ENV', 'development')
app.config.from_object(config_by_name[env])

# Basic logging configuration to see errors in the terminal
logging.basicConfig(level=logging.INFO)

# 從 app.config 取得資料夾路徑，而不是寫死
VISITS_FILE = os.path.join(app.config['DATA_FOLDER'], "visits_data.csv")

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/api/data")
def get_data():
    try:
        # 讀取資料
        try:
            df = pd.read_csv(VISITS_FILE, parse_dates=['GamingDate'])
        except FileNotFoundError:
            logging.error(f"Data file not found: {VISITS_FILE}")
            return jsonify({
                'scorecard_data': [], 'chart_data': {'dates': [], 'datasets': []}, 'latest_date': 'File Not Found'
            })

        if df.empty:
            logging.warning(f"Data file is empty: {VISITS_FILE}")
            return jsonify({
                'scorecard_data': [], 'chart_data': {'dates': [], 'datasets': []}, 'latest_date': 'No Data'
            })

        # 找出最新日期
        latest_date = df['GamingDate'].max()
        
        # 最新日期的資料 (for scorecards)
        latest_data = df[df['GamingDate'] == latest_date]
        scorecard_data = latest_data.to_dict(orient='records')

        # 最近30天的歷史資料 (for chart)
        thirty_days_ago = latest_date - timedelta(days=30)
        date_range_index = pd.date_range(start=thirty_days_ago, end=latest_date, freq='D')
        
        chart_data_df = df[df['GamingDate'].between(thirty_days_ago, latest_date)]
        
        pivot_df = chart_data_df.pivot_table(
            index='GamingDate', 
            columns='ReportGroup', 
            values='Total HeadCount',
            aggfunc='sum'
        )
        pivot_df = pivot_df.reindex(date_range_index).fillna(0)

        # 轉換成適合圖表的格式
        chart_data = { 'dates': pivot_df.index.strftime('%Y-%m-%d').tolist() }
        datasets = []
        for group in pivot_df.columns:
            datasets.append({
                'label': group,
                'data': pivot_df[group].tolist(),
                'fill': False,
                'tension': 0.1
            })
        chart_data['datasets'] = datasets

        return jsonify({
            'scorecard_data': scorecard_data,
            'chart_data': chart_data,
            'latest_date': latest_date.strftime('%Y-%m-%d')
        })

    except Exception as e:
        logging.error(f"An error occurred in /api/data: {e}", exc_info=True)
        error_response = jsonify(message="Error processing data on server", error=str(e))
        error_response.status_code = 500
        return error_response

if __name__ == "__main__":
    app.run(debug=app.config['DEBUG'])
