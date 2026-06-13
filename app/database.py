from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DB_USER = "trabajos_w9zv_user"
DB_PASSWORD = "y1ESuGBLdyPMstcAeFczAERyFtEmz3UP"
DB_HOST = "dpg-d8mddaernols73cg2be0-a.ohio-postgres.render.com"
DB_PORT = "5432"
DB_NAME = "bd_Monitoreo_IoT"

DATABASE_URL = (
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)