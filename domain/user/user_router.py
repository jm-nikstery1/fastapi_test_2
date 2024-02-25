'''
회원 가입 라우터
user_router
'''
from fastapi import APIRouter, HTTPException
from fastapi import Depends
from sqlalchemy.orm import Session
from starlette import status

from database import get_db
from domain.user import user_crud, user_schema
from domain.user.user_crud import pwd_context

from datetime import timedelta, datetime
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError

'''
SECRET_KEY 생성
python 접속
import secrets
secrets.token_hex(32)

이 방법보다는 다른 방법의 토큰 생성이 더 안전해 보임
'''
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24
SECRET_KEY = '5990d082b8b22d72ceb50b7e0e2795df9b2f0959522cfcafadd3b580c1cebcd4'
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/user/login")  #토큰으로 글쓴이 확인

router = APIRouter(
    prefix="/api/user",
)

@router.post("/create", status_code=status.HTTP_204_NO_CONTENT)
def user_create(_user_create: user_schema.UserCreate, db: Session = Depends(get_db)):
    user = user_crud.get_existing_user(db, user_create=_user_create)
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="이미 존재하는 사용자 입니다")
    user_crud.create_user(db=db, user_create=_user_create)


@router.post("/login",response_model=user_schema.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db:Session = Depends(get_db)):

    #check user and password
    user = user_crud.get_user(db, form_data.username)
    if not user or not pwd_context.verify(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password - 비밀번호와 유저틀림",
            headers={"WWW-Authenticate": "Bearer"},
        )

    #make access token
    data = {
        "sub": user.username,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    access_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "username": user.username
    }

'''
test 유저 생성
1234 비밀번호

액세스 토큰과 로그인 사용자명 저장하기 - 부터 시작
'''

'''
토큰으로 글쓴이를 확인하기 위한용
'''
def get_current_user(token:str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials - 맞지않는 토큰 ",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    else:
        user = user_crud.get_user(db, username=username)
        if user is None:
            raise credentials_exception
        return user