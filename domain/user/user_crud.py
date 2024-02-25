'''
회원가입 CRUD

'''
from sqlalchemy.orm import Session
from domain.user.user_schema import UserCreate
from models import User
from passlib.context import CryptContext   # 비밀번호 암호화

# 비밀번호 암호화 pwd_context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_user(db: Session, user_create: UserCreate):
    db_user = User(username=user_create.username,
                   password=pwd_context.hash(user_create.password1),
                   email=user_create.email)
    db.add(db_user)
    db.commit()

'''
등록된 사용자가 있는지 조회
'''
def get_existing_user(db:Session, user_create:UserCreate):
    return db.query(User).filter(
        (User.username == user_create.username)|(User.email == user_create.email)
        # or 조건임
    ).first()

'''
로그인 CRUD
username으로 User데이터를 가져와서 비밀번호를 비교
사용자명으로 사용자 모델 객체를 리턴하는 get_user 함수
'''
def get_user(db:Session, username:str):
    return db.query(User).filter(User.username == username).first()