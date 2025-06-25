import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import config

def generate_mock_visits_data(days=60):
    """
    產生一個 mock DataFrame，包含過去 days 天、四個 Property，每天每個 Property 一筆資料。
    """
    properties = ["GM Property Total", "BW Property Total", "SW Property Total", "GM Casino Total"]
    today = datetime.today()
    data = []
    for i in range(days):
        day = (today - timedelta(days=i)).strftime("%Y-%m-%d")
        for prop in properties:
            visits = np.random.randint(20000, 50000)
            data.append({
                "ReportGroup": prop,
                "GamingDate": day,
                "Total HeadCount": visits,
            })
    df = pd.DataFrame(data)
    return df


def main():
    if config.USE_MOCK_DATA:
        mock_folder = config.get_data_folder()
        df = generate_mock_visits_data()
        df.to_csv(f"{mock_folder}/visits_data.csv", index=False)
    else:
        print("Real data mode, no need to populate fake data.")
    return 0


if __name__ == "__main__":
    main()
