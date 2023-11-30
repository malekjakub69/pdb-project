from faker import Faker
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

fake = Faker()
Base = declarative_base()

class Region(Base):
    __tablename__ = "region"

    id = Column(Integer, primary_key=True, autoincrement=True)
    iso_code = Column(String(3), unique=True, nullable=False)
    country_name = Column(String(255), nullable=False)

engine = create_engine("mysql+pymysql://root:mySuperSecurePassword@db:3306/mySQLdb")
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

def generate_dummy_data(num_regions=50):
    for _ in range(num_regions):
        while True:
            try:
                region = Region(
                    iso_code=fake.country_code(),
                    country_name=fake.country()
                )
                session.add(region)
                session.commit()
                break
            except IntegrityError:
                session.rollback()

if __name__ == "__main__":
    generate_dummy_data()
