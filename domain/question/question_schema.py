'''
Pydantic 을 이용 
pydantic 스키마 작성


질문 등록 API 입력 항목
subject - 등록할 질문의 제목
content - 등록할 질문의 내용

질문 등록 API 출력 항목
없음
'''
import datetime

from pydantic import BaseModel, validator

from domain.answer.answer_schema import Answer
from domain.user.user_schema import User
'''
BaseModel을 상속한 Question 클래스를 만들었다.
pydantic의 BaseModel을 상속한 Question 클래스를 앞으로 Question 스키마라 하겠다. 
4개 항목은 모두 디폴트 값이 없기 때문에 필수항목임을 나타낸다

중요 - user: User | None - 이부분 python 3.9에서는 에러 발생함 - python3.9에서는 맞지 않는 문법
python 3.10에서는 사용 가능한 문법
'''
class Question(BaseModel):
    id: int
    subject: str
    content: str
    create_date: datetime.datetime
    answers: list[Answer] = []  # Question 스키마에 answer 스키마로 구성된 answers 리스트를 추가
    user: User | None
    modify_date: datetime.datetime | None = None  # 수정일시 항목
    voter: list[User] = []   # 추천

    class Config:
        orm_mode = True
    '''
    pydantic.error_wrappers.ValidationError: 1 validation error for Question response -> 0
    에러 해결용
    '''
'''
질문 등록 스키마

'''
class QuestionCreate(BaseModel):
    subject: str
    content: str

    @validator('subject', 'content')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("빈 값은 허용되지 않습니다.")
        return v


'''
질문 등록 스키마 추가
total - 전체 게시물 갯수
question_list - 질문 목록 데이터
API의 출력항목으로 질문 목록 데이터만 있었지만 total 항목을 추가해야 하기 때문에 
질문 목록 API의 응답을 사용할 스키마를 다음과 같이 작성 
'''
class QuestionList(BaseModel):
    total: int = 0
    question_list: list[Question] = []


'''
질문 수정 스키마  
put 요청 방식 
질문 수정
question_id 
subject
content
'''
class QuestionUpdate(QuestionCreate):
    question_id: int


'''
질문 삭제 스키마 
'''
class QuestionDelete(BaseModel):
    question_id: int


'''
질문 추천 스키마
'''
class QuestionVote(BaseModel):
    question_id: int