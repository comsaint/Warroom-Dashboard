import os

class Config:
    """基礎設定"""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'a_very_secret_key')
    DEBUG = False

class DevelopmentConfig(Config):
    """開發環境設定"""
    DEBUG = True
    DATA_FOLDER = os.path.join("data", "mockup")

class ProductionConfig(Config):
    """生產環境設定"""
    DATA_FOLDER = os.path.join("data", "real")

# 提供一個字典，方便根據名稱取得設定
config_by_name = dict(
    development=DevelopmentConfig,
    production=ProductionConfig,
)