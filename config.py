# 設定是否使用 mockup 資料
USE_MOCK_DATA = True

# 資料夾路徑
MOCK_DATA_FOLDER = "data/mockup"
REAL_DATA_FOLDER = "data/real"

def get_data_folder():
    return MOCK_DATA_FOLDER if USE_MOCK_DATA else REAL_DATA_FOLDER