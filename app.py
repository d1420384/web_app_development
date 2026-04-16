from dotenv import load_dotenv
import os

# 載入環境變數（需確保環境中有 .env 檔案）
load_dotenv()

from app import create_app

# 建立 Flask 實體
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
