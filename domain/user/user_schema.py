'''
회원 가입 스키마
회원 가입 API의 입력 항목으로 사용할 스키마

username
password1
password2
email
'''
from pydantic import BaseModel, validator, EmailStr

class UserCreate(BaseModel):
    username: str
    password1: str
    password2: str
    email: EmailStr  # email 형식 확인

    @validator('username', 'password1', 'password2', 'email')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("빈 값은 허용되지 않습니다")
        return v

    @validator('password2')
    def passwords_match(cls, v, values):
        if 'password1' in values and v != values['password1']:
            raise ValueError("비밀번호가 일치하지 않습니다")
        return v

'''
로그인 API
access_token - 액세스 토큰
token_type - 토큰의 종류(Bearer로 고정하여 사용 - Bearer는 JWT 또는 OAuth의 토큰방식)
username - 사용자명 
'''
class Token(BaseModel):
    access_token: str
    token_type: str
    username: str

'''
글쓴이 표시하기 
API 출력 항목에 글쓴이 추가
       
의외로 이 orm_mode문제가 많네 - pydantic 1 버젼과 pydantic 2 차이문제

'''
class User(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        orm_mode = True
