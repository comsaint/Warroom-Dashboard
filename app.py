from flask import Flask, render_template
import pandas as pd
import os

app = Flask(__name__)

DATA_FOLDER = os.path.join("data", "mockup")
VISITS_FILE = os.path.join(DATA_FOLDER, "visits_data.csv")

@app.route("/")
def home():
    # 讀取資料
    df = pd.read_csv(VISITS_FILE)
    # 找出最新日期
    latest_date = df['Date'].max()
    latest_data = df[df['Date'] == latest_date]

    # 依 Property 分組
    gm_bw = latest_data[latest_data['Property'].isin(['GM', 'BW'])]
    casino_fb = latest_data[latest_data['Property'].isin(['Casino', 'F&B'])]

    # 轉成 list of dict 傳給模板
    gm_bw_list = gm_bw.to_dict(orient='records')
    casino_fb_list = casino_fb.to_dict(orient='records')

    return render_template(
        "home.html",
        gm_bw=gm_bw_list,
        casino_fb=casino_fb_list,
        latest_date=latest_date
    )

if __name__ == "__main__":
    app.run(debug=True)
