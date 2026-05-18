import os
import requests
import psycopg2
from dotenv import load_dotenv

def get_api_data(URL):
    
    response = requests.get(URL, timeout=10)
    response.raise_for_status()
    return response.json()

def connect_to_db():
    
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )
    
    return conn

def load_to_stg(conn, posts) -> None:
    with conn.cursor() as cur:
        cur.execute("TRUNCATE TABLE stg.api_posts;")

        insert_query = """
            INSERT INTO stg.api_posts (post_id, user_id, title, body, source)
            VALUES (%s, %s, %s, %s, %s);
        """

        for post in posts:
            cur.execute(
                insert_query,
                (
                    post.get("id"),
                    post.get("userId"),
                    post.get("title"),
                    post.get("body"),
                    "jsonplaceholder"
                )
            )

    conn.commit()

def main():
    
    load_dotenv()

    api_url = os.getenv("API_URL")

    if api_url is None:
        raise ValueError("Задайте URL в .env")
    
    conn = None
    
    try:
        api_data = get_api_data(api_url)
        print(f"Данные получили. Количество: {len(api_data)}")

        conn = connect_to_db()
        print("Подключение успешно")

        load_to_stg(conn, api_data)
        print("Данные загружены в в таблицу api_posts")
    
    except Exception as error:
        if conn is not None:
            conn.rollback()
        print(f"Ошибка при выполнении процесса {error}")
        raise
    
    finally:
        if conn is not None:
            conn.close()
            print("Сеанс завершен")

if __name__ == "__main__":
    main()
    