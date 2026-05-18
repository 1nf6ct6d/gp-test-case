import os

import psycopg2
from dotenv import load_dotenv



def connect_to_db():
    
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )
    return conn

def load_hub_user(conn) -> None:
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO dds.hub_user (
                user_hk,
                user_id,
                load_dttm,
                source
            )
            SELECT DISTINCT
                MD5(user_id::text) AS user_hk,
                user_id,
                CURRENT_TIMESTAMP AS load_dttm,
                source
            FROM stg.api_posts
            ON CONFLICT (user_hk) DO NOTHING;
            """
        )

def load_hub_post(conn) -> None:
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO dds.hub_post (
                post_hk,
                post_id,
                load_dttm,
                source
            )
            SELECT DISTINCT
                MD5(post_id::text) AS post_hk,
                post_id,
                CURRENT_TIMESTAMP AS load_dttm,
                source
            FROM stg.api_posts
            ON CONFLICT (post_hk) DO NOTHING;
            """
        )
    
def load_link_user_post(conn) -> None:
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO dds.link_user_post (
                user_post_hk,
                user_hk,
                post_hk,
                load_dttm,
                source
            )
            SELECT DISTINCT
                MD5(user_id::text || '|' || post_id::text) AS user_post_hk,
                MD5(user_id::text) AS user_hk,
                MD5(post_id::text) AS post_hk,
                CURRENT_TIMESTAMP AS load_dttm,
                source
            FROM stg.api_posts
            ON CONFLICT (user_post_hk) DO NOTHING;
            """
        )
    
def load_sat_post(conn) -> None:
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO dds.sat_post (
                post_hk,
                title,
                body,
                hashdiff,
                load_dttm,
                source
            )
            SELECT
                MD5(post_id::text) AS post_hk,
                title,
                body,
                MD5(
                    COALESCE(title, '') || '|' || COALESCE(body, '')
                ) AS hashdiff,
                CURRENT_TIMESTAMP AS load_dttm,
                source
            FROM stg.api_posts s
            WHERE NOT EXISTS (
                SELECT 1
                FROM dds.sat_post sp
                WHERE sp.post_hk = MD5(s.post_id::text)
                  AND sp.hashdiff = MD5(
                      COALESCE(s.title, '') || '|' || COALESCE(s.body, '')
                  )
            );
            """
        )

def main():
    
    load_dotenv()
    
    conn = None
    
    try:
        conn = connect_to_db()
        print("Подключение успешно")

        load_hub_user(conn)
        print("Данные вставлены в hub_user")

        load_hub_post(conn)
        print("Данные вставлены в hub_post")

        load_link_user_post(conn)
        print("Данные вставлены в link_user_post")

        load_sat_post(conn)
        print("Данные вставлены в sat_post")
        
        conn.commit()
    
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
    