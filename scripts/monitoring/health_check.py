import psycopg2, os, logging, time
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    filename="logs/health.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S"
)

DSN = (
    f"host=localhost port=5432 "
    f"dbname={os.getenv('POSTGRES_DB')} "
    f"user={os.getenv('POSTGRES_USER')} "
    f"password={os.getenv('POSTGRES_PASSWORD')}"
)

CHECKS = [
    ("uptime",       "SELECT now() - pg_postmaster_start_time()"),
    ("connections",  "SELECT count(*) FROM pg_stat_activity"),
    ("db_size",      "SELECT pg_size_pretty(pg_database_size(current_database()))"),
    ("slow_queries", "SELECT count(*) FROM pg_stat_activity WHERE state = 'active' AND now() - query_start > interval '5s'"),
]

def run_checks():
    try:
        with psycopg2.connect(DSN, connect_timeout=5) as conn:
            with conn.cursor() as cur:
                for name, sql in CHECKS:
                    cur.execute(sql)
                    value = cur.fetchone()[0]
                    logging.info(f"CHECK OK  {name}={value}")
        logging.info("STATUS healthy")
    except Exception as e:
        logging.error(f"STATUS unhealthy error={e}")

if __name__ == "__main__":
    logging.info("Health monitor started")
    while True:
        run_checks()
        time.sleep(30)

