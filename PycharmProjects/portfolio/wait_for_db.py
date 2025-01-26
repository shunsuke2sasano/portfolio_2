import time
import os
import pymysql

# 環境変数から接続情報を取得
DB_HOST = os.getenv("DB_HOST", "db")
DB_PORT = int(os.getenv("DB_PORT", 3306))
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "Bullshit03Sasano19")  # デフォルトのパスワードを明示
DB_NAME = os.getenv("DB_NAME", "portfolio_db")  # デフォルトのデータベース名を明示

def wait_for_db():
    print(f"Waiting for database {DB_HOST}:{DB_PORT}...")
    while True:
        try:
            conn = pymysql.connect(
                host=DB_HOST,
                port=DB_PORT,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME,
            )
            conn.close()
            print("Database is ready!")
            break
        except pymysql.MySQLError as e:
            print(f"Database not ready yet: {e}")
            time.sleep(2)

if __name__ == "__main__":
    wait_for_db()