from flask import Flask, render_template, jsonify
import pandas as pd
import os
from datetime import timedelta
import logging
from dotenv import load_dotenv # 1. 引入 load_dotenv
from config import config_by_name # 引入設定
from classes.CSVSource import CSVSource
from classes.ExcelDataSource import BrandHealthSource
from classes.PageMetricOverviewProcessors import PropertyVisitationProcessor, BrandHealthProcessor

# Basic logging configuration to see errors in the terminal
logging.basicConfig(level=logging.INFO)

load_dotenv() # 2. 在程式一開始就載入 .env 檔案

app = Flask(__name__)

# 根據環境變數載入設定
# 這段程式碼現在可以無縫地從 .env 檔案或終端機設定中讀取 FLASK_ENV
env = os.getenv('FLASK_ENV', 'development')
app.config.from_object(config_by_name[env])

# Read metric data
# Internal:
# 1. property visitation 
# 2. F&B Covers
VISITS_FILE = os.path.join(app.config['DATA_FOLDER'], "visits_data.csv")
# External:
# 1. Brand health
# 2. Macau visitation and GGR
# 3. Social SOV (from Newrank?)
# 4. Social search index (from Newrank?)
# 5. Digital spend (from AdMango and CTR)
BRAND_HEALTH_FILE = os.path.join(app.config['DATA_FOLDER'], "BHT - Rolling 3 months KPI.xlsx")

# Register data sources. Add more data sources here as needed
DATA_SOURCES = {
    "property_visits": CSVSource(VISITS_FILE, parse_dates=['GamingDate']),
    "brand_health": BrandHealthSource(BRAND_HEALTH_FILE),
    # "some_db": DBSource("mysql+pymysql://user:pass@host/db", "SELECT * FROM table"),
}

@app.route("/")
def home():
    # 準備兩組 overview data
    df_visitation = DATA_SOURCES['property_visits'].load()
    visitation_data = PropertyVisitationProcessor(df_visitation).process()
    visitation_data['title'] = 'Property Visitation'

    df_brand = DATA_SOURCES['brand_health'].load()
    brand_data = BrandHealthProcessor(df_brand).process()
    brand_data['title'] = 'Brand Health'

    return render_template(
        "home.html",
        visitation_data=visitation_data,
        brand_data=brand_data
    )

 
"""
TODO: Data processors for other HTML pages
"""


if __name__ == "__main__":
    app.run(debug=app.config['DEBUG'])
