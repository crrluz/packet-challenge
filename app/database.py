
import os
import psycopg2
from psycopg2.extras import execute_values
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", 5432))
DB_NAME = os.getenv("DB_NAME", "packetdb")
DB_USER = os.getenv("DB_USER", "packetuser")
DB_PASSWORD = os.getenv("DB_PASSWORD", "packetpass")
def get_connection():
    conn = psycopg2.connect(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD)
    return conn
def create_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS packets (
            id SERIAL PRIMARY KEY,
            src_ip VARCHAR(50),
            dst_ip VARCHAR(50),
            protocol VARCHAR(10),
            packet_size INT,
            capture_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    cursor.close()
    conn.close()
def insert_packets(packets):
    if not packets:
        return
    conn = get_connection()
    cursor = conn.cursor()
    query = "INSERT INTO packets (src_ip, dst_ip, protocol, packet_size) VALUES %s"
    execute_values(cursor, query, packets)
    conn.commit()
    cursor.close()
    conn.close()
