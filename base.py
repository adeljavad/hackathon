from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import DbConfig

# engine = create_engine(DbConfig.database_url)
engine = create_engine('jdbc:sqlite:D://adel//bot//hackathon//db.sqlite3')
# engine = create_engine('mssql+pyodbc://localhost/loc?driver=SQL+Server+Native+Client+11.0')
# engine = create_engine("mssql+pyodbc://adel:9347@local/sadadpsp_info "+ "?driver=SQL+Server+Native+Client+11.0")
Session = sessionmaker(bind=engine)

Base = declarative_base()
# engine = sqlalchemy.create_engine("mssql+pymssql://username:password@servername/dbname")