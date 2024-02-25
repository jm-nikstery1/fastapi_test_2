from sqlalchemy import create_engine, MetaData  # SQLite의 오류 해결용
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URL = "sqlite:///./myapi.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
naming_convention={
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
# SQLite의 오류 해결용 - 글쓴이 저장용
Base.metadata = MetaData(naming_convention=naming_convention)

'''
이 과정에서 데이터베이스에 모델에 정의한 question과 answer라는 이름의 테이블이 생성된다. 
지금까지 잘 따라왔다면 projects/myapi 디렉터리에 myapi.db 파일이 생성되었을 것이다. 
myapi.db가 바로 SQLite 데이터베이스의 데이터 파일이다.
sqlalchemy로 사용중
'''

'''
데이터베이스 세션의 생성과 반환을 자동화
프로그래밍에서 "Dependency Injection(의존성 주입)"의 뜻은 필요한 기능을 선언하여 사용할 수 있다는 의미이다.
'''

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()